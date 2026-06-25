"""
graph_viz.py — Builds vis.js graph HTML for each of the 4 MAGMA memory graph types.
Generates HTML directly (no pyvis) so there is no IPython/ipython dependency.
"""

import json
import networkx as nx
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.scenario import (
    EVENTS, SEMANTIC_EDGES, TEMPORAL_EDGES, CAUSAL_EDGES, ENTITY_EDGES, GRAPH_COLORS
)

# ---------------------------------------------------------------------------
# Build base NetworkX graphs from scenario data
# ---------------------------------------------------------------------------

def _event_label(event_id: str) -> str:
    for e in EVENTS:
        if e["id"] == event_id:
            text = e["content"]
            return text[:40] + "..." if len(text) > 40 else text
    return event_id


def _event_title(event_id: str) -> str:
    for e in EVENTS:
        if e["id"] == event_id:
            return f"[{event_id}] {e['speaker']} — Week {e['week']}, {e['day']} {e['time']}\n\n{e['content']}"
    return event_id


def build_networkx_graphs():
    graphs = {}

    G_sem = nx.Graph()
    for e in EVENTS:
        if "semantic" in e["graph_memberships"]:
            G_sem.add_node(e["id"], label=e["id"], title=_event_title(e["id"]),
                           speaker=e["speaker"], week=e["week"])
    for src, dst in SEMANTIC_EDGES:
        if G_sem.has_node(src) and G_sem.has_node(dst):
            G_sem.add_edge(src, dst)
    graphs["semantic"] = G_sem

    G_tmp = nx.DiGraph()
    for e in EVENTS:
        G_tmp.add_node(e["id"], label=e["id"], title=_event_title(e["id"]),
                       speaker=e["speaker"], week=e["week"])
    for src, dst in TEMPORAL_EDGES:
        G_tmp.add_edge(src, dst)
    graphs["temporal"] = G_tmp

    G_cau = nx.DiGraph()
    for e in EVENTS:
        if "causal" in e["graph_memberships"]:
            G_cau.add_node(e["id"], label=e["id"], title=_event_title(e["id"]),
                           speaker=e["speaker"], week=e["week"])
    for src, dst in CAUSAL_EDGES:
        G_cau.add_node(src)
        G_cau.add_node(dst)
        G_cau.add_edge(src, dst)
    graphs["causal"] = G_cau

    G_ent = nx.Graph()
    for e in EVENTS:
        if "entity" in e["graph_memberships"]:
            G_ent.add_node(e["id"], label=e["id"], title=_event_title(e["id"]),
                           speaker=e["speaker"], week=e["week"], node_type="event")
    for src, entity in ENTITY_EDGES:
        if not G_ent.has_node(entity):
            G_ent.add_node(entity, label=entity, title=f"Entity: {entity}", node_type="entity")
        if G_ent.has_node(src):
            G_ent.add_edge(src, entity)
    graphs["entity"] = G_ent

    return graphs


_GRAPHS = None

def get_graphs():
    global _GRAPHS
    if _GRAPHS is None:
        _GRAPHS = build_networkx_graphs()
    return _GRAPHS


# ---------------------------------------------------------------------------
# vis.js HTML builder (replaces pyvis)
# ---------------------------------------------------------------------------

GRAPH_CONFIG = {
    "semantic": {"node_color": "#6C63FF", "edge_color": "#9D97FF", "node_shape": "dot",    "directed": False},
    "temporal": {"node_color": "#00BFA5", "edge_color": "#00E5CC", "node_shape": "square", "directed": True},
    "causal":   {"node_color": "#FF6B6B", "edge_color": "#FF9999", "node_shape": "diamond","directed": True},
    "entity":   {"node_color": "#FFB347", "edge_color": "#FFD700", "node_shape": "dot",    "directed": False},
}

ENTITY_NODE_COLOR = "#FF69B4"

_VIS_CDN = "https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.js"
_VIS_CSS = "https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/dist/vis-network.min.css"


def build_graph_html(
    graph_type: str,
    highlighted_nodes: list = None,
    highlighted_edges: list = None,
    height: int = 480,
    width: str = "100%",
    physics: bool = True,
    theme: str = "dark",
) -> str:
    highlighted_nodes = highlighted_nodes or []
    highlighted_edges = set(map(tuple, highlighted_edges)) if highlighted_edges else set()

    cfg = GRAPH_CONFIG[graph_type]
    G = get_graphs()[graph_type]

    is_light = theme == "light"
    bgcolor   = "#FFFFFF" if is_light else "#1A1D2E"
    font_color = "#333333" if is_light else "#FAFAFA"
    border_css = "1px solid #CCCCCC" if is_light else "1px solid #333"
    tooltip_bg = "#F0F2F6" if is_light else "#2D3148"

    # Build nodes list
    nodes_data = []
    for node_id, attrs in G.nodes(data=True):
        is_hl = node_id in highlighted_nodes
        is_entity = attrs.get("node_type") == "entity"

        if is_hl:
            color = {"background": "#FFD700", "border": "#FF8C00",
                     "highlight": {"background": "#FFD700", "border": "#FF8C00"}}
            size, border_w = 22, 3
        elif is_entity:
            color = {"background": ENTITY_NODE_COLOR, "border": ENTITY_NODE_COLOR,
                     "highlight": {"background": "#FFD700", "border": "#FF8C00"}}
            size, border_w = 18, 2
        else:
            c = cfg["node_color"]
            color = {"background": c, "border": c,
                     "highlight": {"background": "#FFD700", "border": "#FF8C00"}}
            size, border_w = 14, 1

        shape = "star" if is_entity else cfg["node_shape"]
        title = attrs.get("title", node_id).replace("\n", "<br>")

        nodes_data.append({
            "id": node_id,
            "label": attrs.get("label", node_id),
            "title": title,
            "color": color,
            "size": size,
            "borderWidth": border_w,
            "shape": shape,
            "font": {"size": 11, "color": font_color},
        })

    # Build edges list
    edges_data = []
    for src, dst in G.edges():
        ek, rk = (src, dst), (dst, src)
        is_hl_edge = (ek in highlighted_edges) or (rk in highlighted_edges)
        color = {"color": "#FF8C00", "highlight": "#FF8C00"} if is_hl_edge else {"color": cfg["edge_color"]}
        edges_data.append({
            "from": src,
            "to": dst,
            "color": color,
            "width": 4 if is_hl_edge else 1.5,
            "arrows": {"to": {"enabled": cfg["directed"], "scaleFactor": 0.8}},
            "smooth": {"type": "continuous"},
        })

    options = {
        "physics": {
            "enabled": physics,
            "barnesHut": {
                "gravitationalConstant": -3000,
                "centralGravity": 0.3,
                "springLength": 120,
                "springConstant": 0.04,
                "damping": 0.09,
            },
            "stabilization": {"iterations": 150},
        },
        "interaction": {"hover": True, "tooltipDelay": 100, "zoomView": True, "dragNodes": True},
        "edges": {"smooth": {"type": "continuous"}},
        "nodes": {"font": {"size": 11}},
    }

    nodes_json = json.dumps(nodes_data)
    edges_json = json.dumps(edges_data)
    options_json = json.dumps(options)

    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="{_VIS_CSS}" crossorigin="anonymous">
  <script src="{_VIS_CDN}" crossorigin="anonymous"></script>
  <style>
    body {{ margin: 0; padding: 0; background: {bgcolor}; overflow: hidden; }}
    #magma-graph {{
      width: {width}; height: {height}px;
      background: {bgcolor};
      border: {border_css};
      border-radius: 8px;
    }}
    .vis-tooltip {{
      background: {tooltip_bg} !important;
      border: 1px solid #6C63FF !important;
      color: {font_color} !important;
      border-radius: 6px !important;
      font-size: 12px !important;
      max-width: 280px !important;
      white-space: pre-wrap !important;
    }}
  </style>
</head>
<body>
  <div id="magma-graph"></div>
  <script>
    var nodes = new vis.DataSet({nodes_json});
    var edges = new vis.DataSet({edges_json});
    var container = document.getElementById("magma-graph");
    var network = new vis.Network(container, {{nodes: nodes, edges: edges}}, {options_json});
  </script>
</body>
</html>"""
    return html


def build_all_thumbnails(
    highlighted_by_graph: dict = None,
    height: int = 200,
    physics: bool = False,
) -> dict:
    highlighted_by_graph = highlighted_by_graph or {}
    thumbnails = {}
    for graph_type in ["semantic", "temporal", "causal", "entity"]:
        highlighted = highlighted_by_graph.get(graph_type, [])
        thumbnails[graph_type] = build_graph_html(
            graph_type=graph_type,
            highlighted_nodes=highlighted,
            height=height,
            physics=physics,
        )
    return thumbnails


def get_node_count(graph_type: str) -> int:
    return get_graphs()[graph_type].number_of_nodes()


def get_edge_count(graph_type: str) -> int:
    return get_graphs()[graph_type].number_of_edges()

"""
graph_viz.py — Builds PyVis graph HTML for each of the 4 MAGMA memory graph types.
Supports traversal highlighting by accepting lists of visited nodes/edges.
"""

import networkx as nx
from pyvis.network import Network
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
    """Return a short display label for an event node."""
    for e in EVENTS:
        if e["id"] == event_id:
            text = e["content"]
            return text[:40] + "..." if len(text) > 40 else text
    return event_id


def _event_title(event_id: str) -> str:
    """Return the full hover tooltip for an event node."""
    for e in EVENTS:
        if e["id"] == event_id:
            return f"[{event_id}] {e['speaker']} — Week {e['week']}, {e['day']} {e['time']}\n\n{e['content']}"
    return event_id


def build_networkx_graphs():
    """Build all 4 NetworkX directed graphs. Returns dict of {graph_type: nx.DiGraph}."""
    graphs = {}

    # Semantic graph
    G_sem = nx.Graph()
    for e in EVENTS:
        if "semantic" in e["graph_memberships"]:
            G_sem.add_node(e["id"], label=e["id"], title=_event_title(e["id"]),
                           speaker=e["speaker"], week=e["week"])
    for src, dst in SEMANTIC_EDGES:
        if G_sem.has_node(src) and G_sem.has_node(dst):
            G_sem.add_edge(src, dst)
    graphs["semantic"] = G_sem

    # Temporal graph
    G_tmp = nx.DiGraph()
    for e in EVENTS:
        G_tmp.add_node(e["id"], label=e["id"], title=_event_title(e["id"]),
                       speaker=e["speaker"], week=e["week"])
    for src, dst in TEMPORAL_EDGES:
        G_tmp.add_edge(src, dst)
    graphs["temporal"] = G_tmp

    # Causal graph
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

    # Entity graph (events + entity name nodes)
    G_ent = nx.Graph()
    entities = set()
    for e in EVENTS:
        if "entity" in e["graph_memberships"]:
            G_ent.add_node(e["id"], label=e["id"], title=_event_title(e["id"]),
                           speaker=e["speaker"], week=e["week"], node_type="event")
    for src, entity in ENTITY_EDGES:
        entities.add(entity)
        if not G_ent.has_node(entity):
            G_ent.add_node(entity, label=entity, title=f"Entity: {entity}", node_type="entity")
        if G_ent.has_node(src):
            G_ent.add_edge(src, entity)
    graphs["entity"] = G_ent

    return graphs


# Singleton graphs (built once)
_GRAPHS = None

def get_graphs():
    global _GRAPHS
    if _GRAPHS is None:
        _GRAPHS = build_networkx_graphs()
    return _GRAPHS


# ---------------------------------------------------------------------------
# PyVis HTML builder
# ---------------------------------------------------------------------------

GRAPH_CONFIG = {
    "semantic": {
        "node_color": "#6C63FF",
        "edge_color": "#9D97FF",
        "node_shape": "dot",
        "directed": False,
        "title": "Semantic Graph",
    },
    "temporal": {
        "node_color": "#00BFA5",
        "edge_color": "#00E5CC",
        "node_shape": "square",
        "directed": True,
        "title": "Temporal Graph",
    },
    "causal": {
        "node_color": "#FF6B6B",
        "edge_color": "#FF9999",
        "node_shape": "diamond",
        "directed": True,
        "title": "Causal Graph",
    },
    "entity": {
        "node_color": "#FFB347",
        "edge_color": "#FFD700",
        "node_shape": "dot",
        "directed": False,
        "title": "Entity Graph",
    },
}

ENTITY_NODE_COLOR = "#FF69B4"  # Pink for entity name nodes


def build_graph_html(
    graph_type: str,
    highlighted_nodes: list = None,
    highlighted_edges: list = None,
    height: int = 480,
    width: str = "100%",
    physics: bool = True,
    theme: str = "dark",
) -> str:
    """
    Build a PyVis HTML string for the given graph type.

    Args:
        graph_type: One of 'semantic', 'temporal', 'causal', 'entity'
        highlighted_nodes: List of node IDs to highlight gold (visited during traversal)
        highlighted_edges: List of (src, dst) tuples to highlight orange
        height: Height of the graph container in pixels
        width: Width of the graph container
        physics: Whether to enable vis.js physics simulation

    Returns:
        Self-contained HTML string embeddable via st.components.v1.html()
    """
    highlighted_nodes = highlighted_nodes or []
    highlighted_edges = set(map(tuple, highlighted_edges)) if highlighted_edges else set()

    cfg = GRAPH_CONFIG[graph_type]
    G = get_graphs()[graph_type]

    is_light = theme == "light"
    _bgcolor = "#FFFFFF" if is_light else "#1A1D2E"
    _font_color = "#333333" if is_light else "#FAFAFA"

    net = Network(
        height=f"{height}px",
        width=width,
        directed=cfg["directed"],
        notebook=False,
        bgcolor=_bgcolor,
        font_color=_font_color,
    )
    net.toggle_physics(physics)

    # Add nodes
    for node_id, attrs in G.nodes(data=True):
        is_highlighted = node_id in highlighted_nodes
        is_entity_node = attrs.get("node_type") == "entity"

        if is_highlighted:
            color = "#FFD700"
            size = 22
            border_width = 3
            border_color = "#FF8C00"
        elif is_entity_node:
            color = ENTITY_NODE_COLOR
            size = 18
            border_width = 2
            border_color = "#FF69B4"
        else:
            color = cfg["node_color"]
            size = 14
            border_width = 1
            border_color = cfg["node_color"]

        label = attrs.get("label", node_id)
        title = attrs.get("title", node_id)

        net.add_node(
            node_id,
            label=label,
            title=title,
            color={"background": color, "border": border_color, "highlight": {"background": "#FFD700", "border": "#FF8C00"}},
            size=size,
            borderWidth=border_width,
            shape=cfg["node_shape"] if not is_entity_node else "star",
            font={"size": 11, "color": _font_color},
        )

    # Add edges
    for src, dst in G.edges():
        edge_key = (src, dst)
        rev_key = (dst, src)
        is_highlighted_edge = (edge_key in highlighted_edges) or (rev_key in highlighted_edges)

        if is_highlighted_edge:
            color = "#FF8C00"
            width = 4
            dashes = False
        else:
            color = cfg["edge_color"]
            width = 1.5
            dashes = False

        net.add_edge(
            src, dst,
            color=color,
            width=width,
            dashes=dashes,
            arrows={"to": {"enabled": cfg["directed"], "scaleFactor": 0.8}},
        )

    # Configure physics options
    net.set_options("""
    {
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -3000,
          "centralGravity": 0.3,
          "springLength": 120,
          "springConstant": 0.04,
          "damping": 0.09
        },
        "stabilization": {"iterations": 150}
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 100,
        "zoomView": true,
        "dragNodes": true
      },
      "edges": {
        "smooth": {"type": "continuous"}
      },
      "nodes": {
        "font": {"size": 11}
      }
    }
    """)

    # Generate HTML
    html = net.generate_html()

    # Inject custom styles based on theme
    if is_light:
        custom_style = """
    <style>
      body { margin: 0; padding: 0; background: #FFFFFF; overflow: hidden; }
      #mynetwork { border: 1px solid #CCCCCC; border-radius: 8px; }
      .vis-tooltip {
        background: #F0F2F6 !important;
        border: 1px solid #6C63FF !important;
        color: #1A1D2E !important;
        border-radius: 6px !important;
        font-size: 12px !important;
        max-width: 280px !important;
        white-space: pre-wrap !important;
      }
    </style>
    """
    else:
        custom_style = """
    <style>
      body { margin: 0; padding: 0; background: #1A1D2E; overflow: hidden; }
      #mynetwork { border: 1px solid #333; border-radius: 8px; }
      .vis-tooltip {
        background: #2D3148 !important;
        border: 1px solid #6C63FF !important;
        color: #FAFAFA !important;
        border-radius: 6px !important;
        font-size: 12px !important;
        max-width: 280px !important;
        white-space: pre-wrap !important;
      }
    </style>
    """
    html = html.replace("</head>", custom_style + "</head>")

    return html


def build_all_thumbnails(
    highlighted_by_graph: dict = None,
    height: int = 200,
    physics: bool = False,
) -> dict:
    """
    Build small thumbnail HTML for all 4 graphs simultaneously.
    Used in Act 2 ingestion animation.

    Args:
        highlighted_by_graph: dict of {graph_type: list_of_node_ids} for partial ingestion view
        height: thumbnail height in pixels
        physics: usually False for thumbnails to avoid jitter

    Returns:
        dict of {graph_type: html_string}
    """
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

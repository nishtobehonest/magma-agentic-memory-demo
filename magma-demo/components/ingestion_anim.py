"""
ingestion_anim.py — Act 2: Animated fast-path event ingestion into all 4 graphs.
Shows events arriving one-by-one with graph thumbnails updating in real time.
"""

import time
import streamlit as st
import streamlit.components.v1 as components
from data.scenario import EVENTS, GRAPH_COLORS
from components.graph_viz import build_graph_html, get_node_count, get_edge_count


SPEAKER_COLORS = {
    "Alex":     "#6C63FF",
    "Jordan":   "#00BFA5",
    "Sam":      "#FF6B6B",
    "Maya":     "#FFB347",
    "System":   "#888888",
    "ProfChen": "#FF69B4",
}

WEEK_LABELS = {1: "Week 1 — Trust Building", 2: "Week 2 — The Setup", 3: "Week 3 — Midterm Week"}


def render_event_bubble(event: dict, dimmed: bool = False) -> str:
    """Render a single event as an HTML chat bubble."""
    color = SPEAKER_COLORS.get(event["speaker"], "#888")
    opacity = "0.4" if dimmed else "1.0"
    graph_badges = "".join([
        f'<span style="background:{_badge_color(g)};color:#fff;padding:1px 6px;border-radius:8px;font-size:10px;margin-right:3px">{g}</span>'
        for g in event["graph_memberships"]
    ])
    return f"""
    <div style="opacity:{opacity};margin-bottom:8px;padding:10px 14px;background:#252840;border-left:3px solid {color};border-radius:6px">
      <div style="font-size:11px;color:{color};font-weight:600;margin-bottom:4px">
        {event['speaker']} &nbsp;·&nbsp; {event['id']} &nbsp;·&nbsp; Week {event['week']}, {event['day']} {event['time']}
      </div>
      <div style="font-size:13px;color:#EAEAEA;line-height:1.5">{event['content']}</div>
      <div style="margin-top:6px">{graph_badges}</div>
    </div>
    """


def _badge_color(graph: str) -> str:
    colors = {
        "semantic": "#6C63FF",
        "temporal": "#00BFA5",
        "causal": "#FF6B6B",
        "entity": "#FFB347",
    }
    return colors.get(graph, "#666")


def render_ingestion(speed: str = "1x", theme: str = "dark"):
    """
    Main ingestion animation renderer for Act 2.
    speed: "1x" | "5x" | "Instant"
    """
    delay = {"1x": 0.35, "5x": 0.07, "Instant": 0}[speed]

    st.markdown("### Fast Path: Synaptic Ingestion")
    st.caption("Each event is indexed into the relevant graph(s) in real time.")

    # Layout: left = event log, right = 4 graph thumbnails
    col_log, col_graphs = st.columns([1, 1], gap="medium")

    with col_graphs:
        st.markdown("**Memory Graphs**")
        graph_placeholders = {}
        stat_placeholders = {}
        for gtype, label, color in [
            ("semantic", "Semantic", "#6C63FF"),
            ("temporal", "Temporal", "#00BFA5"),
            ("causal",   "Causal",   "#FF6B6B"),
            ("entity",   "Entity",   "#FFB347"),
        ]:
            st.markdown(
                f'<span style="color:{color};font-weight:600;font-size:13px">{label} Graph</span>',
                unsafe_allow_html=True,
            )
            stat_placeholders[gtype] = st.empty()
            graph_placeholders[gtype] = st.empty()

    # Track which nodes have been "ingested" per graph
    ingested = {"semantic": [], "temporal": [], "causal": [], "entity": []}
    event_log_html = ""

    with col_log:
        st.markdown("**Incoming Events**")
        log_placeholder = st.empty()
        progress_bar = st.progress(0)
        status_text = st.empty()

    total = len(EVENTS)
    for i, event in enumerate(EVENTS):
        # Update ingested nodes per graph
        for gtype in event["graph_memberships"]:
            if event["id"] not in ingested[gtype]:
                ingested[gtype].append(event["id"])

        # Also add entity nodes for entity graph
        if "entity" in event["graph_memberships"]:
            for entity in event.get("entities", []):
                if entity not in ingested["entity"]:
                    ingested["entity"].append(entity)

        # Update event log (show last 6 events, older ones dimmed)
        event_log_html = render_event_bubble(event) + event_log_html
        with log_placeholder:
            st.markdown(event_log_html, unsafe_allow_html=True)

        # Update graph thumbnails
        for gtype, ph in graph_placeholders.items():
            html = build_graph_html(
                graph_type=gtype,
                highlighted_nodes=[event["id"]] if event["id"] in ingested[gtype] else [],
                height=170,
                physics=False,
                theme=theme,
            )
            with ph:
                components.html(html, height=175, scrolling=False)

            # Update stats
            n_ingested = len([x for x in ingested[gtype] if x.startswith("E")])
            e_count = get_edge_count(gtype)
            with stat_placeholders[gtype]:
                st.caption(f"{n_ingested} nodes · {e_count} edges")

        # Update progress
        progress = (i + 1) / total
        progress_bar.progress(progress)
        status_text.markdown(
            f'<span style="color:#AAAAAA;font-size:12px">Processing: **{event["id"]}** '
            f'({i+1}/{total}) — adding to {", ".join(event["graph_memberships"])} graph(s)</span>',
            unsafe_allow_html=True,
        )

        if delay > 0:
            time.sleep(delay)

    # Slow path consolidation phase
    status_text.markdown(
        '<span style="color:#00BFA5;font-size:13px">**Slow Path: Structural Consolidation...**</span>',
        unsafe_allow_html=True,
    )
    if delay > 0:
        time.sleep(0.8)

    status_text.markdown(
        '<span style="color:#6C63FF;font-size:13px">**Memory fully consolidated. All 4 graphs ready.**</span>',
        unsafe_allow_html=True,
    )

    # Mark Act 2 done + award points
    if not st.session_state.get("act2_complete"):
        pts = 150 if speed == "1x" else 100
        st.session_state["score"] = st.session_state.get("score", 0) + pts
        st.session_state["act2_complete"] = True
        st.session_state["act2_pts_earned"] = pts

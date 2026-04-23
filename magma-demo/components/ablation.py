"""
ablation.py — Act 5: Graph ablation explorer.
Uses components.html() for all rich HTML blocks (same pattern as Acts 2 & 3).
"""

import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
from data.scenario import ABLATION_SCORES
from data.themes import LIGHT_IFRAME_CSS, plotly_layout, plotly_grid, plotly_bar_muted, gauge_steps

_BASE_CSS = """
body {{
  margin: 0; padding: 0;
  background: {bg};
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  color: {text};
}}
{overrides}
"""

def _html_doc(body_html: str, theme: str = "dark") -> str:
    if theme == "light":
        css = _BASE_CSS.format(bg="#FFFFFF", text="#1A1D2E", overrides=LIGHT_IFRAME_CSS)
    else:
        css = _BASE_CSS.format(bg="#1A1D2E", text="#FAFAFA", overrides="")
    return f"<html><head><style>{css}</style></head><body>{body_html}</body></html>"


GRAPH_DESCRIPTIONS = {
    "semantic": {
        "label": "Semantic Graph",
        "color": "#6C63FF",
        "icon": "&#9679;",
        "query_type": "WHAT queries",
        "example": "What topics did the group discuss?",
        "role": "Groups conceptually similar events. Enables topic-level retrieval. Without it, MAGMA loses thematic coherence and over-retrieves irrelevant events.",
        "contribution": 12,
    },
    "temporal": {
        "label": "Temporal Graph",
        "color": "#00BFA5",
        "icon": "&#9632;",
        "query_type": "WHEN queries",
        "example": "When did Sam ask for money?",
        "role": "Maintains chronological order. Enables WHEN queries and ensures causal edges respect time. Without it, MAGMA cannot reason about sequence.",
        "contribution": 18,
    },
    "causal": {
        "label": "Causal Graph",
        "color": "#FF6B6B",
        "icon": "&#9670;",
        "query_type": "WHY queries",
        "example": "Why did Sam disappear after the exam?",
        "role": "Tracks cause-and-effect links. Most impactful graph for WHY queries and adversarial reasoning. Biggest contributor to MAGMA's benchmark lead.",
        "contribution": 30,
    },
    "entity": {
        "label": "Entity Graph",
        "color": "#FFB347",
        "icon": "&#9733;",
        "query_type": "WHO queries",
        "example": "Who introduced Sam to the group?",
        "role": "Tracks people, places, and objects across events. Enables WHO queries and cross-referencing the same entity across time. Without it, MAGMA loses object permanence.",
        "contribution": 40,
    },
}


def _get_score(active_graphs: list) -> float:
    key = frozenset(active_graphs)
    if key in ABLATION_SCORES:
        return ABLATION_SCORES[key]
    full_score = 0.700
    base_score = 0.481
    ratio = len(active_graphs) / 4
    return round(base_score + (full_score - base_score) * ratio, 3)


def _score_color(score: float) -> str:
    if score >= 0.68:   return "#00BFA5"
    elif score >= 0.60: return "#FFB347"
    elif score >= 0.50: return "#FF6B6B"
    else:               return "#FF3333"


# ---------------------------------------------------------------------------
# Architecture overview — 4 cards with contribution bars
# ---------------------------------------------------------------------------
def render_architecture_overview(theme: str = "dark"):
    cards_html = ""
    for gtype, info in GRAPH_DESCRIPTIONS.items():
        bar = info["contribution"]
        cards_html += f"""
<div style="background:#1A1D2E;border:1px solid {info['color']}55;border-radius:10px;padding:12px;text-align:center">
  <div style="font-size:22px;color:{info['color']};margin-bottom:4px">{info['icon']}</div>
  <div style="color:{info['color']};font-weight:700;font-size:12px">{info['label'].split()[0]}</div>
  <div style="color:#777;font-size:10px;margin:2px 0 8px 0">{info['query_type']}</div>
  <div style="background:#252840;border-radius:3px;height:5px;overflow:hidden;margin-bottom:4px">
    <div style="background:{info['color']};width:{bar}%;height:100%"></div>
  </div>
  <div style="color:{info['color']};font-size:10px;font-weight:600">{bar}% weight</div>
</div>"""

    html = f"""
<div style="color:#AAAAAA;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px">
  MAGMA's 4-Graph Memory Architecture
</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px">{cards_html}</div>
"""
    components.html(_html_doc(html, theme), height=160, scrolling=False)


# ---------------------------------------------------------------------------
# Gauge chart (Plotly — renders independently)
# ---------------------------------------------------------------------------
def render_gauge(score: float, theme: str = "dark") -> go.Figure:
    color = _score_color(score)
    layout = plotly_layout(theme)
    axis_color = "#777777" if theme == "light" else "#AAAAAA"
    gauge_bg = "#F5F6FA" if theme == "light" else "#252840"
    border_color = "#CCCCCC" if theme == "light" else "#444"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": "", "font": {"size": 36, "color": color}},
        gauge={
            "axis": {"range": [0.3, 0.75], "tickcolor": axis_color, "tickfont": {"color": axis_color}},
            "bar": {"color": color},
            "bgcolor": gauge_bg,
            "borderwidth": 1, "bordercolor": border_color,
            "steps": gauge_steps(theme),
            "threshold": {"line": {"color": "#FFD700", "width": 3}, "thickness": 0.8, "value": 0.700},
        },
        title={"text": "LoComo Score", "font": {"color": layout["font"]["color"], "size": 14}},
        domain={"x": [0, 1], "y": [0, 1]},
    ))
    fig.update_layout(
        height=280, margin=dict(t=30, b=10, l=20, r=20),
        **layout,
    )
    return fig


# ---------------------------------------------------------------------------
# Contribution bar chart
# ---------------------------------------------------------------------------
def render_score_breakdown_chart(active_graphs: list, theme: str = "dark") -> go.Figure:
    graphs = list(GRAPH_DESCRIPTIONS.keys())
    labels = [GRAPH_DESCRIPTIONS[g]["label"].split()[0] for g in graphs]
    contributions = [GRAPH_DESCRIPTIONS[g]["contribution"] for g in graphs]
    muted = "#CCCCCC" if theme == "light" else "#333333"
    colors = [GRAPH_DESCRIPTIONS[g]["color"] if g in active_graphs else muted for g in graphs]
    opacities = [1.0 if g in active_graphs else 0.3 for g in graphs]
    fig = go.Figure(go.Bar(
        x=contributions, y=labels, orientation="h",
        marker=dict(color=colors, opacity=opacities),
        text=[f"{c}%" for c in contributions],
        textposition="inside", textfont=dict(color="#FFFFFF", size=11),
    ))
    layout = plotly_layout(theme)
    grid = plotly_grid(theme)
    fig.update_layout(
        title=dict(text="Graph Contribution Weights", font=dict(color=layout["font"]["color"], size=13)),
        xaxis=dict(gridcolor=grid, title="Relative Contribution %", range=[0, 50]),
        yaxis=dict(gridcolor=grid),
        height=220, margin=dict(t=40, b=20, l=20, r=20), showlegend=False,
        **layout,
    )
    return fig


# ---------------------------------------------------------------------------
# Graph role cards
# ---------------------------------------------------------------------------
def render_graph_cards(active_graphs: list, theme: str = "dark"):
    cards_html = ""
    for gtype, info in GRAPH_DESCRIPTIONS.items():
        is_active = gtype in active_graphs
        opacity = "1.0" if is_active else "0.45"
        status_label = "ACTIVE" if is_active else "REMOVED"
        status_color = "#00BFA5" if is_active else "#FF6B6B"
        status_bg = "#1A2D1A" if is_active else "#2D1A1A"
        border = f"2px solid {info['color']}" if is_active else "1px dashed #555"

        cards_html += f"""
<div style="background:#1A1D2E;border:{border};border-radius:10px;padding:14px;opacity:{opacity}">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
    <div style="display:flex;align-items:center;gap:8px">
      <span style="color:{info['color']};font-size:18px">{info['icon']}</span>
      <div>
        <div style="color:{info['color']};font-weight:700;font-size:13px">{info['label']}</div>
        <div style="color:#666;font-size:10px">{info['query_type']}</div>
      </div>
    </div>
    <span style="background:{status_bg};color:{status_color};font-size:10px;font-weight:700;padding:2px 8px;border-radius:10px">{status_label}</span>
  </div>
  <div style="background:#252840;border-radius:6px;padding:6px 10px;margin-bottom:8px">
    <span style="color:#AAAAAA;font-size:10px">e.g. </span>
    <span style="color:{info['color']};font-size:10px;font-style:italic">{info['example']}</span>
  </div>
  <div style="color:#BBBBBB;font-size:11px;line-height:1.5">{info['role']}</div>
  <div style="margin-top:10px">
    <div style="display:flex;justify-content:space-between;margin-bottom:3px">
      <span style="color:#666;font-size:10px">Contribution weight</span>
      <span style="color:{info['color']};font-size:10px;font-weight:600">{info['contribution']}%</span>
    </div>
    <div style="background:#252840;border-radius:3px;height:4px;overflow:hidden">
      <div style="background:{info['color']};width:{info['contribution']}%;height:100%;opacity:{'1' if is_active else '0.3'}"></div>
    </div>
  </div>
</div>"""

    html = f"""
<div style="color:#AAAAAA;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;padding-top:2px">
  What Each Graph Contributes
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">{cards_html}</div>
"""
    components.html(_html_doc(html, theme), height=610, scrolling=False)


# ---------------------------------------------------------------------------
# Capability gap block
# ---------------------------------------------------------------------------
def render_capability_gaps(active_graphs: list, theme: str = "dark"):
    removed = [g for g in GRAPH_DESCRIPTIONS if g not in active_graphs]
    if not removed:
        return
    rows = ""
    for g in removed:
        info = GRAPH_DESCRIPTIONS[g]
        rows += f"""
<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;padding:6px 10px;background:#3D1A1A;border-radius:6px">
  <span style="color:#FF6B6B;font-size:13px">&#10007;</span>
  <span style="color:{info['color']};font-weight:600;font-size:12px">{info['label']}</span>
  <span style="color:#AAAAAA;font-size:11px">&mdash; cannot answer {info['query_type'].lower()}</span>
</div>"""
    html = f"""
<div style="background:#2D1A1A;border:1px solid rgba(255,107,107,0.3);border-radius:10px;padding:14px">
  <div style="color:#FF6B6B;font-size:12px;font-weight:700;margin-bottom:8px">&#9888; Capability Gaps &mdash; What MAGMA Can't Do Now</div>
  {rows}
</div>
"""
    n = len(removed)
    components.html(_html_doc(html, theme), height=56 + n * 42, scrolling=False)


# ---------------------------------------------------------------------------
# Score status block (below gauge)
# ---------------------------------------------------------------------------
def render_score_status(score: float, theme: str = "dark"):
    delta = score - 0.700
    delta_str = f"{delta:+.3f}" if delta != 0 else "&plusmn;0.000"
    delta_color = "#FF6B6B" if delta < 0 else "#00BFA5"

    if score >= 0.68:
        status_msg, status_color = "Full MAGMA &mdash; all graphs active", "#00BFA5"
    elif score >= 0.60:
        status_msg, status_color = "Degraded &mdash; some capability lost", "#FFB347"
    elif score >= 0.50:
        status_msg, status_color = "Significantly impaired", "#FF6B6B"
    else:
        status_msg, status_color = "Below baseline &mdash; critical failure", "#FF3333"

    html = f"""
<div style="background:#1A1D2E;border:1px solid {delta_color}55;border-radius:10px;padding:12px;text-align:center">
  <div style="color:{delta_color};font-size:22px;font-weight:700">vs MAGMA: {delta_str}</div>
  <div style="color:{status_color};font-size:12px;margin-top:4px">{status_msg}</div>
  <div style="display:flex;justify-content:center;gap:16px;margin-top:10px">
    <div style="text-align:center">
      <div style="color:#6C63FF;font-size:14px;font-weight:700">0.700</div>
      <div style="color:#777;font-size:10px">Full MAGMA</div>
    </div>
    <div style="color:#444;font-size:18px">&rarr;</div>
    <div style="text-align:center">
      <div style="color:{delta_color};font-size:14px;font-weight:700">{score:.3f}</div>
      <div style="color:#777;font-size:10px">Current</div>
    </div>
  </div>
</div>
"""
    components.html(_html_doc(html, theme), height=130, scrolling=False)


# ---------------------------------------------------------------------------
# Final score / achievement card
# ---------------------------------------------------------------------------
def _render_final_score(theme: str = "dark"):
    total_score = st.session_state.get("score", 0)
    if total_score >= 900:
        badge, badge_color, badge_icon, badge_bg = "Master of MAGMA", "#FFD700", "&#9733;", "#2D2800"
        message = "You've mastered every concept in the paper. Outstanding!"
    elif total_score >= 600:
        badge, badge_color, badge_icon, badge_bg = "Lead Detective", "#6C63FF", "&#9670;", "#1E1A35"
        message = "Strong grasp of MAGMA's architecture. Almost perfect!"
    elif total_score >= 300:
        badge, badge_color, badge_icon, badge_bg = "Senior Investigator", "#00BFA5", "&#9632;", "#1A2D2A"
        message = "Solid understanding of graph-based memory systems."
    else:
        badge, badge_color, badge_icon, badge_bg = "Rookie Detective", "#AAAAAA", "&#9679;", "#252840"
        message = "Keep exploring &mdash; revisit the investigation to earn more points!"

    milestones = [
        ("Act 1 &mdash; The Problem",             50,  total_score >= 50),
        ("Act 2 &mdash; Memory Building",         200, total_score >= 50),
        ("Act 3 &mdash; Investigation (4 queries)",400, total_score >= 450),
        ("Act 3 &mdash; Completion Bonus",         200, total_score >= 450),
        ("Act 4 &mdash; The Reveal",               100, total_score >= 550),
        ("Act 4 &mdash; Quiz Correct",             200, st.session_state.get("quiz_correct", False)),
        ("Act 5 &mdash; Ablation Challenge",        50, st.session_state.get("ablation_challenge_won", False)),
    ]
    milestone_rows = ""
    for label, pts, earned in milestones:
        color = "#00BFA5" if earned else "#444"
        icon = "&#10003;" if earned else "&#9675;"
        pts_str = f"+{pts}" if earned else f"{pts}"
        milestone_rows += f"""
<div style="display:flex;justify-content:space-between;align-items:center;padding:5px 0;border-bottom:1px solid #333">
  <span style="color:{color};font-size:11px">{icon} {label}</span>
  <span style="color:{color};font-size:11px;font-weight:600">{pts_str} pts</span>
</div>"""

    html = f"""
<div style="background:{badge_bg};border:2px solid {badge_color};border-radius:14px;overflow:hidden;margin-top:4px">
  <div style="text-align:center;padding:24px 20px 16px 20px">
    <div style="font-size:42px;color:{badge_color}">{badge_icon}</div>
    <div style="font-size:24px;font-weight:700;color:{badge_color};margin:8px 0 4px 0">{badge}</div>
    <div style="font-size:40px;color:#FAFAFA;font-weight:800;font-family:monospace">{total_score}</div>
    <div style="color:#AAAAAA;font-size:12px">detective points</div>
    <div style="color:{badge_color};font-size:13px;margin-top:8px;font-style:italic">{message}</div>
  </div>
  <div style="background:rgba(0,0,0,0.2);padding:14px 20px">
    <div style="color:#AAAAAA;font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px">Score Breakdown</div>
    {milestone_rows}
  </div>
  <div style="text-align:center;padding:12px 20px;background:rgba(0,0,0,0.15)">
    <div style="color:#666;font-size:11px">MAGMA Interactive Demo &nbsp;&middot;&nbsp; Based on the research paper</div>
  </div>
</div>
"""
    components.html(_html_doc(html, theme), height=480, scrolling=False)


# ---------------------------------------------------------------------------
# render_ablation — main entry point
# ---------------------------------------------------------------------------
def render_ablation(theme: str = "dark"):
    render_architecture_overview(theme)

    st.markdown("---")

    col_controls, col_gauge = st.columns([1, 1], gap="large")

    with col_controls:
        st.markdown(
            '<div style="color:#AAAAAA;font-size:12px;font-weight:600;letter-spacing:1px;'
            'text-transform:uppercase;margin-bottom:12px">Toggle Memory Graphs</div>',
            unsafe_allow_html=True,
        )
        active_graphs = []
        for gtype, info in GRAPH_DESCRIPTIONS.items():
            checked = st.checkbox(
                f"{info['icon']} {info['label']}",
                value=True,
                key=f"ablation_{gtype}",
            )
            if checked:
                active_graphs.append(gtype)

        st.markdown("---")
        st.markdown(
            '<div style="background:#252840;border:1px solid rgba(255,179,71,0.3);border-radius:8px;'
            'padding:10px 14px;margin-bottom:12px">'
            '<div style="color:#FFB347;font-size:11px;font-weight:700">&#127919; Challenge</div>'
            '<div style="color:#CCCCCC;font-size:12px;margin-top:4px">Can you get the score below '
            '<b style="color:#FF6B6B">0.500</b>?</div>'
            '<div style="color:#AAAAAA;font-size:11px;margin-top:2px">That\'s below the Full Context baseline.</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        if st.button("Reset — Enable All Graphs", use_container_width=True):
            for gtype in GRAPH_DESCRIPTIONS:
                st.session_state[f"ablation_{gtype}"] = True
            st.rerun()

    score = _get_score(active_graphs)

    with col_gauge:
        st.plotly_chart(render_gauge(score, theme), use_container_width=True)
        render_score_status(score, theme)

        if score <= 0.481 and not st.session_state.get("ablation_challenge_won"):
            st.session_state["score"] = st.session_state.get("score", 0) + 50
            st.session_state["ablation_challenge_won"] = True
            st.success("Challenge unlocked! Score dropped below baseline. +50 pts!")

    st.plotly_chart(render_score_breakdown_chart(active_graphs, theme), use_container_width=True)
    render_graph_cards(active_graphs, theme)
    render_capability_gaps(active_graphs, theme)

    st.markdown("---")

    # Final score card
    _render_final_score(theme)

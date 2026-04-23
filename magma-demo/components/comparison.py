"""
comparison.py — Act 4: Side-by-side MAGMA vs Baseline comparison.
Uses components.html() for all rich HTML blocks (same pattern as Acts 2 & 3).
"""

import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
from data.scenario import BASELINES, TOKEN_STATS, CATEGORY_SCORES
from data.themes import LIGHT_IFRAME_CSS, plotly_layout, plotly_grid, plotly_bar_muted, plotly_legend

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


# ---------------------------------------------------------------------------
# render_verdict_banner
# ---------------------------------------------------------------------------
def render_verdict_banner(theme: str = "dark"):
    html = """
<div style="text-align:center;padding:24px 20px;background:linear-gradient(135deg,#1A1D2E 0%,#252840 100%);border:1px solid #444;border-radius:16px;margin-bottom:4px">
  <div style="color:#AAAAAA;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:16px">THE VERDICT</div>
  <div style="display:flex;justify-content:center;align-items:center;gap:32px;flex-wrap:wrap">

    <div style="text-align:center">
      <div style="color:#FF6B6B;font-size:54px;font-weight:800;line-height:1;font-family:monospace">0.481</div>
      <div style="color:#FF6B6B;font-size:12px;font-weight:700;margin-top:6px">BASELINE</div>
      <div style="color:#888;font-size:11px">Full Context</div>
      <div style="margin-top:8px;background:#2D1A1A;border-radius:6px;padding:4px 10px;display:inline-block">
        <span style="color:#FF4444;font-size:11px">101,000 tokens/query</span>
      </div>
    </div>

    <div style="text-align:center">
      <div style="color:#444;font-size:28px;font-weight:300;margin-bottom:6px">vs</div>
      <div style="background:#1A2D1A;border:1px solid #00BFA5;border-radius:8px;padding:6px 12px">
        <div style="color:#00BFA5;font-size:16px;font-weight:700">+45.5%</div>
        <div style="color:#AAAAAA;font-size:10px">accuracy gain</div>
      </div>
      <div style="background:#1E1A35;border:1px solid #6C63FF;border-radius:8px;padding:6px 12px;margin-top:6px">
        <div style="color:#6C63FF;font-size:16px;font-weight:700">97&times;</div>
        <div style="color:#AAAAAA;font-size:10px">fewer tokens</div>
      </div>
    </div>

    <div style="text-align:center">
      <div style="color:#6C63FF;font-size:54px;font-weight:800;line-height:1;font-family:monospace">0.700</div>
      <div style="color:#6C63FF;font-size:12px;font-weight:700;margin-top:6px">MAGMA</div>
      <div style="color:#888;font-size:11px">Graph Retrieval</div>
      <div style="margin-top:8px;background:#1E1A35;border-radius:6px;padding:4px 10px;display:inline-block">
        <span style="color:#00BFA5;font-size:11px">~3,400 tokens/query</span>
      </div>
    </div>

  </div>

  <div style="margin-top:20px;max-width:480px;margin-left:auto;margin-right:auto">
    <div style="display:flex;justify-content:space-between;margin-bottom:4px">
      <span style="color:#AAAAAA;font-size:10px">Score</span>
      <span style="color:#AAAAAA;font-size:10px">0.3 → 0.8 range</span>
    </div>
    <div style="background:#12141F;border-radius:6px;height:12px;overflow:hidden;border:1px solid #333;position:relative">
      <div style="background:linear-gradient(90deg,#FF6B6B,#FF4444);width:40%;height:100%;border-radius:6px;position:absolute;left:0;top:0;opacity:0.7"></div>
      <div style="background:linear-gradient(90deg,#6C63FF,#8B5CF6);width:80%;height:100%;border-radius:6px;position:absolute;left:0;top:0"></div>
    </div>
    <div style="display:flex;justify-content:space-between;margin-top:4px">
      <span style="color:#FF6B6B;font-size:10px">&larr; Baseline 0.481</span>
      <span style="color:#6C63FF;font-size:10px">MAGMA 0.700 &rarr;</span>
    </div>
  </div>
</div>
"""
    components.html(_html_doc(html, theme), height=290, scrolling=False)


# ---------------------------------------------------------------------------
# render_pipeline_comparison
# ---------------------------------------------------------------------------
def _flow_step(icon, title, subtitle, color, bg):
    return f"""
<div style="padding:9px 12px;background:{bg};border-radius:8px;border-left:3px solid {color};display:flex;align-items:center;gap:10px">
  <div style="font-size:18px">{icon}</div>
  <div>
    <div style="color:{color};font-size:11px;font-weight:600">{title}</div>
    <div style="color:#777;font-size:10px">{subtitle}</div>
  </div>
</div>"""

def _arrow():
    return '<div style="text-align:center;color:#444;font-size:16px;margin:1px 0">&darr;</div>'

def render_pipeline_comparison(theme: str = "dark"):
    baseline_steps = (
        _flow_step("💬", "Raw Chat History", "32 events &middot; unstructured text", "#777", "#252840") +
        _arrow() +
        _flow_step("📦", "Stuff Everything In", "101,000 tokens &middot; no filtering", "#FF6B6B", "#2D1A1A") +
        _arrow() +
        _flow_step("🤖", "LLM Reads Everything", "O(n&sup2;) attention &middot; no structure", "#CCCCCC", "#252840") +
        _arrow() +
        _flow_step("❌", "Vague, Uncited Answer", "Lost in noise &middot; hedged &middot; incomplete", "#FF4444", "#3D1A1A")
    )
    magma_steps = (
        _flow_step("🏷️", "Intent Detection", "WHY &rarr; Causal &middot; WHO &rarr; Entity", "#6C63FF", "#1E1A35") +
        _arrow() +
        _flow_step("🔀", "Graph Router Selects", "Routes to 1&ndash;2 relevant graphs", "#00BFA5", "#1E1A35") +
        _arrow() +
        _flow_step("🔍", "Targeted Traversal", "3&ndash;5 events retrieved &middot; 1.47s latency", "#FFB347", "#1E1A35") +
        _arrow() +
        _flow_step("✅", "Precise, Cited Answer", "~3,400 tokens &middot; multi-hop &middot; accurate", "#00BFA5", "#1A2D1A")
    )

    html = f"""
<div style="color:#AAAAAA;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;padding:2px 0">
  How Each Approach Answers a Query
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">

  <div style="background:#1A1D2E;border:1px solid rgba(255,107,107,0.3);border-radius:12px;padding:16px">
    <div style="color:#FF6B6B;font-weight:700;font-size:13px;margin-bottom:14px">&#10007; Full Context Baseline</div>
    <div style="display:flex;flex-direction:column;gap:4px">{baseline_steps}</div>
  </div>

  <div style="background:#1A1D2E;border:1px solid rgba(108,99,255,0.3);border-radius:12px;padding:16px">
    <div style="color:#6C63FF;font-weight:700;font-size:13px;margin-bottom:14px">&#10003; MAGMA Adaptive Retrieval</div>
    <div style="display:flex;flex-direction:column;gap:4px">{magma_steps}</div>
  </div>

</div>
"""
    components.html(_html_doc(html, theme), height=400, scrolling=False)


# ---------------------------------------------------------------------------
# render_answer_comparison
# ---------------------------------------------------------------------------
def render_answer_comparison(query: dict, theme: str = "dark"):
    criteria_bad = "".join([
        f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:3px"><span style="color:#FF4444;font-size:13px">&#10007;</span><span style="color:#CCBBBB;font-size:11px">{c}</span></div>'
        for c in ["Causal chain traced (WHY)", "Identifies introducer (WHO)", "Cites specific events", "Confident, un-hedged answer"]
    ])
    criteria_good = "".join([
        f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:3px"><span style="color:#00BFA5;font-size:13px">&#10003;</span><span style="color:#AADDCC;font-size:11px">{c}</span></div>'
        for c in ["Causal chain traced (WHY)", "Identifies introducer (WHO)", "Cites specific events", "Confident, un-hedged answer"]
    ])

    html = f"""
<div style="color:#AAAAAA;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;padding:2px 0">
  Answer Quality &mdash; Same Query, Two Systems
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">

  <div style="background:#1A1D2E;border:1px solid #FF6B6B;border-radius:12px;overflow:hidden">
    <div style="background:#2D1A1A;padding:10px 16px;border-bottom:1px solid rgba(255,107,107,0.3);display:flex;justify-content:space-between;align-items:center">
      <div style="color:#FF6B6B;font-weight:700;font-size:13px">&#10007; Baseline-Bot</div>
      <div style="background:rgba(255,107,107,0.15);border-radius:12px;padding:2px 10px"><span style="color:#FF6B6B;font-size:11px">101,000 tokens</span></div>
    </div>
    <div style="padding:14px 16px">
      <div style="color:#DDAAAA;font-size:13px;line-height:1.7;font-style:italic">{query["baseline_answer"]}</div>
    </div>
    <div style="padding:10px 16px;border-top:1px solid #333">
      <div style="color:#888;font-size:11px;font-weight:600;margin-bottom:6px">Quality criteria:</div>
      {criteria_bad}
    </div>
  </div>

  <div style="background:#1A1D2E;border:1px solid #00BFA5;border-radius:12px;overflow:hidden">
    <div style="background:#1A2D1A;padding:10px 16px;border-bottom:1px solid rgba(0,191,165,0.3);display:flex;justify-content:space-between;align-items:center">
      <div style="color:#00BFA5;font-weight:700;font-size:13px">&#10003; MAGMA-Agent</div>
      <div style="background:rgba(0,191,165,0.15);border-radius:12px;padding:2px 10px"><span style="color:#00BFA5;font-size:11px">{query['tokens_used']:,} tokens</span></div>
    </div>
    <div style="padding:14px 16px">
      <div style="color:#AADDCC;font-size:13px;line-height:1.7">{query["magma_answer"]}</div>
    </div>
    <div style="padding:10px 16px;border-top:1px solid #333">
      <div style="color:#888;font-size:11px;font-weight:600;margin-bottom:6px">Quality criteria:</div>
      {criteria_good}
    </div>
  </div>

</div>
"""
    components.html(_html_doc(html, theme), height=440, scrolling=False)


# ---------------------------------------------------------------------------
# render_token_savings_metric
# ---------------------------------------------------------------------------
def render_token_savings_metric(query: dict, theme: str = "dark"):
    reduction_pct = round((1 - query["tokens_used"] / query["baseline_tokens"]) * 100, 1)
    tokens_saved = query["baseline_tokens"] - query["tokens_used"]
    magma_width = max(1, round(query["tokens_used"] / query["baseline_tokens"] * 100, 1))

    html = f"""
<div style="background:#1A1D2E;border:1px solid #333;border-radius:12px;padding:18px 22px">
  <div style="color:#AAAAAA;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:14px">Token Efficiency &mdash; Same Query</div>

  <div style="margin-bottom:12px">
    <div style="display:flex;justify-content:space-between;margin-bottom:5px">
      <span style="color:#FF6B6B;font-size:12px;font-weight:600">Baseline (Full Context)</span>
      <span style="color:#FF6B6B;font-size:12px;font-weight:700">{query['baseline_tokens']:,} tokens</span>
    </div>
    <div style="background:#2D1A1A;border-radius:6px;height:20px;overflow:hidden">
      <div style="background:linear-gradient(90deg,#FF4444,#FF6B6B);width:100%;height:100%;border-radius:6px;display:flex;align-items:center;justify-content:flex-end;padding-right:8px">
        <span style="color:#fff;font-size:10px;font-weight:600">100%</span>
      </div>
    </div>
  </div>

  <div style="margin-bottom:16px">
    <div style="display:flex;justify-content:space-between;margin-bottom:5px">
      <span style="color:#00BFA5;font-size:12px;font-weight:600">MAGMA (Graph Retrieval)</span>
      <span style="color:#00BFA5;font-size:12px;font-weight:700">{query['tokens_used']:,} tokens</span>
    </div>
    <div style="background:#1A2D2A;border-radius:6px;height:20px;overflow:hidden">
      <div style="background:linear-gradient(90deg,#00BFA5,#00E5CC);width:{magma_width}%;height:100%;border-radius:6px;display:flex;align-items:center;padding-left:8px">
        <span style="color:#fff;font-size:10px;font-weight:600">{magma_width}%</span>
      </div>
    </div>
  </div>

  <div style="display:flex;gap:12px;flex-wrap:wrap;padding-top:12px;border-top:1px solid #333">
    <div style="flex:1;min-width:100px;text-align:center;background:#1E1A35;border-radius:8px;padding:10px">
      <div style="color:#6C63FF;font-size:22px;font-weight:700">{tokens_saved:,}</div>
      <div style="color:#AAAAAA;font-size:10px">tokens saved</div>
    </div>
    <div style="flex:1;min-width:100px;text-align:center;background:#1A2D1A;border-radius:8px;padding:10px">
      <div style="color:#00BFA5;font-size:22px;font-weight:700">{reduction_pct}%</div>
      <div style="color:#AAAAAA;font-size:10px">reduction</div>
    </div>
    <div style="flex:1;min-width:100px;text-align:center;background:#2D2418;border-radius:8px;padding:10px">
      <div style="color:#FFB347;font-size:22px;font-weight:700">1.47s</div>
      <div style="color:#AAAAAA;font-size:10px">query latency</div>
    </div>
  </div>
</div>
"""
    components.html(_html_doc(html, theme), height=240, scrolling=False)


# ---------------------------------------------------------------------------
# render_category_breakdown
# ---------------------------------------------------------------------------
def render_category_breakdown(theme: str = "dark"):
    rows_html = ""
    for cat, scores in CATEGORY_SCORES.items():
        magma = scores["MAGMA"]
        baseline = scores["Full Context"]
        delta = magma - baseline
        delta_color = "#00BFA5" if delta > 0 else "#FF6B6B"
        delta_str = f"+{delta:.3f}" if delta > 0 else f"{delta:.3f}"
        magma_pct = round(magma / 0.85 * 100, 1)
        baseline_pct = round(baseline / 0.85 * 100, 1)
        highlight = cat == "Adversarial"
        bg = "#1E1A35" if highlight else "#1A1D2E"
        border = "1px solid #6C63FF" if highlight else "1px solid #333"
        star = '<div style="color:#6C63FF;font-size:10px;margin-top:4px;font-style:italic">&#9733; Biggest improvement &mdash; causal graph neutralizes trick questions</div>' if highlight else ""
        rows_html += f"""
<div style="background:{bg};border:{border};border-radius:8px;padding:10px 14px;margin-bottom:6px">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
    <div style="color:#CCCCCC;font-size:12px;font-weight:600">{cat}</div>
    <div style="display:flex;gap:12px;align-items:center">
      <span style="color:#FF6B6B;font-size:11px;min-width:40px;text-align:right">{baseline:.3f}</span>
      <span style="color:#6C63FF;font-size:11px;min-width:40px;text-align:right">{magma:.3f}</span>
      <span style="color:{delta_color};font-size:11px;font-weight:700;min-width:50px;text-align:right">{delta_str}</span>
    </div>
  </div>
  <div style="display:flex;gap:4px;align-items:center">
    <div style="flex:1;background:#2D1A1A;border-radius:3px;height:6px;overflow:hidden">
      <div style="background:#FF6B6B;width:{baseline_pct}%;height:100%"></div>
    </div>
    <div style="flex:1;background:#1E1A35;border-radius:3px;height:6px;overflow:hidden">
      <div style="background:#6C63FF;width:{magma_pct}%;height:100%"></div>
    </div>
  </div>
  {star}
</div>"""

    header = """
<div style="display:flex;justify-content:space-between;padding:0 14px;margin-bottom:6px">
  <span style="color:#777;font-size:10px;font-weight:600">CATEGORY</span>
  <div style="display:flex;gap:12px">
    <span style="color:#FF6B6B;font-size:10px;font-weight:600;min-width:40px;text-align:right">BASELINE</span>
    <span style="color:#6C63FF;font-size:10px;font-weight:600;min-width:40px;text-align:right">MAGMA</span>
    <span style="color:#AAAAAA;font-size:10px;font-weight:600;min-width:50px;text-align:right">DELTA</span>
  </div>
</div>"""

    html = f"""
<div style="color:#AAAAAA;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;padding:2px 0">
  Category Breakdown &mdash; Where MAGMA Wins
</div>
{header}{rows_html}
"""
    components.html(_html_doc(html, theme), height=380, scrolling=False)


# ---------------------------------------------------------------------------
# render_key_insights
# ---------------------------------------------------------------------------
def render_key_insights(theme: str = "dark"):
    cards = [
        ("#6C63FF", "#1E1A35", "#6C63FF44", "4 Graphs", "Orthogonal memory types", "Semantic &middot; Temporal &middot; Causal &middot; Entity &mdash; each captures a different dimension of memory"),
        ("#00BFA5", "#1A2D1A", "#00BFA544", "1.47s", "Average query latency", "Fast Path ingests events in real-time; Slow Path consolidates nightly &mdash; no cold starts"),
        ("#FFB347", "#2D2418", "#FFB34744", "+53.7%", "Adversarial improvement", "MAGMA 0.742 vs Full Context 0.205 &mdash; causal graph sees through trick questions"),
        ("#FF6B6B", "#2D1A1A", "#FF6B6B44", "O(log&nbsp;n)", "Retrieval scaling", "Graph traversal scales sub-linearly vs O(n&sup2;) attention in full-context approaches"),
    ]
    cards_html = ""
    for color, bg, border_color, stat, label, desc in cards:
        cards_html += f"""
<div style="background:{bg};border:1px solid {border_color};border-radius:8px;padding:12px">
  <div style="color:{color};font-size:20px;font-weight:700">{stat}</div>
  <div style="color:#CCCCCC;font-size:12px;font-weight:600;margin-top:2px">{label}</div>
  <div style="color:#AAAAAA;font-size:11px;margin-top:4px">{desc}</div>
</div>"""

    html = f"""
<div style="background:linear-gradient(135deg,#1A1D2E,#252840);border:1px solid #444;border-radius:12px;padding:18px 22px">
  <div style="color:#AAAAAA;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:14px">Key Takeaways from the Paper</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">{cards_html}</div>
</div>
"""
    components.html(_html_doc(html, theme), height=240, scrolling=False)


# ---------------------------------------------------------------------------
# Plotly charts — theme-aware
# ---------------------------------------------------------------------------
def render_accuracy_chart(theme: str = "dark"):
    methods = list(BASELINES.keys())
    scores = list(BASELINES.values())
    muted = plotly_bar_muted(theme)
    colors = [muted if m != "MAGMA" else "#6C63FF" for m in methods]
    tf_color = "#333333" if theme == "light" else "#FAFAFA"
    fig = go.Figure(go.Bar(
        x=methods, y=scores, marker_color=colors,
        text=[f"{s:.3f}" for s in scores], textposition="outside",
        textfont=dict(color=tf_color, size=12),
    ))
    layout = plotly_layout(theme)
    grid = plotly_grid(theme)
    fig.update_layout(
        title=dict(text="Overall LoComo Accuracy (Judge Score)", font=dict(color=layout["font"]["color"], size=14)),
        xaxis=dict(gridcolor=grid), yaxis=dict(gridcolor=grid, range=[0.3, 0.8], title="Score"),
        height=300, margin=dict(t=50, b=20, l=20, r=20), showlegend=False,
        **layout,
    )
    fig.add_hline(y=0.7, line_dash="dot", line_color="#FFD700",
                  annotation_text="MAGMA: 0.700", annotation_font_color="#FFD700")
    return fig


def render_token_chart(theme: str = "dark"):
    methods = list(TOKEN_STATS.keys())
    tokens = list(TOKEN_STATS.values())
    muted = plotly_bar_muted(theme)
    colors = ["#6C63FF" if "MAGMA" in m else muted for m in methods]
    tf_color = "#333333" if theme == "light" else "#FAFAFA"
    fig = go.Figure(go.Bar(
        x=methods, y=tokens, marker_color=colors,
        text=[f"{t:,}" for t in tokens], textposition="outside",
        textfont=dict(color=tf_color, size=11),
    ))
    layout = plotly_layout(theme)
    grid = plotly_grid(theme)
    fig.update_layout(
        title=dict(text="Average Tokens per Query", font=dict(color=layout["font"]["color"], size=14)),
        xaxis=dict(gridcolor=grid), yaxis=dict(gridcolor=grid, title="Tokens"),
        height=300, margin=dict(t=50, b=20, l=20, r=20), showlegend=False,
        **layout,
    )
    return fig


def render_radar_chart(theme: str = "dark"):
    categories = list(CATEGORY_SCORES.keys())
    magma_vals   = [CATEGORY_SCORES[c]["MAGMA"]        for c in categories]
    nemori_vals  = [CATEGORY_SCORES[c]["Nemori"]       for c in categories]
    baseline_vals= [CATEGORY_SCORES[c]["Full Context"] for c in categories]
    cats_loop     = categories + [categories[0]]
    magma_loop    = magma_vals    + [magma_vals[0]]
    nemori_loop   = nemori_vals   + [nemori_vals[0]]
    baseline_loop = baseline_vals + [baseline_vals[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=magma_loop, theta=cats_loop, fill="toself",
                                   name="MAGMA", line_color="#6C63FF", fillcolor="rgba(108,99,255,0.2)"))
    fig.add_trace(go.Scatterpolar(r=nemori_loop, theta=cats_loop, fill="toself",
                                   name="Nemori", line_color="#00BFA5", fillcolor="rgba(0,191,165,0.1)"))
    fig.add_trace(go.Scatterpolar(r=baseline_loop, theta=cats_loop, fill="toself",
                                   name="Full Context", line_color="#FF6B6B", fillcolor="rgba(255,107,107,0.1)"))
    layout = plotly_layout(theme)
    grid = plotly_grid(theme)
    axis_color = "#777777" if theme == "light" else "#AAAAAA"
    text_color = layout["font"]["color"]
    polar_bg = "#F5F6FA" if theme == "light" else "#252840"
    fig.update_layout(
        title=dict(text="Per-Category Performance (LoComo)", font=dict(color=text_color, size=14)),
        polar=dict(
            bgcolor=polar_bg,
            radialaxis=dict(visible=True, range=[0.1, 0.85], color=axis_color, gridcolor=grid),
            angularaxis=dict(color=text_color, gridcolor=grid),
        ),
        legend=plotly_legend(theme),
        height=360, margin=dict(t=60, b=20, l=20, r=20),
        **layout,
    )
    return fig


# ---------------------------------------------------------------------------
# render_full_comparison — entry point called from app.py
# ---------------------------------------------------------------------------
def render_full_comparison(query: dict, theme: str = "dark"):
    render_verdict_banner(theme)
    st.markdown("---")
    render_pipeline_comparison(theme)
    st.markdown("---")
    render_answer_comparison(query, theme)
    st.markdown("---")
    render_token_savings_metric(query, theme)
    st.markdown("---")

    label_color = "#777777" if theme == "light" else "#AAAAAA"
    st.markdown(
        f'<div style="color:{label_color};font-size:12px;font-weight:600;letter-spacing:1px;'
        'text-transform:uppercase;margin-bottom:4px">Benchmark Results — All Methods</div>',
        unsafe_allow_html=True,
    )
    col_acc, col_tok = st.columns(2)
    with col_acc:
        st.plotly_chart(render_accuracy_chart(theme), use_container_width=True)
    with col_tok:
        st.plotly_chart(render_token_chart(theme), use_container_width=True)

    render_category_breakdown(theme)
    st.plotly_chart(render_radar_chart(theme), use_container_width=True)
    render_key_insights(theme)

    # 9. Quiz
    st.markdown("---")
    st.markdown(
        """
        <div style="background:#252840;border:1px solid rgba(108,99,255,0.3);border-radius:12px;padding:16px 20px;margin-bottom:16px">
          <div style="color:#6C63FF;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px">
            &#127919; Quick Quiz &mdash; Earn 200 Detective Points
          </div>
          <div style="color:#FAFAFA;font-size:15px;font-weight:600">
            Which query category did MAGMA improve the MOST over the Full Context baseline?
          </div>
          <div style="color:#888;font-size:12px;margin-top:4px">
            Hint: look at the category breakdown above &mdash; one delta stands out dramatically.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    quiz_answer = st.radio(
        "Your answer:",
        ["Single-hop", "Multi-hop", "Temporal", "Adversarial", "Conversational"],
        index=None,
        key="quiz_answer",
    )
    if quiz_answer is not None:
        if quiz_answer == "Adversarial":
            if not st.session_state.get("quiz_correct"):
                st.session_state["score"] = st.session_state.get("score", 0) + 200
                st.session_state["quiz_correct"] = True
            st.success("Correct! Adversarial: MAGMA 0.742 vs Full Context 0.205 — a +0.537 improvement!")
            st.balloons()
        else:
            if not st.session_state.get("quiz_wrong_" + quiz_answer):
                st.session_state["score"] = st.session_state.get("score", 0) + 10
                st.session_state["quiz_wrong_" + quiz_answer] = True
            st.error(
                "Not quite. Adversarial is the biggest jump: MAGMA 0.742 vs Full Context 0.205. "
                "Full context models are easily confused by trick questions — MAGMA's causal graph sees through them."
            )

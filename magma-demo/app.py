"""
MAGMA Interactive Demo — "The Study Group Mystery"
A gamified 5-act Streamlit demo of the MAGMA research paper.

Run: streamlit run app.py
"""

import time
import sys
import os
import io
import base64

import streamlit as st
import streamlit.components.v1 as components

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import qrcode

from data.scenario import EVENTS, QUERIES
from data.themes import LIGHT_APP_CSS
from components.graph_viz import build_graph_html, get_node_count, get_edge_count
from components.ingestion_anim import render_ingestion, render_event_bubble, SPEAKER_COLORS
from components.comparison import render_full_comparison
from components.ablation import render_ablation
from components.about import render_about

_APP_URL = "https://magma-agentic-memory-demo.streamlit.app/"


@st.cache_data
def _qr_b64() -> str:
    qr = qrcode.QRCode(version=1, box_size=5, border=2)
    qr.add_data(_APP_URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#6C63FF", back_color="#1A1D2E")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="MAGMA Memory Demo",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS
css_path = os.path.join(os.path.dirname(__file__), "styles", "custom.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state init
# ---------------------------------------------------------------------------
def init_state():
    defaults = {
        "act": 0,
        "score": 0,
        "theme": "dark",
        "act1_complete": False,
        "act2_complete": False,
        "act3_complete": False,
        "act4_complete": False,
        "queries_completed": set(),
        "traversal_running": False,
        "quiz_correct": False,
        "ablation_challenge_won": False,
        "act2_pts_earned": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

theme = st.session_state.get("theme", "dark")
if theme == "light":
    st.markdown(f"<style>{LIGHT_APP_CSS}</style>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
ACT_LABELS = {
    0: ("About the Paper", "📄"),
    1: ("The Problem", "🔴"),
    2: ("Memory Building", "🟡"),
    3: ("Investigation", "🔵"),
    4: ("The Reveal", "🟢"),
    5: ("Deep Dive", "⚪"),
}

with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center;padding:12px 0 4px 0">
          <div style="font-size:28px">🔍</div>
          <div style="font-size:20px;font-weight:700;color:#6C63FF">MAGMA Demo</div>
          <div style="font-size:11px;color:#AAAAAA">The Study Group Mystery</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    st.markdown("**ACT PROGRESS**")
    current_act = st.session_state["act"]
    for act_num, (label, icon) in ACT_LABELS.items():
        if act_num < current_act:
            status_icon = "✓"
            color = "#00BFA5"
        elif act_num == current_act:
            status_icon = "→"
            color = "#6C63FF"
        else:
            status_icon = "○"
            color = "#555555"

        if st.button(
            f"{status_icon} Act {act_num}: {label}",
            key=f"act_nav_{act_num}",
            use_container_width=True,
        ):
            st.session_state["act"] = act_num
            st.rerun()

    st.markdown("---")
    score = st.session_state["score"]
    if score >= 900:
        badge = "Master of MAGMA ★"
        badge_color = "#FFD700"
    elif score >= 600:
        badge = "Lead Detective ◆"
        badge_color = "#6C63FF"
    elif score >= 300:
        badge = "Senior Investigator ■"
        badge_color = "#00BFA5"
    else:
        badge = "Rookie Detective ●"
        badge_color = "#AAAAAA"

    filled = min(10, int(score / 100))
    bar = "█" * filled + "░" * (10 - filled)
    st.markdown(
        f"""
        <div style="margin-bottom:4px">
          <div style="font-size:12px;font-weight:600;color:#FAFAFA">DETECTIVE SCORE</div>
          <div style="font-family:monospace;color:#6C63FF;letter-spacing:1px">[{bar}] {score} pts</div>
          <div style="font-size:11px;color:{badge_color}">{badge}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size:11px;color:#666">
          PAPER STATS<br>
          MAGMA: <b style="color:#6C63FF">0.70</b> (LoComo)<br>
          Baseline: <b style="color:#FF6B6B">0.48</b><br>
          Token reduction: <b style="color:#00BFA5">95%</b><br>
          Query latency: <b style="color:#FFB347">1.47s</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align:center;padding:4px 0 8px 0">
          <img src="data:image/png;base64,{_qr_b64()}" width="130"
               style="border-radius:8px;display:block;margin:0 auto"/>
          <div style="font-size:10px;color:#666;margin-top:6px">Scan to open on mobile</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# ACT 0 — About the Paper
# ---------------------------------------------------------------------------
def render_act0():
    render_about()


# ---------------------------------------------------------------------------
# ACT 1 — The Problem
# ---------------------------------------------------------------------------
def render_act1():
    st.markdown(
        """
        <div style="text-align:center;padding:8px 0 20px 0">
          <div style="font-size:40px">🔴</div>
          <h1 style="color:#FAFAFA;margin:8px 0 4px 0">Act 1: The Problem</h1>
          <p style="color:#AAAAAA;font-size:15px;max-width:620px;margin:0 auto">
            An AI agent is handed 3 weeks of chat logs and asked a question.
            Watch what happens when there's <b style="color:#FF6B6B">no memory system</b>.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Scene-setting: Characters + Timeline strip ──────────────────────────
    st.markdown(
        """
        <div style="margin-bottom:6px;color:#AAAAAA;font-size:12px;font-weight:600;letter-spacing:1px;text-transform:uppercase">The Cast</div>
        <div style="display:flex;gap:10px;margin-bottom:20px;flex-wrap:wrap">
          <div style="flex:1;min-width:120px;background:#1E1A35;border:1px solid #6C63FF;border-radius:10px;padding:12px;text-align:center">
            <div style="font-size:26px">👨‍💻</div>
            <div style="color:#6C63FF;font-weight:700;font-size:13px">Alex</div>
            <div style="color:#AAAAAA;font-size:11px">Protagonist<br>Group organiser</div>
          </div>
          <div style="flex:1;min-width:120px;background:#1A2D2A;border:1px solid #00BFA5;border-radius:10px;padding:12px;text-align:center">
            <div style="font-size:26px">🧑‍🎓</div>
            <div style="color:#00BFA5;font-weight:700;font-size:13px">Jordan</div>
            <div style="color:#AAAAAA;font-size:11px">Trusted friend<br>Introduces Sam</div>
          </div>
          <div style="flex:1;min-width:120px;background:#2D1A1A;border:1px solid #FF6B6B;border-radius:10px;padding:12px;text-align:center">
            <div style="font-size:26px">🕵️</div>
            <div style="color:#FF6B6B;font-weight:700;font-size:13px">Sam</div>
            <div style="color:#AAAAAA;font-size:11px">The mystery<br>Disappears</div>
          </div>
          <div style="flex:1;min-width:120px;background:#2D2418;border:1px solid #FFB347;border-radius:10px;padding:12px;text-align:center">
            <div style="font-size:26px">👩‍🔬</div>
            <div style="color:#FFB347;font-weight:700;font-size:13px">Maya</div>
            <div style="color:#AAAAAA;font-size:11px">Witness<br>Raises alarm</div>
          </div>
          <div style="flex:1;min-width:120px;background:#1E2030;border:1px solid #FF69B4;border-radius:10px;padding:12px;text-align:center">
            <div style="font-size:26px">👩‍🏫</div>
            <div style="color:#FF69B4;font-weight:700;font-size:13px">Prof. Chen</div>
            <div style="color:#AAAAAA;font-size:11px">Instructor<br>Midterm source</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Timeline strip ──────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="display:flex;gap:0;margin-bottom:22px;border-radius:10px;overflow:hidden;border:1px solid #333">
          <div style="flex:1;background:#1E1A35;padding:10px 14px;border-right:1px solid #333">
            <div style="color:#6C63FF;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px">Week 1</div>
            <div style="color:#CCCCCC;font-size:12px;margin-top:3px">Trust Building</div>
            <div style="color:#555;font-size:11px">E01 – E10 · 10 events</div>
            <div style="color:#AAAAAA;font-size:11px;margin-top:4px">Alex joins · Jordan introduces Sam · Group bonds form</div>
          </div>
          <div style="flex:1;background:#1A2D2A;padding:10px 14px;border-right:1px solid #333">
            <div style="color:#00BFA5;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px">Week 2</div>
            <div style="color:#CCCCCC;font-size:12px;margin-top:3px">The Setup</div>
            <div style="color:#555;font-size:11px">E11 – E22 · 12 events</div>
            <div style="color:#AAAAAA;font-size:11px;margin-top:4px">Sam requests notes · $20 loan · Trust exploited</div>
          </div>
          <div style="flex:1;background:#2D1A1A;padding:10px 14px">
            <div style="color:#FF6B6B;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px">Week 3</div>
            <div style="color:#CCCCCC;font-size:12px;margin-top:3px">Midterm Week</div>
            <div style="color:#555;font-size:11px">E23 – E32 · 10 events</div>
            <div style="color:#AAAAAA;font-size:11px;margin-top:4px">Exam stolen · Sam disappears · Maya reports to Dean</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Baseline architecture flow diagram ─────────────────────────────────
    st.markdown(
        '<div style="color:#AAAAAA;font-size:12px;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px">How the Baseline Agent Works (No Memory System)</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:6px;margin-bottom:20px;flex-wrap:wrap">

          <!-- Box 1: Input -->
          <div style="flex:1;min-width:130px;background:#1A1D2E;border:1px solid #444;border-radius:10px;padding:14px;text-align:center">
            <div style="font-size:22px">💬</div>
            <div style="color:#CCCCCC;font-weight:700;font-size:13px;margin-top:4px">Chat History</div>
            <div style="color:#AAAAAA;font-size:11px">32 events<br>3 weeks of logs</div>
          </div>

          <!-- Arrow -->
          <div style="color:#555;font-size:22px;font-weight:300">→</div>

          <!-- Box 2: Stuffing -->
          <div style="flex:1;min-width:130px;background:#2D1A1A;border:2px solid #FF6B6B;border-radius:10px;padding:14px;text-align:center">
            <div style="font-size:22px">📦</div>
            <div style="color:#FF6B6B;font-weight:700;font-size:13px;margin-top:4px">Stuff Everything In</div>
            <div style="color:#DDAAAA;font-size:11px">101,000 tokens<br>per query</div>
          </div>

          <!-- Arrow -->
          <div style="color:#555;font-size:22px;font-weight:300">→</div>

          <!-- Box 3: LLM -->
          <div style="flex:1;min-width:130px;background:#1E2030;border:1px solid #444;border-radius:10px;padding:14px;text-align:center">
            <div style="font-size:22px">🤖</div>
            <div style="color:#CCCCCC;font-weight:700;font-size:13px;margin-top:4px">LLM</div>
            <div style="color:#AAAAAA;font-size:11px">Processes entire<br>context window</div>
          </div>

          <!-- Arrow -->
          <div style="color:#555;font-size:22px;font-weight:300">→</div>

          <!-- Box 4: Vague Output -->
          <div style="flex:1;min-width:130px;background:#2D1A1A;border:2px solid #FF4444;border-radius:10px;padding:14px;text-align:center">
            <div style="font-size:22px">❌</div>
            <div style="color:#FF4444;font-weight:700;font-size:13px;margin-top:4px">Vague Answer</div>
            <div style="color:#DDAAAA;font-size:11px">Lost in noise<br>No citations</div>
          </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Token cost visual ───────────────────────────────────────────────────
    st.markdown(
        """
        <div style="background:#1A1D2E;border:1px solid #333;border-radius:10px;padding:16px 20px;margin-bottom:20px">
          <div style="color:#AAAAAA;font-size:12px;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px">Token Cost Per Query</div>

          <!-- Baseline bar -->
          <div style="margin-bottom:10px">
            <div style="display:flex;justify-content:space-between;margin-bottom:4px">
              <span style="color:#FF6B6B;font-size:12px;font-weight:600">Baseline (Full Context)</span>
              <span style="color:#FF6B6B;font-size:12px;font-weight:700">101,000 tokens</span>
            </div>
            <div style="background:#2D1A1A;border-radius:4px;height:16px;overflow:hidden">
              <div style="background:linear-gradient(90deg,#FF4444,#FF6B6B);width:100%;height:100%;border-radius:4px"></div>
            </div>
          </div>

          <!-- MAGMA bar -->
          <div style="margin-bottom:10px">
            <div style="display:flex;justify-content:space-between;margin-bottom:4px">
              <span style="color:#00BFA5;font-size:12px;font-weight:600">MAGMA (Graph Retrieval)</span>
              <span style="color:#00BFA5;font-size:12px;font-weight:700">~3,400 tokens</span>
            </div>
            <div style="background:#1A2D2A;border-radius:4px;height:16px;overflow:hidden">
              <div style="background:linear-gradient(90deg,#00BFA5,#00E5CC);width:3.4%;height:100%;border-radius:4px"></div>
            </div>
          </div>

          <div style="display:flex;gap:16px;margin-top:12px;padding-top:10px;border-top:1px solid #333">
            <div style="text-align:center;flex:1">
              <div style="color:#FF6B6B;font-size:20px;font-weight:700">97×</div>
              <div style="color:#AAAAAA;font-size:11px">more tokens wasted</div>
            </div>
            <div style="text-align:center;flex:1">
              <div style="color:#00BFA5;font-size:20px;font-weight:700">95%</div>
              <div style="color:#AAAAAA;font-size:11px">reduction with MAGMA</div>
            </div>
            <div style="text-align:center;flex:1">
              <div style="color:#FFB347;font-size:20px;font-weight:700">O(n²)</div>
              <div style="color:#AAAAAA;font-size:11px">scaling with full context</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Conversation log ────────────────────────────────────────────────────
    WEEK_SUMMARIES = {
        1: {
            "label": "Week 1 — Trust Building",
            "color": "#6C63FF",
            "bg": "#1E1A35",
            "border": "#6C63FF",
            "events": "E01–E09 · 9 events",
            "crux": "Alex joins the group via Jordan. Mid-week, Jordan introduces Sam — a dorm friend who impresses everyone with his algorithm skills. Within <b>3 days</b> of joining, Sam asks Jordan for $50 ('textbook situation'). Jordan lends immediately.",
            "key_moment": "E05: Jordan vouches for Sam → unlocks his access to the group's trust network",
            "signal": "🟡 First red flag: money request arrives suspiciously fast after joining",
        },
        2: {
            "label": "Week 2 — The Setup",
            "color": "#00BFA5",
            "bg": "#1A2D2A",
            "border": "#00BFA5",
            "events": "E10–E20 · 11 events",
            "crux": "The group learns Prof. Chen's private handwritten notes contain exam gold (never posted publicly). Sam is spotted by Maya at the library <b>photographing those notes</b>. The group dismisses it. Sam then asks Alex for another $30 using Jordan's social vouching.",
            "key_moment": "E14: Maya witnesses Sam photographing Chen's notes — the group ignores the warning",
            "signal": "🔴 Critical event: the theft happens here, but no one connects the dots yet",
        },
        3: {
            "label": "Week 3 — Midterm Week",
            "color": "#FF6B6B",
            "bg": "#2D1A1A",
            "border": "#FF6B6B",
            "events": "E21–E32 · 12 events",
            "crux": "Sam vanishes immediately after the exam. Maya connects the dots — shared doc notes match exam questions word-for-word. Grades drop: Sam <b>97/100</b>, everyone else ~60. Sam scrubs his social presence. Jordan is devastated — he introduced him. Maya reports to the Dean; $80 in loans gone.",
            "key_moment": "E26: Grades posted. Sam 97, Alex 61, Jordan 58 — the numbers tell the story",
            "signal": "🔴 Deception complete: borrowed trust, stolen notes, ghosted group",
        },
    }

    with st.expander("📜 View the full conversation log (32 events)", expanded=False):
        # Group events by week
        from collections import defaultdict
        weeks = defaultdict(list)
        for event in EVENTS:
            weeks[event["week"]].append(event)

        event_html = ""
        for week_num in sorted(weeks.keys()):
            s = WEEK_SUMMARIES[week_num]
            # Week header label
            event_html += (
                f'<div style="color:{s["color"]};font-size:11px;font-weight:600;'
                f'margin:20px 0 8px 4px;letter-spacing:0.5px;text-transform:uppercase">'
                f'{s["label"]}</div>'
            )
            # Events first
            for event in weeks[week_num]:
                event_html += render_event_bubble(event)
            # Summary card after the events
            event_html += (
                f'<div style="margin:12px 0 4px 0;background:{s["bg"]};border:1px solid {s["border"]};'
                f'border-radius:10px;padding:14px 16px;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">'
                f'<span style="color:{s["color"]};font-weight:700;font-size:13px">Week {week_num} Recap</span>'
                f'<span style="color:#555;font-size:11px">{s["events"]}</span>'
                f'</div>'
                f'<div style="color:#CCCCCC;font-size:12px;line-height:1.6;margin-bottom:10px">{s["crux"]}</div>'
                f'<div style="background:#00000033;border-radius:6px;padding:8px 10px;margin-bottom:8px">'
                f'<span style="color:{s["color"]};font-size:11px;font-weight:600">Key moment: </span>'
                f'<span style="color:#AAAAAA;font-size:11px">{s["key_moment"]}</span>'
                f'</div>'
                f'<div style="color:#AAAAAA;font-size:11px;font-style:italic">{s["signal"]}</div>'
                f'</div>'
            )

        log_doc = (
            "<html><head><style>"
            "body{margin:0;padding:8px 10px;background:#1A1D2E;"
            "font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;}"
            "</style></head>"
            f"<body>{event_html}</body></html>"
        )
        components.html(log_doc, height=500, scrolling=True)

    # ── The question ────────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="padding:18px 20px;background:#252840;border:2px solid #6C63FF;border-radius:10px;margin:20px 0 16px 0">
          <div style="color:#6C63FF;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px">🕵️ The Investigative Query</div>
          <div style="color:#FAFAFA;font-size:18px;font-weight:600;line-height:1.5">"Why did Sam disappear after the midterm, and who introduced him to the group?"</div>
          <div style="display:flex;gap:10px;margin-top:12px;flex-wrap:wrap">
            <span style="background:#FF6B6B22;border:1px solid #FF6B6B;color:#FF6B6B;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:600">WHY (causal)</span>
            <span style="background:#FFB34722;border:1px solid #FFB347;color:#FFB347;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:600">WHO (entity)</span>
            <span style="background:#33333388;border:1px solid #555;color:#AAAAAA;padding:3px 10px;border-radius:12px;font-size:11px">Multi-hop · Spans 3 weeks · Requires causal chain</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Baseline failure — annotated ────────────────────────────────────────
    st.markdown(
        '<div style="background:#1A1D2E;border:1px solid #333;border-radius:10px;padding:16px;margin-bottom:20px">'
        '<div style="color:#AAAAAA;font-size:12px;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px">Baseline Agent Response (after reading 101,000 tokens)</div>'
        '<div style="display:flex;gap:14px;align-items:flex-start">'
        '<div style="font-size:32px;flex-shrink:0;margin-top:4px">🤖</div>'
        '<div style="flex:1">'
        '<div style="background:#2D1A1A;border:1px solid #FF6B6B;border-radius:8px;padding:14px">'
        '<div style="color:#DDAAAA;font-size:13px;font-style:italic;line-height:1.8">'
        '"I\'m not sure why Sam left the group. <span style="background:#FF444444;border-radius:3px;padding:1px 5px;color:#FF8888;font-style:normal;font-size:11px;font-weight:700">① vague</span>'
        '<br>There were many messages about studying and exams. It might be related to the midterm, <span style="background:#FF444444;border-radius:3px;padding:1px 5px;color:#FF8888;font-style:normal;font-size:11px;font-weight:700">② hedged</span>'
        '<br>but with so many conversations I can\'t be certain of the exact cause. There were also some financial exchanges mentioned at some point..." <span style="background:#FF444444;border-radius:3px;padding:1px 5px;color:#FF8888;font-style:normal;font-size:11px;font-weight:700">③ incomplete</span>'
        '</div>'
        '</div>'
        '<div style="display:flex;gap:8px;margin-top:10px;flex-wrap:wrap">'
        '<div style="background:#2D1A1A;border:1px solid #FF4444;border-radius:6px;padding:6px 10px;font-size:11px;color:#DDAAAA"><span style="color:#FF4444;font-weight:700">① </span>Fails the WHY — no causal chain traced</div>'
        '<div style="background:#2D1A1A;border:1px solid #FF4444;border-radius:6px;padding:6px 10px;font-size:11px;color:#DDAAAA"><span style="color:#FF4444;font-weight:700">② </span>"Might be" — hedged, no source cited</div>'
        '<div style="background:#2D1A1A;border:1px solid #FF4444;border-radius:6px;padding:6px 10px;font-size:11px;color:#DDAAAA"><span style="color:#FF4444;font-weight:700">③ </span>Misses WHO entirely — Jordan never mentioned</div>'
        '</div>'
        '</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Three failure modes ─────────────────────────────────────────────────
    st.markdown(
        """
        <div style="display:flex;gap:10px;margin-bottom:24px;flex-wrap:wrap">
          <div style="flex:1;min-width:160px;background:#2D1A1A;border:1px solid #FF6B6B;border-radius:10px;padding:14px;text-align:center">
            <div style="font-size:24px">🌊</div>
            <div style="color:#FF6B6B;font-weight:700;font-size:13px;margin-top:6px">Lost in Noise</div>
            <div style="color:#CCBBBB;font-size:11px;margin-top:4px">101K tokens overwhelm the model. Key events drown in irrelevant messages.</div>
          </div>
          <div style="flex:1;min-width:160px;background:#2D1A1A;border:1px solid #FF6B6B;border-radius:10px;padding:14px;text-align:center">
            <div style="font-size:24px">🔗</div>
            <div style="color:#FF6B6B;font-weight:700;font-size:13px;margin-top:6px">No Causal Chain</div>
            <div style="color:#CCBBBB;font-size:11px;margin-top:4px">Flat text can't express cause → effect. Multi-hop reasoning breaks down.</div>
          </div>
          <div style="flex:1;min-width:160px;background:#2D1A1A;border:1px solid #FF6B6B;border-radius:10px;padding:14px;text-align:center">
            <div style="font-size:24px">📈</div>
            <div style="color:#FF6B6B;font-weight:700;font-size:13px;margin-top:6px">Scales Quadratically</div>
            <div style="color:#CCBBBB;font-size:11px;margin-top:4px">Longer conversations → exponentially more tokens. Every. Single. Query.</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("See how MAGMA solves this →", use_container_width=True, type="primary"):
            if not st.session_state["act1_complete"]:
                st.session_state["score"] += 50
                st.session_state["act1_complete"] = True
            st.session_state["act"] = 2
            st.rerun()

# ---------------------------------------------------------------------------
# ACT 2 — Memory Building
# ---------------------------------------------------------------------------
def render_act2():
    st.markdown(
        '<div style="text-align:center;padding:8px 0 16px 0">'
        '<div style="font-size:40px">🟡</div>'
        '<h1 style="color:#FAFAFA;margin:8px 0 4px 0">Act 2: Memory Building</h1>'
        '<p style="color:#AAAAAA;font-size:15px;max-width:640px;margin:0 auto">'
        'MAGMA ingests 32 events through two parallel write paths into <b style="color:#FFB347">4 orthogonal memory graphs</b>.'
        '</p></div>',
        unsafe_allow_html=True,
    )

    # ── Dual-stream ingestion diagram ───────────────────────────────────────
    st.markdown(
        '<div style="color:#AAAAAA;font-size:12px;font-weight:600;letter-spacing:1px;'
        'text-transform:uppercase;margin-bottom:10px">How Events Become Memory</div>',
        unsafe_allow_html=True,
    )
    stream_html = (
        '<div style="background:#1A1D2E;border:1px solid #333;border-radius:12px;padding:20px;margin-bottom:20px">'

        # Incoming event at top
        '<div style="text-align:center;margin-bottom:16px">'
        '<div style="display:inline-block;background:#252840;border:2px solid #FFB347;border-radius:10px;padding:10px 24px">'
        '<div style="font-size:18px">💬</div>'
        '<div style="color:#FFB347;font-weight:700;font-size:13px;margin-top:4px">Incoming Event</div>'
        '<div style="color:#AAAAAA;font-size:11px">e.g. "Jordan introduces Sam"</div>'
        '</div></div>'

        # Arrow down + split
        '<div style="display:flex;justify-content:center;gap:0;margin-bottom:12px">'
        '<div style="width:2px;height:20px;background:linear-gradient(180deg,#FFB347,#555);margin:0 auto"></div>'
        '</div>'

        # Two paths side by side
        '<div style="display:flex;gap:12px;align-items:flex-start">'

        # Fast path
        '<div style="flex:1;background:#1A2420;border:1px solid #00BFA5;border-radius:10px;padding:14px">'
        '<div style="display:flex;align-items:center;gap:8px;margin-bottom:10px">'
        '<span style="font-size:18px">⚡</span>'
        '<span style="color:#00BFA5;font-weight:700;font-size:13px">Fast Path</span>'
        '<span style="background:#00BFA522;border:1px solid #00BFA5;color:#00BFA5;font-size:10px;padding:2px 7px;border-radius:8px">Real-time · Non-blocking</span>'
        '</div>'
        '<div style="color:#AADDCC;font-size:12px;line-height:1.5;margin-bottom:12px">'
        'Indexes immediately from the event alone — no cross-event reasoning needed.'
        '</div>'
        '<div style="display:flex;gap:8px">'
        '<div style="flex:1;background:#1E1A35;border:1px solid #6C63FF;border-radius:8px;padding:10px;text-align:center">'
        '<div style="color:#6C63FF;font-size:18px;font-weight:700">●</div>'
        '<div style="color:#6C63FF;font-size:12px;font-weight:600">Semantic</div>'
        '<div style="color:#AAAAAA;font-size:10px;margin-top:3px">Topic similarity<br>Embedding-based</div>'
        '</div>'
        '<div style="flex:1;background:#1A2D2A;border:1px solid #00BFA5;border-radius:8px;padding:10px;text-align:center">'
        '<div style="color:#00BFA5;font-size:18px;font-weight:700">■</div>'
        '<div style="color:#00BFA5;font-size:12px;font-weight:600">Temporal</div>'
        '<div style="color:#AAAAAA;font-size:10px;margin-top:3px">Time-ordered chain<br>Append-only</div>'
        '</div>'
        '</div>'
        '</div>'

        # Divider
        '<div style="display:flex;align-items:center;padding:0 4px">'
        '<div style="color:#444;font-size:20px">⟷</div>'
        '</div>'

        # Slow path
        '<div style="flex:1;background:#2D1F1A;border:1px solid #FFB347;border-radius:10px;padding:14px">'
        '<div style="display:flex;align-items:center;gap:8px;margin-bottom:10px">'
        '<span style="font-size:18px">🔄</span>'
        '<span style="color:#FFB347;font-weight:700;font-size:13px">Slow Path</span>'
        '<span style="background:#FFB34722;border:1px solid #FFB347;color:#FFB347;font-size:10px;padding:2px 7px;border-radius:8px">Async · LLM-assisted</span>'
        '</div>'
        '<div style="color:#DDCCAA;font-size:12px;line-height:1.5;margin-bottom:12px">'
        'Runs after ingestion. Requires reasoning across multiple events to build correctly.'
        '</div>'
        '<div style="display:flex;gap:8px">'
        '<div style="flex:1;background:#2D1A1A;border:1px solid #FF6B6B;border-radius:8px;padding:10px;text-align:center">'
        '<div style="color:#FF6B6B;font-size:18px;font-weight:700">◆</div>'
        '<div style="color:#FF6B6B;font-size:12px;font-weight:600">Causal</div>'
        '<div style="color:#AAAAAA;font-size:10px;margin-top:3px">Cause → Effect<br>LLM-inferred</div>'
        '</div>'
        '<div style="flex:1;background:#2D2418;border:1px solid #FFB347;border-radius:8px;padding:10px;text-align:center">'
        '<div style="color:#FFB347;font-size:18px;font-weight:700">★</div>'
        '<div style="color:#FFB347;font-size:12px;font-weight:600">Entity</div>'
        '<div style="color:#AAAAAA;font-size:10px;margin-top:3px">Person tracking<br>Cross-event links</div>'
        '</div>'
        '</div>'
        '</div>'
        '</div>'  # end two-path flex
        '</div>'  # end outer card
    )
    st.markdown(stream_html, unsafe_allow_html=True)

    # ── One event, four perspectives ────────────────────────────────────────
    st.markdown(
        '<div style="color:#AAAAAA;font-size:12px;font-weight:600;letter-spacing:1px;'
        'text-transform:uppercase;margin-bottom:10px">Example: How One Event Gets Indexed</div>',
        unsafe_allow_html=True,
    )
    example_html = (
        '<div style="background:#1A1D2E;border:1px solid #333;border-radius:12px;padding:16px;margin-bottom:20px">'

        # The event
        '<div style="background:#252840;border-left:3px solid #00BFA5;border-radius:6px;padding:10px 14px;margin-bottom:14px">'
        '<div style="color:#00BFA5;font-size:11px;font-weight:600;margin-bottom:3px">EVENT E05 · Week 1, Wed 2:00pm · Jordan</div>'
        '<div style="color:#EAEAEA;font-size:13px">"Hey everyone — this is Sam, he\'s in my dorm. Super sharp with algorithms, let\'s bring him in!"</div>'
        '</div>'

        # Four index cards
        '<div style="display:flex;gap:10px;flex-wrap:wrap">'

        '<div style="flex:1;min-width:140px;background:#1E1A35;border:1px solid #6C63FF;border-radius:8px;padding:10px">'
        '<div style="color:#6C63FF;font-size:11px;font-weight:700;margin-bottom:5px">● SEMANTIC INDEX</div>'
        '<div style="color:#CCCCDD;font-size:11px;line-height:1.5">Linked to E01 (Alex joins) — same topic: group onboarding</div>'
        '</div>'

        '<div style="flex:1;min-width:140px;background:#1A2D2A;border:1px solid #00BFA5;border-radius:8px;padding:10px">'
        '<div style="color:#00BFA5;font-size:11px;font-weight:700;margin-bottom:5px">■ TEMPORAL INDEX</div>'
        '<div style="color:#AADDCC;font-size:11px;line-height:1.5">Chained E04 → E05 → E06. Timestamp locked in sequence.</div>'
        '</div>'

        '<div style="flex:1;min-width:140px;background:#2D1A1A;border:1px solid #FF6B6B;border-radius:8px;padding:10px">'
        '<div style="color:#FF6B6B;font-size:11px;font-weight:700;margin-bottom:5px">◆ CAUSAL INDEX</div>'
        '<div style="color:#DDAAAA;font-size:11px;line-height:1.5">E05 → E08 (Sam asks Jordan for $50). Intro creates the trust that enables the ask.</div>'
        '</div>'

        '<div style="flex:1;min-width:140px;background:#2D2418;border:1px solid #FFB347;border-radius:8px;padding:10px">'
        '<div style="color:#FFB347;font-size:11px;font-weight:700;margin-bottom:5px">★ ENTITY INDEX</div>'
        '<div style="color:#DDCCAA;font-size:11px;line-height:1.5">Nodes created: Sam, Jordan, Alex, StudyGroup. All linked to E05.</div>'
        '</div>'

        '</div>'  # end flex
        '</div>'  # end card
    )
    st.markdown(example_html, unsafe_allow_html=True)

    # ── 4-graph reference cards ─────────────────────────────────────────────
    st.markdown(
        '<div style="color:#AAAAAA;font-size:12px;font-weight:600;letter-spacing:1px;'
        'text-transform:uppercase;margin-bottom:10px">The 4 Memory Graphs</div>',
        unsafe_allow_html=True,
    )
    graph_cards = [
        ("●", "Semantic",  "#6C63FF", "#1E1A35", "WHAT",  "Undirected", "Connects events by topic / concept similarity. Built from embeddings."),
        ("■", "Temporal",  "#00BFA5", "#1A2D2A", "WHEN",  "Directed →", "Strict chronological chain across all events. Enables before/after reasoning."),
        ("◆", "Causal",    "#FF6B6B", "#2D1A1A", "WHY",   "Directed →", "Cause-to-effect links, built by LLM during slow-path consolidation."),
        ("★", "Entity",    "#FFB347", "#2D2418", "WHO",   "Undirected", "Tracks people, places, and objects across every event they appear in."),
    ]
    cols = st.columns(4)
    for col, (shape, label, color, bg, query_word, direction, desc) in zip(cols, graph_cards):
        with col:
            st.markdown(
                f'<div style="background:{bg};border:1px solid {color};border-radius:10px;padding:14px;height:100%">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">'
                f'<span style="font-size:26px;color:{color}">{shape}</span>'
                f'<span style="background:{color}33;border:1px solid {color};color:{color};font-size:10px;font-weight:700;padding:2px 7px;border-radius:8px">{query_word}</span>'
                f'</div>'
                f'<div style="color:{color};font-weight:700;font-size:14px;margin-bottom:4px">{label}</div>'
                f'<div style="color:#777;font-size:10px;margin-bottom:8px">{direction}</div>'
                f'<div style="color:#CCCCCC;font-size:11px;line-height:1.5">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")

    if st.session_state.get("act2_complete"):
        pts = st.session_state.get('act2_pts_earned', 0)
        st.markdown(
            f'<div style="background:#1A2D1A;border:1px solid #00BFA5;border-radius:10px;padding:14px;margin-bottom:16px">'
            f'<div style="color:#00BFA5;font-weight:700;font-size:14px;margin-bottom:4px">✓ Memory fully ingested! +{pts} Detective Points</div>'
            f'<div style="color:#AADDCC;font-size:12px">All 32 events processed through both paths. 4 graphs are live and queryable.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="color:#AAAAAA;font-size:12px;font-weight:600;letter-spacing:1px;'
            'text-transform:uppercase;margin-bottom:10px">Final Graph Sizes</div>',
            unsafe_allow_html=True,
        )
        graph_stats = [
            ("●", "Semantic",  "#6C63FF", "#1E1A35"),
            ("■", "Temporal",  "#00BFA5", "#1A2D2A"),
            ("◆", "Causal",    "#FF6B6B", "#2D1A1A"),
            ("★", "Entity",    "#FFB347", "#2D2418"),
        ]
        cols = st.columns(4)
        for col, (shape, gtype, color, bg) in zip(cols, graph_stats):
            n = get_node_count(gtype.lower())
            e = get_edge_count(gtype.lower())
            max_nodes = 40
            bar_pct = min(100, int(n / max_nodes * 100))
            with col:
                st.markdown(
                    f'<div style="background:{bg};border:1px solid {color};border-radius:10px;padding:12px;text-align:center">'
                    f'<div style="color:{color};font-size:20px">{shape}</div>'
                    f'<div style="color:{color};font-weight:700;font-size:13px;margin:4px 0">{gtype}</div>'
                    f'<div style="color:#FAFAFA;font-size:18px;font-weight:700">{n}</div>'
                    f'<div style="color:#AAAAAA;font-size:11px;margin-bottom:8px">nodes · {e} edges</div>'
                    f'<div style="background:#333;border-radius:4px;height:6px;overflow:hidden">'
                    f'<div style="background:{color};width:{bar_pct}%;height:100%;border-radius:4px"></div>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Begin Investigation →", use_container_width=True, type="primary"):
                st.session_state["act"] = 3
                st.rerun()
        return

    # Speed selector
    speed = st.radio(
        "Ingestion speed (patient = more points!):",
        ["1x", "5x", "Instant"],
        horizontal=True,
        index=2,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        start = st.button("Start Ingestion", use_container_width=True, type="primary")

    if start:
        render_ingestion(speed)
        st.rerun()


# ---------------------------------------------------------------------------
# ACT 3 — Investigation (Core Interactive Moment)
# ---------------------------------------------------------------------------
INTENT_COLORS = {
    "WHY + WHO": "#FF6B6B",
    "WHEN": "#00BFA5",
    "WHO": "#FFB347",
    "WHAT": "#6C63FF",
}

GRAPH_INTENT_MAP = {
    "WHY + WHO": "causal",
    "WHEN": "temporal",
    "WHO": "entity",
    "WHAT": "semantic",
}

GRAPH_ANSWER_OPTIONS = {
    "Q1": ["Causal + Entity (Recommended)", "Temporal", "Semantic", "Entity only"],
    "Q2": ["Temporal (Recommended)", "Semantic", "Causal", "Entity"],
    "Q3": ["Entity (Recommended)", "Causal", "Temporal", "Semantic"],
    "Q4": ["Semantic (Recommended)", "Temporal", "Entity", "Causal"],
}

CORRECT_GRAPH_ANSWERS = {
    "Q1": "Causal + Entity (Recommended)",
    "Q2": "Temporal (Recommended)",
    "Q3": "Entity (Recommended)",
    "Q4": "Semantic (Recommended)",
}


_GRAPH_META = {
    "semantic": ("●", "#6C63FF"),
    "temporal": ("■", "#00BFA5"),
    "causal":   ("◆", "#FF6B6B"),
    "entity":   ("★", "#FFB347"),
}

def _log_html(log_lines, query, final=False):
    """Build the traversal log HTML (avoids duplication between animation and final render)."""
    graph_colors = {"causal": "#FF6B6B", "temporal": "#00BFA5", "entity": "#FFB347", "semantic": "#6C63FF"}
    edge_labels  = {"causal": "CAUSAL", "temporal": "TEMPORAL", "entity": "ENTITY", "semantic": "SEMANTIC"}
    steps_html = ""
    for i, line in enumerate(log_lines):
        # Detect graph type from line prefix
        g_color = "#00BFA5"
        badge = ""
        for gtype, gcol in graph_colors.items():
            if gtype.upper() in line.upper():
                g_color = gcol
                badge = (
                    f'<span style="background:{gcol}33;border:1px solid {gcol};color:{gcol};'
                    f'font-size:9px;font-weight:700;padding:1px 5px;border-radius:5px;margin-right:5px">'
                    f'{edge_labels[gtype]}</span>'
                )
                break
        steps_html += (
            f'<div style="display:flex;gap:8px;align-items:flex-start;margin-bottom:6px">'
            f'<div style="min-width:20px;height:20px;background:{g_color};border-radius:50%;'
            f'display:flex;align-items:center;justify-content:center;font-size:9px;font-weight:700;color:#111;flex-shrink:0">{i+1}</div>'
            f'<div style="flex:1;background:#1E2A2A;border-radius:5px;padding:5px 8px">'
            f'{badge}<span style="color:#CCDDCC;font-size:11px;line-height:1.4">{line}</span>'
            f'</div></div>'
        )

    token_so_far = int(query["tokens_used"] * (len(log_lines) / len(query["traversal_path"])))
    pct = round(len(log_lines) / len(query["traversal_path"]) * 100)
    progress_bar = (
        f'<div style="background:#1A2D2A;border:1px solid #00BFA5;border-radius:8px;padding:10px;margin-top:10px">'
    )
    if final:
        saved = query["baseline_tokens"] - query["tokens_used"]
        pct_saved = round(saved / query["baseline_tokens"] * 100, 1)
        progress_bar += (
            f'<div style="color:#00BFA5;font-size:12px;font-weight:700;margin-bottom:6px">✓ Traversal complete</div>'
            f'<div style="display:flex;justify-content:space-between;margin-bottom:4px">'
            f'<span style="color:#AAAAAA;font-size:11px">Tokens used</span>'
            f'<span style="color:#00BFA5;font-size:12px;font-weight:700">{query["tokens_used"]:,}</span>'
            f'</div>'
            f'<div style="display:flex;justify-content:space-between;margin-bottom:4px">'
            f'<span style="color:#AAAAAA;font-size:11px">Baseline would use</span>'
            f'<span style="color:#FF6B6B;font-size:12px">{query["baseline_tokens"]:,}</span>'
            f'</div>'
            f'<div style="display:flex;justify-content:space-between">'
            f'<span style="color:#AAAAAA;font-size:11px">Saved</span>'
            f'<span style="color:#FFB347;font-size:12px;font-weight:700">{saved:,} ({pct_saved}%)</span>'
            f'</div>'
        )
    else:
        progress_bar += (
            f'<div style="color:#FFB347;font-size:11px;margin-bottom:6px">Tokens retrieved: <b>{token_so_far:,}</b> / {query["tokens_used"]:,}</div>'
            f'<div style="background:#333;border-radius:4px;height:6px;overflow:hidden">'
            f'<div style="background:linear-gradient(90deg,#FFB347,#00BFA5);width:{pct}%;height:100%;border-radius:4px;transition:width 0.3s"></div>'
            f'</div>'
        )
    progress_bar += '</div>'
    return steps_html + progress_bar


def render_act3():
    st.markdown(
        '<div style="text-align:center;padding:8px 0 16px 0">'
        '<div style="font-size:40px">🔵</div>'
        '<h1 style="color:#FAFAFA;margin:8px 0 4px 0">Act 3: Investigation</h1>'
        '<p style="color:#AAAAAA;font-size:15px;max-width:640px;margin:0 auto">'
        'Pick a query, predict which graph MAGMA routes to, then watch the adaptive traversal find the answer.'
        '</p></div>',
        unsafe_allow_html=True,
    )

    # ── 4-stage query pipeline strip ───────────────────────────────────────
    st.markdown(
        '<div style="display:flex;align-items:center;gap:4px;margin-bottom:18px;flex-wrap:wrap">'

        '<div style="flex:1;min-width:110px;background:#252840;border:1px solid #6C63FF;border-radius:8px;padding:10px;text-align:center">'
        '<div style="color:#6C63FF;font-size:18px">🔎</div>'
        '<div style="color:#6C63FF;font-weight:700;font-size:12px;margin-top:4px">① Intent</div>'
        '<div style="color:#AAAAAA;font-size:10px;margin-top:2px">WHY / WHEN<br>WHO / WHAT</div>'
        '</div>'

        '<div style="color:#555;font-size:16px;font-weight:300;padding:0 2px">→</div>'

        '<div style="flex:1;min-width:110px;background:#252840;border:1px solid #00BFA5;border-radius:8px;padding:10px;text-align:center">'
        '<div style="color:#00BFA5;font-size:18px">🕸️</div>'
        '<div style="color:#00BFA5;font-weight:700;font-size:12px;margin-top:4px">② Graph Select</div>'
        '<div style="color:#AAAAAA;font-size:10px;margin-top:2px">RRF fusion across<br>all 4 graphs</div>'
        '</div>'

        '<div style="color:#555;font-size:16px;font-weight:300;padding:0 2px">→</div>'

        '<div style="flex:1;min-width:110px;background:#252840;border:1px solid #FFB347;border-radius:8px;padding:10px;text-align:center">'
        '<div style="color:#FFB347;font-size:18px">⚡</div>'
        '<div style="color:#FFB347;font-weight:700;font-size:12px;margin-top:4px">③ Traversal</div>'
        '<div style="color:#AAAAAA;font-size:10px;margin-top:2px">Beam search along<br>intent-matched edges</div>'
        '</div>'

        '<div style="color:#555;font-size:16px;font-weight:300;padding:0 2px">→</div>'

        '<div style="flex:1;min-width:110px;background:#252840;border:1px solid #FF6B6B;border-radius:8px;padding:10px;text-align:center">'
        '<div style="color:#FF6B6B;font-size:18px">💡</div>'
        '<div style="color:#FF6B6B;font-weight:700;font-size:12px;margin-top:4px">④ Answer</div>'
        '<div style="color:#AAAAAA;font-size:10px;margin-top:2px">Cited, ordered,<br>token-budgeted</div>'
        '</div>'

        '</div>',
        unsafe_allow_html=True,
    )

    # ── Intent routing map ─────────────────────────────────────────────────
    with st.expander("📐 Intent → Graph routing map", expanded=False):
        st.markdown(
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:4px 0">'

            '<div style="background:#2D1A1A;border:1px solid #FF6B6B;border-radius:8px;padding:12px;display:flex;align-items:center;gap:12px">'
            '<div style="font-size:28px;color:#FF6B6B">◆</div>'
            '<div><div style="color:#FF6B6B;font-weight:700;font-size:13px">WHY query → Causal Graph</div>'
            '<div style="color:#AAAAAA;font-size:11px;margin-top:2px">Traverses cause→effect edges. Best for motivation, explanation, consequence.</div></div>'
            '</div>'

            '<div style="background:#1A2D2A;border:1px solid #00BFA5;border-radius:8px;padding:12px;display:flex;align-items:center;gap:12px">'
            '<div style="font-size:28px;color:#00BFA5">■</div>'
            '<div><div style="color:#00BFA5;font-weight:700;font-size:13px">WHEN query → Temporal Graph</div>'
            '<div style="color:#AAAAAA;font-size:11px;margin-top:2px">Walks the chronological chain. Best for ordering, timelines, before/after.</div></div>'
            '</div>'

            '<div style="background:#2D2418;border:1px solid #FFB347;border-radius:8px;padding:12px;display:flex;align-items:center;gap:12px">'
            '<div style="font-size:28px;color:#FFB347">★</div>'
            '<div><div style="color:#FFB347;font-weight:700;font-size:13px">WHO query → Entity Graph</div>'
            '<div style="color:#AAAAAA;font-size:11px;margin-top:2px">Follows person/object nodes. Best for tracking actors and their appearances.</div></div>'
            '</div>'

            '<div style="background:#1E1A35;border:1px solid #6C63FF;border-radius:8px;padding:12px;display:flex;align-items:center;gap:12px">'
            '<div style="font-size:28px;color:#6C63FF">●</div>'
            '<div><div style="color:#6C63FF;font-weight:700;font-size:13px">WHAT query → Semantic Graph</div>'
            '<div style="color:#AAAAAA;font-size:11px;margin-top:2px">Clusters conceptually similar events. Best for themes, topics, attitudes.</div></div>'
            '</div>'

            '</div>',
            unsafe_allow_html=True,
        )

    completed = st.session_state["queries_completed"]
    if len(completed) == len(QUERIES) and not st.session_state.get("act3_complete"):
        st.session_state["score"] += 200
        st.session_state["act3_complete"] = True
        st.session_state["act3_bonus_awarded"] = True

    if st.session_state.get("act3_bonus_awarded"):
        st.success("All 4 queries completed! +200 Bonus Points!")

    # ── Query selector with intent badges ──────────────────────────────────
    st.markdown(
        '<div style="color:#AAAAAA;font-size:12px;font-weight:600;letter-spacing:1px;'
        'text-transform:uppercase;margin-bottom:8px">Choose your investigative query</div>',
        unsafe_allow_html=True,
    )

    _QUERY_INTENT_COLOR = {"WHY + WHO": "#FF6B6B", "WHEN": "#00BFA5", "WHO": "#FFB347", "WHAT": "#6C63FF"}
    _QUERY_INTENT_SHAPE = {"WHY + WHO": "◆", "WHEN": "■", "WHO": "★", "WHAT": "●"}

    query_labels = {q["id"]: q["text"] for q in QUERIES}
    selected_label = st.radio(
        "query_select",
        list(query_labels.values()),
        key="selected_query_text",
        label_visibility="collapsed",
    )
    selected_query = next(q for q in QUERIES if q["text"] == selected_label)
    qid = selected_query["id"]

    # Intent + routing badge
    intent = selected_query["intent"]
    intent_color = _QUERY_INTENT_COLOR.get(intent, "#AAAAAA")
    intent_shape = _QUERY_INTENT_SHAPE.get(intent, "●")
    pg = selected_query["primary_graph"]
    pg_shape, pg_color = _GRAPH_META.get(pg, ("●", "#AAAAAA"))
    st.markdown(
        f'<div style="background:#1A1D2E;border:1px solid #333;border-radius:8px;padding:10px 14px;margin-bottom:14px;display:flex;align-items:center;gap:12px;flex-wrap:wrap">'
        f'<span style="background:{intent_color}33;border:1px solid {intent_color};color:{intent_color};'
        f'padding:3px 10px;border-radius:10px;font-size:12px;font-weight:700">{intent_shape} {intent}</span>'
        f'<span style="color:#555;font-size:14px">→</span>'
        f'<span style="background:{pg_color}33;border:1px solid {pg_color};color:{pg_color};'
        f'padding:3px 10px;border-radius:10px;font-size:12px;font-weight:700">{pg_shape} {pg.capitalize()} Graph</span>'
        f'<span style="color:#AAAAAA;font-size:12px;flex:1">{selected_query["graph_explanation"]}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    col_query, col_graph, col_log = st.columns([1, 2, 1], gap="medium")

    with col_query:
        st.markdown(
            '<div style="color:#FAFAFA;font-size:13px;font-weight:600;margin-bottom:8px">Predict which graph MAGMA uses:</div>',
            unsafe_allow_html=True,
        )
        graph_guess = st.radio(
            "Your guess:",
            GRAPH_ANSWER_OPTIONS[qid],
            key=f"graph_guess_{qid}",
            index=None,
        )

        run_btn = st.button(
            "Run Query →",
            use_container_width=True,
            type="primary",
            disabled=(graph_guess is None),
            key=f"run_{qid}",
        )

        if qid in completed:
            st.markdown(
                '<div style="background:#1A2D1A;border:1px solid #00BFA5;border-radius:6px;'
                'padding:6px 10px;color:#00BFA5;font-size:12px;margin-top:8px">✓ Query completed</div>',
                unsafe_allow_html=True,
            )

        # Progress tracker
        st.markdown("---")
        st.markdown(
            '<div style="color:#AAAAAA;font-size:11px;font-weight:600;letter-spacing:1px;'
            'text-transform:uppercase;margin-bottom:8px">Progress</div>',
            unsafe_allow_html=True,
        )
        for q in QUERIES:
            done = q["id"] in completed
            q_intent = q["intent"]
            q_color = _QUERY_INTENT_COLOR.get(q_intent, "#555")
            q_shape = _QUERY_INTENT_SHAPE.get(q_intent, "●")
            bg = "#1A2D1A" if done else "#1A1D2E"
            border = "#00BFA5" if done else "#333"
            icon = "✓" if done else "○"
            st.markdown(
                f'<div style="background:{bg};border:1px solid {border};border-radius:6px;'
                f'padding:6px 10px;margin-bottom:5px;display:flex;align-items:center;gap:8px">'
                f'<span style="color:{"#00BFA5" if done else "#555"};font-size:12px">{icon}</span>'
                f'<span style="color:{q_color};font-size:11px;font-weight:600">{q_shape} {q["id"]}</span>'
                f'<span style="color:#AAAAAA;font-size:10px">{q["intent_tag"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    graph_placeholder = col_graph.empty()
    log_placeholder = col_log.empty()

    # Show initial graph
    with graph_placeholder:
        initial_html = build_graph_html(graph_type=selected_query["primary_graph"], height=460)
        components.html(initial_html, height=465, scrolling=False)

    with log_placeholder:
        st.markdown(
            '<div style="background:#1A1D2E;border:1px solid #333;border-radius:8px;padding:12px;color:#AAAAAA;font-size:12px">'
            '← Select a graph prediction and click <b>Run Query</b> to begin traversal.'
            '</div>',
            unsafe_allow_html=True,
        )

    if run_btn and graph_guess is not None:
        correct_guess = graph_guess == CORRECT_GRAPH_ANSWERS[qid]
        pts_key = f"pts_awarded_{qid}"

        if pts_key not in st.session_state:
            pts = 150 if correct_guess else 50
            st.session_state["score"] += pts
            st.session_state[pts_key] = pts

        if correct_guess:
            with col_query:
                st.success("Correct! +150 points")
        else:
            with col_query:
                st.warning(f"Not quite — but +50 for trying!\n\n{selected_query['graph_explanation']}")

        # Traversal animation
        visited_nodes = []
        visited_edges = []
        log_lines = []

        with col_log:
            log_ph = st.empty()

        for step in selected_query["traversal_path"]:
            if step["node"] not in visited_nodes:
                visited_nodes.append(step["node"])
            if step["edge"]:
                visited_edges.append(step["edge"])
            log_lines.append(step["description"])

            html = build_graph_html(
                graph_type=step["graph"],
                highlighted_nodes=visited_nodes,
                highlighted_edges=visited_edges,
                height=460,
            )
            with graph_placeholder:
                components.html(html, height=465, scrolling=False)

            with log_ph:
                st.markdown(_log_html(log_lines, selected_query, final=False), unsafe_allow_html=True)

            time.sleep(0.7)

        with log_ph:
            st.markdown(_log_html(log_lines, selected_query, final=True), unsafe_allow_html=True)

        # Mark query complete
        completed.add(qid)
        st.session_state["queries_completed"] = completed

        # ── MAGMA vs Baseline side-by-side answer ──────────────────────────
        st.markdown("---")
        st.markdown(
            '<div style="color:#AAAAAA;font-size:12px;font-weight:600;letter-spacing:1px;'
            'text-transform:uppercase;margin-bottom:10px">Answer Comparison</div>',
            unsafe_allow_html=True,
        )
        ans_col1, ans_col2 = st.columns(2, gap="medium")
        with ans_col1:
            st.markdown(
                '<div style="background:#1A2D1A;border:1px solid #00BFA5;border-radius:10px;padding:14px;height:100%">'
                '<div style="display:flex;align-items:center;gap:8px;margin-bottom:10px">'
                '<span style="font-size:18px">🧠</span>'
                '<span style="color:#00BFA5;font-weight:700;font-size:13px">MAGMA</span>'
                f'<span style="background:#00BFA522;border:1px solid #00BFA5;color:#00BFA5;font-size:10px;padding:2px 7px;border-radius:8px">{selected_query["tokens_used"]:,} tokens</span>'
                '</div>'
                f'<div style="color:#AADDCC;font-size:13px;line-height:1.7">{selected_query["magma_answer"]}</div>'
                '</div>',
                unsafe_allow_html=True,
            )
        with ans_col2:
            st.markdown(
                '<div style="background:#2D1A1A;border:1px solid #FF6B6B;border-radius:10px;padding:14px;height:100%">'
                '<div style="display:flex;align-items:center;gap:8px;margin-bottom:10px">'
                '<span style="font-size:18px">🤖</span>'
                '<span style="color:#FF6B6B;font-weight:700;font-size:13px">Baseline</span>'
                f'<span style="background:#FF6B6B22;border:1px solid #FF6B6B;color:#FF6B6B;font-size:10px;padding:2px 7px;border-radius:8px">{selected_query["baseline_tokens"]:,} tokens</span>'
                '</div>'
                f'<div style="color:#DDAAAA;font-size:13px;line-height:1.7;font-style:italic">{selected_query["baseline_answer"]}</div>'
                '</div>',
                unsafe_allow_html=True,
            )

        if len(completed) == len(QUERIES):
            st.success("All queries investigated! Proceeding to the Reveal...")
            time.sleep(1.5)
            if not st.session_state.get("act3_complete"):
                st.session_state["score"] += 200
                st.session_state["act3_complete"] = True
            st.session_state["act"] = 4
            st.rerun()
        else:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("Try another query", use_container_width=True):
                    st.rerun()

    # Skip to Act 4 button (if at least 1 query done)
    if completed and st.session_state["act"] == 3:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Proceed to The Reveal →", use_container_width=True):
                if not st.session_state.get("act3_complete"):
                    st.session_state["act3_complete"] = True
                st.session_state["act"] = 4
                st.rerun()


# ---------------------------------------------------------------------------
# ACT 4 — The Reveal
# ---------------------------------------------------------------------------
def render_act4():
    st.markdown(
        """
        <div style="text-align:center;padding:12px 0 20px 0">
          <div style="font-size:40px">🟢</div>
          <h1 style="color:#FAFAFA;margin:8px 0 4px 0">Act 4: The Reveal</h1>
          <p style="color:#AAAAAA;font-size:15px;max-width:660px;margin:0 auto">
            MAGMA vs Baseline — the full picture. Pipeline diagrams, answer quality,
            token efficiency, and benchmark numbers from the paper.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.get("act4_complete"):
        st.session_state["score"] += 100
        st.session_state["act4_complete"] = True

    # Use the main mystery query for the reveal
    main_query = QUERIES[0]
    render_full_comparison(main_query)

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Go Deeper — Ablation Explorer →", use_container_width=True, type="primary"):
            st.session_state["act"] = 5
            st.rerun()


# ---------------------------------------------------------------------------
# ACT 5 — Deep Dive (Ablation)
# ---------------------------------------------------------------------------
def render_act5():
    st.markdown(
        """
        <div style="text-align:center;padding:12px 0 20px 0">
          <div style="font-size:40px">⚪</div>
          <h1 style="color:#FAFAFA;margin:8px 0 4px 0">Act 5: Deep Dive</h1>
          <p style="color:#AAAAAA;font-size:15px;max-width:660px;margin:0 auto">
            Toggle individual memory graphs off and watch the LoComo score degrade in real time.
            Mirrors the ablation study in Table 4 of the paper — each graph has a role, and removing it has a cost.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_ablation()


# ---------------------------------------------------------------------------
# Main router
# ---------------------------------------------------------------------------
act_renderers = {
    0: render_act0,
    1: render_act1,
    2: render_act2,
    3: render_act3,
    4: render_act4,
    5: render_act5,
}

current_act = st.session_state["act"]
act_renderers[current_act]()

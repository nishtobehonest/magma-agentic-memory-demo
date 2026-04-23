"""
about.py — Act 0: "About the Paper" — Visually rich panel with SVG diagrams.
"""

import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
from data.themes import LIGHT_IFRAME_CSS, plotly_layout, plotly_grid, plotly_bar_muted


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _section_header(icon, title, color, subtitle=""):
    sub = f'<div style="color:#888;font-size:13px;margin-top:4px">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f"""
        <div style="margin:36px 0 18px 0;padding-bottom:12px;border-bottom:2px solid {color}33">
          <div style="display:flex;align-items:center;gap:12px">
            <span style="font-size:26px">{icon}</span>
            <span style="font-size:20px;font-weight:700;color:{color}">{title}</span>
          </div>
          {sub}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# SVG Diagrams
# ---------------------------------------------------------------------------

def _svg_wrap(svg_body: str, height: int = 160, theme: str = "dark") -> str:
    """Wrap SVG in an HTML block for st.components.v1.html."""
    bg = "#FFFFFF" if theme == "light" else "#1A1D2E"
    light_css = f"<style>{LIGHT_IFRAME_CSS}</style>" if theme == "light" else ""
    return f"""
    <html><head>{light_css}</head>
    <body style="margin:0;padding:0;background:{bg};display:flex;align-items:center;justify-content:center;">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 {height}"
         width="100%" style="max-height:{height}px">
      {svg_body}
    </svg>
    </body></html>
    """


def _svg_semantic(theme: str = "dark") -> str:
    return _svg_wrap("""
      <!-- Cluster A label -->
      <text x="90" y="18" text-anchor="middle" fill="#6C63FF" font-size="12" opacity="0.7">Midterm cluster</text>
      <!-- Cluster A — "midterm" topic -->
      <circle cx="70" cy="65" r="26" fill="#6C63FF" opacity="0.85"/>
      <circle cx="130" cy="42" r="26" fill="#6C63FF" opacity="0.85"/>
      <circle cx="118" cy="105" r="26" fill="#6C63FF" opacity="0.85"/>
      <line x1="70" y1="65" x2="130" y2="42" stroke="#9D97FF" stroke-width="3"/>
      <line x1="70" y1="65" x2="118" y2="105" stroke="#9D97FF" stroke-width="3"/>
      <line x1="130" y1="42" x2="118" y2="105" stroke="#9D97FF" stroke-width="3"/>
      <!-- Cluster B label -->
      <text x="232" y="18" text-anchor="middle" fill="#9D97FF" font-size="12" opacity="0.7">Money cluster</text>
      <!-- Cluster B — "money" topic -->
      <circle cx="210" cy="65" r="26" fill="#9D97FF" opacity="0.75"/>
      <circle cx="268" cy="42" r="26" fill="#9D97FF" opacity="0.75"/>
      <circle cx="260" cy="105" r="26" fill="#9D97FF" opacity="0.75"/>
      <line x1="210" y1="65" x2="268" y2="42" stroke="#9D97FF" stroke-width="2.5"/>
      <line x1="210" y1="65" x2="260" y2="105" stroke="#9D97FF" stroke-width="2.5"/>
      <line x1="268" y1="42" x2="260" y2="105" stroke="#9D97FF" stroke-width="2.5"/>
      <!-- Weak cross-cluster edge -->
      <line x1="130" y1="42" x2="210" y2="65" stroke="#6C63FF" stroke-width="1.5" stroke-dasharray="6,5" opacity="0.3"/>
      <!-- Labels -->
      <text x="70" y="70" text-anchor="middle" fill="white" font-size="11" font-weight="bold">E03</text>
      <text x="130" y="47" text-anchor="middle" fill="white" font-size="11" font-weight="bold">E11</text>
      <text x="118" y="110" text-anchor="middle" fill="white" font-size="11" font-weight="bold">E19</text>
      <text x="210" y="70" text-anchor="middle" fill="white" font-size="11" font-weight="bold">E08</text>
      <text x="268" y="47" text-anchor="middle" fill="white" font-size="11" font-weight="bold">E18</text>
      <text x="260" y="110" text-anchor="middle" fill="white" font-size="11" font-weight="bold">E31</text>
      <!-- Legend -->
      <text x="160" y="150" text-anchor="middle" fill="#9D97FF" font-size="12">Similar topics cluster together (undirected)</text>
    """, height=165, theme=theme)


def _svg_temporal(theme: str = "dark") -> str:
    return _svg_wrap("""
      <defs>
        <marker id="arrowT" markerWidth="10" markerHeight="10" refX="7" refY="4" orient="auto">
          <path d="M0,0 L0,8 L10,4 z" fill="#00E5CC"/>
        </marker>
      </defs>
      <!-- Week brackets -->
      <text x="55" y="22" text-anchor="middle" fill="#00BFA5" font-size="13" opacity="0.6">── Week 1 ──</text>
      <text x="175" y="22" text-anchor="middle" fill="#00BFA5" font-size="13" opacity="0.6">── Week 2 ──</text>
      <text x="285" y="22" text-anchor="middle" fill="#00BFA5" font-size="13" opacity="0.6">Wk 3</text>
      <!-- Timeline nodes -->
      <circle cx="35"  cy="80" r="24" fill="#00BFA5" opacity="0.9"/>
      <circle cx="105" cy="80" r="24" fill="#00BFA5" opacity="0.9"/>
      <circle cx="175" cy="80" r="24" fill="#00BFA5" opacity="0.9"/>
      <circle cx="245" cy="80" r="24" fill="#00BFA5" opacity="0.9"/>
      <circle cx="305" cy="80" r="24" fill="#00BFA5" opacity="0.9"/>
      <!-- Arrows -->
      <line x1="60"  y1="80" x2="78"  y2="80" stroke="#00E5CC" stroke-width="3" marker-end="url(#arrowT)"/>
      <line x1="130" y1="80" x2="148" y2="80" stroke="#00E5CC" stroke-width="3" marker-end="url(#arrowT)"/>
      <line x1="200" y1="80" x2="218" y2="80" stroke="#00E5CC" stroke-width="3" marker-end="url(#arrowT)"/>
      <line x1="270" y1="80" x2="278" y2="80" stroke="#00E5CC" stroke-width="3" marker-end="url(#arrowT)"/>
      <!-- Event IDs -->
      <text x="35"  y="77" text-anchor="middle" fill="white" font-size="12" font-weight="bold">E01</text>
      <text x="105" y="77" text-anchor="middle" fill="white" font-size="12" font-weight="bold">E05</text>
      <text x="175" y="77" text-anchor="middle" fill="white" font-size="12" font-weight="bold">E14</text>
      <text x="245" y="77" text-anchor="middle" fill="white" font-size="12" font-weight="bold">E22</text>
      <text x="305" y="77" text-anchor="middle" fill="white" font-size="12" font-weight="bold">E26</text>
      <!-- Short descriptions below -->
      <text x="35"  y="116" text-anchor="middle" fill="#AAAAAA" font-size="9">Alex joins</text>
      <text x="105" y="116" text-anchor="middle" fill="#AAAAAA" font-size="9">Sam intro'd</text>
      <text x="175" y="116" text-anchor="middle" fill="#AAAAAA" font-size="9">Notes stolen</text>
      <text x="245" y="116" text-anchor="middle" fill="#AAAAAA" font-size="9">Sam gone</text>
      <text x="305" y="116" text-anchor="middle" fill="#AAAAAA" font-size="9">Grades out</text>
      <!-- Legend -->
      <text x="160" y="145" text-anchor="middle" fill="#00BFA5" font-size="12">Directed: past → future · enables WHEN reasoning</text>
    """, height=160, theme=theme)


def _svg_causal(theme: str = "dark") -> str:
    return _svg_wrap("""
      <defs>
        <marker id="arrowC" markerWidth="10" markerHeight="10" refX="7" refY="4" orient="auto">
          <path d="M0,0 L0,8 L10,4 z" fill="#FF9999"/>
        </marker>
      </defs>
      <!-- Root cause -->
      <rect x="90" y="8" width="140" height="38" rx="10" fill="#FF6B6B" opacity="0.9"/>
      <text x="160" y="23" text-anchor="middle" fill="white" font-size="11" font-weight="bold">E05</text>
      <text x="160" y="38" text-anchor="middle" fill="white" font-size="10">Jordan introduces Sam</text>
      <!-- Mid layer -->
      <rect x="18" y="78" width="130" height="38" rx="10" fill="#FF6B6B" opacity="0.75"/>
      <text x="83" y="93" text-anchor="middle" fill="white" font-size="11" font-weight="bold">E08</text>
      <text x="83" y="108" text-anchor="middle" fill="white" font-size="10">Sam asks for $50</text>
      <rect x="172" y="78" width="130" height="38" rx="10" fill="#FF6B6B" opacity="0.75"/>
      <text x="237" y="93" text-anchor="middle" fill="white" font-size="11" font-weight="bold">E14</text>
      <text x="237" y="108" text-anchor="middle" fill="white" font-size="10">Sam steals notes</text>
      <!-- Final effect -->
      <rect x="90" y="148" width="140" height="38" rx="10" fill="#CC2222" opacity="0.95"/>
      <text x="160" y="163" text-anchor="middle" fill="white" font-size="11" font-weight="bold">E22</text>
      <text x="160" y="178" text-anchor="middle" fill="white" font-size="10">Sam disappears</text>
      <!-- Arrows -->
      <line x1="135" y1="46" x2="98"  y2="76" stroke="#FF9999" stroke-width="2.5" marker-end="url(#arrowC)"/>
      <line x1="185" y1="46" x2="222" y2="76" stroke="#FF9999" stroke-width="2.5" marker-end="url(#arrowC)"/>
      <line x1="83"  y1="116" x2="138" y2="146" stroke="#FF9999" stroke-width="2.5" marker-end="url(#arrowC)"/>
      <line x1="237" y1="116" x2="182" y2="146" stroke="#FF9999" stroke-width="2.5" marker-end="url(#arrowC)"/>
      <!-- CAUSE/EFFECT labels -->
      <text x="52"  y="68" fill="#FF9999" font-size="10" opacity="0.6">cause</text>
      <text x="196" y="68" fill="#FF9999" font-size="10" opacity="0.6">cause</text>
      <text x="160" y="140" text-anchor="middle" fill="#FF9999" font-size="10" opacity="0.6">effect</text>
    """, height=200, theme=theme)


def _svg_entity(theme: str = "dark") -> str:
    return _svg_wrap("""
      <!-- Entity nodes -->
      <circle cx="95"  cy="85" r="34" fill="#FFB347" opacity="0.9"/>
      <text x="95"  y="81" text-anchor="middle" fill="white" font-size="13" font-weight="bold">Sam</text>
      <text x="95"  y="97" text-anchor="middle" fill="white" font-size="10">entity</text>
      <circle cx="225" cy="85" r="34" fill="#FFB347" opacity="0.75"/>
      <text x="225" y="81" text-anchor="middle" fill="white" font-size="13" font-weight="bold">Jordan</text>
      <text x="225" y="97" text-anchor="middle" fill="white" font-size="10">entity</text>
      <!-- Event nodes — Sam -->
      <circle cx="28"  cy="30"  r="18" fill="#6C63FF" opacity="0.75"/>
      <text x="28"  y="34"  text-anchor="middle" fill="white" font-size="10" font-weight="bold">E05</text>
      <circle cx="22"  cy="140" r="18" fill="#6C63FF" opacity="0.75"/>
      <text x="22"  y="144" text-anchor="middle" fill="white" font-size="10" font-weight="bold">E14</text>
      <circle cx="95"  cy="160" r="18" fill="#6C63FF" opacity="0.75"/>
      <text x="95"  y="164" text-anchor="middle" fill="white" font-size="10" font-weight="bold">E22</text>
      <!-- Event nodes — Jordan -->
      <circle cx="292" cy="30"  r="18" fill="#6C63FF" opacity="0.75"/>
      <text x="292" y="34"  text-anchor="middle" fill="white" font-size="10" font-weight="bold">E05</text>
      <circle cx="298" cy="140" r="18" fill="#6C63FF" opacity="0.75"/>
      <text x="298" y="144" text-anchor="middle" fill="white" font-size="10" font-weight="bold">E09</text>
      <circle cx="225" cy="160" r="18" fill="#6C63FF" opacity="0.75"/>
      <text x="225" y="164" text-anchor="middle" fill="white" font-size="10" font-weight="bold">E27</text>
      <!-- Edges -->
      <line x1="64"  y1="62"  x2="44"  y2="45"  stroke="#FFD700" stroke-width="2" opacity="0.65"/>
      <line x1="63"  y1="108" x2="38"  y2="130" stroke="#FFD700" stroke-width="2" opacity="0.65"/>
      <line x1="95"  y1="119" x2="95"  y2="142" stroke="#FFD700" stroke-width="2" opacity="0.65"/>
      <line x1="256" y1="62"  x2="276" y2="45"  stroke="#FFD700" stroke-width="2" opacity="0.65"/>
      <line x1="257" y1="108" x2="282" y2="130" stroke="#FFD700" stroke-width="2" opacity="0.65"/>
      <line x1="225" y1="119" x2="225" y2="142" stroke="#FFD700" stroke-width="2" opacity="0.65"/>
      <!-- Cross-entity edge -->
      <line x1="129" y1="85" x2="191" y2="85" stroke="#FFD700" stroke-width="2" stroke-dasharray="5,4" opacity="0.4"/>
      <text x="160" y="79" text-anchor="middle" fill="#FFD700" font-size="10" opacity="0.6">co-appear in E05</text>
    """, height=190, theme=theme)


def _svg_architecture(theme: str = "dark") -> str:
    """Full MAGMA system architecture — Events → Graphs → Query Pipeline → Answer."""
    bg = "#FFFFFF" if theme == "light" else "#1A1D2E"
    light_css = f"<style>{LIGHT_IFRAME_CSS}</style>" if theme == "light" else ""
    return f"""
    <html><head>{light_css}</head><body style="margin:0;padding:12px;background:{bg};">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 310" width="100%" style="max-height:310px">
      <defs>
        <marker id="arrA" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="#666"/>
        </marker>
        <marker id="arrW" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="#AAAAAA"/>
        </marker>
        <marker id="arrG" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="#00BFA5"/>
        </marker>
      </defs>

      <!-- === EVENTS (LEFT) === -->
      <rect x="10" y="120" width="110" height="70" rx="10" fill="#252840" stroke="#555" stroke-width="1.5"/>
      <text x="65" y="148" text-anchor="middle" fill="#FAFAFA" font-size="12" font-weight="bold">Events</text>
      <text x="65" y="164" text-anchor="middle" fill="#AAAAAA" font-size="10">E01 … E32</text>
      <text x="65" y="178" text-anchor="middle" fill="#AAAAAA" font-size="10">32 messages</text>

      <!-- Arrow: Events → Write process -->
      <line x1="120" y1="155" x2="168" y2="155" stroke="#666" stroke-width="2" marker-end="url(#arrA)"/>

      <!-- === WRITE PROCESS (CENTER-LEFT) === -->
      <rect x="170" y="85" width="130" height="140" rx="10" fill="#1E2030" stroke="#444" stroke-width="1.5"/>
      <text x="235" y="108" text-anchor="middle" fill="#FAFAFA" font-size="12" font-weight="bold">Write Process</text>

      <!-- Fast path -->
      <rect x="183" y="116" width="104" height="40" rx="7" fill="#2D2418" stroke="#FFB347" stroke-width="1"/>
      <text x="235" y="132" text-anchor="middle" fill="#FFB347" font-size="10" font-weight="bold">⚡ Fast Path</text>
      <text x="235" y="147" text-anchor="middle" fill="#AAAAAA" font-size="9">Non-blocking</text>

      <!-- Slow path -->
      <rect x="183" y="163" width="104" height="40" rx="7" fill="#1A2420" stroke="#00BFA5" stroke-width="1"/>
      <text x="235" y="179" text-anchor="middle" fill="#00BFA5" font-size="10" font-weight="bold">🔄 Slow Path</text>
      <text x="235" y="194" text-anchor="middle" fill="#AAAAAA" font-size="9">Async LLM refine</text>

      <!-- Arrow: Write → MAG -->
      <line x1="300" y1="155" x2="338" y2="155" stroke="#666" stroke-width="2" marker-end="url(#arrA)"/>

      <!-- === MULTI-GRAPH (CENTER) === -->
      <rect x="340" y="60" width="130" height="190" rx="10" fill="#1E2030" stroke="#6C63FF" stroke-width="2"/>
      <text x="405" y="85" text-anchor="middle" fill="#6C63FF" font-size="13" font-weight="bold">Multi-Graph</text>
      <text x="405" y="100" text-anchor="middle" fill="#888" font-size="10">Memory (MAG)</text>

      <rect x="353" y="108" width="104" height="26" rx="6" fill="#1E1A35" stroke="#6C63FF" stroke-width="1"/>
      <text x="405" y="125" text-anchor="middle" fill="#9D97FF" font-size="11">● Semantic</text>

      <rect x="353" y="140" width="104" height="26" rx="6" fill="#1A2D2A" stroke="#00BFA5" stroke-width="1"/>
      <text x="405" y="157" text-anchor="middle" fill="#00BFA5" font-size="11">■ Temporal</text>

      <rect x="353" y="172" width="104" height="26" rx="6" fill="#2D1A1A" stroke="#FF6B6B" stroke-width="1"/>
      <text x="405" y="189" text-anchor="middle" fill="#FF6B6B" font-size="11">◆ Causal</text>

      <rect x="353" y="204" width="104" height="26" rx="6" fill="#2D2418" stroke="#FFB347" stroke-width="1"/>
      <text x="405" y="221" text-anchor="middle" fill="#FFB347" font-size="11">★ Entity</text>

      <!-- === QUERY (ENTERS FROM BOTTOM-CENTER) === -->
      <rect x="358" y="265" width="94" height="28" rx="7" fill="#252840" stroke="#AAAAAA" stroke-width="1.5"/>
      <text x="405" y="283" text-anchor="middle" fill="#FAFAFA" font-size="11">User Query</text>
      <line x1="405" y1="265" x2="405" y2="252" stroke="#AAAAAA" stroke-width="2" marker-end="url(#arrW)"/>

      <!-- Arrow: MAG → Query Pipeline -->
      <line x1="470" y1="155" x2="508" y2="155" stroke="#666" stroke-width="2" marker-end="url(#arrA)"/>

      <!-- === QUERY PIPELINE (RIGHT) === -->
      <rect x="510" y="60" width="235" height="190" rx="10" fill="#1E2030" stroke="#00BFA5" stroke-width="2"/>
      <text x="627" y="85" text-anchor="middle" fill="#00BFA5" font-size="13" font-weight="bold">Query Pipeline</text>

      <!-- Stage 01 -->
      <rect x="522" y="96" width="210" height="34" rx="6" fill="#1E1A35" stroke="#6C63FF" stroke-width="1"/>
      <text x="542" y="116" fill="#6C63FF" font-size="10" font-weight="bold">01</text>
      <text x="562" y="116" fill="#DDDDDD" font-size="10">Anchor ID — RRF Fusion</text>

      <!-- Stage 02 -->
      <rect x="522" y="135" width="210" height="34" rx="6" fill="#1A2D2A" stroke="#00BFA5" stroke-width="1"/>
      <text x="542" y="155" fill="#00BFA5" font-size="10" font-weight="bold">02</text>
      <text x="562" y="155" fill="#DDDDDD" font-size="10">Beam Search — Intent-aware</text>

      <!-- Stage 03 -->
      <rect x="522" y="174" width="210" height="34" rx="6" fill="#2D2418" stroke="#FFB347" stroke-width="1"/>
      <text x="542" y="194" fill="#FFB347" font-size="10" font-weight="bold">03</text>
      <text x="562" y="194" fill="#DDDDDD" font-size="10">Scaffold + Provenance</text>

      <!-- Stage 04 -->
      <rect x="522" y="213" width="210" height="34" rx="6" fill="#2D1A1A" stroke="#FF6B6B" stroke-width="1"/>
      <text x="542" y="233" fill="#FF6B6B" font-size="10" font-weight="bold">04</text>
      <text x="562" y="233" fill="#DDDDDD" font-size="10">Token Budget (salience)</text>

      <!-- Arrow: Pipeline → Answer -->
      <line x1="627" y1="250" x2="627" y2="270" stroke="#00BFA5" stroke-width="2" marker-end="url(#arrG)"/>

      <!-- Answer -->
      <rect x="555" y="272" width="145" height="30" rx="8" fill="#1A2D1A" stroke="#00BFA5" stroke-width="1.5"/>
      <text x="627" y="291" text-anchor="middle" fill="#00BFA5" font-size="12" font-weight="bold">Answer + Citations</text>

      <!-- Token label -->
      <text x="627" y="308" text-anchor="middle" fill="#666" font-size="10">~700–4,200 tokens  ·  1.47s latency</text>
    </svg>
    </body></html>
    """


def _svg_pipeline_flow(theme: str = "dark") -> str:
    """Horizontal 4-stage pipeline with connecting arrows."""
    bg = "#FFFFFF" if theme == "light" else "#1A1D2E"
    light_css = f"<style>{LIGHT_IFRAME_CSS}</style>" if theme == "light" else ""
    return f"""
    <html><head>{light_css}</head><body style="margin:0;padding:8px 0;background:{bg};">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 110" width="100%" style="max-height:110px">
      <defs>
        <marker id="arrP" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
        </marker>
      </defs>

      <!-- Stage boxes -->
      <!-- 01 -->
      <rect x="10" y="20" width="155" height="70" rx="10" fill="#1E1A35" stroke="#6C63FF" stroke-width="2"/>
      <text x="87" y="48" text-anchor="middle" fill="#6C63FF" font-size="20" font-weight="bold">01</text>
      <text x="87" y="66" text-anchor="middle" fill="#FAFAFA" font-size="11" font-weight="bold">Anchor ID</text>
      <text x="87" y="81" text-anchor="middle" fill="#888" font-size="10">RRF Fusion</text>

      <!-- Arrow -->
      <line x1="165" y1="55" x2="188" y2="55" stroke="#555" stroke-width="2" marker-end="url(#arrP)"/>

      <!-- 02 -->
      <rect x="190" y="20" width="155" height="70" rx="10" fill="#1A2D2A" stroke="#00BFA5" stroke-width="2"/>
      <text x="267" y="48" text-anchor="middle" fill="#00BFA5" font-size="20" font-weight="bold">02</text>
      <text x="267" y="66" text-anchor="middle" fill="#FAFAFA" font-size="11" font-weight="bold">Beam Search</text>
      <text x="267" y="81" text-anchor="middle" fill="#888" font-size="10">Intent-aware traversal</text>

      <!-- Arrow -->
      <line x1="345" y1="55" x2="368" y2="55" stroke="#555" stroke-width="2" marker-end="url(#arrP)"/>

      <!-- 03 -->
      <rect x="370" y="20" width="155" height="70" rx="10" fill="#2D2418" stroke="#FFB347" stroke-width="2"/>
      <text x="447" y="48" text-anchor="middle" fill="#FFB347" font-size="20" font-weight="bold">03</text>
      <text x="447" y="66" text-anchor="middle" fill="#FAFAFA" font-size="11" font-weight="bold">Context Scaffold</text>
      <text x="447" y="81" text-anchor="middle" fill="#888" font-size="10">Topo order + citations</text>

      <!-- Arrow -->
      <line x1="525" y1="55" x2="548" y2="55" stroke="#555" stroke-width="2" marker-end="url(#arrP)"/>

      <!-- 04 -->
      <rect x="550" y="20" width="200" height="70" rx="10" fill="#2D1A1A" stroke="#FF6B6B" stroke-width="2"/>
      <text x="650" y="48" text-anchor="middle" fill="#FF6B6B" font-size="20" font-weight="bold">04</text>
      <text x="650" y="66" text-anchor="middle" fill="#FAFAFA" font-size="11" font-weight="bold">Token Budgeting</text>
      <text x="650" y="81" text-anchor="middle" fill="#888" font-size="10">Salience-based compression</text>
    </svg>
    </body></html>
    """


def _svg_dual_stream(theme: str = "dark") -> str:
    """Dual-stream write process diagram."""
    bg = "#FFFFFF" if theme == "light" else "#1A1D2E"
    light_css = f"<style>{LIGHT_IFRAME_CSS}</style>" if theme == "light" else ""
    return f"""
    <html><head>{light_css}</head><body style="margin:0;padding:8px 0;background:{bg};">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 220" width="100%" style="max-height:220px">
      <defs>
        <marker id="arrF" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="#FFB347"/>
        </marker>
        <marker id="arrS" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="#00BFA5"/>
        </marker>
      </defs>

      <!-- New Event box at top -->
      <rect x="175" y="10" width="170" height="40" rx="10" fill="#252840" stroke="#AAAAAA" stroke-width="1.5"/>
      <text x="260" y="34" text-anchor="middle" fill="#FAFAFA" font-size="13" font-weight="bold">New Event Arrives</text>

      <!-- Branch lines -->
      <line x1="220" y1="50" x2="120" y2="90" stroke="#FFB347" stroke-width="2.5" marker-end="url(#arrF)"/>
      <line x1="300" y1="50" x2="400" y2="90" stroke="#00BFA5" stroke-width="2.5" marker-end="url(#arrS)"/>

      <!-- Fast path box -->
      <rect x="30" y="92" width="185" height="44" rx="10" fill="#2D2418" stroke="#FFB347" stroke-width="2"/>
      <text x="122" y="112" text-anchor="middle" fill="#FFB347" font-size="12" font-weight="bold">⚡ Fast Path</text>
      <text x="122" y="128" text-anchor="middle" fill="#AAAAAA" font-size="10">Non-blocking · immediate</text>

      <!-- Slow path box -->
      <rect x="305" y="92" width="185" height="44" rx="10" fill="#1A2420" stroke="#00BFA5" stroke-width="2"/>
      <text x="397" y="112" text-anchor="middle" fill="#00BFA5" font-size="12" font-weight="bold">🔄 Slow Path</text>
      <text x="397" y="128" text-anchor="middle" fill="#AAAAAA" font-size="10">Async · LLM-assisted</text>

      <!-- Fast path → graph outputs -->
      <line x1="80" y1="136" x2="80" y2="158" stroke="#FFB347" stroke-width="1.5" marker-end="url(#arrF)"/>
      <line x1="165" y1="136" x2="165" y2="158" stroke="#FFB347" stroke-width="1.5" marker-end="url(#arrF)"/>

      <rect x="30" y="160" width="90" height="34" rx="8" fill="#1E1A35" stroke="#6C63FF" stroke-width="1.5"/>
      <text x="75" y="181" text-anchor="middle" fill="#9D97FF" font-size="11" font-weight="bold">● Semantic</text>

      <rect x="127" y="160" width="90" height="34" rx="8" fill="#1A2D2A" stroke="#00BFA5" stroke-width="1.5"/>
      <text x="172" y="181" text-anchor="middle" fill="#00BFA5" font-size="11" font-weight="bold">■ Temporal</text>

      <!-- Slow path → graph outputs -->
      <line x1="355" y1="136" x2="355" y2="158" stroke="#00BFA5" stroke-width="1.5" marker-end="url(#arrS)"/>
      <line x1="440" y1="136" x2="440" y2="158" stroke="#00BFA5" stroke-width="1.5" marker-end="url(#arrS)"/>

      <rect x="303" y="160" width="90" height="34" rx="8" fill="#2D1A1A" stroke="#FF6B6B" stroke-width="1.5"/>
      <text x="348" y="181" text-anchor="middle" fill="#FF6B6B" font-size="11" font-weight="bold">◆ Causal</text>

      <rect x="397" y="160" width="90" height="34" rx="8" fill="#2D2418" stroke="#FFB347" stroke-width="1.5"/>
      <text x="442" y="181" text-anchor="middle" fill="#FFB347" font-size="11" font-weight="bold">★ Entity</text>

      <!-- Annotation: why each path goes where -->
      <text x="122" y="210" text-anchor="middle" fill="#666" font-size="10">Can build from single event</text>
      <text x="397" y="210" text-anchor="middle" fill="#666" font-size="10">Requires cross-event reasoning</text>
    </svg>
    </body></html>
    """


def _chart_locomo(theme: str = "dark"):
    methods = ["Full Context", "MemoryOS", "A-MEM", "Nemori", "MAGMA"]
    scores  = [0.481,         0.553,       0.580,   0.590,    0.700]
    muted = plotly_bar_muted(theme)
    colors  = [muted, muted, muted, muted, "#6C63FF"]
    layout = plotly_layout(theme)
    grid = plotly_grid(theme)
    tf_color = "#333333" if theme == "light" else "#FAFAFA"
    fig = go.Figure(go.Bar(
        x=scores, y=methods, orientation="h",
        marker_color=colors,
        text=[f"{s:.3f}" for s in scores],
        textposition="outside",
        textfont=dict(color=tf_color, size=12),
    ))
    fig.update_layout(
        title=dict(text="LoComo — Overall Judge Score", font=dict(color=layout["font"]["color"], size=13)),
        xaxis=dict(range=[0.3, 0.78], gridcolor=grid, title="Score"),
        yaxis=dict(gridcolor=grid),
        height=240, margin=dict(t=40, b=10, l=10, r=60),
        **layout,
    )
    fig.add_vline(x=0.700, line_dash="dot", line_color="#FFD700",
                  annotation_text="MAGMA", annotation_font_color="#FFD700",
                  annotation_position="top right")
    return fig


def _chart_longmem(theme: str = "dark"):
    methods = ["Full Context", "Nemori", "MAGMA"]
    scores  = [55.0,           56.2,     61.2]
    muted = plotly_bar_muted(theme)
    colors  = [muted, muted, "#6C63FF"]
    layout = plotly_layout(theme)
    grid = plotly_grid(theme)
    tf_color = "#333333" if theme == "light" else "#FAFAFA"
    fig = go.Figure(go.Bar(
        x=scores, y=methods, orientation="h",
        marker_color=colors,
        text=[f"{s}%" for s in scores],
        textposition="outside",
        textfont=dict(color=tf_color, size=12),
    ))
    fig.update_layout(
        title=dict(text="LongMemEval — Exact-Match Accuracy", font=dict(color=layout["font"]["color"], size=13)),
        xaxis=dict(range=[48, 68], gridcolor=grid, title="Accuracy (%)"),
        yaxis=dict(gridcolor=grid),
        height=200, margin=dict(t=40, b=10, l=10, r=60),
        **layout,
    )
    return fig


def _chart_tokens(theme: str = "dark"):
    methods = ["MAGMA (avg)", "A-MEM", "MemoryOS", "Full Context"]
    tokens  = [3400,           8200,    12500,       101000]
    muted = plotly_bar_muted(theme)
    colors  = ["#6C63FF", muted, muted, "#FF6B6B"]
    layout = plotly_layout(theme)
    grid = plotly_grid(theme)
    tf_color = "#333333" if theme == "light" else "#FAFAFA"
    fig = go.Figure(go.Bar(
        x=tokens, y=methods, orientation="h",
        marker_color=colors,
        text=[f"{t:,}" for t in tokens],
        textposition="outside",
        textfont=dict(color=tf_color, size=11),
    ))
    fig.update_layout(
        title=dict(text="Avg Tokens per Query", font=dict(color=layout["font"]["color"], size=13)),
        xaxis=dict(gridcolor=grid, title="Tokens"),
        yaxis=dict(gridcolor=grid),
        height=200, margin=dict(t=40, b=10, l=10, r=80),
        **layout,
    )
    return fig


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render_about(theme: str = "dark"):
    # --- Hero ---
    st.markdown(
        """
        <div style="text-align:center;padding:12px 0 8px 0">
          <div style="font-size:12px;font-weight:700;color:#6C63FF;letter-spacing:3px;text-transform:uppercase;margin-bottom:8px">Research Paper Overview</div>
          <div style="font-size:38px;font-weight:800;color:#FAFAFA;letter-spacing:-1px">MAGMA</div>
          <div style="color:#AAAAAA;font-size:15px;margin:4px 0 2px 0">Multi-Graph based Agentic Memory Architecture</div>
          <div style="color:#555;font-size:12px">University of Texas at Dallas · University of Florida</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Key stats pills
    c1, c2, c3, c4 = st.columns(4)
    for col, val, label, color in [
        (c1, "0.700", "LoComo Score",       "#6C63FF"),
        (c2, "61.2%", "LongMemEval Acc.",   "#6C63FF"),
        (c3, "95%",   "Token Reduction",    "#00BFA5"),
        (c4, "1.47s", "Query Latency",      "#FFB347"),
    ]:
        with col:
            st.markdown(
                f"""
                <div style="text-align:center;padding:14px 8px;background:#252840;border:1px solid {color};border-radius:10px">
                  <div style="font-size:26px;font-weight:800;color:{color}">{val}</div>
                  <div style="font-size:11px;color:#AAAAAA;margin-top:3px">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # -----------------------------------------------------------------------
    # SECTION 1 — System Architecture
    # -----------------------------------------------------------------------
    _section_header("🏗️", "System Architecture — The Big Picture", "#6C63FF",
                    "How events flow in, how memory is structured, how queries get answered")

    components.html(_svg_architecture(theme), height=330, scrolling=False)

    st.markdown(
        """
        <div style="background:#252840;border-left:3px solid #6C63FF;border-radius:0 8px 8px 0;padding:10px 16px;font-size:12px;color:#CCCCCC;line-height:1.6;margin-top:4px">
          Events stream in continuously → the <b style="color:#FFB347">Write Process</b> splits them across two paths into the
          <b style="color:#6C63FF">Multi-Graph (MAG)</b> → when a user queries, a 4-stage pipeline retrieves only the
          relevant subgraph → the LLM answers from <b style="color:#00BFA5">~1,200 tokens</b> instead of 101,000.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------------
    # SECTION 2 — The Problem
    # -----------------------------------------------------------------------
    _section_header("⚠️", "The Problem — Why Existing Approaches Fail", "#FF6B6B",
                    "Full context and basic RAG both break down on long-horizon agent memory")

    col_a, col_b = st.columns(2, gap="medium")
    with col_a:
        st.markdown(
            """
            <div style="background:#2D1A1A;border:1px solid #FF6B6B;border-radius:10px;padding:16px;height:100%">
              <div style="color:#FF6B6B;font-weight:700;font-size:13px;margin-bottom:8px">❌ Full Context</div>
              <div style="color:#CCBBBB;font-size:12px;line-height:1.7">
                Stuffs the entire history into the prompt — <b style="color:#FF6B6B">101K tokens per query</b>,
                scales quadratically with conversation length, and produces vague answers because
                the model gets lost in irrelevant events.
              </div>
            </div>
            """, unsafe_allow_html=True)
    with col_b:
        st.markdown(
            """
            <div style="background:#2D1A1A;border:1px solid #FF6B6B;border-radius:10px;padding:16px;height:100%">
              <div style="color:#FF6B6B;font-weight:700;font-size:13px;margin-bottom:8px">❌ Standard RAG</div>
              <div style="color:#CCBBBB;font-size:12px;line-height:1.7">
                Flat vector search retrieves semantically similar chunks — but <b>WHY</b> questions
                need causal chains, <b>WHEN</b> needs time ordering, <b>WHO</b> needs entity tracking.
                Embeddings alone cannot represent these.
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Token comparison visual
    st.markdown(
        """
        <div style="background:#1E2030;border:1px solid #333;border-radius:10px;padding:16px 20px">
          <div style="font-size:12px;color:#AAAAAA;margin-bottom:10px">Tokens used per query</div>

          <div style="margin-bottom:8px">
            <div style="display:flex;justify-content:space-between;margin-bottom:3px">
              <span style="font-size:12px;color:#FF6B6B">Full Context</span>
              <span style="font-size:12px;color:#FF6B6B;font-weight:700">101,000 tokens ❌</span>
            </div>
            <div style="background:#3D1A1A;border-radius:4px;height:20px;width:100%">
              <div style="background:#FF6B6B;border-radius:4px;height:20px;width:100%"></div>
            </div>
          </div>

          <div style="margin-bottom:8px">
            <div style="display:flex;justify-content:space-between;margin-bottom:3px">
              <span style="font-size:12px;color:#FFB347">MemoryOS</span>
              <span style="font-size:12px;color:#FFB347">12,500 tokens</span>
            </div>
            <div style="background:#2D2418;border-radius:4px;height:14px;width:100%">
              <div style="background:#FFB347;border-radius:4px;height:14px;width:12%"></div>
            </div>
          </div>

          <div style="margin-bottom:8px">
            <div style="display:flex;justify-content:space-between;margin-bottom:3px">
              <span style="font-size:12px;color:#9D97FF">A-MEM</span>
              <span style="font-size:12px;color:#9D97FF">8,200 tokens</span>
            </div>
            <div style="background:#1E1A35;border-radius:4px;height:14px;width:100%">
              <div style="background:#9D97FF;border-radius:4px;height:14px;width:8%"></div>
            </div>
          </div>

          <div>
            <div style="display:flex;justify-content:space-between;margin-bottom:3px">
              <span style="font-size:12px;color:#00BFA5;font-weight:700">MAGMA</span>
              <span style="font-size:12px;color:#00BFA5;font-weight:700">700–4,200 tokens ✓</span>
            </div>
            <div style="background:#1A2420;border-radius:4px;height:20px;width:100%">
              <div style="background:#00BFA5;border-radius:4px;height:20px;width:3%"></div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # SECTION 3 — The 4 Graphs
    # -----------------------------------------------------------------------
    _section_header("🕸️", "The 4 Memory Graphs — Orthogonal Dimensions", "#9D97FF",
                    "Each graph captures what the others fundamentally cannot — together they cover all reasoning types")

    GRAPHS = [
        ("Semantic", "●", "#6C63FF", "#1E1A35", "#6C63FF", "WHAT",
         _svg_semantic,
         "Groups events by conceptual similarity. Built from embeddings. Undirected.",
         "All midterm mentions cluster together, even weeks apart."),
        ("Temporal", "■", "#00BFA5", "#1A2D2A", "#00BFA5", "WHEN",
         _svg_temporal,
         "Strict chronological chain. Directed past→future. Enables before/after reasoning.",
         "Sam's loan request (E08) came 3 days after his intro (E05)."),
        ("Causal",   "◆", "#FF6B6B", "#2D1A1A", "#FF6B6B", "WHY",
         _svg_causal,
         "Directed cause→effect links. Built in slow path via LLM reasoning. Most impactful graph.",
         "Intro → exploits trust → steals notes → disappears."),
        ("Entity",   "★", "#FFB347", "#2D2418", "#FFB347", "WHO",
         _svg_entity,
         "Tracks people, places, objects across time. Object permanence for agents.",
         "Maya links: E14 (witness), E24 (alarm), E30 (reports to Dean)."),
    ]

    # Render as 2×2 grid — each graph gets half the page width
    for row_start in range(0, 4, 2):
        col_l, col_r = st.columns(2, gap="medium")
        for col, (gtype, sym, color, bg, border, intent, diagram_fn, desc, example) in zip(
            [col_l, col_r], GRAPHS[row_start:row_start + 2]
        ):
            with col:
                st.markdown(
                    f"""
                    <div style="background:{bg};border:1px solid {border};border-radius:10px 10px 0 0;padding:14px 16px;display:flex;align-items:center;gap:12px">
                      <span style="font-size:28px;color:{color}">{sym}</span>
                      <div>
                        <div style="color:{color};font-weight:700;font-size:16px">{gtype} Graph</div>
                        <div style="background:{color}22;color:{color};padding:1px 10px;border-radius:8px;font-size:11px;font-weight:600;display:inline-block;margin-top:3px">answers {intent}</div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
                components.html(diagram_fn(theme=theme), height=220, scrolling=False)
                st.markdown(
                    f"""
                    <div style="background:{bg};border:1px solid {border}55;border-top:none;border-radius:0 0 10px 10px;padding:12px 16px">
                      <div style="color:#CCCCCC;font-size:12px;line-height:1.6;margin-bottom:6px">{desc}</div>
                      <div style="color:{color};font-size:11px;font-style:italic">e.g. {example}</div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # SECTION 4 — Dual-Stream Write
    # -----------------------------------------------------------------------
    _section_header("⚡", "Memory Write — Dual-Stream Ingestion", "#FFB347",
                    "Two parallel paths ensure responsiveness without sacrificing depth")

    components.html(_svg_dual_stream(theme), height=230, scrolling=False)

    col_f, col_s = st.columns(2, gap="medium")
    with col_f:
        st.markdown(
            """
            <div style="background:#2D2418;border:1px solid #FFB347;border-radius:10px;padding:14px">
              <div style="color:#FFB347;font-weight:700;font-size:13px;margin-bottom:6px">⚡ Fast Path — Synaptic Ingestion</div>
              <div style="color:#DDCCAA;font-size:12px;line-height:1.6">
                Every new event is <b>immediately indexed</b> into Semantic and Temporal graphs —
                the two that need only the single event to build correctly.
                Non-blocking, so the agent stays responsive during ingestion.
              </div>
            </div>
            """, unsafe_allow_html=True)
    with col_s:
        st.markdown(
            """
            <div style="background:#1A2420;border:1px solid #00BFA5;border-radius:10px;padding:14px">
              <div style="color:#00BFA5;font-weight:700;font-size:13px;margin-bottom:6px">🔄 Slow Path — Structural Consolidation</div>
              <div style="color:#AADDCC;font-size:12px;line-height:1.6">
                Runs <b>asynchronously</b> in the background. An LLM pass refines Causal and Entity
                edges — the two that require <i>cross-event reasoning</i> to build correctly.
                This is why causal links are the richest: they're built thoughtfully.
              </div>
            </div>
            """, unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # SECTION 5 — 4-Stage Query Pipeline
    # -----------------------------------------------------------------------
    _section_header("🔍", "Query Pipeline — 4 Stages", "#00BFA5",
                    "What happens between 'user asks a question' and 'agent answers'")

    components.html(_svg_pipeline_flow(theme), height=120, scrolling=False)

    stages = [
        ("#6C63FF", "01  Anchor Identification",
         "The query is classified by intent (WHY/WHEN/WHO/WHAT). <b>RRF fusion</b> (Reciprocal Rank Fusion) runs across all 4 graphs to find the top-k seed nodes — the starting points for traversal. RRF ranks by consensus across graph types, not just the loudest single signal."),
        ("#00BFA5", "02  Adaptive Hybrid Retrieval",
         "<b>Heuristic beam search</b> expands from anchor nodes — prioritising edges from the intent-matched graph (e.g. causal for WHY) while following secondary graph edges when they add context. Beam score = structural alignment + semantic affinity. This is what makes MAGMA different from standard graph RAG: traversal is intent-aware, not exhaustive."),
        ("#FFB347", "03  Context Scaffolding",
         "Retrieved nodes are assembled with <b>provenance tracking</b> (every fact cites its source event) and <b>topological ordering</b> — causal edges always appear cause-before-effect. This prevents the LLM from inferring backwards causality, a common hallucination failure mode."),
        ("#FF6B6B", "04  Salient-Based Token Budgeting",
         "<b>High-salience nodes</b> (on the traversal path) keep full detail. <b>Low-salience nodes</b> (peripheral) are compressed. This keeps the prompt under budget — 700–4,200 tokens — regardless of conversation length. MAGMA isn't truncating blindly; it's compressing intelligently."),
    ]

    for color, name, detail in stages:
        st.markdown(
            f"""
            <div style="display:flex;gap:14px;margin-bottom:10px;background:#1E2030;border-left:4px solid {color};border-radius:0 10px 10px 0;padding:14px 16px">
              <div>
                <div style="color:{color};font-weight:700;font-size:13px;margin-bottom:5px">{name}</div>
                <div style="color:#CCCCCC;font-size:12px;line-height:1.65">{detail}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # SECTION 6 — Results
    # -----------------------------------------------------------------------
    _section_header("📊", "Results — Two Benchmarks", "#FFD700",
                    "Validated on LoComo (judge-scored) and LongMemEval (exact-match) — different datasets, same story")

    col_loco, col_long = st.columns(2, gap="medium")
    with col_loco:
        st.plotly_chart(_chart_locomo(theme), use_container_width=True)
    with col_long:
        st.plotly_chart(_chart_longmem(theme), use_container_width=True)

    st.plotly_chart(_chart_tokens(theme), use_container_width=True)

    st.markdown(
        """
        <div style="display:flex;gap:12px;margin-top:4px">
          <div style="flex:1;background:#1E2030;border:1px solid #333;border-radius:10px;padding:14px;text-align:center">
            <div style="color:#FF6B6B;font-size:12px;margin-bottom:4px">Biggest individual gain</div>
            <div style="color:#FAFAFA;font-size:14px;font-weight:700">Adversarial queries</div>
            <div style="color:#AAAAAA;font-size:12px">MAGMA 0.742 vs Full Context 0.205</div>
            <div style="color:#888;font-size:11px;margin-top:4px">+0.537 improvement — causal graph sees through trick questions</div>
          </div>
          <div style="flex:1;background:#1E2030;border:1px solid #333;border-radius:10px;padding:14px;text-align:center">
            <div style="color:#00BFA5;font-size:12px;margin-bottom:4px">Generalisation</div>
            <div style="color:#FAFAFA;font-size:14px;font-weight:700">Wins on both benchmarks</div>
            <div style="color:#AAAAAA;font-size:12px">LoComo + LongMemEval — different task formats</div>
            <div style="color:#888;font-size:11px;margin-top:4px">MAGMA wasn't tuned for one specific benchmark</div>
          </div>
          <div style="flex:1;background:#1E2030;border:1px solid #333;border-radius:10px;padding:14px;text-align:center">
            <div style="color:#FFB347;font-size:12px;margin-bottom:4px">Efficiency leader</div>
            <div style="color:#FAFAFA;font-size:14px;font-weight:700">Lowest latency</div>
            <div style="color:#AAAAAA;font-size:12px">1.47s — fastest of all baselines</div>
            <div style="color:#888;font-size:11px;margin-top:4px">Higher accuracy AND faster — not a trade-off</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # CTA
    # -----------------------------------------------------------------------
    st.markdown("---")
    st.markdown(
        '<div style="text-align:center;color:#AAAAAA;font-size:13px;margin-bottom:12px">See all of this come to life through an interactive story demo.</div>',
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start the Demo — The Study Group Mystery →", use_container_width=True, type="primary"):
            st.session_state["act"] = 1
            st.rerun()

"""
themes.py — Light/dark theme CSS overrides and Plotly color helpers for MAGMA demo.

Strategy: instead of rewriting every hardcoded color, inject CSS attribute-selector overrides
that target elements by their inline style values. Works for st.markdown() HTML and can be
embedded into components.html() iframe documents.
"""

# ---------------------------------------------------------------------------
# Inline-style override CSS (works inside iframe documents too)
# ---------------------------------------------------------------------------
_IFRAME_CSS_OVERRIDES = """
/* ── Background overrides ── */
*[style*="background:#1A1D2E"],*[style*="background: #1A1D2E"]{background:#FFFFFF!important}
*[style*="background:#252840"],*[style*="background: #252840"]{background:#F0F2F6!important}
*[style*="background:#1E2030"],*[style*="background: #1E2030"]{background:#F5F6FA!important}
*[style*="background:#1E1A35"]{background:#F3F0FF!important}
*[style*="background:#1A2D2A"]{background:#E8FBF8!important}
*[style*="background:#1A2D1A"]{background:#EBF7EB!important}
*[style*="background:#1A2420"]{background:#E0F5F0!important}
*[style*="background:#1E2A2A"]{background:#E8F5F2!important}
*[style*="background:#2D1A1A"]{background:#FFF0F0!important}
*[style*="background:#3D1A1A"]{background:#FFE0E0!important}
*[style*="background:#2D2418"]{background:#FFF5E0!important}
*[style*="background:#2D2800"]{background:#FFFFF0!important}
*[style*="background:#12141F"],*[style*="background:#12151F"]{background:#EDEEF5!important}
*[style*="background:#2D1F1A"]{background:#FFF2E8!important}
*[style*="background:#3D2E1A"]{background:#FFF0D0!important}
*[style*="background:linear-gradient(135deg,#1A1D2E"]{background:linear-gradient(135deg,#F5F6FA,#ECEEF8)!important}

/* ── Text color overrides ── */
*[style*="color:#FAFAFA"]{color:#1A1D2E!important}
*[style*="color:#EAEAEA"]{color:#222222!important}
*[style*="color:#CCCCCC"]{color:#333333!important}
*[style*="color:#DDDDDD"]{color:#333333!important}
*[style*="color:#AAAAAA"]{color:#777777!important}
*[style*="color:#BBBBBB"]{color:#555555!important}
*[style*="color:#DDAAAA"]{color:#8B3333!important}
*[style*="color:#CCBBBB"]{color:#8B4444!important}
*[style*="color:#AADDCC"]{color:#1A6B5A!important}
*[style*="color:#CCDDCC"]{color:#336633!important}
*[style*="color:#DDCCAA"]{color:#6B4800!important}
*[style*="color:#666"]{color:#999!important}
*[style*="color:#555"]{color:#888!important}
*[style*="color:#444"]{color:#888!important}

/* ── Border overrides ── */
*[style*="border:1px solid #333"],*[style*="border: 1px solid #333"]{border-color:#DDDDDD!important}
*[style*="border-bottom:1px solid #333"]{border-bottom-color:#DDDDDD!important}
*[style*="border-top:1px solid #333"]{border-top-color:#DDDDDD!important}
*[style*="border-right:1px solid #333"]{border-right-color:#DDDDDD!important}
*[style*="border:1px solid #444"],*[style*="border: 1px solid #444"]{border-color:#CCCCCC!important}
*[style*="border:2px solid #444"]{border-color:#CCCCCC!important}
*[style*="border:1px dashed #555"]{border-color:#AAAAAA!important}

/* ── SVG presentation-attribute overrides ── */
[fill="#252840"]{fill:#F0F2F6!important}
[fill="#1A1D2E"]{fill:#FFFFFF!important}
[fill="#1E2030"]{fill:#F5F6FA!important}
[fill="#1E1A35"]{fill:#F3F0FF!important}
[fill="#1A2D2A"]{fill:#E8FBF8!important}
[fill="#1A2D1A"]{fill:#EBF7EB!important}
[fill="#2D1A1A"]{fill:#FFF0F0!important}
[fill="#2D2418"]{fill:#FFF5E0!important}
[fill="#1A2420"]{fill:#E0F5F0!important}
[fill="#FAFAFA"]{fill:#1A1D2E!important}
[fill="#AAAAAA"]{fill:#777777!important}
[fill="#DDDDDD"]{fill:#333333!important}
[fill="#666"]{fill:#999!important}
[fill="#555"]{fill:#999!important}
[stroke="#555"]{stroke:#CCCCCC!important}
[stroke="#444"]{stroke:#CCCCCC!important}
[stroke="#333"]{stroke:#DDDDDD!important}
[stroke="#666"]{stroke:#CCCCCC!important}
"""

# ---------------------------------------------------------------------------
# App-level CSS (injected into Streamlit page via st.markdown)
# Includes Streamlit native overrides AND the inline-style overrides
# ---------------------------------------------------------------------------
LIGHT_APP_CSS = """
html,body,.stApp{background-color:#FFFFFF!important}
section[data-testid="stSidebar"]{
  background:#F0F2F6!important;
  border-right:1px solid #D0D4E8!important;
}
h1{color:#1A1D2E!important;font-size:28px!important}
h2{color:#333333!important}
h3{color:#444444!important}
hr{border-color:#D0D4E8!important}
div[data-testid="metric-container"]{background:#F0F2F6!important;border-color:#D0D4E8!important}
div[data-testid="metric-container"] label{color:#777777!important}
div[data-testid="metric-container"] div[data-testid="stMetricValue"]{color:#6C63FF!important}
div[data-testid="stCaption"]{color:#777777!important}
iframe{border-color:#D0D4E8!important}
div[data-testid="stRadio"] label{color:#444444!important}
div[data-testid="stCheckbox"] label{color:#444444!important}
div[data-testid="stSidebar"] div[data-testid="stRadio"] label{color:#777777!important}
""" + _IFRAME_CSS_OVERRIDES

# ---------------------------------------------------------------------------
# Iframe-level CSS (embed in components.html document <head>)
# ---------------------------------------------------------------------------
LIGHT_IFRAME_CSS = """
body{background:#FFFFFF!important;color:#1A1D2E!important}
""" + _IFRAME_CSS_OVERRIDES

# ---------------------------------------------------------------------------
# Plotly layout helpers
# ---------------------------------------------------------------------------
def plotly_layout(theme: str) -> dict:
    """Base layout kwargs for Plotly charts."""
    if theme == "light":
        return dict(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#F5F6FA",
            font=dict(color="#1A1D2E"),
        )
    return dict(
        paper_bgcolor="#1A1D2E",
        plot_bgcolor="#252840",
        font=dict(color="#FAFAFA"),
    )


def plotly_grid(theme: str) -> str:
    return "#DDDDDD" if theme == "light" else "#333"


def plotly_bar_muted(theme: str) -> str:
    """Color for non-highlighted bars."""
    return "#BBBBBB" if theme == "light" else "#444"


def plotly_textfont(theme: str) -> dict:
    """Text font for bar labels (white on colored bars works for both themes)."""
    return dict(color="#FAFAFA", size=12)


def plotly_legend(theme: str) -> dict:
    if theme == "light":
        return dict(bgcolor="#FFFFFF", bordercolor="#DDDDDD")
    return dict(bgcolor="#1A1D2E", bordercolor="#333")


def gauge_steps(theme: str) -> list:
    if theme == "light":
        return [
            {"range": [0.3, 0.5],  "color": "#FFE8E8"},
            {"range": [0.5, 0.6],  "color": "#FFF0D0"},
            {"range": [0.6, 0.68], "color": "#E0F5F5"},
            {"range": [0.68, 0.75],"color": "#E0F5E0"},
        ]
    return [
        {"range": [0.3, 0.5],  "color": "#3D1A1A"},
        {"range": [0.5, 0.6],  "color": "#3D2E1A"},
        {"range": [0.6, 0.68], "color": "#1A2D2D"},
        {"range": [0.68, 0.75],"color": "#1A2D1A"},
    ]

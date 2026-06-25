# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

An interactive Streamlit demo of the **MAGMA** research paper ("Multi-Graph based Agentic Memory Architecture"). The demo is a gamified 5-act mystery story that visualizes MAGMA's 4-graph memory system — no live LLM calls, everything is scripted simulation. The paper PDF is at `magma-research-paper.pdf`.

## Running the demo

```bash
cd magma-demo
pip install -r requirements.txt
streamlit run app.py
# Opens at http://localhost:8501
```

**No pyvis dependency** — graph HTML is generated directly via vis.js CDN in `components/graph_viz.py`. Do not re-add pyvis; its mandatory `ipython` dependency causes OOM on Streamlit Cloud free tier.

**`streamlit.components.v1` must be imported explicitly** — `import streamlit.components.v1 as components` at the top of any file that calls `components.html(...)`. Accessing it as `st.components.v1` raises an `AttributeError`.

## Architecture

All demo content lives in `magma-demo/`. The app is a single-page Streamlit wizard using `st.session_state["act"]` (1–5) as the router. `app.py` contains all 5 act renderers and calls into `components/` for complex panels.

**Data flow:** `data/scenario.py` is the single source of truth — it defines all 32 events, 4 pre-scripted queries with traversal paths, ablation scores (from paper Table 4), and benchmark numbers (Tables 1–4). Nothing is computed at runtime; graph traversal is a pre-scripted replay.

**Graph rendering:** `components/graph_viz.py` builds NetworkX graphs once (singleton `_GRAPHS`) from the edge lists in `scenario.py`, then serialises nodes/edges to JSON and injects them into a vis.js HTML template (vis-network 9.1.2 via CDN). These self-contained HTML strings are embedded via `components.html(..., height=N, scrolling=False)`. Highlighted nodes/edges for traversal animation are passed as arguments — the function rebuilds the HTML each step.

**Traversal animation pattern** (used in Act 3 and Act 2):
```python
placeholder = st.empty()
for step in query["traversal_path"]:
    visited_nodes.append(step["node"])
    html = build_graph_html(graph_type, highlighted_nodes=visited_nodes, ...)
    with placeholder:
        components.html(html, height=465, scrolling=False)
    time.sleep(0.7)
```
Streamlit re-runs the entire script on every widget interaction — guard any stateful animation with `if st.session_state.get("traversal_running")` to prevent replaying on unrelated widget changes.

**Scoring:** Detective points accumulate in `st.session_state["score"]`. Each act awards points on first completion — guard with `if not st.session_state.get("act_N_complete")` before adding.

## Key constraints from the paper

The 4 graph types and their intent routing:
- **Semantic** (`●`, `#6C63FF`) — WHAT queries; undirected, conceptual similarity
- **Temporal** (`■`, `#00BFA5`) — WHEN queries; directed chronological chain
- **Causal** (`◆`, `#FF6B6B`) — WHY queries; directed cause→effect
- **Entity** (`★`, `#FFB347`) — WHO queries; undirected, person/object tracking

Benchmark numbers (do not invent): MAGMA LoComo score **0.700**, Full Context baseline **0.481**, average tokens **~3,400** vs **101,000** for full context, query latency **1.47s**.

## Deployment

Push `magma-demo/` to a public GitHub repo, then deploy via [share.streamlit.io](https://share.streamlit.io) — no secrets or environment variables needed.

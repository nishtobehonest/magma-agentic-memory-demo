# MAGMA — Multi-Graph Agentic Memory Architecture

> An interactive research demo exploring structured long-term memory for AI agents.  
> Paper by Dongming Jiang, Yi Li, Guanpeng Li, and Bingzhe Li (University of Texas at Dallas).  
> Demo built by Nishchay Vishwanath.  
> **Live:** https://magma-agentic-memory-demo.streamlit.app

---

## The problem

Ask an AI assistant something at the start of a conversation, and it handles it fine. Come back three sessions later expecting it to remember what you said, why you said it, and who was involved — and it will disappoint you.

This isn't a personality flaw. It's a structural one.

Every large language model (LLM) reads text through something called a **context window** (the block of text it's allowed to look at in one go — imagine reading with a flashlight that only illuminates one page at a time). Once earlier information scrolls out of that window, it's gone. The model can't reference what it never saw.

The obvious fix is to make the context window bigger. But 101,000 tokens (roughly 75,000 words — a full novel) isn't free. At that scale, every query is slow, every call is expensive, and research shows the model starts ignoring things buried in the middle anyway.

The smarter fix — the one teams have been reaching for — is **RAG**, or Retrieval-Augmented Generation (a system that stores information in a searchable database and pulls only the relevant pieces when needed, like using an index instead of rereading the whole book). RAG solves the token problem. But it introduces a new one: it retrieves by *similarity*, meaning it surfaces things that *sound like* your question, even when what you actually need is the thing that *caused* your question, or the thing that *happened right before* it. A similarity search doesn't know about sequence. It doesn't know about cause. It doesn't know who "Sam" is across ten different messages.

---

## The tension

Memory isn't one thing. When you try to recall something, you're actually pulling from several different kinds of knowledge simultaneously:

- **What** happened (the content)
- **When** it happened (the sequence)
- **Why** it happened (the cause)
- **Who** was involved (the people and objects that persisted through multiple events)

Current memory systems flatten all four into a single "similarity" score and call it a day. That works when questions are simple. It falls apart the moment someone asks "why did Sam start asking for money?" or "what happened after the midterm?" — questions that are fundamentally about order and cause, not topical similarity.

---

## The decision

The MAGMA paper's answer is to stop treating memory as a single dimension and start treating it as four separate but interlocking graphs (a graph being a structure of nodes connected by edges — think a web of relationships, not a spreadsheet):

**Semantic graph** (the *what*) — Groups events by topic. All midterm-related messages cluster together, even if they happened weeks apart and used different words. This is the layer most similar to traditional RAG, but it's one piece of a larger structure, not the whole system.

**Temporal graph** (the *when*) — An immutable, strictly ordered chain of events from first to last. Think of it as a timeline that never gets rewritten. It anchors every other graph in time.

**Causal graph** (the *why*) — Directed edges (arrows) from cause to effect, inferred by an LLM that reads pairs of events and asks "did this one enable that one?" This is the layer that can answer "why" questions without hallucinating (making things up that sound plausible but aren't true).

**Entity graph** (the *who*) — Tracks people, places, and objects across the full timeline. "Professor Chen's notes" showing up in week one and week three are connected here, even if the surrounding context looks nothing alike.

Each graph is **orthogonal** (independent from the others — removing one degrades certain reasoning without breaking the rest). Together, they give an agent the relational structure it needs to reason the way a person would.

---

## How it works

### Writing a memory

When a new event arrives — a message sent, an action taken — MAGMA handles it in two parallel streams:

The **fast path** fires immediately. The event gets timestamped, linked to the previous one in the temporal chain, and embedded (converted into a dense numeric representation) for semantic search. One write, no waiting.

The **slow path** runs asynchronously (in the background, without blocking anything else). An LLM examines the event's neighborhood in the graph and asks: does this event cause any nearby events? Which entities appear here and where else have they appeared? Causal and entity edges are expensive to infer, so this work happens separately, continuously refining the graph structure without slowing down the agent.

### Answering a query

When the agent needs to remember something, MAGMA classifies the intent of the question first:

- "Why did Sam ask for money?" → route to the causal graph
- "When did they first meet?" → route to the temporal graph
- "What were they studying?" → route to the semantic graph
- "Who did Alex interact with?" → route to the entity graph

Then it runs an **adaptive topological retrieval** (a search that follows graph edges intelligently, prioritizing edge types that match the question's intent, rather than treating every connection as equally relevant). High-priority nodes get retrieved with full context; peripheral ones get summarized. The result is a coherent, ordered narrative with provenance (each retrieved memory carries its timestamp and source) — not a bag of similar-sounding text fragments.

### The results

On LoComo and LongMemEval (standard benchmarks — test suites used by researchers to compare memory systems apples-to-apples):

| System | Judge Score | Tokens per Query |
|---|---|---|
| Full Context | 0.481 | 101,000 |
| Nemori | 0.590 | 3,460 |
| A-MEM | 0.580 | 2,620 |
| **MAGMA** | **0.700** | **3,700** |

The system scores highest while using 95% fewer tokens than full context. On adversarial queries (questions designed to trick similarity-based retrieval into surfacing irrelevant but topic-adjacent memories), MAGMA scores 0.742 — more than double the worst baseline at 0.205.

Ablation studies (experiments where you remove one component at a time to measure what it contributed) confirm that each graph is load-bearing: removing the adaptive traversal policy drops the score from 0.700 to 0.637; removing causal links drops it to 0.644; removing temporal ordering drops it to 0.647.

---

## The demo

Rather than ship a static paper summary, the demo rebuilds MAGMA's memory system around a five-act interactive mystery: **The Study Group Mystery**.

Four students — Alex, Jordan, Sam, and Maya — spend three weeks preparing for a midterm. Over thirty-two scripted events, the player watches MAGMA ingest each memory across all four graphs, then investigates: who photographed the professor's private notes, and why?

**Act 1** establishes the problem — a visual comparison of full context (the expensive flashlight), plain RAG (similarity-only retrieval), and MAGMA side by side on the same scenario.

**Act 2** is memory ingestion. Events stream in one by one. The player watches four graph visualizations populate in real time, earning points by answering which graph type helps with each new event.

**Act 3** is the investigation. The player queries MAGMA — "When did Sam first ask for money?" / "Why did he photograph the notes?" / "Who did he interact with most?" — and watches the system traverse (walk through) the relevant graph, highlighting each node it visits.

**Act 4** is the reveal. The causal chain unfolds, identifying the guilty party and showing which graph edges made the conclusion possible. Score badges range from Senior Investigator to Master of MAGMA.

The demo uses pre-scripted traversals and pre-computed graph states — no live LLM calls, no API keys required. The point isn't to run MAGMA in production; it's to make the architecture's reasoning legible.

---

## How to run it

```bash
git clone https://github.com/FredJiang0324/MAGMA  # the original research repo
cd magma-demo
pip install -r requirements.txt
streamlit run app.py
```

Or visit the live deployment: **https://magma-agentic-memory-demo.streamlit.app**

**Dependencies:** Python 3.10+, Streamlit ≥ 1.35, NetworkX 3.3, PyVis 0.3.2 (pinned — later versions break the HTML graph export API), Plotly 5.22.

---

## What's in this repo

```
MAGMA-agentic-memory-architecture/
├── magma-research-paper.pdf   # Full paper — experiments, ablations, limitations
├── RESUME_MAGMA.md            # Resume bullets for the demo
├── requirements.txt           # Top-level dependencies
├── streamlit_app.py           # Entry point
└── magma-demo/
    ├── app.py                 # Main app router (5-act navigation)
    ├── components/            # Per-act UI components
    ├── data/                  # scenario.py — 32 events, pre-traversed queries
    └── styles/                # CSS overrides
```

---

## Paper & credits

MAGMA: Multi-Graph based Agentic Memory Architecture  
Dongming Jiang, Yi Li, Guanpeng Li, Bingzhe Li — University of Texas at Dallas  
Research code: https://github.com/FredJiang0324/MAGMA

Interactive demo by [Nishchay Vishwanath](https://nishchay.me)

"""
MAGMA Demo — Pre-scripted scenario data.
"The Study Group Mystery": An agent must solve who exploited a CS study group's trust network.
"""

# ---------------------------------------------------------------------------
# EVENTS — 32 messages spanning 3 weeks of a semester
# Each event represents one memory unit ingested into the MAGMA system.
# ---------------------------------------------------------------------------
EVENTS = [
    # --- Week 1 ---
    {
        "id": "E01", "week": 1, "day": "Mon", "time": "10:00am",
        "speaker": "System",
        "content": "Alex joins the CSCI 4300 study group chat. First message: 'Hey everyone, Jordan said this was the place to be!'",
        "entities": ["Alex", "Jordan", "StudyGroup"],
        "graph_memberships": ["temporal", "entity", "semantic"],
        "causal_causes": [], "causal_effects": [],
        "semantic_similar": ["E05", "E07"],
    },
    {
        "id": "E02", "week": 1, "day": "Mon", "time": "10:05am",
        "speaker": "Jordan",
        "content": "Welcome Alex! We meet at Butler Library every Tuesday and Thursday.",
        "entities": ["Jordan", "Alex", "Library"],
        "graph_memberships": ["temporal", "entity"],
        "causal_causes": [], "causal_effects": [],
        "semantic_similar": ["E01"],
    },
    {
        "id": "E03", "week": 1, "day": "Mon", "time": "2:00pm",
        "speaker": "Alex",
        "content": "Just got the syllabus for CSCI 4300. Prof. Chen's midterm is supposed to be brutal.",
        "entities": ["Alex", "ProfChen"],
        "graph_memberships": ["temporal", "semantic"],
        "causal_causes": [], "causal_effects": [],
        "semantic_similar": ["E12", "E19"],
    },
    {
        "id": "E04", "week": 1, "day": "Tue", "time": "4:00pm",
        "speaker": "Jordan",
        "content": "Study session was great today. Covered chapters 1-3.",
        "entities": ["Jordan", "StudyGroup"],
        "graph_memberships": ["temporal", "semantic"],
        "causal_causes": [], "causal_effects": [],
        "semantic_similar": ["E10", "E17"],
    },
    {
        "id": "E05", "week": 1, "day": "Wed", "time": "2:00pm",
        "speaker": "Jordan",
        "content": "Hey everyone — this is Sam, he's in my dorm. Super sharp with algorithms, let's bring him in!",
        "entities": ["Jordan", "Sam", "Alex", "StudyGroup"],
        "graph_memberships": ["temporal", "entity", "semantic"],
        "causal_causes": [],
        "causal_effects": ["E08", "E18"],  # Sam's later actions were enabled by this intro
        "semantic_similar": ["E01"],
    },
    {
        "id": "E06", "week": 1, "day": "Wed", "time": "2:10pm",
        "speaker": "Sam",
        "content": "Hey all! Happy to be here. Jordan's told me a lot about this group. Looking forward to the midterm prep.",
        "entities": ["Sam", "Jordan"],
        "graph_memberships": ["temporal", "entity"],
        "causal_causes": [], "causal_effects": [],
        "semantic_similar": ["E05"],
    },
    {
        "id": "E07", "week": 1, "day": "Thu", "time": "4:00pm",
        "speaker": "Alex",
        "content": "Study session with Sam today — he's brilliant, explained dynamic programming in 10 minutes.",
        "entities": ["Alex", "Sam"],
        "graph_memberships": ["temporal", "entity", "semantic"],
        "causal_causes": [], "causal_effects": [],
        "semantic_similar": ["E04", "E10"],
    },
    {
        "id": "E08", "week": 1, "day": "Fri", "time": "6:00pm",
        "speaker": "Sam",
        "content": "Hey Jordan, embarrassing ask but I'm short $50 this month. Textbook situation. Could you lend me?",
        "entities": ["Sam", "Jordan"],
        "graph_memberships": ["temporal", "entity", "causal"],
        "causal_causes": ["E05"],  # Jordan's intro created the trust that enabled this ask
        "causal_effects": ["E09"],
        "semantic_similar": ["E18"],
    },
    {
        "id": "E09", "week": 1, "day": "Fri", "time": "6:30pm",
        "speaker": "Jordan",
        "content": "Sure Sam, no worries. I'll Venmo you. Pay back whenever.",
        "entities": ["Jordan", "Sam"],
        "graph_memberships": ["temporal", "entity", "causal"],
        "causal_causes": ["E08"],
        "causal_effects": [],
        "semantic_similar": ["E20"],
    },
    # --- Week 2 ---
    {
        "id": "E10", "week": 2, "day": "Mon", "time": "3:00pm",
        "speaker": "Alex",
        "content": "Study session today. We covered graph algorithms and recursion. Good vibes.",
        "entities": ["Alex", "StudyGroup"],
        "graph_memberships": ["temporal", "semantic"],
        "causal_causes": [], "causal_effects": [],
        "semantic_similar": ["E04", "E07", "E17"],
    },
    {
        "id": "E11", "week": 2, "day": "Mon", "time": "5:00pm",
        "speaker": "Jordan",
        "content": "Reminder: midterm is in 2 weeks. Prof Chen's exams are no joke.",
        "entities": ["Jordan", "ProfChen"],
        "graph_memberships": ["temporal", "semantic"],
        "causal_causes": [], "causal_effects": [],
        "semantic_similar": ["E03", "E12", "E19"],
    },
    {
        "id": "E12", "week": 2, "day": "Tue", "time": "1:00pm",
        "speaker": "Alex",
        "content": "Prof Chen posted old exams on Courseworks. But apparently his notes have the real gold — never posted publicly.",
        "entities": ["Alex", "ProfChen", "Notes"],
        "graph_memberships": ["temporal", "semantic", "entity"],
        "causal_causes": [],
        "causal_effects": ["E14"],  # Reveals that Chen's notes are valuable — motivates E14
        "semantic_similar": ["E03", "E11", "E19"],
    },
    {
        "id": "E13", "week": 2, "day": "Tue", "time": "4:00pm",
        "speaker": "Sam",
        "content": "Anyone know if Chen's office hours are on Wednesdays or Thursdays this week?",
        "entities": ["Sam", "ProfChen"],
        "graph_memberships": ["temporal", "entity"],
        "causal_causes": [], "causal_effects": [],
        "semantic_similar": ["E12"],
    },
    {
        "id": "E14", "week": 2, "day": "Wed", "time": "2:30pm",
        "speaker": "Maya",
        "content": "Hey guys... I was at Butler Library and I saw Sam in the study carrel next to Prof Chen photographing pages from what looked like Chen's handwritten notes. Thought that was weird.",
        "entities": ["Maya", "Sam", "ProfChen", "Notes", "Library"],
        "graph_memberships": ["temporal", "entity", "causal"],
        "causal_causes": ["E12"],  # Knowledge that notes had value motivated this
        "causal_effects": ["E22"],  # This action eventually leads to Sam's disappearance
        "semantic_similar": ["E12"],
    },
    {
        "id": "E15", "week": 2, "day": "Wed", "time": "3:00pm",
        "speaker": "Alex",
        "content": "That's strange Maya. Maybe he was just studying nearby?",
        "entities": ["Alex", "Maya", "Sam"],
        "graph_memberships": ["temporal", "entity"],
        "causal_causes": [], "causal_effects": [],
        "semantic_similar": ["E14"],
    },
    {
        "id": "E16", "week": 2, "day": "Wed", "time": "3:05pm",
        "speaker": "Jordan",
        "content": "I'm sure it's nothing. Sam's super focused this semester.",
        "entities": ["Jordan", "Sam"],
        "graph_memberships": ["temporal", "entity"],
        "causal_causes": [], "causal_effects": [],
        "semantic_similar": ["E05", "E06"],
    },
    {
        "id": "E17", "week": 2, "day": "Thu", "time": "4:00pm",
        "speaker": "Alex",
        "content": "Thursday study session. Sam helped explain dynamic programming again. Feeling confident about the midterm.",
        "entities": ["Alex", "Sam", "StudyGroup"],
        "graph_memberships": ["temporal", "semantic"],
        "causal_causes": [], "causal_effects": [],
        "semantic_similar": ["E04", "E07", "E10"],
    },
    {
        "id": "E18", "week": 2, "day": "Fri", "time": "7:00pm",
        "speaker": "Sam",
        "content": "Hey Alex, I know this is awkward but Jordan said you might be able to help — I'm short $30 this week too. Rideshare situation.",
        "entities": ["Sam", "Alex", "Jordan"],
        "graph_memberships": ["temporal", "entity", "causal"],
        "causal_causes": ["E05"],  # Jordan's intro + vouching enabled this second request
        "causal_effects": ["E20"],
        "semantic_similar": ["E08"],
    },
    {
        "id": "E19", "week": 2, "day": "Fri", "time": "8:00pm",
        "speaker": "Jordan",
        "content": "Panic mode — midterm is next Friday. Creating a shared study doc. Everyone add your notes!",
        "entities": ["Jordan", "StudyGroup", "ProfChen"],
        "graph_memberships": ["temporal", "semantic"],
        "causal_causes": [], "causal_effects": [],
        "semantic_similar": ["E03", "E11", "E12"],
    },
    {
        "id": "E20", "week": 2, "day": "Fri", "time": "8:30pm",
        "speaker": "Alex",
        "content": "Sure Sam, Venmo'd you $30. No worries, we've all been there.",
        "entities": ["Alex", "Sam"],
        "graph_memberships": ["temporal", "entity", "causal"],
        "causal_causes": ["E18"],
        "causal_effects": [],
        "semantic_similar": ["E09"],
    },
    # --- Week 3 (Midterm Week) ---
    {
        "id": "E21", "week": 3, "day": "Mon", "time": "10:00am",
        "speaker": "Alex",
        "content": "All-hands study session tonight. 7pm at Butler. Sam said he'll bring practice problems.",
        "entities": ["Alex", "Sam", "StudyGroup", "Library"],
        "graph_memberships": ["temporal", "semantic"],
        "causal_causes": [], "causal_effects": [],
        "semantic_similar": ["E04", "E10", "E17"],
    },
    {
        "id": "E22", "week": 3, "day": "Fri", "time": "11:00pm",
        "speaker": "Alex",
        "content": "Sam hasn't responded since the midterm this morning. Left on read. Anyone heard from him?",
        "entities": ["Alex", "Sam"],
        "graph_memberships": ["temporal", "entity", "causal"],
        "causal_causes": ["E14"],  # His secret accomplished, Sam ghosts
        "causal_effects": ["E23", "E26"],
        "semantic_similar": ["E28"],
    },
    {
        "id": "E23", "week": 3, "day": "Fri", "time": "11:30pm",
        "speaker": "Jordan",
        "content": "Weird — he's not responding to me either. Maybe he's just exhausted from the exam?",
        "entities": ["Jordan", "Sam"],
        "graph_memberships": ["temporal", "entity"],
        "causal_causes": ["E22"],
        "causal_effects": [],
        "semantic_similar": ["E22"],
    },
    {
        "id": "E24", "week": 3, "day": "Sat", "time": "9:00am",
        "speaker": "Maya",
        "content": "I'm thinking about what I saw at the library again. Has anyone checked if the study doc notes we shared are similar to exam questions?",
        "entities": ["Maya", "Sam", "Notes"],
        "graph_memberships": ["temporal", "entity", "semantic"],
        "causal_causes": [], "causal_effects": [],
        "semantic_similar": ["E14", "E12"],
    },
    {
        "id": "E25", "week": 3, "day": "Sat", "time": "10:00am",
        "speaker": "Alex",
        "content": "Oh no. I just checked. Three exam questions matched almost word-for-word what was only in the shared doc. And the doc was editable...",
        "entities": ["Alex", "Notes", "Sam"],
        "graph_memberships": ["temporal", "entity", "causal"],
        "causal_causes": ["E24"],
        "causal_effects": ["E26"],
        "semantic_similar": ["E14"],
    },
    {
        "id": "E26", "week": 3, "day": "Sat", "time": "2:00pm",
        "speaker": "System",
        "content": "Grades posted. Sam scored 97/100 on the midterm. Alex: 61. Jordan: 58. Class average: 64.",
        "entities": ["Sam", "Alex", "Jordan", "ProfChen"],
        "graph_memberships": ["temporal", "entity", "causal"],
        "causal_causes": ["E14", "E22"],
        "causal_effects": ["E27"],
        "semantic_similar": [],
    },
    {
        "id": "E27", "week": 3, "day": "Sat", "time": "3:00pm",
        "speaker": "Jordan",
        "content": "Wait. Sam scored 97?? And he vanished right after?? I feel sick. I introduced him to everyone. I vouched for him.",
        "entities": ["Jordan", "Sam"],
        "graph_memberships": ["temporal", "entity", "causal"],
        "causal_causes": ["E26"],
        "causal_effects": ["E29"],
        "semantic_similar": ["E05"],
    },
    {
        "id": "E28", "week": 3, "day": "Sat", "time": "4:00pm",
        "speaker": "Alex",
        "content": "Sam's Instagram is now private. His Venmo profile is gone. He's scrubbing his presence.",
        "entities": ["Alex", "Sam"],
        "graph_memberships": ["temporal", "entity"],
        "causal_causes": [], "causal_effects": [],
        "semantic_similar": ["E22"],
    },
    {
        "id": "E29", "week": 3, "day": "Sat", "time": "5:00pm",
        "speaker": "Jordan",
        "content": "I just tried calling Sam. Disconnected. He ghosted me too. I was deceived as much as everyone else.",
        "entities": ["Jordan", "Sam"],
        "graph_memberships": ["temporal", "entity"],
        "causal_causes": ["E27"],
        "causal_effects": [],
        "semantic_similar": [],
    },
    {
        "id": "E30", "week": 3, "day": "Sun", "time": "10:00am",
        "speaker": "Maya",
        "content": "I'm going to report what I saw at the library to the Dean of Students. This was academic dishonesty.",
        "entities": ["Maya", "Sam", "ProfChen"],
        "graph_memberships": ["temporal", "entity", "semantic"],
        "causal_causes": [], "causal_effects": [],
        "semantic_similar": ["E14"],
    },
    {
        "id": "E31", "week": 3, "day": "Sun", "time": "2:00pm",
        "speaker": "Alex",
        "content": "We should also report the $80 in Venmo loans. Jordan $50, me $30. He used borrowed trust and borrowed money.",
        "entities": ["Alex", "Jordan", "Sam"],
        "graph_memberships": ["temporal", "entity"],
        "causal_causes": [], "causal_effects": [],
        "semantic_similar": ["E08", "E18"],
    },
    {
        "id": "E32", "week": 3, "day": "Sun", "time": "6:00pm",
        "speaker": "System",
        "content": "Group consensus: Sam systematically exploited the trust network — using Jordan's social capital, the group's notes, and financial goodwill to cheat.",
        "entities": ["Sam", "Jordan", "Alex", "StudyGroup"],
        "graph_memberships": ["temporal", "semantic", "causal"],
        "causal_causes": [],
        "causal_effects": [],
        "semantic_similar": ["E05", "E14", "E22"],
    },
]

# ---------------------------------------------------------------------------
# GRAPH EDGES — Pre-defined for NetworkX construction
# ---------------------------------------------------------------------------

# Semantic: events with similar topics/themes
SEMANTIC_EDGES = [
    ("E01", "E05"), ("E01", "E07"),
    ("E03", "E11"), ("E03", "E12"), ("E03", "E19"),
    ("E04", "E07"), ("E04", "E10"), ("E04", "E17"),
    ("E05", "E06"), ("E05", "E16"),
    ("E08", "E18"),
    ("E09", "E20"),
    ("E10", "E17"), ("E10", "E21"),
    ("E11", "E12"), ("E11", "E19"),
    ("E12", "E24"), ("E12", "E25"),
    ("E14", "E24"), ("E14", "E25"), ("E14", "E30"),
    ("E22", "E28"),
    ("E27", "E05"),
    ("E31", "E08"), ("E31", "E18"),
    ("E32", "E14"),
]

# Temporal: strict chronological chain
TEMPORAL_EDGES = [
    ("E01", "E02"), ("E02", "E03"), ("E03", "E04"), ("E04", "E05"),
    ("E05", "E06"), ("E06", "E07"), ("E07", "E08"), ("E08", "E09"),
    ("E09", "E10"), ("E10", "E11"), ("E11", "E12"), ("E12", "E13"),
    ("E13", "E14"), ("E14", "E15"), ("E15", "E16"), ("E16", "E17"),
    ("E17", "E18"), ("E18", "E19"), ("E19", "E20"), ("E20", "E21"),
    ("E21", "E22"), ("E22", "E23"), ("E23", "E24"), ("E24", "E25"),
    ("E25", "E26"), ("E26", "E27"), ("E27", "E28"), ("E28", "E29"),
    ("E29", "E30"), ("E30", "E31"), ("E31", "E32"),
]

# Causal: cause → effect relationships
CAUSAL_EDGES = [
    ("E05", "E08"),   # Jordan's intro → Sam asks Jordan for money
    ("E05", "E18"),   # Jordan's intro → Sam asks Alex for money (via Jordan vouching)
    ("E08", "E09"),   # Sam asks → Jordan lends
    ("E12", "E14"),   # Group learns notes are valuable → Sam photographs them
    ("E14", "E22"),   # Sam steals notes → Sam disappears after achieving goal
    ("E18", "E20"),   # Sam asks Alex → Alex lends
    ("E22", "E26"),   # Sam disappears → grades reveal unusually high score
    ("E24", "E25"),   # Maya raises alarm → Alex checks shared doc
    ("E25", "E26"),   # Alex confirms tampering → grades reveal
    ("E26", "E27"),   # Grades revealed → Jordan realizes he was deceived
    ("E27", "E29"),   # Jordan's realization → confirms Sam ghosted him too
]

# Entity: tracks each person's appearances across events
ENTITY_EDGES = [
    # Sam's trail
    ("E05", "Sam"), ("E06", "Sam"), ("E07", "Sam"),
    ("E08", "Sam"), ("E13", "Sam"), ("E14", "Sam"),
    ("E18", "Sam"), ("E22", "Sam"), ("E26", "Sam"),
    ("E27", "Sam"), ("E28", "Sam"), ("E29", "Sam"),
    # Jordan's trail
    ("E01", "Jordan"), ("E02", "Jordan"), ("E04", "Jordan"),
    ("E05", "Jordan"), ("E09", "Jordan"), ("E11", "Jordan"),
    ("E16", "Jordan"), ("E23", "Jordan"), ("E27", "Jordan"), ("E29", "Jordan"),
    # Maya's trail
    ("E14", "Maya"), ("E15", "Maya"), ("E24", "Maya"), ("E30", "Maya"),
    # Prof. Chen's trail
    ("E03", "ProfChen"), ("E11", "ProfChen"), ("E12", "ProfChen"),
    ("E13", "ProfChen"), ("E14", "ProfChen"), ("E26", "ProfChen"),
]

# ---------------------------------------------------------------------------
# QUERIES — 4 pre-scripted investigative queries
# ---------------------------------------------------------------------------
QUERIES = [
    {
        "id": "Q1",
        "text": "Why did Sam disappear after the midterm, and who introduced him to the group?",
        "intent": "WHY + WHO",
        "intent_tag": "WHY",
        "primary_graph": "causal",
        "secondary_graph": "entity",
        "graph_explanation": "WHY queries route to the Causal graph first. MAGMA detects a compound question and also activates the Entity graph to trace who introduced Sam.",
        "anchor_nodes": ["E22", "E05"],
        "traversal_path": [
            {
                "step": 1, "node": "E22", "edge": None,
                "description": "Anchor identified: E22 — Sam disappears after midterm",
                "graph": "causal",
            },
            {
                "step": 2, "node": "E14", "edge": ("E14", "E22"),
                "description": "CAUSAL edge ← E14: Sam photographed Prof. Chen's notes (the cause)",
                "graph": "causal",
            },
            {
                "step": 3, "node": "E12", "edge": ("E12", "E14"),
                "description": "CAUSAL edge ← E12: Group learned notes had exam value (motive revealed)",
                "graph": "causal",
            },
            {
                "step": 4, "node": "E26", "edge": ("E22", "E26"),
                "description": "TEMPORAL edge → E26: Sam scores 97/100 — confirms goal achieved",
                "graph": "temporal",
            },
            {
                "step": 5, "node": "E05", "edge": ("E05", "E08"),
                "description": "ENTITY edge → E05: Jordan introduced Sam and vouched for him",
                "graph": "entity",
            },
        ],
        "tokens_used": 1247,
        "baseline_tokens": 101000,
        "magma_answer": (
            "Sam disappeared because he had achieved his goal. He photographed Prof. Chen's private notes [E14], "
            "which gave him insider exam knowledge [E12]. After scoring 97/100 [E26], he had no more use for the group. "
            "Sam was originally introduced by **Jordan** [E05], who vouched for him and later also fell victim — "
            "Jordan lent $50 [E09] and was ghosted as well [E29]. Jordan was deceived, not complicit."
        ),
        "baseline_answer": (
            "I'm not sure why Sam left the group. There were many messages about studying and exams. "
            "It might be related to the midterm, but with so many conversations I can't be certain "
            "of the exact cause. There were also some financial exchanges mentioned at some point..."
        ),
        "correct": True,
    },
    {
        "id": "Q2",
        "text": "When did Sam first ask someone for money?",
        "intent": "WHEN",
        "intent_tag": "WHEN",
        "primary_graph": "temporal",
        "secondary_graph": None,
        "graph_explanation": "WHEN queries route directly to the Temporal graph. MAGMA performs a targeted anchor search for financial exchange events in chronological order.",
        "anchor_nodes": ["E08"],
        "traversal_path": [
            {
                "step": 1, "node": "E08", "edge": None,
                "description": "Temporal anchor: E08 — first financial request event detected",
                "graph": "temporal",
            },
            {
                "step": 2, "node": "E07", "edge": ("E07", "E08"),
                "description": "TEMPORAL edge ← E07: Context — Sam had just earned group's trust via study help",
                "graph": "temporal",
            },
            {
                "step": 3, "node": "E09", "edge": ("E08", "E09"),
                "description": "TEMPORAL edge → E09: Outcome — Jordan lends $50",
                "graph": "temporal",
            },
        ],
        "tokens_used": 423,
        "baseline_tokens": 101000,
        "magma_answer": (
            "Sam first asked for money on **Week 1, Friday at 6:00pm** [E08], just 3 days after being "
            "introduced to the group [E05]. He asked Jordan for $50, citing a textbook expense. "
            "Jordan lent it immediately [E09]. A second request followed in Week 2 [E18], this time targeting Alex ($30)."
        ),
        "baseline_answer": (
            "There were some mentions of money in the chat. I believe there were a couple of Venmo transactions. "
            "I'm not able to precisely determine when the first request was given the volume of messages."
        ),
        "correct": True,
    },
    {
        "id": "Q3",
        "text": "Who witnessed Sam at the library, and what did they see?",
        "intent": "WHO",
        "intent_tag": "WHO",
        "primary_graph": "entity",
        "secondary_graph": None,
        "graph_explanation": "WHO queries route to the Entity graph. MAGMA tracks entity co-occurrences to find which person was co-located with Sam in a library context.",
        "anchor_nodes": ["E14"],
        "traversal_path": [
            {
                "step": 1, "node": "E14", "edge": None,
                "description": "Entity anchor: E14 — library event with multiple entities co-occurring",
                "graph": "entity",
            },
            {
                "step": 2, "node": "Maya", "edge": ("E14", "Maya"),
                "description": "ENTITY edge → Maya: Maya is linked to E14 as an observer",
                "graph": "entity",
            },
            {
                "step": 3, "node": "E24", "edge": ("E14", "E24"),
                "description": "ENTITY edge → E24: Maya resurfaces in E24, raising alarm again",
                "graph": "entity",
            },
            {
                "step": 4, "node": "E30", "edge": ("E14", "E30"),
                "description": "ENTITY edge → E30: Maya takes action — reports to Dean of Students",
                "graph": "entity",
            },
        ],
        "tokens_used": 634,
        "baseline_tokens": 101000,
        "magma_answer": (
            "**Maya** witnessed Sam at Butler Library [E14] on Week 2, Wednesday at 2:30pm. "
            "She saw him in a study carrel next to Prof. Chen, photographing what appeared to be "
            "Chen's handwritten notes. Maya raised the alarm again in E24 after grades were posted, "
            "and ultimately reported the incident to the Dean of Students [E30]."
        ),
        "baseline_answer": (
            "Someone mentioned seeing Sam at the library. I think it was one of the group members. "
            "They said something about notes but I cannot recall who exactly or what they saw precisely."
        ),
        "correct": True,
    },
    {
        "id": "Q4",
        "text": "What was the study group's general attitude toward the midterm?",
        "intent": "WHAT",
        "intent_tag": "WHAT",
        "primary_graph": "semantic",
        "secondary_graph": None,
        "graph_explanation": "WHAT/topic queries route to the Semantic graph. MAGMA clusters events by conceptual similarity to surface a coherent narrative on the midterm theme.",
        "anchor_nodes": ["E03", "E11", "E12", "E19"],
        "traversal_path": [
            {
                "step": 1, "node": "E03", "edge": None,
                "description": "Semantic anchor: E03 — first mention of midterm difficulty",
                "graph": "semantic",
            },
            {
                "step": 2, "node": "E11", "edge": ("E03", "E11"),
                "description": "SEMANTIC edge → E11: Jordan echoes anxiety about Chen's midterm",
                "graph": "semantic",
            },
            {
                "step": 3, "node": "E12", "edge": ("E11", "E12"),
                "description": "SEMANTIC edge → E12: Notes discussion — Chen's private notes flagged as valuable",
                "graph": "semantic",
            },
            {
                "step": 4, "node": "E19", "edge": ("E12", "E19"),
                "description": "SEMANTIC edge → E19: Jordan calls panic mode with 1 week to go",
                "graph": "semantic",
            },
        ],
        "tokens_used": 891,
        "baseline_tokens": 101000,
        "magma_answer": (
            "The group was consistently anxious about the midterm. From Week 1, Alex flagged Prof. Chen's exam "
            "as 'brutal' [E03]. This anxiety grew in Week 2 with Jordan's reminder [E11] and reached peak concern "
            "when Jordan called 'panic mode' one week out [E19]. The group's shared fear of the exam — and their "
            "discussion of Chen's private notes as uniquely valuable [E12] — inadvertently created the conditions "
            "Sam exploited."
        ),
        "baseline_answer": (
            "The group studied together and seemed generally engaged with the course. There were mentions of "
            "the midterm being difficult. They had study sessions multiple times per week."
        ),
        "correct": True,
    },
]

# ---------------------------------------------------------------------------
# ABLATION SCORES — From MAGMA paper Table 4 (LoComo benchmark)
# ---------------------------------------------------------------------------
ABLATION_SCORES = {
    frozenset(["semantic", "temporal", "causal", "entity"]): 0.700,   # Full MAGMA
    frozenset(["temporal", "causal", "entity"]): 0.668,               # w/o semantic
    frozenset(["semantic", "causal", "entity"]): 0.647,               # w/o temporal backbone
    frozenset(["semantic", "temporal", "entity"]): 0.644,             # w/o causal links
    frozenset(["semantic", "temporal", "causal"]): 0.666,             # w/o entity links
    frozenset(["causal", "entity"]): 0.620,
    frozenset(["temporal", "entity"]): 0.610,
    frozenset(["semantic", "entity"]): 0.600,
    frozenset(["semantic", "temporal"]): 0.590,
    frozenset(["semantic", "causal"]): 0.580,
    frozenset(["temporal", "causal"]): 0.570,
    frozenset(["semantic"]): 0.520,
    frozenset(["temporal"]): 0.510,
    frozenset(["causal"]): 0.530,
    frozenset(["entity"]): 0.500,
    frozenset(): 0.481,                                                 # No memory ≈ Full Context baseline
}

# Baseline comparison data (from paper Table 1)
BASELINES = {
    "Full Context": 0.481,
    "A-MEM": 0.580,
    "MemoryOS": 0.553,
    "Nemori": 0.590,
    "MAGMA": 0.700,
}

# Per-category scores for radar chart (from paper Table 1, LoComo)
CATEGORY_SCORES = {
    "Single-hop": {"MAGMA": 0.714, "Nemori": 0.667, "Full Context": 0.571},
    "Multi-hop": {"MAGMA": 0.677, "Nemori": 0.548, "Full Context": 0.484},
    "Temporal": {"MAGMA": 0.710, "Nemori": 0.581, "Full Context": 0.419},
    "Adversarial": {"MAGMA": 0.742, "Nemori": 0.581, "Full Context": 0.205},
    "Conversational": {"MAGMA": 0.677, "Nemori": 0.581, "Full Context": 0.581},
}

# Token usage comparison
TOKEN_STATS = {
    "MAGMA (avg)": 3400,
    "A-MEM": 8200,
    "MemoryOS": 12500,
    "Full Context": 101000,
}

# Graph color scheme
GRAPH_COLORS = {
    "semantic": {"node": "#6C63FF", "edge": "#9D97FF", "label": "Semantic"},
    "temporal": "#00BFA5",
    "causal": "#FF6B6B",
    "entity": "#FFB347",
    "default": "#AAAAAA",
    "highlighted_node": "#FFD700",
    "highlighted_edge": "#FF8C00",
    "visited_node": "#FFA500",
}

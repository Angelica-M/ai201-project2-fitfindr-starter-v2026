"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # Criterion 3 — state. Any query that matches works, since what's
        # being checked is session["selected_item"]["id"] against the id on
        # the dict actually handed to suggest_outfit / create_fit_card, not
        # anything about what the user typed.
        "name": "selected item id persists",
        "query": "90s track jacket in size M",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        # Criterion 4 — the fit card. run_eval.py already runs every scenario
        # five times, so one query that reliably selects the same top item
        # (search is deterministic keyword scoring) gives five independent
        # fit cards for that one item — exactly what "run more than once"
        # needs, without listing the query five times by hand.
        "name": "fit card has required metadata",
        "query": "silk slip dress in midi length under $40",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # Criterion 5 — empty wardrobe. A user with nothing saved, searching
        # for something the data can match, so suggest_outfit actually runs
        # and has to fall back to general advice instead of naming owned
        # pieces. Also doubles as one of unit 4's three failure modes.
        "name": "empty wardrobe gets general advice",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": 5,
    },
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems

"""
All 5 scenarios ran cleanly end-to-end (single-try smoke test, 
not the full 5× eval you'll ask for next) — no crashes, and 
each branch behaved as its criterion expects: criterion 2 
stopped early with `item: None`, criterion 5 correctly 
triggered the "Since this is the very first piece in their 
wardrobe" general-advice path.

**What's in [scenarios.py](scenarios.py) now** — exactly 5 scenarios, 
one per criterion, so the run log's rows line up 1:1 with criteria.md numbering:

| Criterion | Scenario | Query | Wardrobe | Why this shape |
|---|---|---|---|---|
| 1 | `matching query completes` | *(unchanged)* vintage graphic tee under $30 | example | Already shipped correctly — a query the data can match |
| 2 | `impossible query stops early` | *(unchanged)* designer ballgown size XXS under $5 | example | Already shipped correctly — the empty-search branch |
| 3 | `selected item id persists` *(new)* | 90s track jacket in size M | example | Criterion 3 only needs *any* matching query — it's checking `session["selected_item"]["id"]` against what reached `suggest_outfit`/`create_fit_card`, not the query text |
| 4 | `fit card has required metadata` *(new)* | silk slip dress in midi length under $40 | example | One scenario, 5 tries (handled automatically by `run_eval.py`), gives 5 independent fit cards for the *same* selected item — exactly what "same item run more than once" needs |
| 5 | `empty wardrobe gets general advice` *(relabeled)* | *(unchanged)* denim jacket under $50 | empty | The scenario that shipped as a `criterion: None` diagnostic already does exactly what criterion 5 asks — a matching query with an empty wardrobe — so I pointed its `criterion` at 5 instead of adding a duplicate |

No full `run_eval.py --label before` run was done — that's the 
actual test you said you'd ask for next. This was just 
wiring + a single-try sanity check to confirm the scenarios 
execute without error before you spend real tries on them.
"""
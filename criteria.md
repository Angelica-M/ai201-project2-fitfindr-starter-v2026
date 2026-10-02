# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->
I picked 4 of 5 because `search_listings` relies on plain keyword overlap scoring; natural phrasing variations or specific user synonyms might fail to overlap with dataset terms and return zero matches, causing an intentional early stop.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->
This target is 5 of 5 because empty-state branching is controlled by a deterministic Python conditional check (`if not listings:`) in the loop rather than an LLM decision, making failure on an empty search result an unambiguous code defect.

---

## 3. Selected item ID persists across tool calls
<!-- YOU WRITE THIS ONE. Something about state.
     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.
     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->
When `search_listings` returns results, the item ID stored in `session["selected_item"]["id"]` matches the `id` field of the `new_item` dictionary passed into both `suggest_outfit` and `create_fit_card` — in 5 of 5 tries.

**Why this target:**
State persistence between tools is handled by deterministic Python dict assignments inside the agent loop (`session["selected_item"] = results[0]`), so any discrepancy between what search selected and what subsequent tools received represents a critical data-flow bug that should never occur.

---

## 4. Fit card contains required metadata and valid length
<!-- YOU WRITE THIS ONE. Something about the fit card.
     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?
     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->
Given a valid outfit suggestion and listing input, `create_fit_card` returns a 2-to-4 sentence caption that explicitly mentions the item's title, price, and platform — in at least 4 of 5 tries.

**Why this target:**
I picked 4 of 5 because `create_fit_card` relies on generative LLM output with `TEMPERATURE > 0.0`; while prompt engineering enforces sentence count and metadata inclusion, occasional stochastic variations in model output may omit a required field or alter sentence formatting.

---

## 5. Empty wardrobe triggers general styling advice
<!-- YOU WRITE THIS ONE TOO. Your choice.
     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->
Given a valid item listing and an empty wardrobe dictionary (`{"items": []}`), `suggest_outfit` returns a non-empty string containing general styling advice without raising an error or returning an empty string — in 5 of 5 tries.

**Why this target:**
This is set to 5 of 5 because checking `if not wardrobe.get("items"):` is a deterministic code branch in `suggest_outfit` executed prior to formatting the prompt, guaranteeing that the empty wardrobe prompt path is selected every single time.

---


<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

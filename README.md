# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does
<!-- Three or four sentences: what a user asks for, and what they get back. -->



---

## Tool Inventory
<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them. "Returns a list" earns NOTHING. The 
     description has to say what is IN the list. The empty case isn't 
     optional either — it's the thing your loop branches on, and if you 
     don't decide it here you'll discover it as a crash in Milestone 5. 
     Ensure that name and type each: `max_price` (float), not "a price". -->
### Architectural Rationale: Specifying Tools Before Implementation

Defining the explicit interface contracts for `tools.py` before writing implementation code is essential because agent loops rely on deterministic return types to make control-flow decisions. When a tool returns ambiguous, poorly typed, or variable structures (such as returning `None` instead of `[]` on an empty search, or raising unhandled exceptions), the agent loop cannot branch reliably, resulting in unhandled exceptions or infinite execution loops. Establishing explicit function signatures, dictionary schemas, empty-state return values, and branching rules ensures that the agent can evaluate tool outputs programmatically without guessing.

### Tool Inventory: `search_listings`

- **What it does:** Search the dataset for thrift listings that match a keyword description, while applying optional size and price filters.
- **Inputs:** The inputs for `search_listings` are `description` of type `str` (required search keywords), `size` of type `str | None` (optional size string to filter by, defaulting to `None`), and `max_price` of type `float | None` (optional maximum price ceiling, inclusive, defaulting to `None`).
- **What it returns, specifically:** It returns a `list[dict]` containing at most `config.SEARCH_RESULT_LIMIT` listing dictionaries sorted in descending order by keyword match score. Each dictionary in the list contains the following fields: `id` (`str`), `title` (`str`), `description` (`str`), `category` (`str`), `style_tags` (`list[str]`), `size` (`str`), `condition` (`str`), `price` (`float`), `colors` (`list[str]`), `brand` (`str | None`), and `platform` (`str`).
- **What it returns when it has nothing to give:** It returns an empty list `[]` when no items match the filter criteria or score above zero, never returning `None` or raising an exception.

### Tool Inventory: `suggest_outfit`

- **What it does:** Suggest one or two outfit combinations by pairing a selected thrift item with pieces from the user's wardrobe using the language model.
- **Inputs:** The inputs for `suggest_outfit` are `new_item` of type `dict` (a single listing dictionary containing fields like `title`, `category`, `style_tags`, `colors`, and `brand`) and `wardrobe` of type `dict` (a dictionary containing an `'items'` key whose value is a list of wardrobe item dictionaries, each with `id`, `name`, `category`, `colors`, `style_tags`, and `notes`).
- **What it returns, specifically:** It returns a non-empty `str` containing model-generated outfit suggestions that explicitly reference specific clothing items owned by the user in their `wardrobe['items']` list.
- **What it returns when it has nothing to give:** When `wardrobe['items']` is an empty list, it returns a non-empty `str` containing general styling advice for `new_item` instead of returning `""` or raising an exception.

### Tool Inventory: `create_fit_card`

- **What it does:** Generate a short social media post caption for a thrift find based on an outfit recommendation and item details.
- **Inputs:** The inputs for `create_fit_card` are `outfit` of type `str` (the outfit suggestion text produced by `suggest_outfit`) and `new_item` of type `dict` (the listing dictionary for the target item).
- **What it returns, specifically:** It returns a `str` containing a two-to-four sentence caption written like an authentic social media post that mentions `new_item['title']`, `new_item['price']`, `new_item['platform']` once each, and captures the specific aesthetic vibe of the find.
- **What it returns when it has nothing to give:** If `outfit` is empty or consists only of whitespace, it returns a descriptive fallback `str` message stating that an outfit pairing was missing, rather than raising an exception or returning an empty string.

---

### Agent Loop Branching Rule

If `search_listings` returns an empty list, put a message in the session and stop. Otherwise, take the first result and go to `suggest_outfit`.

---

### Specification Audit

Could someone else build these tools from what was written without asking any questions? Yes, because every function contract explicitly specifies exact Python primitive and container types, full dictionary schema keys, boundary filtering behavior (such as non-substring size matching and max price inclusivity), empty-state default returns, and explicit fallback execution paths for LLM prompts.

---

### Milestone Commitment

All three tools in `tools.py` now have fully typed inputs, explicitly specified return structures down to individual dictionary fields, deterministic empty-state return rules, and a locked control-flow rule for the agent loop.

---

## Planning Loop
<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.
     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent
     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->

**What moves through the session:** <!-- which fields, in what order -->

---

## Sample Run
<!-- Two things go here.
     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

```

**The three tools, tested one at a time**

### Testing Tool 1 (search_listings): 

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
```
Terminal Output: 
```
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]
```

### Testing Tool 2 (suggest_outfit): 

```
$ python -c "from tools import suggest_outfit; ..."
```
```
     python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
```
Terminal Output: 
```
Here are two outfit suggestions that seamlessly integrate the vintage Levi's 501 jeans into their existing wardrobe:

### Outfit 1: Effortless Streetwear Casual
* **The Vibe:** Relaxed, balanced, and everyday-ready. 
* **The Look:** Pair the mid-wash Levi's 501s with the **White ribbed tank top** tucked in to define the waist. Layer the **Vintage black denim jacket** over top for a classic denim-on-denim look with contrasting washes. Finish the fit with the **Chunky white sneakers**, the **Brown leather belt**, and the **Black crossbody bag**. 

### Outfit 2: Cozy Contrast
* **The Vibe:** Comfortable proportions with a hint of grunge edge.
* **The Look:** Wear the Levi's 501s with the **Oversized grey crewneck sweatshirt**. Because the crewneck is very oversized and drops below the hip, doing a "half-tuck" into the front of the jeans will add shape while keeping that cozy, slouchyfeel. Pair with the **Black combat boots** to ground the look, accented by the **Brown leather belt** and the **Black crossbody bag**.
```

### Testing Tool 3 (create_fit_card): 

```
$ python -c "from tools import create_fit_card; ..."
```
```
     python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
```
Terminal Output: 
```
Found these broken-in vintage Levi's 501 jeans on Depop for $38 and my closet has never looked better. They have that 90s slouch that no brand-new pair can ever quite get right, so I'm styling them today with crisp white sneakers for running errands.
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before
<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses
<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement
<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**
<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken
<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

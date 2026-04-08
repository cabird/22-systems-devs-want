# Survey Analysis Methodology

## Research Goal

This analysis identifies **high-impact opportunities for AI-powered developer tools** based on survey data from 860 software developers. The goal is to surface actionable research directions that the software engineering community can pursue.

**High impact means:**
- Affects many developers (prevalence in responses)
- Addresses unmet needs (high preference, low current usage)
- Targets automation-friendly tasks (high cognitive demand, low professional identity)
- Has clear success criteria (measurable improvement possible)

This analysis is **domain-agnostic** — we let the data speak for itself rather than filtering through any particular team's lens. All categories of AI tooling (code generation, testing, documentation, operations, design assistance, etc.) are equally valid if the evidence supports them.

---

## Data Source

Survey: **"AI Where It Matters: Where, Why, and How Developers Want AI Support in Daily Work"** (Choudhuri et al., 2025)

- 860 Microsoft developers surveyed
- Each respondent answered about 2-3 task categories
- Data captures task appraisals (value, identity, accountability, demands), AI preferences, current AI usage, and open-ended responses

---

## Categories to Analyze

| Category | File | Respondents | Tasks |
|----------|------|-------------|-------|
| Infrastructure & Ops | `infrastructure_ops.csv` | 283 | DevOps/CI/CD, Environment Setup, Monitoring, Customer Support |
| Quality & Risk | `quality_risk.csv` | 401 | Testing & QA, Code Review/PRs, Security & Compliance |
| Meta-Work | `meta_work.csv` | 532 | Documentation, Communication, Mentoring, Learning, Research |
| Design & Planning | `design_planning.csv` | 548 | System Architecture, Requirements, Project Planning |
| Development | `development.csv` | 816 | Coding, Bug Fixing, Performance Optimization, Refactoring, AI Development |

---

## Multi-Model Thematic Analysis Approach

To ensure rigor and reduce single-model bias, we use **three LLM families** as independent coders, plus **human author review**:

| Model | Family | Role |
|-------|--------|------|
| GPT-5.2 | OpenAI | Independent theme discovery & coding |
| Gemini-3-Pro | Google | Independent theme discovery & coding |
| Claude Opus 4.5 | Anthropic | Independent theme discovery & coding (via subagent) |
| Human Authors | — | Theme validation, refinement, and final approval |

### Why Three Models?

1. **Reduced bias**: No single model's training data or tendencies dominate
2. **Inter-rater reliability**: We can calculate agreement statistics (Krippendorff's α or Fleiss' κ)
3. **Academic rigor**: Multi-coder approaches are standard in qualitative research
4. **Reproducibility**: Documented models, prompts, and agreement levels

---

## Analysis Process Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 1: Quantitative Analysis                                             │
│  - Calculate task metrics from CSV (demand, identity, AI preference, usage) │
│  - Extract open-ended responses with PIDs                                   │
│  Output: {category}_quantitative.json, {category}_responses.json            │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 2: Independent Theme Discovery (3 Models)                            │
│  - Each model independently proposes themes from "want AI help" responses   │
│  - Each model independently identifies constraints from "do NOT want"       │
│  - Generate interactive HTML review page                                    │
│  Output: {category}_themes_gpt.json                                         │
│          {category}_themes_gemini.json                                      │
│          {category}_themes_opus.json                                        │
│          {category}_review.html          (interactive review page)          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 3: Theme Reconciliation + Human Review                **HUMAN STEP** │
│  - Author opens {category}_review.html in browser                           │
│  - Reviews themes, reads sample responses, marks actions (keep/merge/etc)   │
│  - Clicks "Copy" at bottom, pastes output back to Claude                    │
│  - Claude parses review and generates final codebook                        │
│  Output: {category}_codebook_final.json   (after human review)              │
│          {category}_human_review_notes.md (changes & rationale)             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 4: Systematic Coding (3 Models against Unified Codebook)             │
│  - Each model codes EVERY response against the finalized codebook           │
│  - Output format: {pid, assigned_themes[]}                                  │
│  Output: {category}_coding_gpt.json                                         │
│          {category}_coding_gemini.json                                      │
│          {category}_coding_opus.json                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 5: Inter-Rater Reliability Calculation                               │
│  - Calculate Krippendorff's Alpha (α) or Fleiss' Kappa (κ)                  │
│  - Report agreement levels per theme and overall                            │
│  - Flag themes with low agreement for human adjudication (optional)         │
│  Output: {category}_irr_report.json                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 6: Final Analysis Assembly                                           │
│  - Use majority vote or consensus for final theme assignments               │
│  - Rank themes by prevalence × quantitative signals                         │
│  - Build top 5 research opportunity cards                                   │
│  - Attach constraints from "do NOT want" responses                          │
│  Output: {category}_analysis.json (final output)                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Quantitative Analysis

### Step 1.1: Understand the Category Structure

Read `DATA_DICTIONARY.md` to identify:
- What tasks are in this category
- Which columns map to which questions
- The open-ended question column numbers

### Step 1.2: Calculate Quantitative Signals

For each task in the category, compute these metrics from the CSV:

```python
# Response value mappings
demand_identity_map = {
    'Strongly disagree': 1, 'Disagree': 2, 'Neither agree nor disagree': 3,
    'Agree': 4, 'Strongly agree': 5, "I don't do this task / N.A.": None
}
preference_map = {'None': 1, 'Low': 2, 'Medium': 3, 'Moderate': 3, 'High': 4, 'Very High': 5}
usage_map = {
    'Never': 1, 'A few times a month': 2, '1-3 days a week': 3,
    'A few times a day': 4, 'Many times a day': 5
}

# Metrics to calculate per task
avg_demand = mean(task_demand_column)  # Cognitive load
avg_identity = mean(task_identity_column)  # Enjoyment/professional identification
avg_ai_preference = mean(ai_preference_column)  # Desired AI support
avg_ai_usage = mean(ai_usage_column)  # Current AI usage frequency

# Derived metrics
automation_sweet_spot = ((avg_demand - 1) / 4 + (5 - avg_identity) / 4) / 2  # 0-1 scale
preference_usage_gap = avg_ai_preference - avg_ai_usage  # Higher = more unmet need
pct_want_high_support = percentage responding 'High' or 'Very High' to AI preference
```

**Important:** Strip whitespace from column values (e.g., `'High '` -> `'High'`). The AI Preference columns may contain "Moderate" which should map to 3 (same as "Medium").

### Step 1.3: Extract Open-Ended Responses with PIDs

```python
# For "Where do you want AI help" question
want_ai_responses = [
    {"pid": row['PID'], "quote": row['Q_WANT_AI_COLUMN'].strip()}
    for row in csv_reader
    if row['Q_WANT_AI_COLUMN'].strip() and row['Q_WANT_AI_COLUMN'].strip() != '.'
]

# For "What do you NOT want AI to handle" question
do_not_want_responses = [
    {"pid": row['PID'], "quote": row['Q_NOT_WANT_COLUMN'].strip()}
    for row in csv_reader
    if row['Q_NOT_WANT_COLUMN'].strip() and row['Q_NOT_WANT_COLUMN'].strip() != '.'
]
```

---

## Phase 2: Independent Theme Discovery

Each of the three models independently analyzes the responses and proposes themes.

### Prompt Template for Theme Discovery

```
You are analyzing open-ended survey responses from software developers about where they
want AI assistance in their work. Your task is to identify themes in these responses.

Guidelines for theme creation:
- Themes should be SPECIFIC and ACTIONABLE (e.g., "Automated test generation for edge cases"
  not just "Testing")
- Themes should be PROBLEM-FOCUSED (describe the pain point, not a specific solution)
- A response can belong to MULTIPLE themes
- Aim for 8-15 themes that capture the major patterns

For each response, return:
{
  "pid": <participant ID>,
  "themes": ["theme_code_1", "theme_code_2", ...]
}

Also provide a theme codebook:
{
  "theme_code": {
    "name": "Human-readable theme name",
    "description": "What this theme captures",
    "example_keywords": ["keyword1", "keyword2"]
  }
}

RESPONSES TO ANALYZE:
[Include all responses here]
```

### Models Used

| Model | How Invoked |
|-------|-------------|
| GPT-5.2 | `mcp__pal__chat` with `model: "gpt-5.2"` |
| Gemini-3-Pro | `mcp__pal__chat` with `model: "gemini-3-pro-preview"` |
| Claude Opus | Task subagent with `model: "opus"` |

---

## Phase 3: Theme Reconciliation + Human Review

### Step 3.1: Generate Interactive Review Page

After collecting themes from all three models, generate an **interactive HTML review page**:

**File:** `{category}_review.html`

This HTML page (pure HTML + vanilla JavaScript, no dependencies) provides:

1. **Theme Cards** — For each proposed theme:
   - Theme name and description
   - Which models proposed it (GPT / Gemini / Opus)
   - Response count and percentage
   - Sample responses (3-5 quotes, expandable to show more)
   - **Action controls:**
     - Keep (default)
     - Rename (with new name input)
     - Merge with other themes (multi-select)
     - Split into multiple themes (with new names)
     - Remove (with rationale)
   - Notes field for reviewer comments

2. **New Theme Section** — Add themes the models missed

3. **General Notes** — Overall observations text area

4. **Aggregated Output Panel** — Live-updating text block that collects all actions/notes:
   - "Copy to Clipboard" button
   - Structured format that can be pasted back to Claude

### Step 3.2: Human Author Review **← REQUIRED HUMAN STEP**

The author opens `{category}_review.html` in a browser and reviews:

**Review checklist:**
- [ ] Read sample responses for each theme (at least 3-5 per theme)
- [ ] Are themes specific enough? Too granular? Missing patterns?
- [ ] Mark actions: Keep / Rename / Merge / Split / Remove
- [ ] Add notes explaining any changes
- [ ] Add any new themes the models missed
- [ ] Add general observations

**When done:**
1. Click "Copy to Clipboard" at the bottom of the page
2. Paste the output into the chat with Claude
3. Claude parses the output and generates the final codebook

### Step 3.3: Review Output Format

The HTML page generates structured text like this:

```
=== HUMAN REVIEW: infrastructure_ops ===
Date: 2026-02-17
Reviewer: [name]

ACTIONS:
- KEEP: incident_rca
- RENAME: log_analysis → cross_service_log_correlation
  Note: "More specific about the actual pain point"
- MERGE: env_setup, env_maintenance → environment_management
  Note: "These are really the same thing"
- SPLIT: automation → deployment_automation, pipeline_automation
  Note: "Distinct concerns"
- REMOVE: generic_ai_help
  Note: "Too vague, covered by other themes"

NEW THEMES:
- on_call_burden: "Reducing cognitive load during on-call"
  Note: "Several responses mentioned this specifically"

GENERAL NOTES:
[Overall observations from the reviewer]
```

### Step 3.4: Generate Final Codebook

After receiving the human review output, Claude:
1. Parses the actions and applies them to create `{category}_codebook_final.json`
2. Extracts notes into `{category}_human_review_notes.md`
3. Documents any ambiguities or questions

### Step 3.5: Approval Gate

**Do not proceed to Phase 4 until the final codebook is confirmed.**

---

## Phase 4: Systematic Coding

Once the codebook is finalized, all three models re-code every response against the unified codebook.

### Prompt Template for Systematic Coding

```
You are coding survey responses against a predefined codebook. For each response,
assign ALL themes that apply from the codebook below. Do not create new themes.

CODEBOOK:
[Insert finalized codebook here]

For each response, return:
{
  "pid": <participant ID>,
  "assigned_themes": ["theme_code_1", "theme_code_2", ...]
}

If no themes apply, return an empty array.

RESPONSES TO CODE:
[Include all responses here]
```

### Output Format

Each model produces:
```json
{
  "model": "gpt-5.2",
  "coding_date": "2026-02-17",
  "codebook_version": "final",
  "codings": [
    {"pid": 123, "assigned_themes": ["incident_rca", "log_correlation"]},
    {"pid": 456, "assigned_themes": ["deployment_automation"]},
    ...
  ]
}
```

---

## Phase 5: Inter-Rater Reliability

### Metrics to Calculate

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **Percent Agreement** | (# agreements) / (# total) | Simple baseline, doesn't account for chance |
| **Fleiss' Kappa (κ)** | Accounts for chance agreement with 3+ raters | κ > 0.8 = excellent, 0.6-0.8 = substantial |
| **Krippendorff's Alpha (α)** | Handles missing data, multiple raters | α > 0.8 = reliable, 0.667-0.8 = tentative |

### Calculating Agreement for Multi-Label Coding

Since each response can have multiple themes, we calculate agreement per-theme:

For each theme T:
- For each response, each model votes "present" or "absent"
- Calculate Fleiss' κ across the 3 raters for theme T
- Report overall κ as the average across themes (or weighted by prevalence)

### Handling Disagreements

Options for resolving disagreements:
1. **Majority vote**: Theme assigned if 2+ models agree
2. **Consensus required**: Theme assigned only if all 3 models agree
3. **Human adjudication**: Author reviews responses with low agreement (optional)

Document which approach was used.

### Output

```json
{
  "category": "infrastructure_ops",
  "n_responses": 150,
  "n_themes": 12,
  "overall_fleiss_kappa": 0.73,
  "overall_krippendorff_alpha": 0.75,
  "per_theme_agreement": {
    "incident_rca": {"kappa": 0.85, "agreement_pct": 92},
    "deployment_automation": {"kappa": 0.78, "agreement_pct": 88},
    ...
  },
  "low_agreement_themes": ["theme_with_kappa_below_0.6"],
  "resolution_method": "majority_vote"
}
```

---

## Phase 6: Final Analysis Assembly

### Step 6.1: Determine Final Theme Assignments

Using the chosen resolution method (majority vote, consensus, etc.), determine which themes are assigned to each response.

### Step 6.2: Calculate Theme Prevalence

For each theme:
- Count of responses assigned to this theme
- Percentage of total responses
- List of PIDs and verbatim quotes

### Step 6.3: Rank Themes for Research Opportunities

Combine signals:
- **Prevalence** (affects many developers)
- **Preference-usage gap** (unmet need in quantitative data)
- **Automation sweet spot** (high demand, low identity tasks)

### Step 6.4: Build Top 5 Research Opportunity Cards

For each of the top 5 themes:
- **Problem statement** (1 clear sentence)
- **Who it affects** (prevalence + quantitative signals + supporting quotes with PIDs)
- **Impact** (what would change if solved)
- **Proposed capability** (summary + required context/data sources)
- **Constraints and guardrails** (from "do NOT want" responses)
- **Success definition** (qualitative and quantitative measures)

### Step 6.5: Build Constraint Map

From the "do NOT want" responses:
- **No-go zones** — categories of actions AI must not do autonomously
- **Design principles** — how AI tools should behave based on developer concerns

---

## Key Column Mappings by Category

### infrastructure_ops.csv
- **Tasks:** DevOps/CI/CD (1), Environment Setup (2), Monitoring (3), Customer Support (4)
- **Want AI Help:** Q76
- **Do NOT Want:** Q78
- **AI Preference:** Q75_1, Q75_2, Q75_3, Q75_4
- **AI Usage:** Q77_1, Q77_2, Q77_3, Q77_4
- **Task Demand:** Q74_1, Q74_2, Q74_3, Q74_4
- **Task Identity:** Q72_1, Q72_2, Q72_3, Q72_4

### quality_risk.csv
- **Tasks:** Testing & QA (1), Code Review/PRs (2), Security & Compliance (3)
- **Want AI Help:** Q52
- **Do NOT Want:** Q54
- **AI Preference:** Q51_1, Q51_2, Q51_3
- **AI Usage:** Q53_1, Q53_2, Q53_3
- **Task Demand:** Q50_1, Q50_2, Q50_3
- **Task Identity:** Q48_1, Q48_2, Q48_3

### design_planning.csv
- **Tasks:** System Architecture (1), Requirements Gathering (2), Project Planning (3)
- **Want AI Help:** Q64
- **Do NOT Want:** Q66
- **AI Preference:** Q63_1, Q63_2, Q63_3
- **AI Usage:** Q65_1, Q65_2, Q65_3
- **Task Demand:** Q62_1, Q62_2, Q62_3
- **Task Identity:** Q60_1, Q60_2, Q60_3

### development.csv
- **Tasks:** Coding (1), Bug Fixing (2), Perf Optimization (3), Refactoring (4), AI Development (5)
- **Want AI Help:** Q17
- **Do NOT Want:** Q19
- **AI Preference:** Q16_1, Q16_2, Q16_3, Q16_4, Q16_5
- **AI Usage:** Q18_1, Q18_2, Q18_3, Q18_4, Q18_5
- **Task Demand:** Q15_1, Q15_2, Q15_3, Q15_4, Q15_5
- **Task Identity:** Q13_1, Q13_2, Q13_3, Q13_4, Q13_5

### meta_work.csv
- **Tasks:** Documentation (1), Communication (2), Mentoring (3), Learning (4), Research (5)
- **Want AI Help:** Q88
- **Do NOT Want:** Q90
- **AI Preference:** Q87_1, Q87_2, Q87_3, Q87_4, Q87_5
- **AI Usage:** Q89_1, Q89_2, Q89_3, Q89_4, Q89_5
- **Task Demand:** Q86_1, Q86_2, Q86_3, Q86_4, Q86_5
- **Task Identity:** Q84_1, Q84_2, Q84_3, Q84_4, Q84_5

---

## Output Files Per Category

### Phase 1 Outputs
- `{category}_quantitative.json` — task-level metrics
- `{category}_responses.json` — extracted open-ended responses with PIDs

### Phase 2 Outputs
- `{category}_themes_gpt.json` — GPT-5.2 theme discovery
- `{category}_themes_gemini.json` — Gemini-3-Pro theme discovery
- `{category}_themes_opus.json` — Claude Opus theme discovery
- `{category}_review.html` — Interactive HTML review page for human review

### Phase 3 Outputs
- `{category}_codebook_final.json` — human-approved codebook (after review)
- `{category}_human_review_notes.md` — documentation of human changes

### Phase 4 Outputs
- `{category}_coding_gpt.json` — GPT-5.2 systematic coding
- `{category}_coding_gemini.json` — Gemini-3-Pro systematic coding
- `{category}_coding_opus.json` — Claude Opus systematic coding

### Phase 5 Outputs
- `{category}_irr_report.json` — inter-rater reliability statistics

### Phase 6 Outputs
- `{category}_analysis.json` — final analysis with top 5 research opportunities

---

## Final JSON Output Schema

```json
{
  "metadata": {
    "category": "string - e.g., 'Infrastructure & Ops'",
    "csv_file": "string - e.g., 'infrastructure_ops.csv'",
    "respondent_count": "integer - total rows in CSV",
    "open_ended_response_counts": {
      "want_ai_help": "integer - non-empty responses",
      "do_not_want": "integer - non-empty responses"
    },
    "analysis_date": "string - YYYY-MM-DD",
    "methodology": {
      "models_used": ["GPT-5.2", "Gemini-3-Pro", "Claude Opus 4.5"],
      "human_reviewers": ["Author 1", "Author 2"],
      "resolution_method": "majority_vote | consensus | human_adjudicated",
      "inter_rater_reliability": {
        "fleiss_kappa": "float",
        "krippendorff_alpha": "float"
      }
    }
  },

  "quantitative_summary": {
    "tasks": [
      {
        "task_name": "string",
        "avg_demand": "float - 1.0 to 5.0",
        "avg_identity": "float - 1.0 to 5.0",
        "avg_ai_preference": "float - 1.0 to 5.0",
        "avg_ai_usage": "float - 1.0 to 5.0",
        "automation_sweet_spot": "float - 0.0 to 1.0",
        "preference_usage_gap": "float",
        "pct_want_high_support": "integer - 0 to 100"
      }
    ]
  },

  "theme_codebook": {
    "theme_code": {
      "name": "string - human-readable name",
      "description": "string - what this theme captures",
      "human_modified": "boolean - true if authors changed this theme",
      "modification_notes": "string - what was changed (if applicable)"
    }
  },

  "top_research_opportunities": [
    {
      "rank": "integer - 1 to 5",
      "theme_code": "string - from codebook",
      "opportunity_name": "string - short descriptive name",
      "problem_statement": "string - 1 clear sentence",

      "who_it_affects": {
        "prevalence_count": "integer",
        "prevalence_pct": "float",
        "model_agreement": {
          "gpt": "integer - count",
          "gemini": "integer - count",
          "opus": "integer - count",
          "consensus": "integer - count after resolution"
        },
        "supporting_responses": [
          {"pid": "integer", "quote": "string"}
        ]
      },

      "impact": {
        "description": "string",
        "supporting_quotes": [{"pid": "integer", "quote": "string"}]
      },

      "proposed_capability": {
        "summary": "string",
        "required_context": ["string - data sources needed"],
        "capability_steps": ["string - step 1", "string - step 2"]
      },

      "constraints_and_guardrails": [
        {
          "constraint": "string",
          "pid": "integer",
          "quote": "string"
        }
      ],

      "success_definition": {
        "qualitative_measures": ["string"],
        "quantitative_measures": ["string"]
      }
    }
  ],

  "constraint_map": {
    "no_go_zones": [
      {
        "zone_name": "string",
        "prevalence_count": "integer",
        "description": "string",
        "supporting_responses": [{"pid": "integer", "quote": "string"}]
      }
    ],
    "design_principles": [
      {
        "principle": "string",
        "rationale": "string",
        "implementation_guidance": "string"
      }
    ]
  }
}
```

---

## For the Paper: Methods Section Language

Example text for the methodology section:

> **Thematic Analysis.** Open-ended responses were analyzed using a multi-model thematic
> analysis approach. Three large language models from different families (GPT-5.2,
> Gemini-3-Pro, and Claude Opus 4.5) independently generated initial theme codebooks
> from the response data. These codebooks were merged algorithmically, then reviewed
> and refined by the authors, who read sample responses for each theme and made
> adjustments for clarity and completeness (documented in supplementary materials).
>
> The finalized codebook was then used for systematic coding, where all three models
> independently assigned themes to each response. Inter-rater reliability was calculated
> using Krippendorff's alpha (α = X.XX) and Fleiss' kappa (κ = X.XX), indicating
> [excellent/substantial/moderate] agreement. Final theme assignments were determined
> by majority vote across the three models.

---

## Citation

```
Choudhuri, R., Badea, C., Bird, C., Butler, J.L., DeLine, R., & Houck, B. (2025).
AI Where It Matters: Where, Why, and How Developers Want AI Support in Daily Work.
```

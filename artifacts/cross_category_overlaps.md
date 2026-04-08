# Cross-Category Theme Overlaps

**Status: RESOLVED** (2026-02-18)

See `consolidated_codebook.json` for the full implementation.

---

## Summary of Decisions

### Universal Principles (Extracted from Categories)

Two "boundary themes" were elevated to **cross-cutting universal principles** that apply to all AI tooling:

| Theme | Original Category | Decision |
|-------|-------------------|----------|
| `human_oversight_reliability` | Development | Moved to `cross_cutting_principles` |
| `human_ownership_trust` | Design & Planning | Moved to `cross_cutting_principles` |

**Rationale:** Low IRR (α=0.444-0.759) reflects their subjective nature. These aren't discrete themes to code; they're design constraints that apply universally.

**Combined into:**
- `human_oversight_required` - AI must support, not replace, human decision-making
- `ai_reliability_transparency` - Trust requires visibility into AI reasoning

---

## Overlap Resolutions

### 1. Debugging / Root Cause Analysis
- `debugging_runtime_analysis` (Development)
- `debugging_rca` (Quality & Risk)
- `incident_response_rca` (Infrastructure & Ops)

**Decision:** Documented as `cross_cutting_capability` called `debugging_root_cause_analysis`

**Rationale:** Same underlying capability (tracing issues to root causes) appears across the software lifecycle. This is a strong signal that a unified debugging/RCA AI capability would have broad impact.

---

### 2. Test Generation
- `test_generation_coverage` (Development)
- `test_generation_coverage` (Quality & Risk)

**Decision:** Keep separate in category analysis; acknowledge as cross-cutting capability

**Rationale:** Same code name already reflects same capability. Context differs (during dev vs. QA phase) but the underlying AI capability is identical.

---

### 3. Documentation
- `documentation_artifacts` (Design & Planning) - design docs, specs, diagrams
- `documentation_automation` (Meta-Work) - code docs, READMEs, API docs

**Decision:** Keep separate; acknowledge as cross-cutting capability

**Rationale:** Distinct artifact types with different inputs and outputs. Design docs come from requirements/discussions; code docs come from code analysis.

---

### 4. Codebase Understanding
- `codebase_comprehension` (Development) - understanding code to modify it
- `codebase_system_understanding` (Design & Planning) - understanding code for design decisions

**Decision:** Keep separate; acknowledge as cross-cutting capability

**Rationale:** Same underlying need but different purposes. The capability could be unified but the use cases are distinct enough to warrant separate themes.

---

### 5. Task/Project Planning
- `task_management` (Meta-Work) - day-to-day prioritization, tracking
- `task_project_automation` (Design & Planning) - strategic work breakdown, estimation

**Decision:** Keep separate; acknowledge as cross-cutting capability

**Rationale:** Tactical vs. strategic planning have different workflows and stakeholders.

---

## Impact on Theme Counts

| Category | Original | After Consolidation |
|----------|----------|---------------------|
| design_planning | 6 | 5 |
| development | 7 | 6 |
| quality_risk | 7 | 7 |
| infrastructure_ops | 6 | 6 |
| meta_work | 7 | 7 |
| **Total Category Themes** | **33** | **31** |
| Cross-Cutting Principles | 0 | 2 |
| Cross-Cutting Capabilities | 0 | 5 |

---

## For the Paper

Suggested language for methods section:

> We identified five capabilities that emerged across multiple categories: debugging/RCA,
> test generation, documentation, codebase understanding, and task planning. Rather than
> artificially forcing these into single categories, we documented them as cross-cutting
> capabilities with context-specific manifestations. Additionally, we extracted two
> boundary themes expressing human oversight requirements and elevated them to universal
> design principles, reflecting their role as constraints on AI autonomy rather than
> discrete feature requests.

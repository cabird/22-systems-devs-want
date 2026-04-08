# Survey Data Dictionary

## Overview

This directory contains survey response data from the study **"AI Where It Matters: Where, Why, and How Developers Want AI Support in Daily Work"** (Choudhuri et al., 2025). The study surveyed **860 software developers** at Microsoft to understand:

1. How developers appraise different aspects of their work (value, identity, accountability, demands)
2. Their openness to and current use of AI tools for various tasks
3. Which Responsible AI (RAI) principles they prioritize for AI-enabled developer tools

## File Structure

The data is split into **5 CSV files**, one per task category. Each respondent answered questions about 2-3 categories, so the same respondent may appear in multiple files.

| File | Respondents | Description |
|------|-------------|-------------|
| `development.csv` | 816 | Core coding and development tasks |
| `design_planning.csv` | 548 | System design, requirements, project management |
| `quality_risk.csv` | 401 | Testing, code review, security/compliance |
| `infrastructure_ops.csv` | 283 | DevOps, environment setup, monitoring, support |
| `meta_work.csv` | 532 | Documentation, communication, mentoring, learning |

**Note on meta_work.csv**: This category was automatically shown to respondents who selected only 2 of the 4 main categories. 54 respondents in this file have no data in the category-specific columns (they may have dropped out before completing this section).

---

## Common Columns (All Files)

These columns appear in every CSV file and contain demographic/background information.

### Respondent ID
| Column | Description |
|--------|-------------|
| `PID` | Unique participant identifier (integer) |

### AI Experience & Disposition
| Column | Question | Values |
|--------|----------|--------|
| `Q3` | How experienced do you feel using AI tools in your work? | Not at all experienced, Slightly experienced, Somewhat experienced, Moderately experienced, Very experienced |
| `Q4_1` | AI interaction frequency: Auto-complete suggestions (e.g., inline code completions) | Never, A few times a month, 1-3 days a week, A few times a day, Many times a day |
| `Q4_2` | AI interaction frequency: Chat mode (e.g., GitHub Copilot Chat/Ask Mode) | (same scale) |
| `Q4_3` | AI interaction frequency: Collaborative mode (e.g., GitHub Copilot Edit Mode) | (same scale) |
| `Q4_4` | AI interaction frequency: Agentic AI (e.g., GitHub Copilot Agent Mode) | (same scale) |
| `Q5_1` | "I explore and learn about AI technologies, even if it's not critical for my job" | Strongly disagree, Disagree, Neither agree nor disagree, Agree, Strongly agree |
| `Q5_2` | "I am usually one of the first to try out new AI tools or features that haven't been proven to work" | (same scale) |

### Demographics
| Column | Question | Values |
|--------|----------|--------|
| `Q6` | Years of experience in the software industry | Less than 1 year, 1-5 years, 6-10 years, 11-15 years, 16-20 years, Over 20 years |
| `Q8` | Gender identity | Man, Woman, Non-binary, Prefer not to say, Other |
| `Q9` | Geographic region | North America, South and Southeast Asia, Eastern Europe, Western Europe, Pacific/Oceania, etc. |
| `Q10` | Which task categories they selected (2-3 categories) | Comma-separated list of selected categories |

### End-of-Survey Questions
| Column | Question | Values |
|--------|----------|--------|
| `Q24` | What contributes most to your job satisfaction? | Free text |
| `Q26` | Anything else about using AI tools at work? | Free text |
| `Q101` | What contributes most to your job dissatisfaction? | Free text |
| `Q27` | Consent for follow-up contact | Yes/No or blank |
| `Q28` | Email for raffle entry | Email or blank |
| `Q_UnansweredQuestions` | Count of skipped questions | Integer |
| `Duration (in seconds)` | Time to complete survey | Integer |

---

## Category-Specific Columns

Each category has the same structure of questions, but applied to different tasks. The questions measure:

1. **Task Value**: How important is this task for project success?
2. **Task Identity**: Do you personally enjoy doing this task?
3. **Task Accountability**: How accountable/responsible do you feel for outcomes?
4. **Task Demands**: How cognitively demanding is this task?
5. **AI Support Preference**: How much AI support would you prefer in the future?
6. **AI Usage**: How frequently did you use AI for this task in the last 3 months?

### Response Scales

**Task Appraisals (Value, Identity, Demands):**
- Strongly disagree, Disagree, Neither agree nor disagree, Agree, Strongly agree
- Also: "I don't do this task / N.A."

**Task Accountability:**
- Not at all accountable, Slightly accountable, Moderately accountable, Very accountable, Extremely accountable
- Also: "I don't do this task / N.A."

**AI Support Preference:**
- None, Low, Medium, High, Very High

**AI Usage Frequency:**
- Never, A few times a month, 1-3 days a week, A few times a day, Many times a day

---

## development.csv (34 category columns)

**Tasks:** Coding/Programming, Bug Fixing/Debugging, Performance Optimization, Refactoring/Maintenance/Updates, AI Development/Integration

| Column | Question Type | Task |
|--------|--------------|------|
| `Q12_1` | Task Value | Coding/Programming |
| `Q12_2` | Task Value | Bug Fixing/Debugging |
| `Q12_3` | Task Value | Performance Optimization |
| `Q12_4` | Task Value | Refactoring, Maintenance & Updates |
| `Q12_5` | Task Value | AI development / integration into products |
| `Q13_1` | Task Identity | Coding/Programming |
| `Q13_2` | Task Identity | Bug Fixing/Debugging |
| `Q13_3` | Task Identity | Performance Optimization |
| `Q13_4` | Task Identity | Refactoring, Maintenance & Updates |
| `Q13_5` | Task Identity | AI development / integration into products |
| `Q14_1` | Task Accountability | Coding/Programming |
| `Q14_2` | Task Accountability | Bug Fixing/Debugging |
| `Q14_3` | Task Accountability | Performance Optimization |
| `Q14_4` | Task Accountability | Refactoring, Maintenance & Updates |
| `Q14_5` | Task Accountability | AI development / integration into products |
| `Q15_1` | Task Demands | Coding/Programming |
| `Q15_2` | Task Demands | Bug Fixing/Debugging |
| `Q15_3` | Task Demands | Performance Optimization |
| `Q15_4` | Task Demands | Refactoring, Maintenance & Updates |
| `Q15_5` | Task Demands | AI development / integration into products |
| `Q16_1` | AI Support Preference | Coding/Programming |
| `Q16_2` | AI Support Preference | Bug Fixing/Debugging |
| `Q16_3` | AI Support Preference | Performance Optimization |
| `Q16_4` | AI Support Preference | Refactoring, Maintenance & Updates |
| `Q16_5` | AI Support Preference | AI development / integration into products |
| `Q17` | Open-ended | Where do you want AI to play the biggest role for development activities? |
| `Q18_1` | AI Usage Frequency | Coding/Programming |
| `Q18_2` | AI Usage Frequency | Bug Fixing/Debugging |
| `Q18_3` | AI Usage Frequency | Performance Optimization |
| `Q18_4` | AI Usage Frequency | Refactoring, Maintenance & Updates |
| `Q18_5` | AI Usage Frequency | AI development / integration into products |
| `Q19` | Open-ended | What aspects do you NOT want AI to handle and why? |
| `Q39` | RAI Priorities | Select 5 most important AI features (see RAI Principles below) |
| `Q20` | Open-ended | Experience that made selected RAI features feel important |

---

## quality_risk.csv (22 category columns)

**Tasks:** Testing & Quality Assurance, Code Review/Pull Requests, Security & Compliance

| Column | Question Type | Task |
|--------|--------------|------|
| `Q47_1` | Task Value | Testing & Quality Assurance |
| `Q47_2` | Task Value | Code Review/Pull Requests |
| `Q47_3` | Task Value | Security & Compliance |
| `Q48_1` | Task Identity | Testing & Quality Assurance |
| `Q48_2` | Task Identity | Code Review/Pull Requests |
| `Q48_3` | Task Identity | Security & Compliance |
| `Q49_1` | Task Accountability | Testing & Quality Assurance |
| `Q49_2` | Task Accountability | Code Review/Pull Requests |
| `Q49_3` | Task Accountability | Security & Compliance |
| `Q50_1` | Task Demands | Testing & Quality Assurance |
| `Q50_2` | Task Demands | Code Review/Pull Requests |
| `Q50_3` | Task Demands | Security & Compliance |
| `Q51_1` | AI Support Preference | Testing & Quality Assurance |
| `Q51_2` | AI Support Preference | Code Review/Pull Requests |
| `Q51_3` | AI Support Preference | Security & Compliance |
| `Q52` | Open-ended | Where do you want AI to play the biggest role for quality & risk activities? |
| `Q53_1` | AI Usage Frequency | Testing & Quality Assurance |
| `Q53_2` | AI Usage Frequency | Code Review/Pull Requests |
| `Q53_3` | AI Usage Frequency | Security & Compliance |
| `Q54` | Open-ended | What aspects do you NOT want AI to handle and why? |
| `Q56` | RAI Priorities | Select 5 most important AI features |
| `Q57` | Open-ended | Experience that made selected RAI features feel important |

---

## design_planning.csv (22 category columns)

**Tasks:** System Architecture & Design, Requirements Gathering & Analysis, Task/Project Planning & Management

| Column | Question Type | Task |
|--------|--------------|------|
| `Q59_1` | Task Value | System Architecture & Design |
| `Q59_2` | Task Value | Requirements Gathering & Analysis |
| `Q59_3` | Task Value | Task/Project Planning & Management |
| `Q60_1` | Task Identity | System Architecture & Design |
| `Q60_2` | Task Identity | Requirements Gathering & Analysis |
| `Q60_3` | Task Identity | Task/Project Planning & Management |
| `Q61_1` | Task Accountability | System Architecture & Design |
| `Q61_2` | Task Accountability | Requirements Gathering & Analysis |
| `Q61_3` | Task Accountability | Task/Project Planning & Management |
| `Q62_1` | Task Demands | System Architecture & Design |
| `Q62_2` | Task Demands | Requirements Gathering & Analysis |
| `Q62_3` | Task Demands | Task/Project Planning & Management |
| `Q63_1` | AI Support Preference | System Architecture & Design |
| `Q63_2` | AI Support Preference | Requirements Gathering & Analysis |
| `Q63_3` | AI Support Preference | Task/Project Planning & Management |
| `Q64` | Open-ended | Where do you want AI to play the biggest role for design & planning activities? |
| `Q65_1` | AI Usage Frequency | System Architecture & Design |
| `Q65_2` | AI Usage Frequency | Requirements Gathering & Analysis |
| `Q65_3` | AI Usage Frequency | Task/Project Planning & Management |
| `Q66` | Open-ended | What aspects do you NOT want AI to handle and why? |
| `Q68` | RAI Priorities | Select 5 most important AI features |
| `Q69` | Open-ended | Experience that made selected RAI features feel important |

---

## infrastructure_ops.csv (28 category columns)

**Tasks:** DevOps (CI/CD)/Deployment, Environment Setup & Maintenance, Infrastructure Monitoring & Alerts, Customer Support

| Column | Question Type | Task |
|--------|--------------|------|
| `Q71_1` | Task Value | DevOps (CI/CD) / Deployment |
| `Q71_2` | Task Value | Environment Setup & Maintenance |
| `Q71_3` | Task Value | Infrastructure Monitoring & Alerts |
| `Q71_4` | Task Value | Customer Support |
| `Q72_1` | Task Identity | DevOps (CI/CD) / Deployment |
| `Q72_2` | Task Identity | Environment Setup & Maintenance |
| `Q72_3` | Task Identity | Infrastructure Monitoring & Alerts |
| `Q72_4` | Task Identity | Customer Support |
| `Q73_1` | Task Accountability | DevOps (CI/CD) / Deployment |
| `Q73_2` | Task Accountability | Environment Setup & Maintenance |
| `Q73_3` | Task Accountability | Infrastructure Monitoring & Alerts |
| `Q73_4` | Task Accountability | Customer Support |
| `Q74_1` | Task Demands | DevOps (CI/CD) / Deployment |
| `Q74_2` | Task Demands | Environment Setup & Maintenance |
| `Q74_3` | Task Demands | Infrastructure Monitoring & Alerts |
| `Q74_4` | Task Demands | Customer Support |
| `Q75_1` | AI Support Preference | DevOps (CI/CD) / Deployment |
| `Q75_2` | AI Support Preference | Environment Setup & Maintenance |
| `Q75_3` | AI Support Preference | Infrastructure Monitoring & Alerts |
| `Q75_4` | AI Support Preference | Customer Support |
| `Q76` | Open-ended | Where do you want AI to play the biggest role for infrastructure & ops activities? |
| `Q77_1` | AI Usage Frequency | DevOps (CI/CD) / Deployment |
| `Q77_2` | AI Usage Frequency | Environment Setup & Maintenance |
| `Q77_3` | AI Usage Frequency | Infrastructure Monitoring & Alerts |
| `Q77_4` | AI Usage Frequency | Customer Support |
| `Q78` | Open-ended | What aspects do you NOT want AI to handle and why? |
| `Q80` | RAI Priorities | Select 5 most important AI features |
| `Q81` | Open-ended | Experience that made selected RAI features feel important |

---

## meta_work.csv (34 category columns)

**Tasks:** Documentation, Client/Stakeholder Communication, Mentoring & Onboarding, Learning New Technologies, Research & Brainstorming

| Column | Question Type | Task |
|--------|--------------|------|
| `Q83_1` | Task Value | Documentation |
| `Q83_2` | Task Value | Client/Stakeholder Communication |
| `Q83_3` | Task Value | Mentoring & Onboarding |
| `Q83_4` | Task Value | Learning New Technologies |
| `Q83_5` | Task Value | Research & Brainstorming |
| `Q84_1` | Task Identity | Documentation |
| `Q84_2` | Task Identity | Client/Stakeholder Communication |
| `Q84_3` | Task Identity | Mentoring & Onboarding |
| `Q84_4` | Task Identity | Learning New Technologies |
| `Q84_5` | Task Identity | Research & Brainstorming |
| `Q85_1` | Task Accountability | Documentation |
| `Q85_2` | Task Accountability | Client/Stakeholder Communication |
| `Q85_3` | Task Accountability | Mentoring & Onboarding |
| `Q85_4` | Task Accountability | Learning New Technologies |
| `Q85_5` | Task Accountability | Research & Brainstorming |
| `Q86_1` | Task Demands | Documentation |
| `Q86_2` | Task Demands | Client/Stakeholder Communication |
| `Q86_3` | Task Demands | Mentoring & Onboarding |
| `Q86_4` | Task Demands | Learning New Technologies |
| `Q86_5` | Task Demands | Research & Brainstorming |
| `Q87_1` | AI Support Preference | Documentation |
| `Q87_2` | AI Support Preference | Client/Stakeholder Communication |
| `Q87_3` | AI Support Preference | Mentoring & Onboarding |
| `Q87_4` | AI Support Preference | Learning New Technologies |
| `Q87_5` | AI Support Preference | Research & Brainstorming |
| `Q88` | Open-ended | Where do you want AI to play the biggest role for meta-work activities? |
| `Q89_1` | AI Usage Frequency | Documentation |
| `Q89_2` | AI Usage Frequency | Client/Stakeholder Communication |
| `Q89_3` | AI Usage Frequency | Mentoring & Onboarding |
| `Q89_4` | AI Usage Frequency | Learning New Technologies |
| `Q89_5` | AI Usage Frequency | Research & Brainstorming |
| `Q90` | Open-ended | What aspects do you NOT want AI to handle and why? |
| `Q92` | RAI Priorities | Select 5 most important AI features |
| `Q93` | Open-ended | Experience that made selected RAI features feel important |

---

## RAI Priorities Column Format

The RAI Priorities columns (Q39, Q56, Q68, Q80, Q92) contain comma-separated selections of 5 principles from:

1. **Reliability & Safety** - AI produces consistent, accurate outputs and avoids harmful actions
2. **Privacy & Security** - AI protects sensitive data and prevents unauthorized access
3. **Transparency** - AI explains its reasoning and shows sources/confidence
4. **Goal Maintenance** - AI stays aligned with user objectives as they evolve
5. **Steerability** - User can easily redirect, interrupt, or correct AI behavior
6. **AI Accountability** - AI provides provenance and audit trails for its actions
7. **Fairness** - AI treats all users/code/scenarios equitably without bias
8. **Inclusiveness** - AI works well for diverse users, contexts, and accessibility needs

---

## Key Findings from the Study

The study identified three clusters of tasks based on appraisal patterns:

1. **Core Work (C1)**: High value, high demands, high accountability, moderate-high identity
   - Coding, bug fixing, testing, code review, system design, performance optimization, security, learning, research

2. **People & AI Building (C2)**: Moderate value/demands/accountability, strong identity
   - Mentoring, AI integration

3. **Ops & Coordination (C3)**: Moderate-high value/demands/accountability, weak identity
   - DevOps, environment setup, refactoring, monitoring, documentation, customer support, stakeholder communication

Developers generally want AI to:
- **Improve** core work (coding, testing, code review) - high need, high current use
- **Build** support for ops/toil work (DevOps, documentation) - high need, low current use
- **De-prioritize** for relational work (mentoring, stakeholder communication) - low need, low use

---

## Citation

```
Choudhuri, R., Badea, C., Bird, C., Butler, J.L., DeLine, R., & Houck, B. (2025).
AI Where It Matters: Where, Why, and How Developers Want AI Support in Daily Work.
```

Data and interactive dashboard: https://aka.ms/AI-Where-It-Matters

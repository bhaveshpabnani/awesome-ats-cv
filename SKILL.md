---
name: ats-cv-crafter
description: Create, rewrite, audit, or package ATS-friendly CVs and resumes, especially technical or campus-placement resumes in LaTeX/PDF. Use when Codex needs to apply strict recruiter-readable formatting, bullet style rules, action verbs, quantified impact, one-page/two-page tradeoffs, STAR/XYZ bullet writing, skills extraction, project/internship positioning, or ATS parsing validation.
---

# ATS CV Crafter

## Core Workflow

1. Inspect the current CV, source files, project repos, job target, and any user-provided rules before rewriting.
2. Prefer a clean single-column structure with standard headings: Education, Experience, Projects, Skills, Leadership/Achievements.
3. Write each bullet as one idea with a distinct action verb, concrete scope, bolded technical keywords, and measurable impact where evidence supports it.
4. Keep content specific to the candidate. Avoid explaining the organization, society, competition, or summit unless the detail proves the candidate's contribution.
5. For one-page technical resumes, tune content so each bullet renders on one line and fills about 90 percent of the available width without clipping.
6. Build in LaTeX, HTML/CSS, or another parser-safe format, then compile/render and extract text to confirm readable order.
7. Run the style linter when a text or LaTeX source is available: `python3 scripts/lint_cv_text.py <path>`.

## Non-Negotiables

- Do not use bullet full stops.
- Use exactly one space after each bullet marker.
- Use strict spacing rules: comma/colon spacing, spaces around standalone hyphens and pipes, no spaces around slash, and no spaces inside brackets.
- Use 10pt or 11pt body font. Never use 9pt or smaller.
- Keep dates consistent, full-year, and aligned right when rendering: `Apr 2021 - Jul 2021`, `Jan 2026 - Present`.
- Avoid repeated action verbs in nearby bullets.
- Avoid KGP-specific or local jargon unless expanded for external recruiters.
- Keep only explainable, truthful claims. Do not invent metrics.
- Bold high-value keywords inside bullets, especially technologies, systems, metrics, platforms, algorithms, frameworks, and named products.
- Do not leave large empty space at the page bottom in a one-page resume; rebalance content, spacing, section order, or lower-value sections.
- Prefer impact and scale over internal implementation names. Replace low-signal internal fields with recruiter-readable systems, data volume, latency, records, users, cost, revenue, or deployment impact.

## Reference Routing

- Read `references/formatting-rules.md` for detailed typography, spacing, date, and ATS layout rules.
- Read `references/bullet-writing.md` before rewriting internship, project, leadership, or achievement bullets.
- Read `references/action-verbs.md` when bullets need stronger verbs or verb de-duplication.
- Read `references/skills-packaging.md` when extracting, grouping, or deduplicating a comprehensive skills section.
- Read `references/process-safety.md` when preparing a CV for a fragile portal, final submission, peer review, printing, or interview-readiness.

## Validation

Before delivering a final CV:

1. Compile or export the document.
2. Render at least one visual preview of every page.
3. For layout-sensitive one-page CVs, measure or visually verify that every bullet stays on one line and uses roughly 90 percent of the line width.
4. Extract plain text from the PDF and verify section order, links, dates, bullets, and names.
5. Run the linter script if possible.
6. Confirm grammar, print readability, backup/source export, and interview defensibility.
7. Report any unverifiable metric, missing phone number, missing link, or source limitation.

# Awesome ATS CV

<p align="center">
  <img src="https://img.shields.io/badge/Codex-Skill-111827?style=for-the-badge" alt="Codex Skill">
  <img src="https://img.shields.io/badge/Resume-ATS%20friendly-2ea44f?style=for-the-badge" alt="ATS friendly resume skill">
  <img src="https://img.shields.io/badge/Layout-One%20page%20ready-4f46e5?style=for-the-badge" alt="One page resume layout">
  <img src="https://img.shields.io/badge/Bullets-Impact%20first-f59e0b?style=for-the-badge" alt="Impact first bullets">
  <img src="https://img.shields.io/badge/Toolkit-Cross%20platform-0ea5e9?style=for-the-badge" alt="Cross-platform toolkit">
</p>

**A cross-platform ATS CV skill and validation toolkit for building clean, recruiter-readable technical resumes with dense one-line bullets, bold keywords, quantified impact, and render-verified PDF/DOCX output.**

Awesome ATS CV packages the resume rules I use when I need a CV that is not just pretty, but parseable, defensible, and ready for technical hiring workflows. It gives Codex a repeatable process for rewriting internships, projects, skills, leadership, and achievements into a compact resume with measurable outcomes and consistent formatting, and it also ships normal Python scripts that can be used without Codex.

The goal is simple: every bullet should prove something real. It should start with an action verb, include relevant technical keywords, show scope or result, avoid filler, and render cleanly on the final page.

## What It Is

Awesome ATS CV is both a local Codex skill named `ats-cv-crafter` and a portable CV QA toolkit. It helps you or an agent:

1. Inspect an existing resume, source PDF, LaTeX, DOCX, HTML, or project repository before rewriting
2. Convert raw work history into concise STAR/XYZ-style bullets
3. Keep formatting consistent across sections, dates, bullets, links, spacing, and headings
4. Bold the right technical keywords without turning the whole resume into noise
5. Render role-specific HTML templates from structured JSON data
6. Validate final layout by rendering previews, measuring bullet widths, checking page coverage, and extracting PDF text
7. Compare job-description keywords against resume content before applying
8. Run an end-to-end workflow from evidence inventory to final portal-safe submission

## What It Optimizes

| Area | Rule |
| --- | --- |
| ATS parsing | Prefer simple single-column structure, standard headings, visible links, and extractable text |
| Bullet density | Keep one-page bullets on one rendered line and around `90-98%` of available width |
| Impact | Replace adjectives with metrics such as latency, accuracy, records, users, cost, scale, rankings, or deployments |
| Keywords | Include target-relevant technologies, frameworks, systems, clouds, models, databases, and algorithms |
| Bold text | Bold only the strongest keywords: technologies, systems, metrics, model names, platforms, and named products |
| Page fit | Avoid large empty bottom gaps; restore high-value content or tune spacing before adding filler |
| Dates | Use readable full-year dates such as `May 2025 - Jul 2025` and align them right |
| Readability | Use 10pt or 11pt body text only; never shrink to 9pt to force fit |
| Process safety | Finish early, keep backups, validate portal output, print-check final resumes, and get human review |

## Core Rules

- No full stops at the end of bullets
- Exactly one space after each bullet marker
- One space after commas and colons, never before
- Spaces around standalone hyphens and pipe characters
- No spaces around slash, as in `CI/CD`, `EXE/ZIP`, or `macOS/Windows`
- No spaces immediately inside brackets
- No tables for ATS-first education or experience layouts unless explicitly requested
- No low-signal internal field names when recruiter-readable impact is available
- No unverifiable metrics or claims that cannot be explained in an interview

## Repository Layout

```text
awesome-ats-cv/
├── SKILL.md
├── pyproject.toml
├── agents/
│   └── openai.yaml
├── references/
│   ├── ats-research.md
│   ├── action-verbs.md
│   ├── bullet-writing.md
│   ├── end-to-end-workflow.md
│   ├── formatting-rules.md
│   ├── grammar-checking.md
│   ├── non-kgp-general-guidance.md
│   ├── process-safety.md
│   ├── resource-library.md
│   ├── skills-packaging.md
│   └── validation-matrix.md
├── templates/
│   ├── data-ai.html
│   ├── executive-leadership.html
│   ├── internship-campus.html
│   ├── product-analytics.html
│   ├── research-academic.html
│   └── technical-sde.html
├── examples/
│   ├── job-description.txt
│   └── resume-data.json
└── scripts/
    ├── audit_ats_structure.py
    ├── audit_resume_content.py
    ├── atscv_utils.py
    ├── check_grammar.py
    ├── extract_pdf_text.py
    ├── extract_job_keywords.py
    ├── html_to_pdf.py
    ├── lint_cv_text.py
    ├── measure_bullet_widths.py
    ├── measure_page_coverage.py
    ├── render_resume_template.py
    ├── render_pdf_pages.py
    ├── update_resume_data.py
    └── validate_cv.py
```

## Install as a Codex Skill

Clone this repository into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/bhaveshpabnani/awesome-ats-cv.git ~/.codex/skills/ats-cv-crafter
```

If you already have the skill installed:

```bash
cd ~/.codex/skills/ats-cv-crafter
git pull
```

## Install as a Cross-Platform Toolkit

The scripts are plain Python and work on macOS, Linux, and Windows. Use Python `3.10+`.

```bash
git clone https://github.com/bhaveshpabnani/awesome-ats-cv.git
cd awesome-ats-cv
python3 -m pip install -e ".[validate,docx,grammar]"
python3 -m playwright install chromium
```

For PDF rendering and text extraction, install Poppler:

| OS | Command |
| --- | --- |
| macOS | `brew install poppler` |
| Ubuntu/Debian | `sudo apt-get install poppler-utils` |
| Windows | Install Poppler and add its `bin` directory to `PATH` |

If your browser or Poppler tools are outside `PATH`, set these environment variables:

```bash
export ATS_CV_CHROME="/path/to/chrome-or-edge"
export ATS_CV_PDFTOPPM="/path/to/pdftoppm"
export ATS_CV_PDFTOTEXT="/path/to/pdftotext"
```

## Use with Codex

Ask Codex to use the skill explicitly:

```text
Use $ats-cv-crafter to rewrite my CV for a Microsoft SDE role.
Keep it one page, make bullets single-line, bold keywords, quantify impact, and validate the PDF.
```

Or use it for a focused pass:

```text
Use $ats-cv-crafter to audit this resume for ATS parsing, bullet density, dates, spacing, and missing technical keywords.
```

## CLI Validation Workflow

The toolkit is designed to validate the final artifact instead of trusting the source file blindly:

1. Lint source text or LaTeX spacing rules
2. Audit resume content for metrics, weak phrases, contact, sections, action verbs, and repeated openings
3. Audit HTML structure for ATS parsing risks
4. Measure rendered HTML bullet width ratios
5. Convert HTML to PDF through Chrome/Chromium/Edge
6. Render PDF pages into PNG previews
7. Measure page coverage, content box, margins, and bottom whitespace
8. Extract PDF text to verify ATS-readable order
9. Check grammar through the offline validator plus a final Grammarly or LanguageTool pass

For plain text or LaTeX-like sources, run:

```bash
python3 scripts/lint_cv_text.py path/to/resume.tex
python3 scripts/audit_resume_content.py path/to/resume.tex
python3 scripts/check_grammar.py path/to/resume.tex --provider offline
```

For HTML resumes, run the full validator:

```bash
python3 scripts/validate_cv.py path/to/resume.html --min-width 0.90 --max-width 0.98 --max-bottom-mm 14
```

To render a bundled HTML template from structured JSON:

```bash
python3 scripts/render_resume_template.py --list
python3 scripts/render_resume_template.py --template technical-sde.html --data examples/resume-data.json --out out/resume.html
python3 scripts/validate_cv.py out/resume.html
```

To edit resume JSON without touching template markup:

```bash
python3 scripts/update_resume_data.py examples/resume-data.json --out out/resume-data.json --set "profile.headline=Software Engineer | Azure Data | Distributed Systems"
python3 scripts/update_resume_data.py out/resume-data.json --in-place --add-skill "Cloud=Azure" --add-bullet "projects:0:Optimized **PDF validation** checks across macOS, Linux, and Windows"
```

To extract job keywords and check resume coverage:

```bash
python3 scripts/extract_job_keywords.py examples/job-description.txt --limit 30
python3 scripts/extract_job_keywords.py examples/job-description.txt --resume out/resume.html --limit 30
```

To run grammar validation:

```bash
python3 scripts/check_grammar.py out/resume.html --provider offline
python3 scripts/check_grammar.py out/resume.html --provider spellchecker --dictionary references/resume-dictionary.txt
python3 scripts/check_grammar.py out/resume.html --provider languagetool
python3 scripts/check_grammar.py --provider manual
```

For PDF-only validation:

```bash
python3 scripts/render_pdf_pages.py path/to/resume.pdf atscv-validation/rendered
python3 scripts/measure_page_coverage.py atscv-validation/rendered/page-1.png --max-bottom-mm 14
python3 scripts/extract_pdf_text.py path/to/resume.pdf --out atscv-validation/extracted.txt
```

## Script Reference

| Script | Purpose |
| --- | --- |
| `scripts/audit_ats_structure.py` | Flags risky HTML structures such as tables, images, headers, footers, grids, absolute positioning, and non-standard headings |
| `scripts/audit_resume_content.py` | Audits metrics, action verbs, weak phrases, repeated openings, section coverage, contact, and link signals |
| `scripts/check_grammar.py` | Runs offline hygiene checks, optional dictionary spellcheck, LanguageTool API checks, or a manual Grammarly review gate |
| `scripts/lint_cv_text.py` | Checks bullet full stops, comma/colon/slash/bracket/pipe spacing, date style, and repeated action verbs |
| `scripts/extract_job_keywords.py` | Extracts job-description keyword candidates and compares whether they appear in a resume source |
| `scripts/render_resume_template.py` | Renders bundled ATS-safe HTML templates from `examples/resume-data.json`-style structured data |
| `scripts/update_resume_data.py` | Edits structured resume JSON fields, skill categories, and bullets without manual JSON surgery |
| `scripts/measure_bullet_widths.py` | Uses Playwright to measure whether each rendered bullet fills the target width range |
| `scripts/html_to_pdf.py` | Converts parser-safe HTML resumes into print PDFs with Chrome, Chromium, or Edge |
| `scripts/render_pdf_pages.py` | Renders PDF pages to PNG using Poppler `pdftoppm` for visual inspection |
| `scripts/measure_page_coverage.py` | Measures ink coverage, content box, margins, and bottom whitespace from rendered page images |
| `scripts/extract_pdf_text.py` | Extracts ATS-readable text from PDFs using Poppler `pdftotext` or `pypdf` fallback |
| `scripts/validate_cv.py` | Runs the full HTML/PDF validation pipeline with one command |
| `scripts/atscv_utils.py` | Shared cross-platform discovery for browsers and Poppler tools |

## HTML Templates

The package includes six single-column HTML templates:

| Template | Best for |
| --- | --- |
| `technical-sde.html` | SDE, backend, cloud, infra, distributed systems, and platform roles |
| `data-ai.html` | ML engineering, data science, AI platform, analytics engineering, and LLM roles |
| `internship-campus.html` | Campus placements, internships, early-career profiles, and one-page student resumes |
| `product-analytics.html` | Product analytics, business analytics, strategy, and data-heavy product roles |
| `research-academic.html` | Research internships, academic CVs, publications, labs, and graduate applications |
| `executive-leadership.html` | Senior engineering, founding, program ownership, and leadership-oriented resumes |

All templates avoid tables, sidebars, photos, icon-only contact rows, headers, footers, and non-standard section labels. They support `**bold keywords**` inside JSON bullets.

## What the Full Validator Reports

The full validator is intentionally quantitative. A good one-page technical CV should produce output like:

```text
measured 35 bullet(s)
ratio range: 0.901 - 0.979
rendered 1 page(s)
page-1.png: bottom=8.47mm, coverage=0.14558
ATS CV validation complete
```

Use these signals when polishing the final resume:

| Signal | Target |
| --- | --- |
| Bullet width ratio | Usually `0.90-0.98` for dense one-line bullets |
| Bottom whitespace | Keep low enough that the page feels fully used, usually below `14mm` |
| Page count | Keep one-page resumes to exactly `1` rendered page |
| Extracted text | Confirm headings, dates, links, and bullets appear in recruiter-readable order |

## Bullet Formula

Use this structure when evidence exists:

```text
Action verb + work done + technology/method + scale/constraint + measurable result
```

Examples:

- Reduced search latency from `4s` to `843ms` using DynamoDB batch queries and a 20-thread executor
- Built multi-tenant analytics on AWS EC2, Aurora, and Redis, serving 384K+ records through tenant-scoped APIs
- Packaged macOS/Windows releases with PKG/ZIP, EXE/ZIP, Homebrew, Scoop, Chocolatey, WinGet, and CI/CD checks

## Skills Section Guidance

The skill keeps technical skills useful for both ATS and humans. It groups supported skills across:

- Languages
- Backend
- Frontend
- AI/ML
- Data
- Cloud/DevOps
- Observability/Quality

It should add keywords that are actually supported by experience or projects, such as `FastAPI`, `Redis`, `Aurora`, `AWS EC2`, `Kafka`, `Playwright`, `WinUI 3`, `SwiftUI`, `LangGraph`, or `Docker`.

## Why This Exists

Most resume advice says "use action verbs" and stops there. That is not enough. A technical CV has to survive three readers:

1. The ATS parser
2. The recruiter scanning in seconds
3. The interviewer asking for proof

Awesome ATS CV is designed around all three. It favors concrete ownership, numbers, systems, implementation detail, and visual discipline.

## Cross-Platform Design

The toolkit avoids Codex-specific runtime assumptions. The skill files help Codex follow the rules, while the scripts can be used in CI, local pre-submission checks, GitHub Actions, or any resume build pipeline. The browser and Poppler discovery logic supports macOS app bundles, Linux package installs, Windows executable paths, and explicit environment-variable overrides.

## Research-Backed ATS Guidance

The latest research notes are in `references/ats-research.md`. The current package encodes guidance from Harvard Mignone Center for Career Success, Indeed Career Guide, Santa Clara University Career Center, Columbia Career Education, Yale Office of Career Strategy, and Jobscan into concrete checks and defaults: standard headings, single-column templates, natural job-description keywords, long-form/acronym keyword variants, body contact information, no tables/graphics/headers/footers, and render-plus-extract validation.

## Complete Workflow

For a full resume pass, follow `references/end-to-end-workflow.md`:

1. Pick the target role family and file strategy
2. Build an evidence inventory from projects, repos, internships, metrics, and links
3. Extract job-description keywords and map them to truthful resume sections
4. Choose a standard section architecture
5. Rewrite bullets with STAR/XYZ compression, action verbs, keywords, and metrics
6. Apply ATS-safe formatting and template constraints
7. Validate line width, page fill, structure, content, PDF render, and extracted text
8. Run grammar, print, peer, and interview-defensibility review
9. Preserve portal backups and final submitted files

The generalized peer-review rules from the uploaded notes live in `references/non-kgp-general-guidance.md`. The validation playbook lives in `references/validation-matrix.md`.

Grammar and proofreading rules live in `references/grammar-checking.md`. The package uses deterministic offline hygiene checks for CI, supports optional `pyspellchecker` dictionary checks, supports LanguageTool for automated grammar review, and treats Grammarly as a final manual or enterprise-configured review gate.

## External Resource Library

The curated source list lives in `references/resource-library.md` and includes MIT CAPD, Harvard, Columbia, Santa Clara University, Yale, Indeed, The Muse, Jobscan, Skillsyncer, and Resume Worded. Use university/career-center sources as baseline rules, and treat commercial scoring tools as secondary checks rather than final authority.

## Repository Status

This repository is intentionally focused. The useful knowledge lives in `SKILL.md`, `references/`, and the validation scripts. There is no web server or application runtime required, but the toolkit is ready to be used by Codex, local Python, or CI.

# End-to-End ATS Resume Workflow

This workflow turns raw experience into a role-targeted, ATS-readable, recruiter-readable, interview-defensible resume.

## Phase 0: Submission Strategy

- Decide the target profile before rewriting: SDE, data/AI, product analytics, research, consulting, finance, or leadership
- Create one master resume and one tailored resume per target role family
- Finish structural edits at least 2 days before the deadline
- Keep timestamped backups of source, rendered PDF, extracted text, and submitted file
- Use the exact file type requested by the portal; otherwise keep both PDF and DOCX-ready versions

## Phase 1: Evidence Inventory

- Collect source material before writing: current resume, transcripts, offer letters, project READMEs, GitHub links, demos, reports, metrics, screenshots, and deployment notes
- For every internship or project, capture ownership, technologies, scale, users, data volume, latency, revenue/cost, ranking, accuracy, reliability, releases, or integrations
- Mark each claim as `verified`, `estimated`, or `unknown`
- Remove claims that cannot be explained with code, architecture, tradeoffs, metrics, or examples
- Convert internal jargon into recruiter-readable systems, scope, and impact

## Phase 2: Job Description Mapping

- Paste the job description into `scripts/extract_job_keywords.py`
- Extract repeated hard skills, tools, role titles, cloud services, databases, certifications, and domain terms
- Map every important keyword to one of: summary, skills, experience bullet, project bullet, coursework, certification, or omit
- Include long-form and acronym variants where useful, such as `Large Language Models (LLMs)` or `Search Engine Optimization (SEO)`
- Use keywords only where they are truthful and interview-defensible
- Avoid keyword stuffing and invisible keyword tricks

## Phase 3: Section Architecture

- Use standard headings that ATS and recruiters recognize: Summary, Education, Work Experience, Projects, Technical Skills, Certifications, Leadership, Achievements, Publications
- Put the most relevant sections in the first half of the page
- Use reverse chronological order inside Education and Experience unless a role-specific project section should lead
- For technical roles, prioritize internships, projects, systems, skills, and measurable engineering work over generic activities
- Split Positions and Achievements when both matter and space allows
- Remove lower-level duplicate achievements when a stronger achievement proves the same skill

## Phase 4: Bullet Drafting

- Start each bullet with a strong action verb
- Use one idea per bullet
- Prefer STAR/XYZ compression: accomplished X, measured by Y, by doing Z
- Replace adjectives with evidence: latency, accuracy, data size, users, records, tests, costs, revenue, deployment count, services, endpoints, or rankings
- Use role-specific technical terms naturally in bullets, not only in the Skills section
- Bold only the highest-value keywords: systems, tools, metrics, models, platforms, products, and hard skills
- Avoid vague verbs and fillers such as `worked on`, `helped`, `responsible for`, `various`, `multiple`, `several`, and `etc.`
- Keep bullets without full stops if following the compact campus/technical style

## Phase 5: Formatting

- Use a single-column layout for ATS-first resumes
- Avoid tables, text boxes, sidebars, headers, footers, images, icons, charts, and complex multi-column designs
- Keep contact information in the main body
- Use common fonts such as Arial, Calibri, Cambria, Georgia, Helvetica, or Times New Roman
- Keep body font at 10pt or 11pt for compact one-page resumes; never use 9pt or smaller for body text
- Keep spacing consistent across sections, role headers, bullets, dates, links, and dividers
- Use full-year dates consistently: `Apr 2021 - Jul 2021`, `Jan 2026 - Present`, or `04/2021 - 07/2021` only when a platform asks for numeric dates
- Use visible, absolute links for GitHub, LinkedIn, portfolio, demos, papers, or blogs

## Phase 6: Line Width and Page Fit

- For one-page technical resumes, keep each bullet on one rendered line when possible
- Target about `0.90-0.98` bullet-width ratio for dense one-line bullets
- If a line is too short, add truthful scale, architecture, tool, result, user impact, or deployment context
- If a line is too long, remove filler before removing metrics or core technologies
- Fill the page gracefully without leaving a large empty bottom block
- Fix bottom whitespace by restoring high-value content, rebalancing sections, or tuning spacing, not by adding generic filler

## Phase 7: Automated Validation

- Run `python3 scripts/lint_cv_text.py <source>` for text, Markdown, or LaTeX sources
- Run `python3 scripts/audit_resume_content.py <source>` to inspect metrics, verbs, weak phrases, section coverage, and keyword quality
- Run `python3 scripts/audit_ats_structure.py <resume.html>` for HTML templates
- Run `python3 scripts/measure_bullet_widths.py <resume.html>` for bullet density
- Run `python3 scripts/validate_cv.py <resume.html>` for structure audit, HTML-to-PDF, PDF rendering, page coverage, and text extraction
- Run `python3 scripts/check_grammar.py <source> --provider offline` for deterministic grammar checks
- Run a Grammarly or LanguageTool pass before final submission
- Open the extracted text and verify that name, contact, headings, dates, links, and bullets appear in the intended order
- Print or visually inspect the rendered PDF at final size

## Phase 8: Human Review

- Ask at least one domain-relevant reviewer to inspect the resume
- Ask reviewers to check missing keywords, unclear impact, weak bullets, grammar, layout, and interview defensibility
- Ask one non-domain reader to check whether the resume is understandable without local jargon
- Run a grammar/spell check after every major rewrite
- Verify official capitalization and spelling for programming languages, frameworks, companies, products, competitions, and universities

## Phase 9: Portal Safety

- Let the portal fully load before editing, previewing, or saving
- Export/download the source or HTML after every meaningful portal edit
- Preview after save, not only before save
- Keep a local paste-ready backup in case bullets, bold text, spacing, or content disappear
- Avoid last-day structural edits because portal styles can distort under deadline pressure

## Phase 10: Final Submission Gate

- Confirm the resume targets the exact role family
- Confirm the file type matches instructions
- Confirm the resume has no missing email, phone, GitHub/LinkedIn, or critical dates
- Confirm all bullets are truthful and explainable
- Confirm no section order, extraction, or link issue appears in the final PDF/text extraction
- Confirm CI or local validation logs are saved for the final artifact
- Save final files as `Name_Role_Company_Resume_YYYY-MM-DD.pdf` or equivalent

## Minimum Acceptance Criteria

- Standard headings and single-column structure
- No tables, text boxes, images, icons, sidebars, or hidden text in the ATS version
- Contact information in body text
- 10pt or 11pt readable body text
- Consistent date format
- Job-description keywords mapped naturally into the resume
- Bullets start with action verbs and contain measurable evidence where available
- No bullet full stops if using compact technical style
- No repeated weak verbs or unexplained jargon
- Rendered PDF is visually clean and text extraction preserves order
- Resume is reviewed by at least one person before submission

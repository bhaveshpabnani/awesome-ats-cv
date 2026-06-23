# HTML Template Pack

All templates are ATS-first, single-column, text-based HTML files. They avoid tables, images, sidebars, icons, and headers/footers.

## Templates

- `technical-sde.html`: dense technical resume for software engineering, backend, cloud, infra, and distributed systems roles
- `data-ai.html`: data science, ML engineering, analytics engineering, and AI platform roles
- `internship-campus.html`: campus placement, internship, early-career, and one-page student resumes
- `product-analytics.html`: product analytics, business analytics, strategy, and data-heavy product roles
- `research-academic.html`: research internships, academic projects, publications, labs, and graduate applications
- `executive-leadership.html`: senior engineering, product leadership, founding, and program ownership resumes

## Render

```bash
python3 scripts/render_resume_template.py --list
python3 scripts/render_resume_template.py --template technical-sde.html --data examples/resume-data.json --out out/resume.html
python3 scripts/validate_cv.py out/resume.html
```

## Placeholder Tokens

Each template supports these tokens:

- `{{NAME}}`
- `{{HEADLINE}}`
- `{{CONTACT}}`
- `{{SUMMARY}}`
- `{{SKILLS}}`
- `{{EXPERIENCE}}`
- `{{PROJECTS}}`
- `{{EDUCATION}}`
- `{{CERTIFICATIONS}}`
- `{{LEADERSHIP}}`
- `{{ACHIEVEMENTS}}`
- `{{PUBLICATIONS}}`

Use `**keyword**` inside JSON bullets to render bold keywords.

# Validation Matrix

This matrix maps resume risks to local checks, manual checks, and acceptable thresholds.

| Risk | Automated check | Manual check | Target |
| --- | --- | --- | --- |
| ATS cannot parse layout | `audit_ats_structure.py` | Inspect source for tables, headers, footers, sidebars, images | No blocking risky tags |
| Text extraction order is wrong | `validate_cv.py` then inspect `extracted.txt` | Read extracted text top to bottom | Name, contact, sections, bullets in expected order |
| Bullets are too short or too long | `measure_bullet_widths.py` | Visual PDF inspection | Usually `0.90-0.98` for dense one-page technical resumes |
| Page has empty bottom space | `measure_page_coverage.py` | Visual PDF inspection | Bottom whitespace usually below `14mm` |
| Style spacing errors | `lint_cv_text.py` | Read PDF and source | No punctuation, slash, bracket, pipe, date, or bullet-full-stop issues |
| Weak or vague bullets | `audit_resume_content.py` | Reviewer check | Low weak-phrase count, high metric and action-verb coverage |
| Missing role keywords | `extract_job_keywords.py --resume` | Compare with job description | Important truthful keywords represented naturally |
| Missing contact | `audit_ats_structure.py`, `audit_resume_content.py` | Click links and check phone/email | Email, phone, GitHub/LinkedIn where relevant |
| Unsupported claims | None | Interview rehearsal | Every bullet explainable with examples |
| Grammar errors | `check_grammar.py` | Grammarly, LanguageTool, and human review | No spelling/grammar errors |
| Wrong file type | None | Portal/job-posting check | Match application instructions |

## Strict Local Validation

For HTML resumes:

```bash
python3 scripts/validate_cv.py path/to/resume.html --min-width 0.90 --max-width 0.98 --max-bottom-mm 14
python3 scripts/audit_resume_content.py path/to/resume.html --strict
python3 scripts/check_grammar.py path/to/resume.html --provider offline
python3 scripts/extract_job_keywords.py path/to/job-description.txt --resume path/to/resume.html --limit 40
```

For LaTeX or Markdown sources:

```bash
python3 scripts/lint_cv_text.py path/to/resume.tex
python3 scripts/audit_resume_content.py path/to/resume.tex --strict
python3 scripts/check_grammar.py path/to/resume.tex --provider offline
```

For PDF-only resumes:

```bash
python3 scripts/render_pdf_pages.py path/to/resume.pdf atscv-validation/rendered
python3 scripts/measure_page_coverage.py atscv-validation/rendered/page-1.png --max-bottom-mm 14
python3 scripts/extract_pdf_text.py path/to/resume.pdf --out atscv-validation/extracted.txt
python3 scripts/audit_resume_content.py atscv-validation/extracted.txt --strict
python3 scripts/check_grammar.py atscv-validation/extracted.txt --provider offline
```

## Human Review Checklist

- Does the top half prove fit for the target role
- Are the strongest technical keywords present and bolded sparingly
- Does every bullet show individual ownership
- Does every bullet have one idea
- Are metrics accurate and defensible
- Are project affiliations and links clear
- Are dates consistent
- Is there any unexplained local acronym
- Are there repeated action verbs
- Is the printed resume readable
- Can the candidate explain every bullet

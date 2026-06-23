# ATS Research Notes

These rules summarize current public ATS and career-center guidance. Use them as guardrails, not as a promise that every ATS behaves identically.

## High-Confidence Formatting Rules

- Use a clean single-column layout with standard section headings such as `Work Experience`, `Education`, `Skills`, `Projects`, and `Certifications`
- Keep contact details in the main body at the top of the resume, not in document headers or footers
- Avoid tables, text boxes, graphics, photos, icons, charts, columns, and custom decorative bullets for ATS-first versions
- Use common fonts such as Arial, Calibri, Georgia, or Times New Roman, generally in the 10-12pt range for body text
- Use clear dates with full months/years or numeric month/year formats when a platform asks for them
- Prefer reverse chronological or hybrid ordering for most professional resumes
- Submit `.docx` when an application specifically requests it or when ATS compatibility matters more than exact visual fidelity; submit PDF when requested or when layout preservation matters

## Keyword Rules

- Extract repeated hard skills, tools, job titles, certifications, and qualifications from the job description before rewriting
- Include exact job-description language naturally in summary, skills, experience, and project bullets
- Include both long-form and acronym forms when relevant, for example `Search Engine Optimization (SEO)` or `Large Language Models (LLMs)`
- Avoid keyword stuffing; the resume must still read naturally to a recruiter and interviewer
- Use the strongest keywords in bullet context, not only in a skills list

## Bullet Rules

- Start bullets with varied action verbs
- Write accomplishments, not responsibility lists
- Quantify impact wherever evidence exists: latency, cost, records, users, revenue, rank, accuracy, throughput, uptime, page count, team size, or deployment scope
- Keep each bullet to one idea, especially in dense one-page formats
- Make every bullet defensible in an interview

## Sources Consulted

- Harvard Mignone Center for Career Success: strong resumes should be specific, active, fact-based, easy to scan, consistent, reverse chronological within sections, and checked after PDF conversion
  - https://careerservices.fas.harvard.edu/resources/hes-create-impactful-resumes-and-cover-letters/
  - https://careerservices.fas.harvard.edu/resources/create-a-strong-resume/
- Indeed Career Guide: ATS resumes should use simple formatting, clear section headings, no graphics or tables, natural keywords from the posting, and reverse chronological structure
  - https://www.indeed.com/career-advice/resumes-cover-letters/ats-resume-template
- Santa Clara University Career Center/Jobscan summary: include long-form and acronym keyword variants, avoid critical info in headers/footers, avoid tables/graphics/non-standard bullets, and use conventional headings
  - https://www.scu.edu/careercenter/toolkit/job-scan-common-ats-resume-formatting-mistakes/
  - https://www.scu.edu/careercenter/toolkit/resumes/
- Columbia Career Education: use common section headers, include keywords in a summary where useful, and keep resume structure easy for ATS systems to categorize
  - https://www.careereducation.columbia.edu/resources/optimizing-your-resume-applicant-tracking-systems
- Yale Office of Career Strategy: action verbs and quantified accomplishment language make bullets stronger and more specific
  - https://ocs.yale.edu/resources/resume-action-verbs/
- Jobscan ATS guidance: tailor each resume to the job, match keywords to the job description, use chronological or hybrid formats, and avoid tables/columns/graphics/headers/footers
  - https://www.jobscan.co/blog/20-ats-friendly-resume-templates/
  - https://www.jobscan.co/blog/ats-formatting-mistakes/

## Automation Implications

- `scripts/audit_ats_structure.py` checks for risky HTML elements and non-standard headings
- `scripts/extract_job_keywords.py` extracts candidate keywords from a job description and compares them with resume text
- `scripts/render_resume_template.py` renders single-column HTML templates from structured JSON
- `scripts/validate_cv.py` combines structure audit, bullet-width measurement, PDF rendering, page coverage, and text extraction

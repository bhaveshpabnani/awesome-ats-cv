# Formatting Rules

## ATS-safe layout

- Use a single-column document for ATS-first resumes.
- Avoid logos, photos, icons, text boxes, section shading, complex tables, multi-column layouts, and decorative graphics.
- Put name, email, phone, GitHub, LinkedIn, and portfolio in the main document body, not a header/footer.
- Use common fonts and readable sizes: 10pt or 11pt body text only.
- Keep bold labels visually smaller or no larger than surrounding body text. In LaTeX, avoid oversized bold section labels.
- Use standard section headings that parsers recognize: Education, Experience, Projects, Skills, Leadership, Achievements, Certifications.
- Use black text and high contrast. Color should be avoided unless explicitly required.
- For off-campus ATS submissions, prefer PDF unless the platform explicitly requests DOCX; verify by extracting plain text from the PDF.

## Spacing and punctuation

- End bullets without full stops.
- Put exactly one space after bullet markers.
- Put one space after commas, never before commas.
- Put one space after colons, never before colons.
- Put spaces before and after standalone hyphens in date ranges and ranges: `Apr 2021 - Jul 2021`.
- Do not put spaces around slash: `EXE/ZIP`, `macOS/Windows`, `CI/CD`.
- Do not put a space after an opening bracket: `(RAG)`, `[GitHub]`, `{key}`.
- Do not put a space before a closing bracket: `(RAG)`, `[GitHub]`, `{key}`.
- Put one space before and after pipe characters: `Amazon | SDE Intern | May 2025 - Jul 2025`.
- Avoid double or triple spaces anywhere.
- Use full years: `2026`, not `'26`.
- Do not use local abbreviations unless expanded once.

## Dates

- Preferred format: `Apr 2021 - Jul 2021`.
- Use three-letter month abbreviations with a space before the year.
- Use `Present` with capital `P`.
- Use full years.
- Align dates to the extreme right in rendered PDFs using layout primitives, not random manual spaces if writing LaTeX.
- If a platform specifically asks for ATS dates in numeric form, use `04/2021 - 07/2021`; otherwise use the readable month-year format consistently.

## Line length and density

- For one-page technical CVs, keep every bullet on one rendered line unless the user explicitly allows wrapping.
- Do not split one strong point merely to satisfy line length; split only when a bullet contains multiple ideas.
- Aim for each bullet to use about 90 percent of the available line width. A practical target band is 90-99 percent after rendering.
- If a bullet is short, add truthful detail: scale, data volume, latency, users, records, deployment surface, architecture, framework, model, cloud/service, or business impact.
- If a bullet is too long, remove low-signal words first, not metrics or core technologies.
- Validate line width from the rendered PDF/HTML when possible; visual inspection is better than character counting.
- Prefer fewer high-signal bullets over many filler bullets.
- For technical profiles, reduce positions of responsibility if they crowd out internships, projects, systems, or metrics.

## Page fill and padding

- One-page CVs should use the full page gracefully, with no large empty block at the bottom.
- Do not solve bottom whitespace with generic filler such as `Target Focus` or `Core Strength` unless the user explicitly asks for such a summary.
- Prefer these fixes for bottom whitespace: restore missing high-value bullets, separate Positions and Achievements, rebalance section spacing, tune margins, or include one more evidence-backed line.
- Keep spacing and padding consistent across all sections: same section-title rhythm, same role-title/date rhythm, and same bullet indentation.
- Avoid tables for Education and other content unless the user explicitly requests them; use parser-safe grids or aligned text instead.

## LaTeX guidance

- Use `article` or a similarly simple class.
- Avoid `tcolorbox`, images, wrapped figures, complex tabular layouts, and multi-column packages for ATS-first versions.
- Use `hyperref` with plain visible link text.
- Use `glyphtounicode` and `\pdfgentounicode=1` for pdfLaTeX when available.
- Disable ugly word splitting when possible and verify text extraction after compilation.
- If forcing one page requires 9pt or excessive compression, keep two readable pages instead.

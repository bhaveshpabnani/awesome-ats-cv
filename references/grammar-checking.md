# Grammar and Proofreading Validation

Grammar checking is a required final gate for resume quality, but automated suggestions must not override technical accuracy or the user's chosen resume style.

## Recommended Stack

- Use `scripts/check_grammar.py --provider offline` only for deterministic hygiene checks in CI
- Use `scripts/check_grammar.py --provider spellchecker` for generalized dictionary-based spelling checks with a custom resume dictionary
- Use `scripts/check_grammar.py --provider languagetool` for a deeper LanguageTool grammar/spelling API pass when network access and privacy constraints allow it
- Use Grammarly as a final manual review gate for grammar, spelling, clarity, concision, and tone
- Rerender and revalidate the resume after accepting any grammar suggestions

## Provider Design

The checker is layered because no single local rule set can safely understand every technical resume:

- `offline` is not a full spellchecker. It catches repeated words, spacing before punctuation, and a small fallback typo list for deterministic CI
- `spellchecker` uses `pyspellchecker` for generalized spelling and supports custom dictionaries for technical terms
- `languagetool` calls a LanguageTool endpoint for broader grammar and spelling review
- `manual` prints the Grammarly review checklist for final human-in-the-loop proofreading

Install optional spelling dependencies with:

```bash
python3 -m pip install -e ".[grammar]"
```

## Grammarly Gate

Grammarly is best included in this toolkit as a manual or enterprise-configured validation gate:

- Paste the final resume text into Grammarly or open the final editable source in a Grammarly-enabled editor
- Review grammar, spelling, punctuation, tone, clarity, and concision suggestions
- Reject suggestions that change technical meaning, metrics, company/product names, proper nouns, or the compact bullet style
- Avoid adding full stops to bullets if the resume style guide says bullets should not end with full stops
- Save a timestamped source/PDF after the Grammarly-reviewed edits
- Rerun `scripts/validate_cv.py` after edits to catch layout or extraction drift

Grammarly has developer-facing APIs for organizations and business workflows, but open-source local usage is usually better served by a deterministic script plus a manual Grammarly pass unless the user has enterprise API credentials.

## LanguageTool Gate

LanguageTool is useful for automated grammar checks because it provides a documented HTTP API and can be self-hosted.

```bash
python3 scripts/check_grammar.py resume.html --provider languagetool
python3 scripts/check_grammar.py resume.html --provider languagetool --url http://localhost:8081/v2/check
```

Use a local/self-hosted endpoint for private resumes when possible.

## Offline Gate

The offline gate catches deterministic hygiene issues without sending resume text anywhere:

```bash
python3 scripts/check_grammar.py resume.html --provider offline
```

It checks repeated words, spacing before punctuation, and a small fallback typo list. It is intentionally conservative and should be combined with `spellchecker`, LanguageTool, human review, or Grammarly for final submissions.

## Dictionary Spellcheck Gate

Use this when you want generalized typo detection without sending resume text to a remote service:

```bash
python3 scripts/check_grammar.py resume.html --provider spellchecker --dictionary references/resume-dictionary.txt
```

Keep adding domain terms to `references/resume-dictionary.txt` so proper nouns, products, libraries, and internal project names do not become false positives.

## Review Policy

- Grammar tools are advisory
- Preserve exact technical names and capitalization
- Preserve metrics unless the source data changes
- Preserve compact bullet style when requested
- Do not accept rewrites that make bullets vague or less defensible
- Rerun line-width, page-fill, PDF render, and extraction checks after grammar edits

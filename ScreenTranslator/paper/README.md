# Thesis

Bachelor's thesis in Russian, written in Markdown and exported to Word
with Pandoc (3.x). Headings, tables, figure captions and references are in
English; the body text is Russian.

## Build

```bash
pandoc paper/thesis_outline_ru.md \
  -o paper/thesis_final.docx \
  --reference-doc paper/reference.docx \
  --lua-filter paper/loose-lists.lua \
  --syntax-highlighting=none \
  --shift-heading-level-by=-1 --toc --toc-depth=2 \
  --resource-path=paper \
  --bibliography paper/refs.bib \
  --csl paper/harvard.csl \
  --citeproc
```

Open the result in Word and update the table of contents when asked.

## Files

- `thesis_outline_ru.md` — thesis source. Title, author and abstract are in
  the YAML block at the top.
- `refs.bib` — bibliography; `harvard.csl` — Cite Them Right (Harvard)
  style, CC BY-SA 3.0, with a local override that prints citations and the
  reference list in English.
- `figures/` — Figures 4.1 and 6.1–6.5; `figures/make_figures.py` rebuilds
  them from `study/evaluation/`.
- `reference.docx` — Word template (Times New Roman, 12 pt body at 1.5
  spacing, 18/14/12 pt bold headings, 10 pt bibliography, page breaks
  before the abstract, contents, chapters and references); rebuilt by
  `make_reference_docx.py`.
- `loose-lists.lua` — Pandoc filter that gives list items body-text
  spacing.

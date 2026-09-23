# Annotation notes — DRAFT

## eval-v2 re-score (2026-09-23, build `af1236c`)

`units.csv` now scores the **eval-v2** captures; `units_eval-v1.csv` keeps the
v1 scores (`87500c1`). Source units are unchanged: the v2 source screenshots
of the three menus are pixel-identical to v1, and the only changed source
line is the Settings storage summary (61 % → 62 %, 6,19 → 6,10 ГБ), which
the device itself changed. Two menu_ru v2 runs were invalid (Photos showed
another menu) and are marked INVALID in `runs.csv`.

| Case | Usable coverage v1 → v2 | Correct / detected v1 → v2 | Spurious cards on English/excluded text v1 → v2 |
|---|---|---|---|
| settings_ru | 12/17 → 12/17 | 13/17 → 13/17 | 0 → 0 |
| menu_ru | 1/102 → 2/102 | 20/62 → 22/60 | 0 → 0 |
| menu_fr | 2/20 → 2/20 | 6/20 → 6/20 | 12 → 1 |
| menu_de | 0/2 → 0/2 | 0/2 → 0/2 | 2 → 0 |
| english_control | — | — | 0 → 0 |

The Phase 0 routing rules removed almost all garbage cards (14 → 1) without
lowering coverage. menu_ru readings vary between runs of the same image
(OCR region cap and Tesseract crop variants), so its per-unit detections
changed in both directions; placement remains the dominant failure.

## News cases (2026-09-23, build `af1236c`)

`browser_es` = Wikipedia es "Café" rev 175479450, `browser_ru` = ru "Кофе"
rev 153564774, mobile site, top of article. Chrome was set to "Never
translate" Spanish and Russian so its own translate bar does not cover the
page. The two pages took different paths: Spanish went through OCR (first
pass 3.7 s), Russian through Chrome's accessibility tree (first pass
14.3 s, 42 nodes). Chrome builds its web accessibility tree lazily after a
service connects, so the path can depend on timing. The a11y path does not
log per-node text; its cards were scored from `output.png`. Chrome also
exposes icon labels, which produced six spurious icon cards on the Russian
page ("Tongue" for the language icon).

## Decisions

1. **Tiny text counts (author, 2026-09-23).** menu_ru keeps all 102 units,
   including h≈13 px body and h≈9 px small lines.
2. menu_de as a control — open.
3. Dish-name eligibility — as drafted unless the author changes it.

## eval-v1 notes

`units_eval-v1.csv` rows for `menu_ru`, `menu_fr`, `menu_de`, `settings_ru` and
`english_control` (captures of build `87500c1`) are a **draft by Claude,
pending review by the author**. The draft was not blind: the annotator had
already seen the overlay screenshots before listing source units. Before
publishing numbers, re-check the unit list against each `source.png`. No
second reader is available (author decision 2026-09-23): the thesis reports
single-annotator labels and states that agreement was not measured.

## Scoring rules applied

- **Unit** = one visible text line (or separately bounded label). A dish
  whose name wraps is two units; each is judged by the combined output.
- **detected** = a logged OCR region or card covers the unit's location in
  the final OCR pass of `pipeline.log` (for `settings_ru`, the a11y
  fast-path card visible in `output.png`). An `[und]`/`[en]` region with no
  card still counts as detected, with `correct=0`.
- **correct** = the translation text in the log keeps the item's important
  meaning (dish type and main ingredient for menus). One garbled modifier
  with the dish still clear is marked `BORDERLINE` in notes and scored 1;
  flip these if you prefer a stricter rule.
- **placed** = that translation is readable at the unit's location and does
  not hide another unit, including English description lines. Clipped or
  covered cards, and cards taller than the line pitch, score 0.
- `eligible=0` rows are English text (and `DISPUTED` exclusions such as
  proper names and German dish names). `detected=1` on these means a card
  sits on text that needed none; `score_quality.py` reports them in the
  "Control units with cards" column.

## Decisions for the author

1. **Readability threshold (menu_ru).** Body text is about 13 px tall at
   the fit-to-screen viewport (~0.7 mm on a Pixel 7) and small print about
   9 px. The protocol excludes text "too small for a human to read at the
   captured zoom". The draft includes every line legible in the screenshot
   pixels and records `h≈` in notes. Either keep that, or exclude `h≈13px`
   and `h≈9px` rows. With the second choice, fix a zoomed viewport for v2
   so the case keeps a real denominator.
2. **menu_de has 2 eligible units.** Its German text is dish names that
   English menus keep unchanged; the rest is English. It is useful as a
   false-positive case, but it distorts the equal-case macro average.
   Consider reporting it with the controls, or replacing it in protocol v2.
3. **Dish-name eligibility.** Excluded as normally unchanged: Quiche
   Vichyssoise, Boeuf Bourguignon, CAFÉ BIGOT ROUGE and the German
   sausage names. Russian transliterated dish names (Вителло Тонато,
   Аджапсандали) are eligible, because Cyrillic is unreadable to the
   target reader.

## Failure patterns seen while scoring (hypotheses for W16, not fixes)

- **Russian-first fallback on Latin text.** For suspect regions,
  `recognizeRussianComicText` runs before the eng+rus reader, and
  `acceptRussianReading` accepts any 4+ Cyrillic letters. The rus-only
  model always emits Cyrillic, so English and French lines become garbage
  cards ("and tuna." → "ADF Kipa.", "FRENCH MENU" → "Erkemsn Memo",
  Photos "Delete" → "Island! £! Is,").
- **Card height vs line pitch.** On dense menus the cards are drawn about
  3× taller than the 13–17 px lines, so neighbouring cards stack and hide
  each other; menu_ru detects 61% of units but places 1%.
- **Region cap.** menu_ru produced 168 OCR regions; `MAX_LOG_LINES = 120`
  processed only the first 120.
- **Price-column merges.** Regions spanning item and price columns yield
  cards like "th choto 390 @ rolls".
- **NMT word choice on UI strings.** Поиск настроек → "CREDICAL",
  Уведомления → "Alert", Хранилище → "Repository".

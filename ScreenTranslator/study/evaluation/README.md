# W13/W16 fixed evaluation set — protocol v1

This directory defines the quality test set before further Android changes. It
does not turn the earlier menu estimates into measured recall. Keep this
protocol and the source annotations stable when comparing builds. Add a new
version rather than silently changing a case or its denominator.

## Cases

`cases.csv` is the fixed case list. The three menu cases have source images
and historical output screenshots in `../menu_findings/`; those screenshots
are **pilot artifacts**, not a current-build result. The remaining cases need
source screens and output captures. Record the exact app, URL or local asset,
locale, viewport, zoom and focused-language setting in the case notes before
capture. A screenshot and its CSV trace must come from the same run and build.

The set includes Latin and Cyrillic content across image viewers, native UI,
browser, chat, map, game and PDF. English source text is a negative control:
it should not acquire translation cards.

**Cut from v1 (author decision, 2026-09-23):** `chat_es`, `map_fr`,
`game_ru` and `pdf_fr` were not captured and are excluded from the v1
results; `cases.csv` marks them `cut`. The v1 results therefore cover
images (menus), native UI (Settings), browser (Wikipedia) and the English
control only. State this in the thesis rather than generalising to chat,
map, game or PDF content. A case that cannot be reproduced must
be marked unavailable with a reason; do not substitute an easier screen.

## Capture procedure

1. Record build SHA, emulator/device model, Android version, display size,
   target language (English), app package, source asset/URL and network/model
   state in `runs.csv`. Use one row per case and run.
2. Start the app and wait for on-device models to be ready. Capture a warm
   quality screenshot after the screen has stopped changing and the overlay
   has settled. Save the matching raw source screenshot without cards. Keep
   the source at the specified zoom and scroll position.
3. Save the matching `frames.csv` excerpt. Cold-start/model-download trials
   are separate latency trials; do not mix them into warm quality scores.
4. Annotate **every eligible visible source unit** in `units.csv` from the raw
   source screenshot before looking at the overlay result. Use a short text
   line or a separately bounded UI label as one unit. If one card translates
   two lines, each source line still gets its own row. If one line is split
   across cards, judge its combined visible output.
5. A second pass scores the output screenshot. Keep the original source unit
   text, approximate bounds, observed card text and a short reason for any
   failure. If possible, have a second Russian/English reader independently
   score the Cyrillic cases and resolve disagreements in notes.

### Scripted capture

`scripts/eval_capture.py` performs steps 1–3 for one case over adb, using
the launch recipe, expected locale and viewport in `capture_plan.csv`:

```bash
python3 scripts/eval_capture.py --list        # cases and capture status
python3 scripts/eval_capture.py menu_ru       # one case
python3 scripts/eval_capture.py all-auto      # every non-manual case
```

It refuses a `.dirty` APK or one whose `android/` sources differ from
`HEAD` (the git SHA is stamped into `versionName`), a device locale other
than the plan's, and a missing translation model (a cold run). It turns
the accessibility service off, opens the source, saves `source.png`, turns
the service on, sets the case's focus through the debug-only
`EvalControlReceiver`, and waits until no new pipeline pass and no pixel
change (below the status bar) has occurred for 4 s. It then saves
`output.png`, the matching `frames.csv` rows and `pipeline.log` under
`captures/<case_id>/<UTC time>/`, appends one `runs.csv` row and restores
the previous accessibility setting. The service reconnects before every
capture, so each quality run starts with warm models and empty caches.
`manual` cases pause while you open the exact screen; record the URL or
viewer and zoom with `--notes`. A run that times out before settling is
still recorded, with `settled=NO` in its notes; do not score it as a warm
quality run.

The script only captures. Annotating `units.csv` stays manual (step 4).

## Eligibility and scoring

Include visible non-English text that an English reader needs to understand:
headings, menu item names/descriptions, messages, labels and map names when
translation is meaningful. Count repeated visible occurrences separately.
Exclude prices, numerals, URLs, decorative logos, already-English text and
proper names whose English rendering is normally unchanged. Record excluded
items only when their exclusion could be disputed. Do not count text outside
the visible viewport or source text too small for a human to read at the
captured zoom. Do not move a unit out of the denominator because OCR missed it.

For each eligible unit, `detected=1` means a card or logged OCR region covers
the correct source location. `correct=1` requires a readable English rendering
that preserves the important meaning; a garbled, truncated, or misleading
translation is 0. `placed=1` means the readable translation appears at the
source location without hiding another scored unit. A unit passes only when
all three are 1. For English negative-control cases, enter `eligible=0` rows
for visible English units and count cards over them as false positives.

The primary metric is **usable coverage** = passing eligible units / all
eligible units. Report per-case numerator and denominator, and both pooled
micro and equal-case macro coverage. Also report detection coverage, semantic
accuracy among detected units, placement success, and English control units
with spurious cards. Count distinct spurious cards separately during visual
review if multiple units share a card. `n_cards / ocr_raw` is not a capture
rate: neither value counts
ground-truth source units.

Run `python3 scripts/score_quality.py study/evaluation/units.csv` from the
repository root. The script refuses an empty annotation set and incomplete
scores. Do not publish a percentage for an unannotated case.

## Interpretation

The older `../menu_findings/RECALL.md` estimates are useful hypotheses, but
its 17 French cards and 109 Russian cards must not be interpreted as correct
translations. The French source itself contains substantial English copy,
and the historical overlay also puts cards on some English text. This fixed
set will determine whether the stated 90% target is reached on each script
and category. Report failures rather than averaging them away.

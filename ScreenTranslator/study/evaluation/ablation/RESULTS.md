# Ablation study (2026-09-23)

One component switched off at a time through debug-only `EvalFlags`
(build `7bde7ad`; with all flags on it runs the `eval-v2` code). Quality:
fresh captures in `captures/`, scored against the unchanged source units in
`units.csv` (baseline = `study/evaluation/units.csv`, whose eval-v2 outputs
matched the same-session all-on captures pixel for pixel on both menus and
differed only in status/badge pixels elsewhere). Latency: 10 first-view
passes per configuration (`latency/`), all-on measured in the same session.
`browser_es` latency rows force the OCR path (`a11y=0`) because Chrome
exposes the article once its accessibility tree is built; its quality
captures took the OCR path on their own. Five runs affected by a flag-order
bug are kept in `runs.csv` marked INVALID and were re-captured.

| Component off | Case | Quality: all on → off | Latency p50 (p95), ms: all on → off |
|---|---|---|---|
| Accessibility fast path | settings_ru | 12/17 usable · 13 correct · 17 detected · 0 spurious → **11/17 usable · 11 correct · 17 detected · 0 spurious** | 292 (414) → 917 (1081) |
| Accessibility fast path | browser_ru | 7/20 usable · 9 correct · 17 detected · 6 spurious → **15/20 usable · 15 correct · 20 detected · 0 spurious** | 603 (746) → 1591 (1828) |
| Multi-scale OCR | menu_ru | 2/102 usable · 22 correct · 60 detected · 0 spurious → **2/102 usable · 24 correct · 43 detected · 0 spurious** | 4544 (6925) → 3494 (3838) |
| Multi-scale OCR | menu_fr | 2/20 usable · 6 correct · 20 detected · 1 spurious → **2/20 usable · 6 correct · 20 detected · 1 spurious** | 1453 (1771) → 1318 (2421) |
| Multi-scale OCR | browser_es | 12/19 usable · 12 correct · 19 detected · 0 spurious → **12/19 usable · 12 correct · 19 detected · 0 spurious** | 1257 (1618) → 1179 (1664) |
| Tesseract fallback | menu_ru | 2/102 usable · 22 correct · 60 detected · 0 spurious → **0/102 usable · 0 correct · 69 detected · 0 spurious** | 4544 (6925) → 2095 (2299) |
| Tesseract fallback | menu_fr | 2/20 usable · 6 correct · 20 detected · 1 spurious → **2/20 usable · 6 correct · 20 detected · 1 spurious** | 1453 (1771) → 726 (926) |
| Tesseract fallback | browser_es | 12/19 usable · 12 correct · 19 detected · 0 spurious → **12/19 usable · 12 correct · 18 detected · 0 spurious** | 1257 (1618) → 871 (1133) |
| Language focus | menu_ru | 2/102 usable · 22 correct · 60 detected · 0 spurious → **1/102 usable · 11 correct · 69 detected · 0 spurious** | 4544 (6925) → 2580 (3056) |
| Language focus | browser_ru | 7/20 usable · 9 correct · 17 detected · 6 spurious → **7/20 usable · 9 correct · 17 detected · 6 spurious** | 603 (746) → 568 (894) |

**Readings.**
- *Accessibility fast path*: 3× faster (Settings 292 → 917 ms, Wikipedia
  603 → 1 591 ms without it). Quality depends on the app: on Settings it is
  about equal (12 vs 11 usable; each path makes different NMT word errors),
  but on Wikipedia the OCR path is better (15 vs 7 usable, 0 vs 6 spurious
  icon cards) because Chrome's accessibility nodes split lines into link
  fragments and expose icon labels.
- *Multi-scale OCR*: no quality change on the Latin pages; on the Russian
  menu it adds detections (43 → 60) but not correct lines (24 → 22), for
  about 1 s more per pass (3 494 → 4 544 ms).
- *Tesseract fallback*: essential for Cyrillic images (Russian menu 22 → 0
  correct lines without it) and irrelevant to Latin quality, where it only
  costs time (French menu 726 → 1 453 ms) and occasionally adds a wrong
  card ("Hair Wari Ya.").
- *Language focus*: doubles correct lines on the Russian menu (11 → 22) at
  a latency cost (2 580 → 4 544 ms); no effect on the accessibility path.

Single emulator runs per quality configuration; menu outputs are
deterministic (repeat captures were pixel-identical), but timings vary
between sessions by roughly 10–30 % (compare `../latency/`).

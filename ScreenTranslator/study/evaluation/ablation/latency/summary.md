# Latency run

Build `7bde7ad`, emulator (Pixel 7 profile, Android 14, Apple Silicon host), warm models unless the scenario is `cold`. Times in ms, nearest-rank percentiles.

| Scenario | Case | Path | n | Total p50 | Total p95 | Max | Harvest p50 | OCR p50 | LID+NMT p50 | Overlay p50 | Cards (median) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| first_view | settings_ru | a11y_full | 10 | 292 | 414 | 414 | 7 | 0 | 112 | 22 | 15 |
| first_view [a11y=0] | settings_ru | ocr_full | 10 | 917 | 1081 | 1081 | 93 | 260 | 417 | 1 | 13 |
| first_view | menu_fr | ocr_full | 10 | 1453 | 1771 | 1771 | 25 | 494 | 734 | 1 | 12 |
| first_view [multiscale=0] | menu_fr | ocr_full | 10 | 1318 | 2421 | 2421 | 22 | 294 | 849 | 1 | 15 |
| first_view [tesseract=0] | menu_fr | ocr_full | 10 | 726 | 926 | 926 | 26 | 465 | 81 | 0 | 10 |
| first_view | menu_ru | ocr_full | 10 | 4544 | 6925 | 6925 | 38 | 738 | 3548 | 2 | 77 |
| first_view [multiscale=0] | menu_ru | ocr_full | 10 | 3494 | 3838 | 3838 | 32 | 413 | 2922 | 1 | 67 |
| first_view [tesseract=0] | menu_ru | ocr_full | 10 | 2095 | 2299 | 2299 | 35 | 640 | 1236 | 1 | 9 |
| first_view [focus=0] | menu_ru | ocr_full | 10 | 2580 | 3056 | 3056 | 27 | 533 | 1858 | 1 | 39 |
| first_view | browser_ru | a11y_full | 10 | 603 | 746 | 746 | 129 | 0 | 167 | 40 | 25 |
| first_view [a11y=0] | browser_ru | ocr_full | 10 | 1591 | 1828 | 1828 | 136 | 361 | 902 | 1 | 20 |
| first_view [focus=0] | browser_ru | a11y_full | 10 | 568 | 894 | 894 | 121 | 0 | 151 | 32 | 25 |
| first_view [a11y=0] | browser_es | ocr_full | 10 | 1257 | 1618 | 1618 | 237 | 318 | 539 | 1 | 12 |
| first_view [a11y=0,multiscale=0] | browser_es | ocr_full | 10 | 1179 | 1664 | 1664 | 269 | 274 | 488 | 1 | 12 |
| first_view [a11y=0,tesseract=0] | browser_es | ocr_full | 10 | 871 | 1133 | 1133 | 264 | 316 | 155 | 1 | 12 |

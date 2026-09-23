# Ablation study 



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



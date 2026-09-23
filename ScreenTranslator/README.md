# ScreenTranslator

Real-time, on-device screen translation for Android, built for a bachelor's
thesis. An `AccessibilityService` reads the text of the current screen —
from the accessibility tree or from a screenshot with OCR (ML Kit for Latin
script, Tesseract for Cyrillic) — translates it into English with ML Kit
Translate and draws translation cards over the original text in a
`TYPE_ACCESSIBILITY_OVERLAY` window. Nothing leaves the device.

## Repository

```
android/          Android app (Kotlin), unit and instrumented tests
ios/              iOS companion (SwiftUI): text recognition only, no translation
paper/            Thesis source (Russian Markdown), bibliography, figures, Word template
scripts/          Evaluation tools: capture, latency runs, scoring, Tesseract download
study/evaluation/ Evaluation protocol, annotations, runs, latency and ablation data
study/menu_findings/  Source menu images used by the evaluation
ScreenTranslator-ML/   Paused work on a custom Cyrillic OCR model (data preparation only)
```

## Build and run (Android)

Requirements: Android Studio / JDK 17+, Android SDK 37, a device or emulator
with Android 11+ (API 30+) and Google Play services.

```bash
./scripts/download_tessdata.sh          # Tesseract models (not in git)
cd android
./gradlew :app:installDebug
```

Then enable the service: Settings → Accessibility → ScreenTranslator.

Tests:

```bash
cd android
./gradlew :app:testDebugUnitTest            # JVM tests
./gradlew :app:connectedDebugAndroidTest    # instrumented tests (emulator)
```

## Evaluation

The protocol and scoring rules are in `study/evaluation/README.md`.
Screens are captured with `scripts/eval_capture.py`, latency with
`scripts/latency_run.py`, and quality is scored with
`scripts/score_quality.py study/evaluation/units.csv`. All measurements
were taken on the Android emulator (Pixel 7 profile, Android 14).

## ScreenTranslator-ML

Python package (`pip install -e .` inside the folder) with synthetic data
generation, real-screenshot capture, Label Studio export and PyTorch
datasets for a custom Cyrillic text detector and recogniser. Training was
not started; the thesis uses Tesseract for Cyrillic instead (chapter 8).
Fonts, the full Wikipedia corpus and generated data are not in git:
`scripts/download_fonts.py`, `scripts/download_ru_wiki.py` and
`scripts/generate_synthetic.py` recreate them. Tests: `pytest`.


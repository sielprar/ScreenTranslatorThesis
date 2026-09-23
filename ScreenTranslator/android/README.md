# Android app

Kotlin, `minSdk` 30 (Android 11, the first version with
`AccessibilityService.takeScreenshot()`), `compileSdk` 37.

```
app/src/main/java/com/screentranslator/android/
├── MainActivity.kt        Onboarding screen and link to accessibility settings
├── service/               Accessibility service: events, path choice, caches, focus
├── pipeline/              OCR, Tesseract, accessibility-tree walk, language ID,
│                          translation, routing rules, hash, card style, benchmark log
└── overlay/               Translation cards and the language-focus chip
app/src/debug/             EvalControlReceiver: adb hooks for the evaluation (debug only)
```

Dependencies: ML Kit Text Recognition v2, Language ID, Translate;
Tesseract4Android; Kotlin coroutines.

Before the first build, download the Tesseract models with
`../scripts/download_tessdata.sh`.

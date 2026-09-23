# iOS companion

SwiftUI app with three text-recognition surfaces: camera (VisionKit
`DataScannerViewController`), photo picker and a Share extension (Vision
`VNRecognizeTextRequest`). It recognises text but does not translate it.
Work on iOS was stopped because third-party apps cannot read or draw over
other apps on iOS; see chapter 3 of the thesis.

Open `ScreenTranslator/ScreenTranslator.xcodeproj` in Xcode. The camera
view needs a physical iPhone; the simulator has no camera.

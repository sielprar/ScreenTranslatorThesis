import SwiftUI
import VisionKit

struct CameraView: View {
    var body: some View {
        if DataScannerViewController.isSupported && DataScannerViewController.isAvailable {
            DataScannerRepresentable()
                .ignoresSafeArea()
        } else {
            unavailable
        }
    }

    private var unavailable: some View {
        VStack(spacing: 16) {
            Image(systemName: "camera.fill")
                .font(.system(size: 60))
                .foregroundColor(.secondary)
            Text("Camera not available")
                .font(.title2)
            Text("Live camera translation requires a physical iPhone (iOS 16+). The iPhone Simulator has no camera — use the Photo tab to test OCR on selected images instead.")
                .multilineTextAlignment(.center)
                .foregroundColor(.secondary)
                .padding()
        }
        .padding()
    }
}

private struct DataScannerRepresentable: UIViewControllerRepresentable {
    func makeUIViewController(context: Context) -> DataScannerViewController {
        let scanner = DataScannerViewController(
            recognizedDataTypes: [.text()],
            qualityLevel: .balanced,
            recognizesMultipleItems: true,
            isHighFrameRateTrackingEnabled: true,
            isGuidanceEnabled: true,
            isHighlightingEnabled: true,
        )
        try? scanner.startScanning()
        return scanner
    }

    func updateUIViewController(_ uiViewController: DataScannerViewController, context: Context) {}
}

#Preview {
    CameraView()
}

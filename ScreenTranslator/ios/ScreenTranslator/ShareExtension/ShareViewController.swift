import SwiftUI
import UIKit
import UniformTypeIdentifiers
import Vision

final class ShareViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()

        let host = UIHostingController(
            rootView: ShareOCRView(
                extensionContext: extensionContext,
                onDone: { [weak self] in
                    self?.extensionContext?.completeRequest(returningItems: [], completionHandler: nil)
                },
            ),
        )

        addChild(host)
        host.view.frame = view.bounds
        host.view.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        view.addSubview(host.view)
        host.didMove(toParent: self)
    }
}

struct ShareOCRView: View {
    struct Observation: Identifiable {
        let id = UUID()
        let text: String
        let boundingBox: CGRect
    }

    let extensionContext: NSExtensionContext?
    let onDone: () -> Void

    @State private var image: UIImage?
    @State private var observations: [Observation] = []
    @State private var status: String = "Loading shared image…"

    var body: some View {
        NavigationStack {
            VStack {
                if let image {
                    GeometryReader { geo in
                        ZStack(alignment: .topLeading) {
                            Image(uiImage: image)
                                .resizable()
                                .aspectRatio(contentMode: .fit)
                                .frame(width: geo.size.width, height: geo.size.height)

                            ForEach(observations) { obs in
                                let box = viewRect(for: obs.boundingBox, in: geo.size, image: image)
                                Rectangle()
                                    .strokeBorder(Color.red, lineWidth: 2)
                                    .frame(width: box.width, height: box.height)
                                    .offset(x: box.minX, y: box.minY)
                            }
                        }
                    }
                } else {
                    Spacer()
                    Image(systemName: "photo")
                        .font(.system(size: 48))
                        .foregroundColor(.secondary)
                    Spacer()
                }

                Text(status)
                    .font(.footnote)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
                    .padding()
            }
            .navigationTitle("ScreenTranslator")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Done", action: onDone)
                }
            }
            .task {
                await loadAndRecognize()
            }
        }
    }

    private func loadAndRecognize() async {
        let loaded = await loadSharedImage()
        await MainActor.run {
            self.image = loaded
            self.status = loaded == nil ? "No image was shared." : "Running OCR…"
        }
        if let loaded {
            await recognize(loaded)
        }
    }

    private func loadSharedImage() async -> UIImage? {
        guard let items = extensionContext?.inputItems as? [NSExtensionItem] else { return nil }
        let imageType = UTType.image.identifier
        for item in items {
            for attachment in item.attachments ?? [] where attachment.hasItemConformingToTypeIdentifier(imageType) {
                return await withCheckedContinuation { continuation in
                    attachment.loadItem(forTypeIdentifier: imageType, options: nil) { data, _ in
                        if let url = data as? URL,
                           let d = try? Data(contentsOf: url),
                           let img = UIImage(data: d) {
                            continuation.resume(returning: img)
                        } else if let img = data as? UIImage {
                            continuation.resume(returning: img)
                        } else if let d = data as? Data, let img = UIImage(data: d) {
                            continuation.resume(returning: img)
                        } else {
                            continuation.resume(returning: nil)
                        }
                    }
                }
            }
        }
        return nil
    }

    private func recognize(_ uiImage: UIImage) async {
        guard let cgImage = uiImage.cgImage else {
            await MainActor.run { status = "Image has no CGImage." }
            return
        }

        let request = VNRecognizeTextRequest()
        request.recognitionLevel = .accurate
        request.usesLanguageCorrection = true
        request.recognitionLanguages = [
            "en-US", "ru-RU", "ja-JP", "zh-Hans", "ar-SA", "es-ES", "fr-FR",
        ]

        let orientation = cgOrientation(from: uiImage.imageOrientation)
        let handler = VNImageRequestHandler(cgImage: cgImage, orientation: orientation, options: [:])
        do {
            try handler.perform([request])
        } catch {
            await MainActor.run { status = "OCR failed: \(error.localizedDescription)" }
            return
        }

        let results = request.results ?? []
        let obs: [Observation] = results.compactMap { obs in
            guard let text = obs.topCandidates(1).first?.string else { return nil }
            return Observation(text: text, boundingBox: obs.boundingBox)
        }

        await MainActor.run {
            self.observations = obs
            self.status = obs.isEmpty
                ? "No text found."
                : "Found \(obs.count) region(s): " + obs.map(\.text).joined(separator: " | ")
        }
    }

    private func viewRect(for boxNormalized: CGRect, in geometry: CGSize, image: UIImage) -> CGRect {
        let imageSize = image.size
        guard imageSize.width > 0 && imageSize.height > 0 else { return .zero }
        let scale = min(geometry.width / imageSize.width, geometry.height / imageSize.height)
        let displaySize = CGSize(width: imageSize.width * scale, height: imageSize.height * scale)
        let offsetX = (geometry.width - displaySize.width) / 2
        let offsetY = (geometry.height - displaySize.height) / 2

        let x = boxNormalized.minX * displaySize.width + offsetX
        let width = boxNormalized.width * displaySize.width
        let height = boxNormalized.height * displaySize.height
        let y = (1 - boxNormalized.maxY) * displaySize.height + offsetY
        return CGRect(x: x, y: y, width: width, height: height)
    }

    private func cgOrientation(from ui: UIImage.Orientation) -> CGImagePropertyOrientation {
        switch ui {
        case .up: return .up
        case .down: return .down
        case .left: return .left
        case .right: return .right
        case .upMirrored: return .upMirrored
        case .downMirrored: return .downMirrored
        case .leftMirrored: return .leftMirrored
        case .rightMirrored: return .rightMirrored
        @unknown default: return .up
        }
    }
}

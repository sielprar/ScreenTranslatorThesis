import PhotosUI
import SwiftUI
import Vision

struct PhotoOCRView: View {
    struct Observation: Identifiable {
        let id = UUID()
        let text: String
        let boundingBox: CGRect
    }

    @State private var selectedItem: PhotosPickerItem?
    @State private var image: UIImage?
    @State private var observations: [Observation] = []
    @State private var status: String = "Pick a photo to run OCR."

    var body: some View {
        VStack(spacing: 16) {
            PhotosPicker(selection: $selectedItem, matching: .images) {
                Label("Pick a photo", systemImage: "photo.on.rectangle.angled")
            }
            .buttonStyle(.borderedProminent)

            if let image {
                GeometryReader { geometry in
                    ZStack(alignment: .topLeading) {
                        Image(uiImage: image)
                            .resizable()
                            .aspectRatio(contentMode: .fit)
                            .frame(width: geometry.size.width, height: geometry.size.height)

                        ForEach(observations) { obs in
                            let box = viewRect(for: obs.boundingBox, in: geometry.size, image: image)
                            Rectangle()
                                .strokeBorder(Color.red, lineWidth: 2)
                                .frame(width: box.width, height: box.height)
                                .offset(x: box.minX, y: box.minY)
                        }
                    }
                }
            } else {
                Spacer()
            }

            Text(status)
                .font(.footnote)
                .foregroundColor(.secondary)
                .padding(.horizontal)
                .multilineTextAlignment(.center)
        }
        .padding()
        .onChange(of: selectedItem) { item in
            guard let item else { return }
            Task { await loadAndRecognize(item) }
        }
    }

    private func loadAndRecognize(_ item: PhotosPickerItem) async {
        await MainActor.run {
            status = "Loading image…"
            observations = []
        }
        guard let data = try? await item.loadTransferable(type: Data.self),
              let uiImage = UIImage(data: data) else {
            await MainActor.run { status = "Could not load image." }
            return
        }
        await MainActor.run {
            self.image = uiImage
            self.status = "Running OCR…"
        }
        await recognize(uiImage)
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

#Preview {
    PhotoOCRView()
}

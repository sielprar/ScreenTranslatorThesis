import SwiftUI

struct ContentView: View {
    var body: some View {
        TabView {
            CameraView()
                .tabItem { Label("Camera", systemImage: "camera") }

            PhotoOCRView()
                .tabItem { Label("Photo", systemImage: "photo") }
        }
    }
}

#Preview {
    ContentView()
}

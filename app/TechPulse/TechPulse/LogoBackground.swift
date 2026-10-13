import SwiftUI

struct LogoBackground: ViewModifier {
    func body(content: Content) -> some View {
        content
            .background {
                Color.black
                    .overlay(
                        Image("bgLogo")
                            .resizable()
                            .scaledToFill()
                            .opacity(0.25)
                    )
                    .ignoresSafeArea()
            }
    }
}

extension View {
    func logoBackground() -> some View { modifier(LogoBackground()) }
}

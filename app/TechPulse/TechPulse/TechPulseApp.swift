//
//  TechPulseApp.swift
//  TechPulse
//
//  Created by Abraham Manu on 10/2/26.
//

import SwiftUI

@main
struct TechPulseApp: App {
    init() {
        let appearance = UINavigationBarAppearance()
        appearance.configureWithOpaqueBackground()
        appearance.backgroundColor = .black
        if let large = UIFont(name: "MajorMonoDisplay-Regular", size: 17) {
            appearance.largeTitleTextAttributes = [.font: large, .foregroundColor: UIColor.white]
        }
        if let small = UIFont(name: "MajorMonoDisplay-Regular", size: 17) {
            appearance.titleTextAttributes = [.font: small, .foregroundColor: UIColor.white]
        }
        UINavigationBar.appearance().standardAppearance = appearance
        UINavigationBar.appearance().scrollEdgeAppearance = appearance
    }

    var body: some Scene {
        WindowGroup {
            ContentView().preferredColorScheme(.dark)
        }
    }
}

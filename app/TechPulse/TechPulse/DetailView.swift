//
//  DetailView.swift
//  TechPulse
//
//  Created by Abraham Manu on 10/2/26.
//

import SwiftUI

struct DetailView: View {
    let item: NewsItem
    @State private var deepDive: String?
    @State private var isLoading = false
    @State private var failed = false

    func loadDeepDive() {
        Task {
            isLoading = true
            failed = false
            do {
                let text = try await fetchDeepDive(for: item)
                if text.isEmpty || text == "No response." {
                    failed = true                 // don't cache a failure
                } else {
                    deepDive = text
                    storeDeepDive(text, for: item.id)
                }
            } catch {
                failed = true
            }
            isLoading = false
        }
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 12) {
                Text(item.title).font(.title2).bold()
                Text(item.source).font(.subheadline).foregroundStyle(.secondary)
                Text(item.summary).font(.body)
                Link("Read full article", destination: URL(string: item.url)!).padding(.top)

                Divider().padding(.vertical, 8)

                if isLoading {
                    ProgressView()
                } else if let deepDive {
                    Text(deepDive).font(.body)
                } else if failed {
                    Text("Couldn't load more details.")
                        .foregroundStyle(.secondary)
                    Button("Try Again") { loadDeepDive() }
                        .buttonStyle(.borderedProminent)
                } else {
                    Button("Tell me more") { loadDeepDive() }
                        .buttonStyle(.borderedProminent)
                }
            }
            .padding()
        }
        .navigationTitle(item.category.capitalized)
        .navigationBarTitleDisplayMode(.inline)
        .logoBackground()
        .task {
            if let cached = cachedDeepDive(for: item.id) {
                if cached.isEmpty || cached == "No response." {
                    clearDeepDive(for: item.id)   // purge the bad cache from before the fix
                } else {
                    deepDive = cached
                }
            }
        }
    }
}

func clearDeepDive(for id: String) {
    UserDefaults.standard.removeObject(forKey: "deepdive-\(id)")
}

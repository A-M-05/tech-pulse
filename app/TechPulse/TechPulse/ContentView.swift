//
//  ContentView.swift
//  TechPulse
//
//  Created by Abraham Manu on 10/2/26.
//

import SwiftUI

struct ContentView: View {
    @State private var items: [NewsItem] = []

    var body: some View {
        NavigationStack {
            Group {
                if items.isEmpty {
                    ProgressView("Loading…")
                } else {
                    List {
                        Text("tech pulse")
                            .font(.custom("MajorMonoDisplay-Regular", size: 40))
                            .foregroundStyle(.white)
                            .padding(.vertical, 8)
                            .listRowBackground(Color.clear)
                            .listRowSeparator(.hidden)

                        ForEach(items) { item in
                            NavigationLink {
                                DetailView(item: item)
                            } label: {
                                VStack(alignment: .leading, spacing: 4) {
                                    Text(item.title).font(.headline)
                                    Text(item.source).font(.caption).foregroundStyle(.secondary)
                                    Text(item.summary).font(.subheadline)
                                }
                            }
                            .listRowBackground(Color.clear)   // let the watermark show behind rows
                        }
                    }
                    .scrollContentBackground(.hidden)
                }
            }
            .logoBackground()
            .navigationBarTitleDisplayMode(.inline)
            .task {
                do {
                    let digest = try await fetchDigest()
                    items = digest.items
                } catch {
                    print("Failed to load:", error)
                }
            }
        }
    }
}

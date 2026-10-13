//
//  TechPulseWidget.swift
//  TechPulseWidget
//
//  Created by Abraham Manu on 10/3/26.
//

import WidgetKit
import SwiftUI

struct NewsEntry: TimelineEntry {
    let date: Date
    let item: NewsItem?
}

struct Provider: TimelineProvider {
    func placeholder(in context: Context) -> NewsEntry {
        NewsEntry(date: Date(), item: nil)
    }

    func getSnapshot(in context: Context, completion: @escaping (NewsEntry) -> Void) {
        completion(NewsEntry(date: Date(), item: nil))
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<NewsEntry>) -> Void) {
        Task {
            var entries: [NewsEntry] = []
            do {
                let digest = try await fetchDigest()
                let items = Array(digest.items.prefix(10))
                let now = Date()
                for (i, item) in items.enumerated() {
                    // one entry per story, 2 min apart (shorter won't be honored reliably)
                    let date = Calendar.current.date(byAdding: .minute, value: i * 2, to: now)!
                    entries.append(NewsEntry(date: date, item: item))
                }
            } catch {
                entries = [NewsEntry(date: Date(), item: nil)]
            }
            // after the last entry, reload to fetch fresh stories
            completion(Timeline(entries: entries, policy: .atEnd))
        }
    }
}

struct TechPulseWidgetEntryView: View {
    var entry: NewsEntry

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text("TECH PULSE")
                .font(.caption2).bold()
                .foregroundStyle(.secondary)
            if let item = entry.item {
                Text(item.title)
                    .font(.headline)
                    .foregroundStyle(.white)
                    .lineLimit(3)
                Text(item.summary)
                    .font(.caption2)
                    .foregroundStyle(.white.opacity(0.8))
                    .lineLimit(4)
            } else {
                Text("Loading…").foregroundStyle(.white)
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
    }
}

struct TechPulseWidget: Widget {
    let kind: String = "TechPulseWidget"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: Provider()) { entry in
            TechPulseWidgetEntryView(entry: entry)
                .containerBackground(.black, for: .widget)
        }
        .configurationDisplayName("Tech Pulse")
        .description("Latest tech news summaries.")
        .supportedFamilies([.systemSmall, .systemMedium, .systemLarge])
    }
}

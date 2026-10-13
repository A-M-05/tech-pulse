#if !targetEnvironment(macCatalyst)
//
//  TechPulseWidgetLiveActivity.swift
//  TechPulseWidget
//
//  Created by Abraham Manu on 10/3/26.
//

import ActivityKit
import WidgetKit
import SwiftUI

struct TechPulseWidgetAttributes: ActivityAttributes {
    public struct ContentState: Codable, Hashable {
        // Dynamic stateful properties about your activity go here!
        var emoji: String
    }

    // Fixed non-changing properties about your activity go here!
    var name: String
}

struct TechPulseWidgetLiveActivity: Widget {
    var body: some WidgetConfiguration {
        ActivityConfiguration(for: TechPulseWidgetAttributes.self) { context in
            // Lock screen/banner UI goes here
            VStack {
                Text("Hello \(context.state.emoji)")
            }
            .activityBackgroundTint(Color.cyan)
            .activitySystemActionForegroundColor(Color.black)

        } dynamicIsland: { context in
            DynamicIsland {
                // Expanded UI goes here.  Compose the expanded UI through
                // various regions, like leading/trailing/center/bottom
                DynamicIslandExpandedRegion(.leading) {
                    Text("Leading")
                }
                DynamicIslandExpandedRegion(.trailing) {
                    Text("Trailing")
                }
                DynamicIslandExpandedRegion(.bottom) {
                    Text("Bottom \(context.state.emoji)")
                    // more content
                }
            } compactLeading: {
                Text("L")
            } compactTrailing: {
                Text("T \(context.state.emoji)")
            } minimal: {
                Text(context.state.emoji)
            }
            .widgetURL(URL(string: "http://www.apple.com"))
            .keylineTint(Color.red)
        }
    }
}

extension TechPulseWidgetAttributes {
    fileprivate static var preview: TechPulseWidgetAttributes {
        TechPulseWidgetAttributes(name: "World")
    }
}

extension TechPulseWidgetAttributes.ContentState {
    fileprivate static var smiley: TechPulseWidgetAttributes.ContentState {
        TechPulseWidgetAttributes.ContentState(emoji: "😀")
     }
     
     fileprivate static var starEyes: TechPulseWidgetAttributes.ContentState {
         TechPulseWidgetAttributes.ContentState(emoji: "🤩")
     }
}

#Preview("Notification", as: .content, using: TechPulseWidgetAttributes.preview) {
   TechPulseWidgetLiveActivity()
} contentStates: {
    TechPulseWidgetAttributes.ContentState.smiley
    TechPulseWidgetAttributes.ContentState.starEyes
}
#endif

//
//  TechPulseWidgetBundle.swift
//  TechPulseWidget
//
//  Created by Abraham Manu on 10/3/26.
//

import WidgetKit
import SwiftUI

@main
struct TechPulseWidgetBundle: WidgetBundle {
    var body: some Widget {
        TechPulseWidget()
        TechPulseWidgetControl()
        TechPulseWidgetLiveActivity()
    }
}

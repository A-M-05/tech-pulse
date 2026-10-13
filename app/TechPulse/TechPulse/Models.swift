//
//  Models.swift
//  TechPulse
//
//  Created by Abraham Manu on 10/2/26.
//

struct NewsItem : Codable, Identifiable{
    let id : String
    let title : String
    let source : String
    let url : String
    let published : String
    let summary : String
    let category : String
    let blurb : String
}

struct Digest: Codable{
    let generatedAt : String
    let items : [NewsItem]
}

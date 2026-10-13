//
//  NewsService.swift
//  TechPulse
//
//  Created by Abraham Manu on 10/2/26.
//

import Foundation

func fetchDigest() async throws -> Digest{
    let url = URL(string : "https://raw.githubusercontent.com/A-M-05/tech-pulse/main/output/digest.json")!
    let (data, _) = try await URLSession.shared.data(from : url)
    
    let decoder = JSONDecoder()
    decoder.keyDecodingStrategy = .convertFromSnakeCase
    return try decoder.decode(Digest.self, from : data)
}

struct DeepDiveResponse: Codable {
    let text: String
}

func fetchDeepDive(for item: NewsItem) async throws -> String {
    let url = URL(string: "https://techpulse-proxy.abrahammanu.workers.dev")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")

    let payload = ["title": item.title, "summary": item.summary]
    request.httpBody = try JSONEncoder().encode(payload)

    let (data, _) = try await URLSession.shared.data(for: request)
    return try JSONDecoder().decode(DeepDiveResponse.self, from: data).text
}

func cachedDeepDive(for id: String) -> String? {
    UserDefaults.standard.string(forKey: "deepdive-\(id)")
}

func storeDeepDive(_ text: String, for id: String) {
    UserDefaults.standard.set(text, forKey: "deepdive-\(id)")
}

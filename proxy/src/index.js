export default {
  async fetch(request, env) {
    if (request.method !== "POST") {
      return new Response("POST only", { status: 405 });
    }

    const { title, summary } = await request.json();
    const prompt = `Give more detail on this tech news story in 4-6 sentences — background and why it matters.
Title: ${title}
Summary: ${summary}`;

    const geminiURL =
      "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent";

    const r = await fetch(geminiURL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-goog-api-key": env.GEMINI_API_KEY,   // the secret, injected by Cloudflare
      },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: { maxOutputTokens: 2000 }
        }),
    });

    const data = await r.json();
    const parts = data?.candidates?.[0]?.content?.parts ?? [];
    const text = parts.map(p => p.text ?? "").join("").trim() || "No response.";

    return new Response(JSON.stringify({ text }), {
      headers: { "Content-Type": "application/json" },
    });
  },
};

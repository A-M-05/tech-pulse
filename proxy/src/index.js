export default {
  async fetch(request, env) {
    if (request.method !== "POST") {
      return new Response("POST only", { status: 405 });
    }

    const { title, summary } = await request.json();
    const prompt = `Give more detail on this tech news story in 4-6 sentences — background and why it matters.
Title: ${title}
Summary: ${summary}`;

    const model = "gemini-3.1-flash-lite";
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`;
    const body = JSON.stringify({
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: { maxOutputTokens: 2000 },
    });

    // retry on 503 ("high demand") with backoff
    let r;
    for (let attempt = 0; attempt < 3; attempt++) {
      r = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json", "x-goog-api-key": env.GEMINI_API_KEY },
        body,
      });
      if (r.ok || r.status !== 503) break;
      await new Promise(res => setTimeout(res, 800 * (attempt + 1)));
    }

    if (!r.ok) {
      const err = await r.text();
      return new Response(JSON.stringify({ text: `No response.` }),
        { headers: { "Content-Type": "application/json" } });
    }

    const data = await r.json();
    const parts = data?.candidates?.[0]?.content?.parts ?? [];
    const text = parts.map(p => p.text ?? "").join("").trim() || ("No response.");

    return new Response(JSON.stringify({ text }), {
      headers: { "Content-Type": "application/json" },
    });
  },
};

"use client";

import { useEffect, useState, type FormEvent } from "react";

const examples = ["A tiny house beside a pine tree", "A smiling sun over rolling hills", "A blue whale swimming under stars"];

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [svgUrl, setSvgUrl] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => () => { if (svgUrl) URL.revokeObjectURL(svgUrl); }, [svgUrl]);

  async function createDrawing(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!prompt.trim() || loading) return;
    setLoading(true);
    setError("");
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/svgdrawer`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt.trim() }),
      });
      if (!response.ok) throw new Error((await response.text()) || `Request failed (${response.status})`);
      const blob = await response.blob();
      if (!blob.type.includes("svg")) throw new Error("The server did not return an SVG image.");
      setSvgUrl((oldUrl) => { if (oldUrl) URL.revokeObjectURL(oldUrl); return URL.createObjectURL(blob); });
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Could not create the drawing. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="workspace">
      <header className="topbar"><a className="brand" href="#"><span className="brand-mark">✳</span> form<span>folk</span></a><span className="topbar-note">A little studio for vector ideas</span></header>
      <section className="hero">
        <div className="eyebrow"><span className="eyebrow-dot" /> PROMPT TO SVG</div>
        <h1>Make something<br /><em>shapely.</em></h1>
        <p className="intro">Describe a little illustration. Let AI build it from simple, editable vector shapes.</p>
      </section>
      <section className="studio" aria-label="SVG drawing studio">
        <form className="prompt-card" onSubmit={createDrawing}>
          <label htmlFor="prompt">What should we draw?</label>
          <textarea id="prompt" value={prompt} onChange={(event) => setPrompt(event.target.value)} placeholder="A cozy cabin tucked between tall mountains…" rows={3} maxLength={500} />
          <div className="prompt-bottom"><span>{prompt.length}/500</span><button type="submit" disabled={!prompt.trim() || loading}>{loading ? <><span className="spinner" /> Drawing</> : <>Draw it <span aria-hidden="true">↗</span></>}</button></div>
        </form>
        <div className="examples"><span>TRY ONE</span>{examples.map((example) => <button key={example} onClick={() => setPrompt(example)}>{example}</button>)}</div>
        <section className={`canvas-card${svgUrl ? " has-art" : ""}`} aria-label="Drawing preview">
          {svgUrl ? <><div className="canvas-toolbar"><span><i /> YOUR DRAWING</span><a href={svgUrl} download="formfolk-drawing.svg">Download SVG <span>↓</span></a></div><iframe title="Generated SVG preview" src={svgUrl} /></> : <div className="empty-state"><div className="empty-art" aria-hidden="true"><span className="sun" /><span className="hill hill-back" /><span className="hill hill-front" /><span className="flower flower-one">✳</span><span className="flower flower-two">✳</span></div><strong>Your canvas is waiting</strong><span>Your drawing will appear here</span></div>}
        </section>
        {error && <p role="alert" className="error-message">{error}</p>}
      </section>
      <footer>Made of shapes, made for you <span>✳</span></footer>
    </main>
  );
}

import { useState } from "react";

export default function Home() {
  const [title, setTitle] = useState("");
  const [narrative, setNarrative] = useState("");
  const [media, setMedia] = useState("");

  const createCase = async () => {
    const payload = {
      title,
      narrative,
      media: media.split(",").map(s => s.trim()).filter(Boolean),
      options: { run_cv: true, run_nlp: true }
    };
    const res = await fetch("http://localhost:8000/v1/cases", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data?.case_id) {
      window.location.href = `/results/${data.case_id}`;
    } else {
      alert("Error creating case");
    }
  };

  return (
    <main style={{ fontFamily: "sans-serif", padding: 20 }}>
      <h1>Desi Holmes — Upload Case</h1>
      <label>Title</label><br/>
      <input value={title} onChange={e=>setTitle(e.target.value)} style={{width:"60%"}}/><br/><br/>
      <label>Narrative</label><br/>
      <textarea rows={8} value={narrative} onChange={e=>setNarrative(e.target.value)} style={{width:"80%"}}></textarea><br/><br/>
      <label>Media URLs (comma separated)</label><br/>
      <input value={media} onChange={e=>setMedia(e.target.value)} style={{width:"80%"}}/><br/><br/>
      <button onClick={createCase}>Create Case</button>
    </main>
  );
}

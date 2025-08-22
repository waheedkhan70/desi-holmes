import { useState, useEffect } from "react";
import { useRouter } from "next/router";

export default function Results() {
  const router = useRouter();
  const { id } = router.query;
  const [result, setResult] = useState(null);

  useEffect(() => {
    if (!id) return;
    const poll = async () => {
      const res = await fetch(`http://localhost:8000/v1/cases/${id}/results`);
      if (res.ok) {
        const data = await res.json();
        // If data has content it's done
        if (data && (data.entities?.length || data.theories?.length || data.detections?.length)) {
          setResult(data);
        } else {
          setTimeout(poll, 1500);
        }
      } else {
        setTimeout(poll, 1500);
      }
    };
    poll();
  }, [id]);

  if (!result) return <div style={{padding:20}}>Waiting for results for case {id}...</div>;

  return (
    <main style={{padding:20}}>
      <h1>Results — {id}</h1>
      <h2>Theories</h2>
      {result.theories?.map(t => (
        <div key={t.id} style={{border:"1px solid #ddd", padding:10, marginBottom:8}}>
          <strong>{t.explanation?.summary}</strong> — score: {t.score}
          <pre>{JSON.stringify(t.explanation,null,2)}</pre>
        </div>
      ))}
      <h2>Entities</h2>
      <pre>{JSON.stringify(result.entities, null, 2)}</pre>
      <h2>Detections</h2>
      <pre>{JSON.stringify(result.detections, null, 2)}</pre>
    </main>
  );
}

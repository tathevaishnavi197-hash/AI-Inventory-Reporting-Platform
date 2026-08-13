"use client";

import { useEffect, useState } from "react";

export default function AIReport() {
  const [report, setReport] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/ai/inventory-report")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to generate AI report");
        }

        return response.json();
      })
      .then((result) => {
        setReport(result.report);
      })
      .catch((error) => {
        console.error("AI Report Error:", error);
        setError("Unable to generate AI inventory report.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div className="rounded-xl bg-white p-6 shadow">
      <h2 className="mb-4 text-xl font-semibold text-slate-800">
        🤖 AI Inventory Report
      </h2>

      {loading && (
        <p className="text-slate-500">
          Generating AI report...
        </p>
      )}

      {error && (
        <p className="text-red-600">
          {error}
        </p>
      )}

      {!loading && !error && (
        <div className="whitespace-pre-wrap leading-7 text-slate-700">
          {report}
        </div>
      )}
    </div>
  );
}
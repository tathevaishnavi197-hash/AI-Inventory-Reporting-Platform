"use client";

import { useState } from "react";

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchedQuery, setSearchedQuery] = useState("");
  const [showResults, setShowResults] = useState(false);

  const handleAnalyze = () => {
    if (!searchQuery.trim()) return;

    setSearchedQuery(searchQuery);
    setShowResults(true);
  };

  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (event.key === "Enter") {
      handleAnalyze();
    }
  };

  const handleExample = (query: string) => {
    setSearchQuery(query);
    setSearchedQuery(query);
    setShowResults(true);
  };

  return (
    <main className="min-h-screen bg-[#080d1c] text-white">

      {/* ================= HEADER ================= */}
      <header className="border-b border-slate-800 bg-[#11172b]">
        <div className="mx-auto max-w-7xl px-6 py-4">

          <div className="flex items-center gap-4">

            <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-blue-400/40 bg-gradient-to-br from-indigo-500 to-cyan-400 text-2xl shadow-lg shadow-blue-500/20">
              📊
            </div>

            <div>
              <h1 className="text-2xl font-bold tracking-tight text-blue-400">
                BoardView AI
              </h1>

              <p className="text-xs font-medium tracking-widest text-slate-500">
                INTELLIGENT INVENTORY REPORTING SYSTEM
              </p>
            </div>

          </div>

        </div>
      </header>


      {/* ================= MAIN ================= */}
      <div className="mx-auto max-w-7xl px-6 py-12">


        {/* ================= SEARCH BAR ================= */}
        <section>

          <div className="flex flex-col gap-3 rounded-2xl border border-blue-500/20 bg-[#182136] p-2 shadow-2xl shadow-black/20 md:flex-row">

            <div className="flex flex-1 items-center gap-3 px-4">

              <span className="text-xl">
                🔍
              </span>

              <input
                type="text"
                value={searchQuery}
                onChange={(event) =>
                  setSearchQuery(event.target.value)
                }
                onKeyDown={handleKeyDown}
                placeholder="Ask anything about your inventory, sales, orders or payments..."
                className="w-full bg-transparent py-3 text-base text-white outline-none placeholder:text-slate-400"
              />

            </div>


            <button
              onClick={handleAnalyze}
              disabled={!searchQuery.trim()}
              className="rounded-xl bg-gradient-to-r from-indigo-500 to-cyan-400 px-8 py-3 font-semibold text-white transition hover:scale-[1.02] hover:shadow-lg hover:shadow-cyan-500/20 disabled:cursor-not-allowed disabled:opacity-40"
            >
              Analyze →
            </button>

          </div>


          {/* ================= TRY EXAMPLES ================= */}
          <div className="mt-4 flex flex-wrap items-center gap-2">

            <span className="mr-1 text-sm text-slate-500">
              Try:
            </span>

            <button
              onClick={() =>
                handleExample("Which products need immediate reorder?")
              }
              className="rounded-full border border-indigo-500/30 bg-[#11182b] px-4 py-2 text-xs text-slate-300 transition hover:border-indigo-400 hover:text-white"
            >
              Which products need immediate reorder?
            </button>

            <button
              onClick={() =>
                handleExample("Show monthly sales trend")
              }
              className="rounded-full border border-indigo-500/30 bg-[#11182b] px-4 py-2 text-xs text-slate-300 transition hover:border-indigo-400 hover:text-white"
            >
              Show monthly sales trend
            </button>

            <button
              onClick={() =>
                handleExample("Show payment status analysis")
              }
              className="rounded-full border border-indigo-500/30 bg-[#11182b] px-4 py-2 text-xs text-slate-300 transition hover:border-indigo-400 hover:text-white"
            >
              Show payment status analysis
            </button>

            <button
              onClick={() =>
                handleExample("Show top selling products")
              }
              className="rounded-full border border-indigo-500/30 bg-[#11182b] px-4 py-2 text-xs text-slate-300 transition hover:border-indigo-400 hover:text-white"
            >
              Show top selling products
            </button>

          </div>

        </section>


        {/* ================= RESULTS ================= */}
        {showResults && (
          <section className="mt-12">

            {/* Results heading + PDF button */}
            <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">

              <p className="text-sm text-slate-500">
                Results for:
                <span className="ml-2 font-medium italic text-indigo-400">
                  "{searchedQuery}"
                </span>
              </p>

              <button
                className="rounded-xl border border-indigo-500/30 bg-[#11182b] px-5 py-2.5 text-sm font-semibold text-indigo-300 transition hover:border-indigo-400 hover:bg-indigo-500/10"
              >
                📄 Download PDF
              </button>

            </div>


            {/* ================= KEY METRICS ================= */}
            <div className="mt-10">

              <h2 className="mb-5 text-xl font-semibold text-slate-200">
                📊 Key Metrics
              </h2>

              <div className="grid grid-cols-1 gap-5 md:grid-cols-3">

                <div className="rounded-2xl border border-slate-700 bg-[#151e32] p-6">
                  <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-slate-800 text-xl">
                    📦
                  </div>

                  <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                    Total Products
                  </p>

                  <p className="mt-2 text-3xl font-bold text-white">
                    —
                  </p>
                </div>


                <div className="rounded-2xl border border-slate-700 bg-[#151e32] p-6">
                  <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-slate-800 text-xl">
                    ⚠️
                  </div>

                  <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                    Low Stock Products
                  </p>

                  <p className="mt-2 text-3xl font-bold text-white">
                    —
                  </p>
                </div>


                <div className="rounded-2xl border border-slate-700 bg-[#151e32] p-6">
                  <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-slate-800 text-xl">
                    💰
                  </div>

                  <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                    Total Sales
                  </p>

                  <p className="mt-2 text-3xl font-bold text-white">
                    —
                  </p>
                </div>

              </div>

            </div>


            {/* ================= VISUALIZATIONS ================= */}
            <div className="mt-10">

              <h2 className="mb-5 text-xl font-semibold text-slate-200">
                📈 Visualizations
              </h2>

              <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">

                <div className="flex min-h-[360px] items-center justify-center rounded-2xl border border-slate-700 bg-[#151e32]">

                  <div className="text-center">
                    <div className="text-4xl">
                      📊
                    </div>

                    <p className="mt-3 font-semibold text-slate-300">
                      Relevant chart will appear here
                    </p>

                    <p className="mt-1 text-sm text-slate-500">
                      Based on your search query
                    </p>
                  </div>

                </div>


                <div className="flex min-h-[360px] items-center justify-center rounded-2xl border border-slate-700 bg-[#151e32]">

                  <div className="text-center">
                    <div className="text-4xl">
                      📈
                    </div>

                    <p className="mt-3 font-semibold text-slate-300">
                      Dynamic analysis
                    </p>

                    <p className="mt-1 text-sm text-slate-500">
                      Visualization will be generated here
                    </p>
                  </div>

                </div>

              </div>

            </div>


            {/* ================= AI ANALYSIS ================= */}
            <div className="mt-10">

              <h2 className="mb-5 text-xl font-semibold text-slate-200">
                🤖 AI Analysis
              </h2>

              <div className="rounded-2xl border border-slate-700 bg-[#151e32] p-6">

                <p className="leading-7 text-slate-400">
                  Gemini AI analysis will appear here after the
                  search query is connected to the backend.
                </p>

              </div>

            </div>


            {/* ================= RECOMMENDATIONS ================= */}
            <div className="mt-8">

              <h2 className="mb-5 text-xl font-semibold text-slate-200">
                💡 Recommendations
              </h2>

              <div className="rounded-2xl border border-slate-700 bg-[#151e32] p-6">

                <p className="leading-7 text-slate-400">
                  AI-powered recommendations based on the
                  selected query will appear here.
                </p>

              </div>

            </div>

          </section>
        )}

      </div>

    </main>
  );
}
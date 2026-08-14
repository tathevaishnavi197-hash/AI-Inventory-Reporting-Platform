"use client";

import { useState } from "react";
import ReactECharts from "echarts-for-react";

type Metric = {
  label: string;
  value: number | string;
};

type ChartData = {
  type: string;
  title: string;
  labels: string[];
  values: number[];
};

type AIResponse = {
  query: string;
  query_type: string;
  analysis: string;
  metrics: Metric[];
  charts: ChartData[];
  recommendations: string[];
};

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("");
  const [result, setResult] = useState<AIResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // =========================================================
  // AI SEARCH
  // =========================================================

  const handleAISearch = async (queryOverride?: string) => {
    const query = queryOverride ?? searchQuery;

    if (!query.trim()) return;

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
  `${process.env.NEXT_PUBLIC_API_URL}/ai/analyze?query=${encodeURIComponent(
    query
  )}`
);

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "AI analysis failed");
      }

      setSearchQuery(query);
      setResult(data);
    } catch (err) {
      console.error("AI Search Error:", err);

      setError(
        "Unable to analyze the query. Please check that the FastAPI server is running."
      );
    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // ENTER KEY
  // =========================================================

  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (event.key === "Enter") {
      handleAISearch();
    }
  };

  // =========================================================
  // SUGGESTIONS
  // =========================================================

  const runSuggestion = (query: string) => {
    handleAISearch(query);
  };

  // =========================================================
  // CHART OPTION
  // =========================================================

  const getChartOption = (chart: ChartData) => {
    // -------------------------------------------------------
    // PIE
    // -------------------------------------------------------

    if (chart.type === "pie") {
      return {
        tooltip: {
          trigger: "item",
        },

        legend: {
          bottom: "2%",
          textStyle: {
            color: "#cbd5e1",
          },
        },

        series: [
          {
            name: chart.title,
            type: "pie",
            radius: ["42%", "68%"],
            center: ["50%", "45%"],

            data: chart.labels.map((label, index) => ({
              name: label,
              value: chart.values[index] ?? 0,
            })),

            label: {
              color: "#e2e8f0",
            },

            emphasis: {
              itemStyle: {
                shadowBlur: 15,
                shadowOffsetX: 0,
                shadowColor: "rgba(0,0,0,0.4)",
              },
            },
          },
        ],
      };
    }

    // -------------------------------------------------------
    // LINE
    // -------------------------------------------------------

    if (chart.type === "line") {
      return {
        tooltip: {
          trigger: "axis",
        },

        grid: {
          left: "6%",
          right: "5%",
          bottom: "15%",
          containLabel: true,
        },

        xAxis: {
          type: "category",
          data: chart.labels,

          axisLabel: {
            color: "#94a3b8",
            rotate: chart.labels.length > 6 ? 25 : 0,
          },

          axisLine: {
            lineStyle: {
              color: "#334155",
            },
          },
        },

        yAxis: {
          type: "value",

          axisLabel: {
            color: "#94a3b8",
          },

          splitLine: {
            lineStyle: {
              color: "#263449",
            },
          },
        },

        series: [
          {
            name: chart.title,
            type: "line",
            data: chart.values,

            smooth: true,

            symbol: "circle",
            symbolSize: 8,

            lineStyle: {
              width: 3,
            },

            areaStyle: {
              opacity: 0.08,
            },
          },
        ],
      };
    }

    // -------------------------------------------------------
    // BAR
    // -------------------------------------------------------

    return {
      tooltip: {
        trigger: "axis",
      },

      grid: {
        left: "6%",
        right: "5%",
        bottom: "15%",
        containLabel: true,
      },

      xAxis: {
        type: "category",
        data: chart.labels,

        axisLabel: {
          color: "#94a3b8",
          rotate: chart.labels.length > 6 ? 25 : 0,
        },

        axisLine: {
          lineStyle: {
            color: "#334155",
          },
        },
      },

      yAxis: {
        type: "value",

        axisLabel: {
          color: "#94a3b8",
        },

        splitLine: {
          lineStyle: {
            color: "#263449",
          },
        },
      },

      series: [
        {
          name: chart.title,
          type: "bar",
          data: chart.values,

          barMaxWidth: 55,

          itemStyle: {
            borderRadius: [6, 6, 0, 0],
          },
        },
      ],
    };
  };

  // =========================================================
  // PAGE
  // =========================================================

  return (
    <main className="min-h-screen bg-[#070b18] text-white">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <header className="border-b border-slate-800 bg-[#11172b]">

        <div className="mx-auto flex max-w-7xl items-center px-6 py-5">

          <div className="mr-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-500 to-cyan-400 text-3xl shadow-lg">
            📊
          </div>

          <div>

            <h1 className="text-2xl font-bold tracking-tight text-blue-400">
              BoardView AI
            </h1>

            <p className="text-xs font-medium tracking-[0.18em] text-slate-500">
              INTELLIGENT INVENTORY REPORTING SYSTEM
            </p>

          </div>

        </div>

      </header>


      {/* =====================================================
          MAIN
      ===================================================== */}

      <div className="mx-auto max-w-7xl px-6 py-12">

        {/* =================================================
            SEARCH
        ================================================= */}

        <section>

          <div className="flex flex-col gap-3 rounded-2xl border border-blue-900/60 bg-[#172035] p-2 shadow-xl md:flex-row">

            <div className="flex flex-1 items-center">

              <span className="px-4 text-xl">
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
                className="w-full bg-transparent px-2 py-4 text-slate-200 outline-none placeholder:text-slate-500"
              />

            </div>

            <button
              onClick={() => handleAISearch()}
              disabled={loading || !searchQuery.trim()}
              className="rounded-xl bg-gradient-to-r from-indigo-500 to-cyan-400 px-8 py-3 font-semibold text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {loading ? "Analyzing..." : "Analyze →"}
            </button>

          </div>


          {/* =================================================
              PDF
          ================================================= */}

          <div className="mt-4 flex justify-end">

            <button
              onClick={() => {

                if (!searchQuery.trim()) {
                  alert("Please enter a query first.");
                  return;
                }

                window.open(
                  `http://127.0.0.1:8000/reports/inventory-pdf?query=${encodeURIComponent(
                    searchQuery
                  )}`,
                  "_blank"
                );

              }}
              className="rounded-xl border border-indigo-500/40 bg-slate-900 px-5 py-3 font-semibold text-indigo-300 transition hover:bg-indigo-500/10"
            >
              📄 Download PDF
            </button>

          </div>


          {/* =================================================
              TRY OPTIONS
          ================================================= */}

          <div className="mt-4 flex flex-wrap items-center gap-3">

            <span className="text-sm text-slate-500">
              Try:
            </span>

            <button
              onClick={() =>
                runSuggestion(
                  "Which products need immediate reorder?"
                )
              }
              className="rounded-full border border-indigo-900 px-4 py-2 text-sm text-slate-300 transition hover:bg-indigo-950"
            >
              Which products need immediate reorder?
            </button>

            <button
              onClick={() =>
                runSuggestion(
                  "Show monthly sales trend"
                )
              }
              className="rounded-full border border-indigo-900 px-4 py-2 text-sm text-slate-300 transition hover:bg-indigo-950"
            >
              Show monthly sales trend
            </button>

            <button
              onClick={() =>
                runSuggestion(
                  "Show payment status analysis"
                )
              }
              className="rounded-full border border-indigo-900 px-4 py-2 text-sm text-slate-300 transition hover:bg-indigo-950"
            >
              Show payment status analysis
            </button>

            <button
              onClick={() =>
                runSuggestion(
                  "Show top selling products"
                )
              }
              className="rounded-full border border-indigo-900 px-4 py-2 text-sm text-slate-300 transition hover:bg-indigo-950"
            >
              Show top selling products
            </button>

          </div>

        </section>


        {/* =================================================
            ERROR
        ================================================= */}

        {error && (

          <div className="mt-8 rounded-xl border border-red-900 bg-red-950/30 p-5 text-red-300">
            {error}
          </div>

        )}


        {/* =================================================
            RESULTS
        ================================================= */}

        {result && (

          <>

            {/* =================================================
                RESULT TITLE
            ================================================= */}

            <div className="mt-12">

              <p className="text-sm text-slate-500">
                Results for:
              </p>

              <p className="mt-1 text-lg font-medium italic text-indigo-400">
                "{result.query}"
              </p>

            </div>


            {/* =================================================
                KEY METRICS
            ================================================= */}

            <section className="mt-8">

              <h2 className="mb-5 text-xl font-bold">
                📊 Key Metrics
              </h2>

              <div className="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">

                {result.metrics?.map(
                  (metric, index) => (

                    <div
                      key={index}
                      className="rounded-2xl border border-slate-800 bg-[#151e32] p-6 shadow-lg"
                    >

                      <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                        {metric.label}
                      </p>

                      <p className="mt-3 text-3xl font-bold text-slate-100">

                        {typeof metric.value === "number"
                          ? metric.value.toLocaleString("en-IN")
                          : metric.value}

                      </p>

                    </div>

                  )
                )}

              </div>

            </section>


            {/* =================================================
                VISUALIZATIONS
            ================================================= */}

            <section className="mt-10">

              <h2 className="mb-5 text-xl font-bold">
                📈 Visualizations
              </h2>


              {result.charts && result.charts.length > 0 ? (

                <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">

                  {result.charts.map(
                    (chart, index) => (

                      <div
                        key={`${result.query_type}-${index}-${chart.title}`}
                        className="rounded-2xl border border-slate-800 bg-[#151e32] p-6 shadow-lg"
                      >

                        <h3 className="mb-5 text-lg font-semibold text-slate-200">
                          {index === 0 ? "📊" : "📈"}{" "}
                          {chart.title}
                        </h3>

                        <div className="h-[360px] w-full">

                          <ReactECharts
                            key={`${result.query_type}-${chart.title}-${index}`}
                            option={getChartOption(chart)}
                            style={{
                              height: "100%",
                              width: "100%",
                            }}
                            opts={{
                              renderer: "canvas",
                            }}
                          />

                        </div>

                      </div>

                    )
                  )}

                </div>

              ) : (

                <div className="rounded-2xl border border-slate-800 bg-[#151e32] p-10 text-center">

                  <div className="text-5xl">
                    📊
                  </div>

                  <p className="mt-4 font-semibold text-slate-300">
                    No visualization available
                  </p>

                  <p className="mt-2 text-sm text-slate-500">
                    This query does not require a chart.
                  </p>

                </div>

              )}

            </section>


            {/* =================================================
                AI ANALYSIS
            ================================================= */}

            <section className="mt-10">

              <h2 className="mb-5 text-xl font-bold">
                🤖 AI Analysis
              </h2>

              <div className="rounded-2xl border border-slate-800 bg-[#151e32] p-7 shadow-lg">

                <div className="whitespace-pre-wrap leading-8 text-slate-300">
                  {result.analysis}
                </div>

              </div>

            </section>


            {/* =================================================
                RECOMMENDATIONS
            ================================================= */}

            <section className="mt-10">

              <h2 className="mb-5 text-xl font-bold">
                💡 Recommendations
              </h2>

              <div className="rounded-2xl border border-slate-800 bg-[#151e32] p-7 shadow-lg">

                <div className="space-y-4">

                  {result.recommendations?.map(
                    (recommendation, index) => (

                      <div
                        key={index}
                        className="flex gap-4 rounded-xl border border-slate-800 bg-slate-900/40 p-4"
                      >

                        <span className="text-lg">
                          {index + 1}.
                        </span>

                        <p className="leading-7 text-slate-300">
                          {recommendation}
                        </p>

                      </div>

                    )
                  )}

                </div>

              </div>

            </section>

          </>

        )}

      </div>

    </main>
  );
}
"use client";

import ReactECharts from "echarts-for-react";
import { useEffect, useState } from "react";

type SalesData = {
  month: string;
  sales: number;
};

export default function SalesChart() {
  const [data, setData] = useState<SalesData[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/analytics/monthly-sales")
      .then((response) => response.json())
      .then((result) => {
        setData(
  result.monthly_sales.map((item: any) => ({
    month: item.month,
    sales: Number(item.total_sales),
  }))
);
      })
      .catch((error) => {
        console.error("Sales API Error:", error);
      });
  }, []);

  const option = {
    tooltip: {
      trigger: "axis",
      formatter: (params: any) => {
        const value = params[0].value;
        return `${params[0].name}<br/>Sales: ₹${Number(
          value
        ).toLocaleString("en-IN")}`;
      },
    },

    xAxis: {
      type: "category",
      data: data.map((item) => item.month),
    },

    yAxis: {
      type: "value",
    },

    series: [
      {
        name: "Sales",
        type: "line",
        data: data.map((item) => item.sales),
        smooth: true,
        lineStyle: {
          width: 3,
        },
      },
    ],
  };

  return (
    <div className="rounded-xl bg-white p-6 shadow">
      <h2 className="mb-4 text-xl font-semibold text-slate-800">
        📈 Monthly Sales Overview
      </h2>

      <div className="h-80 w-full">
        <ReactECharts
          option={option}
          style={{ height: "100%", width: "100%" }}
        />
      </div>
    </div>
  );
}
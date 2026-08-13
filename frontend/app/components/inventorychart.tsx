"use client";

import { useEffect, useState } from "react";
import ReactECharts from "echarts-for-react";

type InventoryData = {
  product_name: string;
  stock_available: number;
};

export default function InventoryChart() {
  const [data, setData] = useState<InventoryData[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/inventory")
      .then((response) => response.json())
      .then((result) => {
        const formattedData = result.inventory
          .slice(0, 10)
          .map(
            (item: {
              product_name: string;
              stock_available: number;
            }) => ({
              product_name: item.product_name,
              stock_available: Number(item.stock_available),
            })
          );

        setData(formattedData);
      })
      .catch((error) => {
        console.error("Inventory API Error:", error);
      });
  }, []);

  const option = {
    tooltip: {
      trigger: "axis",
    },

    grid: {
      left: "3%",
      right: "4%",
      bottom: "20%",
      containLabel: true,
    },

    xAxis: {
      type: "category",
      data: data.map((item) => item.product_name),
      axisLabel: {
        rotate: 25,
      },
    },

    yAxis: {
      type: "value",
      name: "Stock",
    },

    series: [
      {
        name: "Stock Available",
        type: "bar",
        data: data.map((item) => item.stock_available),
      },
    ],
  };

  return (
    <div className="rounded-xl bg-white p-6 shadow">
      <h2 className="mb-4 text-xl font-semibold text-slate-800">
        📦 Inventory Stock Analysis
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
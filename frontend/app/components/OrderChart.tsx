"use client";

import { useEffect, useState } from "react";
import ReactECharts from "echarts-for-react";

type Order = {
  order_status: string;
};

type ChartData = {
  status: string;
  count: number;
};

export default function OrderChart() {
  const [data, setData] = useState<ChartData[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/orders")
      .then((response) => response.json())
      .then((result) => {
        const orders: Order[] = result.orders;

        const statusCount: Record<string, number> = {};

        orders.forEach((order) => {
          const status = order.order_status;

          statusCount[status] = (statusCount[status] || 0) + 1;
        });

        const formattedData = Object.entries(statusCount).map(
          ([status, count]) => ({
            status,
            count,
          })
        );

        setData(formattedData);
      })
      .catch((error) => {
        console.error("Orders API Error:", error);
      });
  }, []);

  const option = {
    tooltip: {
      trigger: "axis",
    },

    grid: {
      left: "3%",
      right: "4%",
      bottom: "10%",
      containLabel: true,
    },

    xAxis: {
      type: "category",
      data: data.map((item) => item.status),
    },

    yAxis: {
      type: "value",
      name: "Orders",
    },

    series: [
      {
        name: "Orders",
        type: "bar",
        data: data.map((item) => item.count),
        barMaxWidth: 60,
      },
    ],
  };

  return (
    <div className="rounded-xl bg-white p-6 shadow">
      <h2 className="mb-4 text-xl font-semibold text-slate-800">
        📊 Order Status Analysis
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
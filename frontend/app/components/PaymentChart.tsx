"use client";

import { useEffect, useState } from "react";
import ReactECharts from "echarts-for-react";

type Payment = {
  payment_status: string;
};

type ChartData = {
  name: string;
  value: number;
};

export default function PaymentChart() {
  const [data, setData] = useState<ChartData[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/payments")
      .then((response) => response.json())
      .then((result) => {
        const payments: Payment[] = result.payments;

        const statusCount: Record<string, number> = {};

        payments.forEach((payment) => {
          const status = payment.payment_status;

          statusCount[status] = (statusCount[status] || 0) + 1;
        });

        const formattedData = Object.entries(statusCount).map(
          ([name, value]) => ({
            name,
            value,
          })
        );

        setData(formattedData);
      })
      .catch((error) => {
        console.error("Payment API Error:", error);
      });
  }, []);

  const option = {
    tooltip: {
      trigger: "item",
    },

    legend: {
      bottom: "0%",
    },

    series: [
      {
        name: "Payment Status",
        type: "pie",
        radius: "65%",
        data: data,
        label: {
          show: true,
          formatter: "{b}: {c}",
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: "rgba(0, 0, 0, 0.3)",
          },
        },
      },
    ],
  };

  return (
    <div className="rounded-xl bg-white p-6 shadow">
      <h2 className="mb-4 text-xl font-semibold text-slate-800">
        💳 Payment Status Analysis
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
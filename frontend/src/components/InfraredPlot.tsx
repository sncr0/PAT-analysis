// src/components/InfraredPlot.tsx
import { useEffect, useState } from 'react';
import axios from 'axios';
import {
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts';

interface Measurement {
  timestamp: string;
  x_preview: number[];
}

interface ChartPoint {
  time: string;
  x0: number;
}

export default function InfraredPlot() {
  const [data, setData] = useState<ChartPoint[]>([]);

  useEffect(() => {
    axios
      .get<{ count: number; measurements: Measurement[] }>('http://localhost:8000/api/infrared/all')
      .then((response) => {
        const chartData: ChartPoint[] = response.data.measurements.map((m) => ({
          time: new Date(m.timestamp).toLocaleTimeString(),
          x0: m.x_preview[0],
        }));
        setData(chartData);
      })
      .catch((error) => console.error('Error fetching data:', error));
  }, []);

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Spectroscopy Scatter Plot (x₀ vs. Time)</h2>
      <ResponsiveContainer width="100%" height={400}>
        <ScatterChart>
          <CartesianGrid />
          <XAxis dataKey="time" name="Time" />
          <YAxis dataKey="x0" name="First X Value" unit=" cm⁻¹" />
          <Tooltip cursor={{ strokeDasharray: '3 3' }} />
          <Scatter name="Spectra" data={data} fill="#82ca9d" />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
}

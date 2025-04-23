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

interface Prediction {
  timestamp: string;
  predicted_concentration: number;
}

function PredictedConcentrationPlot() {
  const [data, setData] = useState<Prediction[]>([]);

  useEffect(() => {
    axios
      .get<{ count: number; predictions: Prediction[] }>('http://localhost:8000/measurements/predicted')
      .then((response) => {
        setData(response.data.predictions);
      })
      .catch((error) => console.error('Error fetching predicted data:', error));
  }, []);

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Predicted Concentration vs. Time</h2>
      {data.length === 0 ? (
        <p>No predictions yet...</p>
      ) : (
        <ResponsiveContainer width="100%" height={400}>
          <ScatterChart>
            <CartesianGrid />
            <XAxis
              dataKey="timestamp"
              name="Time"
              tickFormatter={(val) => new Date(val).toLocaleTimeString()}
            />
            <YAxis
              dataKey="predicted_concentration"
              name="Concentration"
              domain={['auto', 'auto']}
            />
            <Tooltip
              formatter={(val: number) => val.toFixed(3)}
              labelFormatter={(label) => new Date(label).toLocaleTimeString()}
            />
            <Scatter name="Prediction" data={data} fill="#8884d8" />
          </ScatterChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}

export default PredictedConcentrationPlot;

// src/App.tsx
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import InfraredPlot from './components/InfraredPlot';
import PredictedPlot from './components/PredictedPlot';

function App() {
  return (
    <Router>
      <nav style={{ padding: '1rem', background: '#f4f4f4' }}>
        <Link to="/" style={{ marginRight: '1rem' }}>Infrared</Link>
        <Link to="/predicted">Predicted</Link>
      </nav>

      <Routes>
        <Route path="/" element={<InfraredPlot />} />
        <Route path="/predicted" element={<PredictedPlot />} />
      </Routes>
    </Router>
  );
}

export default App;

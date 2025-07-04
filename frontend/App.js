import React, { useState } from 'react';
import PredictionForm from './PredictionForm';
import PredictionResult from './PredictionResult';

function App() {
  const [result, setResult] = useState(null);
  return (
    <div className="container">
      <h1>Harare Rainfall Prediction</h1>
      <PredictionForm onResult={setResult} />
      <PredictionResult result={result} />
    </div>
  );
}

export default App;

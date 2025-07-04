import React from 'react';

export default function PredictionResult({ result }) {
  if (!result) return null;
  return (
    <div>
      <h2>Rain Prediction</h2>
      <p>{result.location}: <b>{result.rain_chance}% chance of rain</b></p>
    </div>
  );
}

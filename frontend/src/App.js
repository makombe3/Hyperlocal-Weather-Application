import React, { useState } from 'react';
import axios from 'axios';
import './style.css';

const NEIGHBORHOODS = [
  'Mount Pleasant', 'Avondale', 'Borrowdale', 'Highfield', 'Eastlea',
  'Hatcliffe', 'Ruwa', 'Epworth', 'Glen Lorne', 'Chishawasha'
];

export default function App() {
  // Prediction state
  const [predLocation, setPredLocation] = useState(NEIGHBORHOODS[0]);
  const [prediction, setPrediction] = useState(null);
  const [predLoading, setPredLoading] = useState(false);
  const [predError, setPredError] = useState('');

  // Report state
  const [repLocation, setRepLocation] = useState(NEIGHBORHOODS[0]);
  // const [temp, setTemp] = useState('');
  const [rain, setRain] = useState(false);
  const [comment, setComment] = useState('');
  const [repLoading, setRepLoading] = useState(false);
  const [repSuccess, setRepSuccess] = useState('');
  const [repError, setRepError] = useState('');

  // Prediction handler
  const handlePredict = async (e) => {
    e.preventDefault();
    setPredLoading(true);
    setPredError('');
    setPrediction(null);
    try {
      const res = await axios.get('/api/weather-prediction/', { params: { location: predLocation } });
      setPrediction(res.data);
    } catch (err) {
      setPredError('Could not fetch prediction.');
    }
    setPredLoading(false);
  };

  // Report handler
  const handleReport = async (e) => {
    e.preventDefault();
    setRepLoading(true);
    setRepSuccess('');
    setRepError('');
    try {
      await axios.post('/api/weather-reports/', {
        location: repLocation,
        rain,
        comment
      });
      setRepSuccess('Report submitted! Thank you for helping improve the predictions.');
      setRain(false); setComment('');
    } catch (err) {
      setRepError('Error submitting report.');
    }
    setRepLoading(false);
  };

  return (
    <div className="container">
      <h1>Harare Rainfall Prediction</h1>
      <div className="prediction-section">
        <h2>Check Rain Prediction</h2>
        <form onSubmit={handlePredict}>
          <label>Neighborhood:
            <select value={predLocation} onChange={e => setPredLocation(e.target.value)}>
              {NEIGHBORHOODS.map(n => <option key={n} value={n}>{n}</option>)}
            </select>
          </label>
          <button type="submit" disabled={predLoading}>{predLoading ? 'Checking...' : 'Check Prediction'}</button>
        </form>
        {predError && <p className="error">{predError}</p>}
        {prediction && (
          <div className="prediction-result">
            <p><b>{prediction.location}</b>: {prediction.rain_chance}% chance of rain</p>
            <p className="notice">If this prediction does not match the actual weather, please submit a report below.</p>
          </div>
        )}
      </div>
      <div className="report-section">
        <h2>Submit Weather Report</h2>
        <form onSubmit={handleReport}>
          <label>Neighborhood:
            <select value={repLocation} onChange={e => setRepLocation(e.target.value)}>
              {NEIGHBORHOODS.map(n => <option key={n} value={n}>{n}</option>)}
            </select>
          </label>
          {/* Temperature field removed */}
          <label>Rain?
            <input type="checkbox" checked={rain} onChange={e => setRain(e.target.checked)} />
          </label>
          <label>Comment:
            <input type="text" value={comment} onChange={e => setComment(e.target.value)} />
          </label>
          <button type="submit" disabled={repLoading}>{repLoading ? 'Submitting...' : 'Submit Report'}</button>
        </form>
        {repSuccess && <p className="success">{repSuccess}</p>}
        {repError && <p className="error">{repError}</p>}
      </div>
    </div>
  );
}


import React, { useState } from 'react';
import axios from 'axios';

const NEIGHBORHOODS = [
  'Mount Pleasant', 'Avondale', 'Borrowdale', 'Highfield', 'Eastlea',
  'Hatcliffe', 'Ruwa', 'Epworth', 'Glen Lorne', 'Chishawasha'
];

export default function PredictionForm({ onResult }) {
  const [location, setLocation] = useState(NEIGHBORHOODS[0]);
  const [rain, setRain] = useState(false);
  const [comment, setComment] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      // Submit weather report (no temp field)
      await axios.post('/api/weather-reports/', {
        location,
        rain,
        comment
      });
      // Get prediction
      const res = await axios.post('/api/predict/', { location });
      onResult(res.data);
    } catch (err) {
      alert('Error submitting or predicting.');
    }
    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>Neighborhood:
        <select value={location} onChange={e => setLocation(e.target.value)}>
          {NEIGHBORHOODS.map(n => <option key={n} value={n}>{n}</option>)}
        </select>
      </label>
      <label>Rain?
        <input type="checkbox" checked={rain} onChange={e => setRain(e.target.checked)} />
      </label>
      <label>Comment:
        <input type="text" value={comment} onChange={e => setComment(e.target.value)} />
      </label>
      <button type="submit" disabled={loading}>{loading ? 'Submitting...' : 'Submit & Predict'}</button>
    </form>
  );
}

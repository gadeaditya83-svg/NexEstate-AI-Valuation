import React, { useState } from 'react';
import axios from 'axios';

const cityLocalities = {
  Pune: ['Kothrud', 'Hinjewadi', 'Viman Nagar', 'Baner', 'Hadapsar'],
  Mumbai: ['Andheri', 'Bandra', 'Thane', 'Navi Mumbai', 'Borivali'],
  Bangalore: ['Koramangala', 'Whitefield', 'Indiranagar', 'Electronic City', 'HSR Layout'],
  Delhi: ['Dwarka', 'South Delhi', 'Noida', 'Gurgaon', 'Rohini']
};

function App() {
  const [formData, setFormData] = useState({
    city: 'Pune',
    locality: 'Hinjewadi',
    area_sqft: 1200,
    bhk: 1,
    balcony: 'Has Balcony',
    property_type: 'Apartment',
    furnished_status: 'Semi-Furnished',
    property_age: '1-5 Years',
    amenities_score: 7
  });

  const [prediction, setPrediction] = useState(null);
  const [latency, setLatency] = useState('< 48 ms');
  const [errorMsg, setErrorMsg] = useState('');

  const handleCityChange = (e) => {
    const selectedCity = e.target.value;
    setFormData({
      ...formData,
      city: selectedCity,
      locality: cityLocalities[selectedCity][0]
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    try {
      
const response = await axios.post('http://localhost:8000/predict', formData);
      setPrediction(response.data.predicted_price);
      setLatency(response.data.latency_ms);
    } catch (error) {
      console.error("Valuation Error", error);
      setErrorMsg('Backend Connection Failed! Ensure Uvicorn server is running.');
    }
  };

  return (
    <div style={{ backgroundColor: '#090d16', color: '#fff', minHeight: '100vh', padding: '40px', fontFamily: 'Arial, sans-serif' }}>
      <header style={{ borderBottom: '1px solid #1e293b', paddingBottom: '20px', marginBottom: '30px' }}>
        <h1 style={{ color: '#38bdf8', margin: 0 }}>NexEstate AI Valuation Engine</h1>
        <p style={{ color: '#94a3b8' }}>Real-Time Hyper-Local Valuation Engine | Latency: {latency}</p>
      </header>

      <div style={{ display: 'flex', gap: '40px', flexWrap: 'wrap' }}>
        <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', width: '520px', backgroundColor: '#111827', padding: '25px', borderRadius: '12px', border: '1px solid #1f2937' }}>
          
          <div>
            <label style={{ fontSize: '14px', color: '#cbd5e1' }}>Select City</label>
            <select value={formData.city} onChange={handleCityChange} style={inputStyle}>
              {Object.keys(cityLocalities).map(city => (
                <option key={city} value={city}>{city}</option>
              ))}
            </select>
          </div>

          <div>
            <label style={{ fontSize: '14px', color: '#cbd5e1' }}>Select Area / Locality</label>
            <select value={formData.locality} onChange={(e) => setFormData({...formData, locality: e.target.value})} style={inputStyle}>
              {cityLocalities[formData.city].map(loc => (
                <option key={loc} value={loc}>{loc}</option>
              ))}
            </select>
          </div>

          <div>
            <label style={{ fontSize: '14px', color: '#cbd5e1' }}>Area (Sq. Ft.)</label>
            <input type="number" value={formData.area_sqft} onChange={(e) => setFormData({...formData, area_sqft: parseFloat(e.target.value) || 0})} style={inputStyle}/>
          </div>

          <div>
            <label style={{ fontSize: '14px', color: '#cbd5e1' }}>BHK Configuration</label>
            <select value={formData.bhk} onChange={(e) => setFormData({...formData, bhk: parseInt(e.target.value)})} style={inputStyle}>
              <option value={1}>1 BHK</option>
              <option value={2}>2 BHK</option>
              <option value={3}>3 BHK</option>
              <option value={4}>4 BHK</option>
            </select>
          </div>

          <div>
            <label style={{ fontSize: '14px', color: '#cbd5e1' }}>Property Type</label>
            <select value={formData.property_type} onChange={(e) => setFormData({...formData, property_type: e.target.value})} style={inputStyle}>
              <option value="Apartment">Apartment</option>
              <option value="Villa">Villa</option>
              <option value="Independent House">Independent House</option>
            </select>
          </div>

          <div>
            <label style={{ fontSize: '14px', color: '#cbd5e1' }}>Furnished Status</label>
            <select value={formData.furnished_status} onChange={(e) => setFormData({...formData, furnished_status: e.target.value})} style={inputStyle}>
              <option value="Unfurnished">Unfurnished</option>
              <option value="Semi-Furnished">Semi-Furnished</option>
              <option value="Fully Furnished">Fully Furnished</option>
            </select>
          </div>

          <button type="submit" style={{ gridColumn: 'span 2', padding: '14px', backgroundColor: '#0284c7', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold', fontSize: '16px', marginTop: '10px' }}>
            Get Hyper-Local Valuation →
          </button>
        </form>

        <div style={{ backgroundColor: '#111827', padding: '30px', borderRadius: '12px', flex: '1', minWidth: '300px', border: '1px solid #1f2937' }}>
          <h2 style={{ borderBottom: '1px solid #374151', paddingBottom: '10px', marginTop: 0 }}>Valuation Output</h2>
          {errorMsg && <p style={{ color: '#ef4444' }}>{errorMsg}</p>}
          {prediction !== null ? (
            <div style={{ marginTop: '20px' }}>
              <p style={{ color: '#94a3b8', fontSize: '14px' }}>Estimated Price for <b>{formData.locality}, {formData.city}</b>:</p>
              <h1 style={{ color: '#4ade80', fontSize: '3.5rem', margin: '10px 0' }}>₹ {prediction} Lakhs</h1>
              <p style={{ color: '#38bdf8' }}>Execution Latency: {latency}</p>
            </div>
          ) : (
            <p style={{ color: '#64748b', marginTop: '20px' }}>Select property attributes and click button.</p>
          )}
        </div>
      </div>
    </div>
  );
}

const inputStyle = {
  width: '100%',
  padding: '10px',
  marginTop: '6px',
  backgroundColor: '#1f2937',
  color: 'white',
  border: '1px solid #374151',
  borderRadius: '6px',
  boxSizing: 'border-box'
};

export default App;
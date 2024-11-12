import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import './TestPage.css';  // Importing the external CSS file

function TestPage() {
  const [url, setUrl] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null); // State to store ML model prediction
  const location = useLocation();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const testUrl = params.get('url');
    if (testUrl) {
      setUrl(testUrl);
    }
  }, [location]);

  const handleTestClick = async () => {
    if (!url) {
      alert('Please paste a URL');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/test-url', { url });
      setResults(response.data);
    } catch (error) {
      console.error('Error testing URL:', error);
      alert('Error occurred while testing URL');
    } finally {
      setLoading(false);
    }
  };

  const handleRunModelClick = async () => {
    if (!url) {
      alert('Please paste a URL');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/predict-url', { url });
      setPrediction(response.data.prediction);
    } catch (error) {
      console.error('Error running ML model:', error);
      alert('Error occurred while running ML model');
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="test-page">
      <h2>Testing URL: {url}</h2>
      <button className="test-button" onClick={handleTestClick}>Start Testing</button>

      {loading && <div className="loading-circle"></div>} {/* Updated loading circle */}

      {results && (
        <div className="results">
          <h3>Test Results:</h3>
          <div className="result-item">
            <strong>Domain Age:</strong>
            <p>{results.domain_age}</p>
          </div>
          <div className="result-item">
            <strong>SSL Certificate:</strong>
            <p>{results.ssl_certificate}</p>
          </div>
          <div className="result-item">
            <strong>Virus Total Report:</strong>
            <p>{results.virus_total}</p>
          </div>
          <div className="result-item">
            <strong>Similarity Score: </strong>
            <p>{results.web_scraping}</p>
          </div>

          {/* Run ML Model button appears only after results are displayed */}
          <button className="run-model-button" onClick={handleRunModelClick}>Run ML Model</button>
        </div>
      )}
      {/* Display prediction in large, bold text */}
      {prediction && (
        <div className="prediction-result">
          <h3 style={{ fontSize: '24px', fontWeight: 'bold', color: 'red' }}>{prediction}</h3>
        </div>

        
      )}
    </div>
  );
}

export default TestPage;
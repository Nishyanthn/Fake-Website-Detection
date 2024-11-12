import React, { useState } from 'react';
import axios from 'axios';
import './HomePage2.css'; // Import your external CSS file

function HomePage2() {
  const [url, setUrl] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null); // State to store ML model prediction

  // Handle testing URL (VirusTotal, Domain Age, SSL, and Web Scraping)
  const handleTestClick = async () => {
    if (!url) {
      alert('Please enter a URL');
      return;
    }

    setLoading(true);
    try {
      // Send the URL to the backend to run the tests
      const response = await axios.post('http://localhost:5000/test-url', { url });
      setResults(response.data);  // Set the results after receiving response
    } catch (error) {
      console.error('Error testing URL:', error);
      alert('Error occurred while testing URL');
    } finally {
      setLoading(false);
    }
  };

  // Handle running the ML model
  const handleRunModelClick = async () => {
    if (!url) {
      alert('Please enter a URL');
      return;
    }

    setLoading(true);
    try {
      // Send the URL to the backend to run the ML prediction
      const response = await axios.post('http://localhost:5000/predict-url', { url });
      setPrediction(response.data.prediction);  // Set the prediction result
    } catch (error) {
      console.error('Error running ML model:', error);
      alert('Error occurred while running ML model');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home-page2">
      <h2>Enter URL to Test</h2>
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter URL"
        className="inputField"
      />
      <button className="test-button" onClick={handleTestClick}>Start Testing</button>

      {loading && <div className="loading-circle"></div>} {/* Loading circle when tests or model is running */}

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

          {/* Show ML Model Button after results */}
          <button className="run-model-button" onClick={handleRunModelClick}>Run ML Model</button>
        </div>
      )}

      {/* Show prediction after running ML Model */}
      {prediction && (
        <div className="prediction-result">
          <h3 style={{ fontSize: '24px', fontWeight: 'bold', color: 'red' }}>{prediction}</h3>
        </div>
      )}
    </div>
  );
}

export default HomePage2;

import React from 'react';
import { useNavigate } from 'react-router-dom';
import './frontpage.css';  // Import the external CSS file for styling

function FrontPage() {
  const navigate = useNavigate();

  // Handle "Scan" button click - Navigate to HomePage for generating suspicious URLs
  const handleScanClick = () => {
    navigate('/homepage');  // Navigate to the page where the user can generate suspicious URLs
  };

  // Handle "ML Prediction" button click - Navigate to HomePage2 for ML prediction
  const handleMLPredictionClick = () => {
    navigate('/homepage2');  // Navigate to the ML prediction page where the user can input a URL
  };

  return (
    <div className="front-page">
      <h1 className="main-title">Fake Website Detection</h1>
      <div className="container">
        <h2 className="heading">Choose an option:</h2>

        {/* Button for generating suspicious URLs */}
        <button onClick={handleScanClick} className="scanButton">Scan URL</button>

        {/* Button for running the ML model on a given URL */}
        <button onClick={handleMLPredictionClick} className="mlButton">URL Validation</button>
      </div>
    </div>
  );
}


export default FrontPage;

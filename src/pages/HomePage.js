import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';

function HomePage() {
  const [url, setUrl] = useState('');
  const [liveUrls, setLiveUrls] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleRunClick = async () => {
    if (!url) {
      alert('Please enter a URL');
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post('http://localhost:5000/generate-urls', { url });
      setLiveUrls(response.data.live_urls);
    } catch (error) {
      console.error('Error generating URLs:', error);
      alert('Error occurred while generating URLs');
    } finally {
      setLoading(false);
    }
  };

  const handleStartTestingClick = (testUrl) => {
    navigate(`/test?url=${encodeURIComponent(testUrl)}`);
  };

  return (
    <div>
      <h1 className="main-title">Fake Website Detection</h1> {/* Title outside container */}
      <div className="container">
        <h2 className="heading">Enter URL to Generate Suspicious URLs</h2>
        <input 
          type="text" 
          value={url} 
          onChange={(e) => setUrl(e.target.value)} 
          placeholder="Enter original URL"
          className="inputField"
        />
        <button onClick={handleRunClick} className="runButton">Run</button>

        {loading && <div className="loading-circle"></div>} {/* Loading circle */}

        {liveUrls.length > 0 && (
          <div className="liveUrls">
            <h3 className="heading">Live Suspicious URLs:</h3>
            <ul className="urlList">
              {liveUrls.map((liveUrl, index) => (
                <li key={index} className="urlItem">
                  {liveUrl}
                  <button 
                    onClick={() => handleStartTestingClick(liveUrl)} 
                    className="startTestingButton"
                  >
                    Check
                  </button>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );  
}

export default HomePage;
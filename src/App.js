import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import FrontPage from './pages/frontpage';   // Import the FrontPage component (all lowercase)
import HomePage from './pages/HomePage';     // Import the HomePage component for URL generation
import HomePage2 from './pages/HomePage2';   // Import the HomePage2 component for ML prediction
import TestPage from './pages/TestPage';     // Import the TestPage component for testing suspicious URLs

function App() {
  return (
    <Router>
      <Routes>
        {/* FrontPage route with buttons for scanning or ML prediction */}
        <Route path="/" element={<FrontPage />} />

        {/* HomePage route for URL generation and testing */}
        <Route path="/homepage" element={<HomePage />} />

        {/* HomePage2 route for ML prediction */}
        <Route path="/homepage2" element={<HomePage2 />} />

        {/* TestPage route for testing suspicious URLs */}
        <Route path="/test" element={<TestPage />} />
      </Routes>
    </Router>
  );
}

export default App;





























// import React from 'react';
// import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
// import HomePage from './pages/HomePage';
// import TestPage from './pages/TestPage';

// function App() {
//   return (
//     <Router>
//       <Routes>
//         <Route path="/" element={<HomePage />} />
//         <Route path="/test" element={<TestPage />} />
//       </Routes>
//     </Router>
//   );
// }

// export default App;













// // src/App.js
// import React, { useState } from "react";
// import axios from "axios";
// import "./App.css";

// function App() {
//   const [url, setUrl] = useState("");
//   const [resultsData, setResultsData] = useState({});
//   const [loading, setLoading] = useState(false);
//   const [progress, setProgress] = useState(0);

//   const startDetection = () => {
//     if (!url) {
//       alert("Please enter a URL.");
//       return;
//     }

//     setLoading(true); // Show loading spinner
//     setProgress(10); // Set progress to 10%

//     axios
//       .post("http://127.0.0.1:5000/detect", { url: url }, {
//         headers: { "Content-Type": "application/json" },
//       })
//       .then((response) => {
//         setLoading(false); // Hide loading spinner
//         setProgress(100); // Set progress to 100%
//         setResultsData(response.data); // Store the results data
//       })
//       .catch(() => {
//         setLoading(false); // Hide loading spinner
//         setProgress(0); // Reset progress
//         alert("An error occurred while processing. Please try again.");
//       });
//   };

//   const showResults = () => {
//     let resultHTML = "";
//     for (const [url, result] of Object.entries(resultsData)) {
//       const sslResultKey = `${url}_ssl`; // Key for SSL validation result
//       const sslResult = resultsData[sslResultKey] || "No SSL validation result";

//       // Determine row color based on detection and SSL results
//       let rowColor;
//       if (result.includes("safe") && sslResult.includes("valid")) {
//         rowColor = "table-success"; // Green for safe and valid
//       } else if (result.includes("fake") || !sslResult.includes("valid")) {
//         rowColor = "table-danger"; // Red for fake or invalid SSL
//       } else {
//         rowColor = ""; // Default color (optional)
//       }

//       resultHTML += `<tr class="${rowColor}"><td>${url}</td><td>${result}</td><td>${sslResult}</td></tr>`;
//     }
//     return resultHTML;
//   };

//   return (
//     <div className="container mt-5">
//       <h2 className="text-center">FAKE WEBSITE DETECTION</h2>
//       <div className="form-group">
//         <input
//           type="text"
//           className="form-control"
//           id="url-input"
//           value={url}
//           onChange={(e) => setUrl(e.target.value)}
//           placeholder="Enter the URL"
//         />
//       </div>
//       <button className="btn btn-primary" onClick={startDetection}>
//         Start Detection
//       </button>
//       <div className="progress mt-3" style={{ height: "20px" }}>
//         <div
//           className="progress-bar"
//           id="progress-bar"
//           role="progressbar"
//           style={{ width: `${progress}%` }}
//           aria-valuenow={progress}
//           aria-valuemin="0"
//           aria-valuemax="100"
//         >
//           {progress}% - {progress === 0 ? "Error" : progress === 100 ? "Completed" : "In Progress"}
//         </div>
//       </div>

//       {loading && (
//         <div id="loading" className="text-center mt-3">
//           <img
//             src="templates/Magnify@1x-1.0s-200px-200px.gif"
//             alt="Loading..."
//             style={{ width: "50px", height: "50px" }}
//           />
//         </div>
//       )}
//       <button
//         className="btn btn-success mt-3"
//         id="show-results-btn"
//         style={{ display: Object.keys(resultsData).length > 0 ? "block" : "none" }}
//         onClick={showResults}
//       >
//         Show Results
//       </button>

//       {Object.keys(resultsData).length > 0 && (
//         <div id="results" className="mt-3">
//           <table className="table table-bordered">
//             <thead>
//               <tr>
//                 <th>URL</th>
//                 <th>Detection Result</th>
//                 <th>SSL Validation Result</th>
//               </tr>
//             </thead>
//             <tbody dangerouslySetInnerHTML={{ __html: showResults() }}></tbody>
//           </table>
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;

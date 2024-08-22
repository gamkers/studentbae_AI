import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './Login';
import Signup from './Signup';
import Home from './Chat';
import './App.css';  

function App() {
  const [isAuthenticated, setIsAuthenticated] = React.useState(false);

  // Check authentication status on component mount
  React.useEffect(() => {
    fetch('http://localhost:5000/check_auth', {
      credentials: 'include', // Include credentials in requests to handle session cookies
    })
      .then(response => response.json())
      .then(data => {
        console.log('Authentication status:', data); // Debugging line
        setIsAuthenticated(data.authenticated);
      })
      .catch(error => {
        console.error('Error checking authentication:', error);
        setIsAuthenticated(false); // Ensure unauthenticated state on error
      });
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/chat" element={isAuthenticated ? <Home /> : <Navigate to="/login" />} />
        <Route path="/" element={<Navigate to={isAuthenticated ? "/chat" : "/login"} />} />
      </Routes>
    </Router>
  );
}

export default App;

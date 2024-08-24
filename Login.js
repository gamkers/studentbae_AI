import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // Import useNavigate for navigation

const Login = ({ setIsAuthenticated }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate(); // Initialize useNavigate for programmatic navigation

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/login', { email, password }, { withCredentials: true });
            alert(response.data.message);
            // Set authentication status and redirect to chat
            setIsAuthenticated(true);
            navigate('/chat');
        } catch (error) {
            setError(error.response?.data?.error || 'An error occurred'); // Set error message for display
        }
    };

    return (
        <div className="container">
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email"
                    required
                />
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                    required
                />
                <button type="submit">Login</button>
                {error && <p>{error}</p>} {/* Display error message if exists */}
            </form>
            <p>Don't have an account? <a href="/signup">Sign up</a></p> {/* Link to sign-up page */}
        </div>
    );
};

export default Login;

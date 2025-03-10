// src/components/Login.js
import React, { useState } from 'react';
import { post } from '../apiService';
import { useNavigate } from 'react-router-dom';  // ✅ Import useNavigate

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();  // ✅ Hook for navigation

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(''); // Reset error state
  
    try {
      const response = await post('/login/', { email, password });  // ✅ Added trailing slash
      console.log('Logged in:', response);
  
      localStorage.setItem('user', JSON.stringify(response.user));
  
      navigate('/chat/inbox/my-inbox');  // ✅ Redirect to correct inbox path
    } catch (error) {
      setError(error.error || 'Login failed. Please try again.');
    }
  };
  

  return (
    <div>
      <h1>Login</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleLogin}>
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
      </form>
    </div>
  );
};

export default Login;

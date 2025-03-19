import React, { useState, useEffect } from 'react';
import { post, get } from '../apiService';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // ✅ Ensure CSRF cookie is set before login attempt
  useEffect(() => {
    get('/csrf/')
      .then(() => console.log('CSRF token set'))
      .catch(() => console.warn('CSRF token not set'));
  }, []);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await post('/login/', { email, password });
      console.log('Logged in:', response);

      navigate('/chat/inbox/');  // ✅ Redirect to inbox
    } catch (error) {
      console.error('Login Error:', error);
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

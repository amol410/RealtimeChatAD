import React, { useState } from 'react';
import { post } from '../apiService';

const Register = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState(''); // ✅ Success message
  const [error, setError] = useState(''); // ✅ Error message

  const handleRegister = async (e) => {
    e.preventDefault();
    setMessage('');
    setError('');

    const requestData = {
      username: username.trim(),
      email: email.trim(),
      password: password.trim()
    };

    console.log('Sending Data:', requestData); // Debugging

    try {
      const response = await post('/register/', requestData);
      console.log('Success:', response);

      setMessage(response.message || 'Registration successful!'); // ✅ Show success message
      setUsername('');
      setEmail('');
      setPassword('');
    } catch (error) {
      console.error('Registration Error:', error.response?.data || error.message);
      setError(error.response?.data?.error || 'Registration failed. Please try again.');
    }
  };

  return (
    <div>
      <h1>Register</h1>
      {message && <p style={{ color: 'green' }}>{message}</p>} {/* ✅ Success message */}
      {error && <p style={{ color: 'red' }}>{error}</p>} {/* ✅ Error message */}
      
      <form onSubmit={handleRegister}>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
          required
        />
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
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Register;

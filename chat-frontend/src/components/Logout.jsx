// src/components/Logout.js
import React from 'react';
import { post } from '../apiService';

const Logout = () => {
  const handleLogout = () => {
    // Send logout request
    post('/logout', {})
      .then(data => console.log('Logged out', data))
      .catch(error => console.error('Logout failed', error));
  };

  return (
    <div>
      <h1>Logout</h1>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default Logout;

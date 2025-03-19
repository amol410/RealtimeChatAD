// src/components/Inbox.js
import React, { useState, useEffect } from 'react';
import { get } from '../apiService';

const Inbox = () => {
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    get('/chat/inbox/')
      .then(data => {
        console.log('Inbox API Response:', data); // ✅ Debugging
        setMessages(Array.isArray(data) ? data : [data]); // ✅ Ensure it's always an array
      })
      .catch(error => {
        console.error('Error fetching inbox messages:', error);
        setError('Failed to load messages');
      });
  }, []);

  return (
    <div>
      <h1>My Inbox</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <ul>
        {messages.length > 0 ? (
          messages.map((msg, index) => (
            <li key={index}>
              <strong>{msg.sender_profile?.full_name}:</strong> {msg.message}  
              <br />
              <small>{new Date(msg.date).toLocaleString()}</small>
            </li>
          ))
        ) : (
          <p>No messages found.</p>
        )}
      </ul>
    </div>
  );
};

export default Inbox;

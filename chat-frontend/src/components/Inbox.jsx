// src/components/Inbox.js
import React, { useState, useEffect } from 'react';
import { get } from '../apiService';

const Inbox = () => {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    // Fetch messages from the inbox
    get('/chat/inbox/my-inbox')
      .then(data => setMessages(data))
      .catch(error => console.error('Error fetching inbox messages', error));
  }, []);

  return (
    <div>
      <h1>My Inbox</h1>
      <ul>
        {messages.map((message, index) => (
          <li key={index}>{message.content}</li>
        ))}
      </ul>
    </div>
  );
};

export default Inbox;

// src/components/ChatHistory.js
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { get } from '../apiService';

const ChatHistory = () => {
  const { userId } = useParams();
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    // Fetch chat history for a specific user
    get(`/chat/history/${userId}`)
      .then(data => setMessages(data))
      .catch(error => console.error('Error fetching chat history', error));
  }, [userId]);

  return (
    <div>
      <h1>Chat History</h1>
      <ul>
        {messages.map((message, index) => (
          <li key={index}>{message.content}</li>
        ))}
      </ul>
    </div>
  );
};

export default ChatHistory;

// src/components/Messages.js
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { get } from '../apiService';

const Messages = () => {
  const { senderId, receiverId } = useParams();
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    // Fetch messages between two users
    get(`/chat/messages/${senderId}/${receiverId}`)
      .then(data => setMessages(data))
      .catch(error => console.error('Error fetching messages', error));
  }, [senderId, receiverId]);

  return (
    <div>
      <h1>Messages</h1>
      <ul>
        {messages.map((message, index) => (
          <li key={index}>{message.content}</li>
        ))}
      </ul>
    </div>
  );
};

export default Messages;

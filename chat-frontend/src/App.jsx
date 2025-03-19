// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Inbox from './components/Inbox';
import ChatHistory from './components/chathistory';
import Messages from './components/Messages';
import Login from './components/Login';
import Register from './components/Register';
import Logout from './components/Logout';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/chat/inbox" element={<Inbox />} />
        <Route path="/chat/history/:userId" element={<ChatHistory />} />
        <Route path="/chat/messages/:senderId/:receiverId" element={<Messages />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/logout" element={<Logout />} />
      </Routes>
    </Router>
  );
};

export default App;

import React from 'react';
import { Routes, Route, BrowserRouter as Router } from 'react-router-dom';
import Home from './pages/Home';
import Marketplace from './pages/Marketplace';
import Proposals from './pages/Proposals';
import Ratings from './pages/Ratings';
import UserProfile from './pages/UserProfile';
import AdminPanel from './pages/AdminPanel';

const App = () => {
  return (
    <div>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/marketplace" element={<Marketplace />} />
          <Route path="/proposals" element={<Proposals />} />
          <Route path="/ratings" element={<Ratings />} />
          <Route path="/profile" element={<UserProfile />} />
          <Route path="/admin" element={<AdminPanel />} />
        </Routes>
      </Router>
    </div>
  );
};

export default App;

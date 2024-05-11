import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Search from './pages/Search';

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Search />} />
    </Routes>
  );
};

export default App;


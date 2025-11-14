import React, { useState } from 'react';
import ChatbotMessenger from './components/ChatbotMessenger';
import CodeGenerator from './components/CodeGenerator';
import CodeValidator from './components/CodeValidator';
import './index.css';

function App() {
  const [activeTab, setActiveTab] = useState('messenger');

  return (
    <div className="App">
      <nav className="navbar">
        <div className="navbar-content">
          <h1 className="logo">🚀 AI Code Assistant</h1>
          <div className="nav-tabs">
            <button 
              className={`nav-tab ${activeTab === 'messenger' ? 'active' : ''}`}
              onClick={() => setActiveTab('messenger')}
            >
              💬 Chat
            </button>
            <button 
              className={`nav-tab ${activeTab === 'generator' ? 'active' : ''}`}
              onClick={() => setActiveTab('generator')}
            >
              🤖 Code Generator
            </button>
            <button 
              className={`nav-tab ${activeTab === 'validator' ? 'active' : ''}`}
              onClick={() => setActiveTab('validator')}
            >
              ✓ Validator
            </button>
          </div>
        </div>
      </nav>

      <main className="main-content">
        {activeTab === 'messenger' && <ChatbotMessenger />}
        {activeTab === 'generator' && <CodeGenerator />}
        {activeTab === 'validator' && <CodeValidator />}
      </main>
    </div>
  );
}

export default App;
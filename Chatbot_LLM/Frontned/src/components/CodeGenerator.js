import React, { useState } from 'react';
import { Copy, Download, Zap } from 'lucide-react';
import '../styles/CodeGenerator.css';

const CodeGenerator = () => {
  const [query, setQuery] = useState('');
  const [language, setLanguage] = useState('python');
  const [generatedCode, setGeneratedCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const generateCode = async () => {
    if (!query.trim()) {
      alert('Please enter a code generation query');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/generate-code`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, language })
      });

      const data = await response.json();
      if (data.status === 'success') {
        setGeneratedCode(data.code);
      } else {
        alert('Error: ' + (data.error || 'Failed to generate code'));
      }
    } catch (error) {
      alert('Error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const copyCode = () => {
    navigator.clipboard.writeText(generatedCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const downloadCode = () => {
    const extensions = {
      python: 'py',
      javascript: 'js',
      java: 'java',
      cpp: 'cpp',
      csharp: 'cs',
      go: 'go',
      rust: 'rs'
    };

    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(generatedCode));
    element.setAttribute('download', `generated_code.${extensions[language] || 'txt'}`);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="code-generator-container">
      <div className="generator-header">
        <h2>🤖 AI Code Generator</h2>
        <p>Describe what you need, and let AI generate the code for you</p>
      </div>

      <div className="generator-input-section">
        <div className="input-group">
          <label>What do you want to generate?</label>
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="E.g., Create a function to calculate fibonacci number with memoization..."
            rows="4"
            disabled={loading}
          />
        </div>

        <div className="input-row">
          <div className="input-group">
            <label>Programming Language</label>
            <select 
              value={language} 
              onChange={(e) => setLanguage(e.target.value)}
              disabled={loading}
            >
              <option value="python">Python</option>
              <option value="javascript">JavaScript</option>
              <option value="java">Java</option>
              <option value="cpp">C++</option>
              <option value="csharp">C#</option>
              <option value="go">Go</option>
              <option value="rust">Rust</option>
            </select>
          </div>

          <button 
            className="btn-generate" 
            onClick={generateCode}
            disabled={loading}
          >
            <Zap size={18} />
            {loading ? 'Generating...' : 'Generate Code'}
          </button>
        </div>
      </div>

      {generatedCode && (
        <div className="generator-output-section">
          <div className="output-header">
            <h3>Generated Code</h3>
            <div className="output-actions">
              <button 
                className="btn-secondary" 
                onClick={copyCode}
                title="Copy to clipboard"
              >
                <Copy size={16} />
                {copied ? 'Copied!' : 'Copy'}
              </button>
              <button 
                className="btn-secondary" 
                onClick={downloadCode}
                title="Download file"
              >
                <Download size={16} />
                Download
              </button>
            </div>
          </div>

          <pre className="code-output">
            <code>{generatedCode}</code>
          </pre>
        </div>
      )}
    </div>
  );
};

export default CodeGenerator;

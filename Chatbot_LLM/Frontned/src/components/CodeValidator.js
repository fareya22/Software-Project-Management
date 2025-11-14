import React, { useState } from 'react';
import { CheckCircle, AlertCircle, Zap } from 'lucide-react';
import '../styles/CodeValidator.css';

const CodeValidator = () => {
  const [generatedCode, setGeneratedCode] = useState('');
  const [referenceCode, setReferenceCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [validationResult, setValidationResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const validateCode = async () => {
    if (!generatedCode.trim() || !referenceCode.trim()) {
      alert('Please enter both generated and reference code');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/validate-code`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          generated_code: generatedCode,
          reference_code: referenceCode,
          language
        })
      });

      const data = await response.json();
      if (data.status === 'success') {
        setValidationResult(data);
      } else {
        alert('Error: ' + (data.error || 'Validation failed'));
      }
    } catch (error) {
      alert('Error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const getQualityColor = (quality) => {
    switch (quality) {
      case 'Excellent': return '#10b981';
      case 'Good': return '#3b82f6';
      case 'Fair': return '#f59e0b';
      case 'Poor': return '#ef4444';
      default: return '#6b7280';
    }
  };

  const getQualityIcon = (quality) => {
    if (quality === 'Excellent' || quality === 'Good') {
      return <CheckCircle size={20} color={getQualityColor(quality)} />;
    }
    return <AlertCircle size={20} color={getQualityColor(quality)} />;
  };

  return (
    <div className="code-validator-container">
      <div className="validator-header">
        <h2>✓ Code Quality Validator</h2>
        <p>Compare generated code against reference code using CodeBLEU metric</p>
      </div>

      <div className="validator-input-section">
        <div className="code-comparison">
          <div className="code-box">
            <label>Generated Code</label>
            <textarea
              value={generatedCode}
              onChange={(e) => setGeneratedCode(e.target.value)}
              placeholder="Paste your generated code here..."
              rows="8"
              disabled={loading}
            />
          </div>

          <div className="code-box">
            <label>Reference Code</label>
            <textarea
              value={referenceCode}
              onChange={(e) => setReferenceCode(e.target.value)}
              placeholder="Paste the reference/expected code here..."
              rows="8"
              disabled={loading}
            />
          </div>
        </div>

        <div className="validator-controls">
          <div className="input-group">
            <label>Language</label>
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
            </select>
          </div>

          <button 
            className="btn-validate" 
            onClick={validateCode}
            disabled={loading}
          >
            <Zap size={18} />
            {loading ? 'Validating...' : 'Validate Code'}
          </button>
        </div>
      </div>

      {validationResult && (
        <div className="validator-result">
          <div className="result-card" style={{ borderColor: getQualityColor(validationResult.quality) }}>
            <div className="result-header">
              <div className="result-icon">
                {getQualityIcon(validationResult.quality)}
              </div>
              <div className="result-info">
                <h3>Quality Assessment</h3>
                <p style={{ color: getQualityColor(validationResult.quality) }}>
                  {validationResult.quality}
                </p>
              </div>
            </div>

            <div className="score-section">
              <div className="score-display">
                <span className="score-label">CodeBLEU Score</span>
                <span 
                  className="score-value" 
                  style={{ color: getQualityColor(validationResult.quality) }}
                >
                  {(validationResult.codebleu_score * 100).toFixed(2)}%
                </span>
              </div>
              <div className="score-bar">
                <div 
                  className="score-fill" 
                  style={{ 
                    width: `${validationResult.codebleu_score * 100}%`,
                    backgroundColor: getQualityColor(validationResult.quality)
                  }}
                />
              </div>
            </div>

            <div className="quality-guide">
              <h4>Quality Levels:</h4>
              <ul>
                <li><span className="badge excellent">Excellent</span> ≥ 85%</li>
                <li><span className="badge good">Good</span> 70-84%</li>
                <li><span className="badge fair">Fair</span> 50-69%</li>
                <li><span className="badge poor">Poor</span> &lt; 50%</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CodeValidator;

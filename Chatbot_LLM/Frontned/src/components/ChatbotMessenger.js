import React, { useMemo } from 'react';
import { Send, Bot, User } from 'lucide-react';
import { useChat } from '../hooks/useChat';

export default function ChatbotMessenger() {
  const {
    messages,
    input,
    setInput,
    isLoading,
    sendMessage,
    handleKeyPress,
    messagesEndRef
  } = useChat();

  // Memoized message formatting function
  const formatMessage = useMemo(() => {
    const formatInlineElements = (text) => {
      if (!text.includes('**') && !text.includes('`')) {
        return text;
      }

      const parts = [];
      let currentText = text;
      let key = 0;

      // Handle bold text
      currentText = currentText.replace(/\*\*(.*?)\*\*/g, (match, boldText) => {
        parts.push(<strong key={key++} className="font-semibold text-gray-800">{boldText}</strong>);
        return `%%BOLD_${key - 1}%%`;
      });

      // Handle inline code
      currentText = currentText.replace(/`(.*?)`/g, (match, codeText) => {
        parts.push(<code key={key++} className="bg-gray-100 px-1 py-0.5 rounded text-xs font-mono text-gray-800">{codeText}</code>);
        return `%%CODE_${key - 1}%%`;
      });

      // Replace placeholders
      const segments = currentText.split(/(%%.*?%%)/);
      return segments.map((segment, index) => {
        if (segment.startsWith('%%BOLD_')) {
          const boldIndex = parseInt(segment.match(/%%BOLD_(\d+)%%/)[1]);
          return parts[boldIndex];
        }
        if (segment.startsWith('%%CODE_')) {
          const codeIndex = parseInt(segment.match(/%%CODE_(\d+)%%/)[1]);
          return parts[codeIndex];
        }
        return segment;
      });
    };

    return (text, isBot) => {
      if (!isBot) return text;

      // Simple cleanup
      let cleanedText = text.replace(/\*•/g, '').replace(/\*\*/g, '**');

      // Split into paragraphs
      const paragraphs = cleanedText.split('\n\n').filter(p => p.trim());

      return paragraphs.map((paragraph, index) => {
        let processedParagraph = paragraph;

        // Handle headings
        if (processedParagraph.trim().startsWith('###')) {
          const headingText = processedParagraph.replace(/^###\s*/, '');
          return (
            <h3 key={index} className="mb-3 text-base font-semibold text-blue-700 border-b border-blue-200 pb-1">
              {headingText}
            </h3>
          );
        }

        if (processedParagraph.trim().startsWith('##')) {
          const headingText = processedParagraph.replace(/^##\s*/, '');
          return (
            <h2 key={index} className="mb-3 text-lg font-bold text-blue-800">
              {headingText}
            </h2>
          );
        }

        // Handle bullet points
        if (processedParagraph.trim().startsWith('•') || processedParagraph.trim().match(/^\d+\./) || processedParagraph.trim().startsWith('- ')) {
          const bulletText = processedParagraph.replace(/^•\s*/, '').replace(/^\d+\.\s*/, '').replace(/^- \s*/, '');
          const isNumbered = processedParagraph.trim().match(/^\d+\./);
          const number = isNumbered ? isNumbered[0] : null;

          return (
            <div key={index} className="mb-2 ml-4">
              <div className="flex items-start gap-2">
                <span className="text-blue-500 mt-1 flex-shrink-0 min-w-[20px]">
                  {number || '•'}
                </span>
                <div className="flex-1">{formatInlineElements(bulletText)}</div>
              </div>
            </div>
          );
        }

        // Handle code blocks
        if (processedParagraph.includes('```')) {
          const codeBlockRegex = /```(\w+)?\s*\n?([\s\S]*?)\n?```/g;
          const codeMatch = codeBlockRegex.exec(processedParagraph);

          if (codeMatch) {
            const language = codeMatch[1] || 'python';
            const codeContent = codeMatch[2].trim();

            return (
              <div key={index} className="mb-3">
                <div className="bg-gray-800 text-gray-100 p-3 rounded-lg text-xs font-mono overflow-x-auto border">
                  <div className="text-gray-400 text-xs mb-2 uppercase tracking-wide">
                    {language}
                  </div>
                  <pre className="whitespace-pre-wrap">
                    <code className={`language-${language}`}>
                      {codeContent}
                    </code>
                  </pre>
                </div>
              </div>
            );
          }
        }

        // Regular paragraph
        return (
          <p key={index} className="mb-3 leading-relaxed">
            {formatInlineElements(processedParagraph)}
          </p>
        );
      });
    };
  }, []);

  // Memoized Message Component
  const MessageComponent = React.memo(({ msg }) => (
    <div
      className={`flex gap-3 ${msg.sender === 'user' ? 'flex-row-reverse' : 'flex-row'}`}
    >
      <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
        msg.sender === 'user'
          ? 'bg-gray-700'
          : 'bg-gradient-to-br from-blue-500 to-blue-600'
      }`}>
        {msg.sender === 'user' ? (
          <User className="w-5 h-5 text-white" />
        ) : (
          <Bot className="w-5 h-5 text-white" />
        )}
      </div>

      <div className={`max-w-[70%] ${msg.sender === 'user' ? 'items-end' : 'items-start'} flex flex-col gap-1`}>
        <div className={`px-4 py-2.5 rounded-2xl ${
          msg.sender === 'user'
            ? 'bg-blue-600 text-white rounded-tr-sm'
            : 'bg-white text-gray-800 border border-gray-200 rounded-tl-sm shadow-sm'
        }`}>
          {msg.sender === 'bot' ? (
            <div className="text-sm">
              {formatMessage(msg.text, true)}
            </div>
          ) : (
            <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.text}</p>
          )}
        </div>
        <span className="text-xs text-gray-400 px-1">
          {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>
    </div>
  ));

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-gray-900">ChatBot</h1>
            <p className="text-xs text-gray-500">Always here to help</p>
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto px-4 py-6 messages-container">
        <div className="max-w-3xl mx-auto space-y-4">
          {messages.map((msg) => (
            <div key={msg.id} className="message-item">
              <MessageComponent msg={msg} />
            </div>
          ))}

          {isLoading && (
            <div className="flex gap-3">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div className="bg-white border border-gray-200 px-4 py-3 rounded-2xl rounded-tl-sm shadow-sm">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 px-4 py-4">
        <div className="max-w-3xl mx-auto">
          <div className="flex gap-3 items-end">
            <div className="flex-1 bg-gray-100 rounded-3xl px-5 py-3 focus-within:bg-white focus-within:ring-2 focus-within:ring-blue-500 transition-all">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type a message..."
                disabled={isLoading}
                className="w-full bg-transparent outline-none text-gray-900 placeholder-gray-500 text-sm"
              />
            </div>
            <button
              onClick={sendMessage}
              disabled={!input.trim() || isLoading}
              className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors shadow-lg"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
import React, { useState, useRef, useEffect } from 'react';
import { FiSend } from 'react-icons/fi';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

const ChatBox: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    const botMessage: Message = {
      id: (Date.now() + 1).toString(),
      text: '',
      isUser: false,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, botMessage]);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: inputValue }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const mode = process.env.NEXT_PUBLIC_NLUX_MODE;

      if (mode === 'stream' && response.body) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
          const { value, done } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          if (chunk) {
            setMessages(prev => 
              prev.map(msg => 
                msg.id === botMessage.id 
                  ? { ...msg, text: msg.text + chunk }
                  : msg
              )
            );
          }
        }
      } else {
        const data = await response.json();
        setMessages(prev => 
          prev.map(msg => 
            msg.id === botMessage.id 
              ? { ...msg, text: data.message || 'No response received' }
              : msg
          )
        );
      }
    } catch (err) {
      console.error('Chat error:', err);
      setMessages(prev => 
        prev.map(msg => 
          msg.id === botMessage.id 
            ? { ...msg, text: 'Error: Failed to get response' }
            : msg
        )
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-container" style={{ height: '80vh', display: 'flex', flexDirection: 'column' }}>
      <div 
        style={{ 
          flex: 1, 
          overflowY: 'auto', 
          padding: '1rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '0.5rem'
        }}
      >
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', color: 'var(--accent)', padding: '2rem' }}>
            Start a conversation...
          </div>
        )}
        
        {messages.map((message) => (
          <div
            key={message.id}
            style={{
              alignSelf: message.isUser ? 'flex-end' : 'flex-start',
              maxWidth: '70%',
              padding: '0.75rem',
              borderRadius: '8px',
              backgroundColor: message.isUser ? 'var(--accent)' : 'var(--hover)',
              color: 'var(--text)',
              wordWrap: 'break-word',
            }}
          >
            {message.text}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      <div style={{ padding: '1rem', borderTop: '1px solid var(--border)' }}>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <textarea
            className="chat-input"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            rows={1}
            style={{ flex: 1 }}
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={!inputValue.trim() || isLoading}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              minWidth: '50px',
              opacity: !inputValue.trim() || isLoading ? 0.5 : 1,
            }}
          >
            <FiSend size={18} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatBox;
import Head from "next/head";
import React, { useState } from "react";

export default function Settings() {
  const [apiKey, setApiKey] = useState("");
  const [apiUrl, setApiUrl] = useState("https://api.nlux.com/v1/chat");
  const [mode, setMode] = useState("stream");
  const [theme, setTheme] = useState("dark");

  const handleSave = () => {
    // In a real app, you would save these to localStorage or a backend
    alert("Settings saved!");
  };

  return (
    <>
      <Head>
        <title>Aegis Nexus - Settings</title>
        <meta name="description" content="Application Settings" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div>
        <h1 style={{ 
          fontSize: '2.5rem', 
          fontWeight: 'bold', 
          marginBottom: '2rem',
          color: 'var(--text)'
        }}>
          Settings
        </h1>
        
        <div style={{
          maxWidth: '600px'
        }}>
          <div style={{
            background: 'var(--panel)',
            padding: '2rem',
            borderRadius: '8px',
            border: '1px solid var(--border)',
            marginBottom: '2rem'
          }}>
            <h2 style={{
              fontSize: '1.5rem',
              marginBottom: '1.5rem',
              color: 'var(--text)'
            }}>
              API Configuration
            </h2>
            
            <div style={{ marginBottom: '1.5rem' }}>
              <label style={{
                display: 'block',
                marginBottom: '0.5rem',
                color: 'var(--text)',
                fontWeight: '500'
              }}>
                API Key
              </label>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="Enter your NLUX API key"
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  backgroundColor: 'var(--bg)',
                  color: 'var(--text)',
                  border: '1px solid var(--border)',
                  borderRadius: '4px',
                  outline: 'none'
                }}
              />
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={{
                display: 'block',
                marginBottom: '0.5rem',
                color: 'var(--text)',
                fontWeight: '500'
              }}>
                API URL
              </label>
              <input
                type="url"
                value={apiUrl}
                onChange={(e) => setApiUrl(e.target.value)}
                placeholder="https://api.nlux.com/v1/chat"
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  backgroundColor: 'var(--bg)',
                  color: 'var(--text)',
                  border: '1px solid var(--border)',
                  borderRadius: '4px',
                  outline: 'none'
                }}
              />
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={{
                display: 'block',
                marginBottom: '0.5rem',
                color: 'var(--text)',
                fontWeight: '500'
              }}>
                Response Mode
              </label>
              <select
                value={mode}
                onChange={(e) => setMode(e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  backgroundColor: 'var(--bg)',
                  color: 'var(--text)',
                  border: '1px solid var(--border)',
                  borderRadius: '4px',
                  outline: 'none'
                }}
              >
                <option value="stream">Streaming</option>
                <option value="single">Single Response</option>
              </select>
            </div>
          </div>

          <div style={{
            background: 'var(--panel)',
            padding: '2rem',
            borderRadius: '8px',
            border: '1px solid var(--border)',
            marginBottom: '2rem'
          }}>
            <h2 style={{
              fontSize: '1.5rem',
              marginBottom: '1.5rem',
              color: 'var(--text)'
            }}>
              Appearance
            </h2>
            
            <div style={{ marginBottom: '1.5rem' }}>
              <label style={{
                display: 'block',
                marginBottom: '0.5rem',
                color: 'var(--text)',
                fontWeight: '500'
              }}>
                Theme
              </label>
              <select
                value={theme}
                onChange={(e) => setTheme(e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  backgroundColor: 'var(--bg)',
                  color: 'var(--text)',
                  border: '1px solid var(--border)',
                  borderRadius: '4px',
                  outline: 'none'
                }}
              >
                <option value="dark">Dark</option>
                <option value="light">Light</option>
                <option value="auto">Auto</option>
              </select>
            </div>
          </div>

          <div style={{
            background: 'var(--panel)',
            padding: '2rem',
            borderRadius: '8px',
            border: '1px solid var(--border)'
          }}>
            <h2 style={{
              fontSize: '1.5rem',
              marginBottom: '1.5rem',
              color: 'var(--text)'
            }}>
              System Information
            </h2>
            
            <div style={{ display: 'grid', gap: '1rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text)', opacity: 0.8 }}>Version:</span>
                <span style={{ color: 'var(--text)' }}>1.0.0</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text)', opacity: 0.8 }}>Build:</span>
                <span style={{ color: 'var(--text)' }}>2024.01.15</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text)', opacity: 0.8 }}>Environment:</span>
                <span style={{ color: 'var(--text)' }}>Development</span>
              </div>
            </div>
          </div>

          <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem' }}>
            <button
              onClick={handleSave}
              style={{
                padding: '0.75rem 2rem',
                backgroundColor: 'var(--accent)',
                color: 'var(--text)',
                border: '1px solid var(--border)',
                borderRadius: '6px',
                cursor: 'pointer',
                fontWeight: '500'
              }}
            >
              Save Settings
            </button>
            <button
              style={{
                padding: '0.75rem 2rem',
                backgroundColor: 'transparent',
                color: 'var(--text)',
                border: '1px solid var(--border)',
                borderRadius: '6px',
                cursor: 'pointer'
              }}
            >
              Reset to Defaults
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
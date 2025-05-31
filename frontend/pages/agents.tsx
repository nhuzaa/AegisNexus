import Head from "next/head";
import React from "react";

export default function Agents() {
  const agents = [
    {
      id: 1,
      name: "Customer Support Agent",
      status: "Active",
      description: "Handles customer inquiries and support tickets",
      lastActive: "2 minutes ago"
    },
    {
      id: 2,
      name: "Data Analysis Agent",
      status: "Inactive",
      description: "Processes and analyzes large datasets",
      lastActive: "1 hour ago"
    },
    {
      id: 3,
      name: "Code Review Agent",
      status: "Active",
      description: "Reviews code changes and suggests improvements",
      lastActive: "5 minutes ago"
    }
  ];

  return (
    <>
      <Head>
        <title>Aegis Nexus - AI Agents</title>
        <meta name="description" content="Manage AI Agents" />
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
          AI Agents
        </h1>
        
        <div style={{ marginBottom: '2rem' }}>
          <button style={{
            padding: '0.75rem 1.5rem',
            backgroundColor: 'var(--accent)',
            color: 'var(--text)',
            border: '1px solid var(--border)',
            borderRadius: '6px',
            cursor: 'pointer'
          }}>
            Create New Agent
          </button>
        </div>

        <div style={{
          display: 'grid',
          gap: '1rem'
        }}>
          {agents.map((agent) => (
            <div key={agent.id} style={{
              background: 'var(--panel)',
              padding: '1.5rem',
              borderRadius: '8px',
              border: '1px solid var(--border)',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}>
              <div>
                <h3 style={{ 
                  marginBottom: '0.5rem', 
                  color: 'var(--text)',
                  fontSize: '1.25rem'
                }}>
                  {agent.name}
                </h3>
                <p style={{ 
                  color: 'var(--text)', 
                  opacity: 0.8,
                  marginBottom: '0.5rem'
                }}>
                  {agent.description}
                </p>
                <p style={{ 
                  color: 'var(--text)', 
                  opacity: 0.6,
                  fontSize: '0.875rem'
                }}>
                  Last active: {agent.lastActive}
                </p>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <span style={{
                  padding: '0.25rem 0.75rem',
                  borderRadius: '4px',
                  fontSize: '0.875rem',
                  backgroundColor: agent.status === 'Active' ? '#10b981' : '#6b7280',
                  color: 'white'
                }}>
                  {agent.status}
                </span>
                <button style={{
                  padding: '0.5rem 1rem',
                  backgroundColor: 'transparent',
                  color: 'var(--text)',
                  border: '1px solid var(--border)',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}>
                  Configure
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
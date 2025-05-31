import Head from "next/head";
import React from "react";

export default function Home() {
  return (
    <>
      <Head>
        <title>Aegis Nexus - Dashboard</title>
        <meta name="description" content="Aegis Nexus AI Platform Dashboard" />
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
          Dashboard
        </h1>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '1.5rem',
          marginTop: '2rem'
        }}>
          <div style={{
            background: 'var(--panel)',
            padding: '1.5rem',
            borderRadius: '8px',
            border: '1px solid var(--border)'
          }}>
            <h3 style={{ marginBottom: '1rem', color: 'var(--text)' }}>AI Agents</h3>
            <p style={{ color: 'var(--text)', opacity: 0.8 }}>
              Manage and deploy AI agents for various tasks and workflows.
            </p>
          </div>
          <div style={{
            background: 'var(--panel)',
            padding: '1.5rem',
            borderRadius: '8px',
            border: '1px solid var(--border)'
          }}>
            <h3 style={{ marginBottom: '1rem', color: 'var(--text)' }}>Chat Interface</h3>
            <p style={{ color: 'var(--text)', opacity: 0.8 }}>
              Interactive chat interface powered by NLUX for seamless AI conversations.
            </p>
          </div>
          <div style={{
            background: 'var(--panel)',
            padding: '1.5rem',
            borderRadius: '8px',
            border: '1px solid var(--border)'
          }}>
            <h3 style={{ marginBottom: '1rem', color: 'var(--text)' }}>System Status</h3>
            <p style={{ color: 'var(--text)', opacity: 0.8 }}>
              Monitor system health and performance metrics in real-time.
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
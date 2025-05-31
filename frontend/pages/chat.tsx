import Head from "next/head";
import React from "react";
import ChatBox from "@/components/ChatBox";

export default function Chat() {
  return (
    <>
      <Head>
        <title>Aegis Nexus - Chat</title>
        <meta name="description" content="AI Chat Interface" />
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
          AI Chat
        </h1>
        <ChatBox />
      </div>
    </>
  );
}
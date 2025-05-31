"use client"

import { ChatInterface } from "@/components/chat-interface"

export default function ChatPage() {
  return (
    <div className="flex flex-1 flex-col h-screen">
      <main className="flex-1 bg-[#111111] p-4 md:p-6">
        <ChatInterface />
      </main>
    </div>
  )
} 
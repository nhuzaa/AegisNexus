"use client"

import type React from "react"
import { useState, useRef, useEffect } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Send, ImageIcon, Bot, User, X, Paperclip, FileText, Shield, AlertTriangle, Search } from "lucide-react"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { askAIAssistant } from "@/lib/api"
import { VoiceInterface } from "@/components/voice-interface"
import { SREPromptSuggestions } from "@/components/sre-prompt-suggestions"

interface Message {
  id: string
  type: "user" | "assistant"
  content: string
  timestamp: Date
  attachments?: Array<{
    type: "image" | "file"
    name: string
    url: string
  }>
}

const quickStartOptions = [
  "What is Site Reliability Engineering?",
  "Show me recent security threats",
  "Review system logs",
  "Explain incident response protocol"
]

interface ChatInterfaceProps {
  initialMessage?: string | null
}

export function ChatInterface({ initialMessage }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>(() => [
    {
      id: "1",
      type: "assistant",
      content: initialMessage || "Hello! I'm your AI SRE assistant. How can I help you today?",
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [showQuickStart, setShowQuickStart] = useState(true)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const scrollRef = useRef<HTMLDivElement>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  useEffect(() => {
    if (initialMessage) {
      const timelineMessage: Message = {
        id: Date.now().toString(),
        type: "assistant",
        content: initialMessage,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, timelineMessage])
      setShowQuickStart(false)
    }
  }, [initialMessage])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleSendMessage = async (content: string) => {
    if (!content.trim()) return

    // Hide quick start options after first message
    setShowQuickStart(false)

    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content,
      timestamp: new Date(),
    }

    if (selectedFile) {
      userMessage.attachments = [
        {
          type: selectedFile.type.startsWith("image/") ? "image" : "file",
          name: selectedFile.name,
          url: previewUrl || "",
        },
      ]
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setSelectedFile(null)
    setPreviewUrl(null)
    setIsLoading(true)
    setError(null)

    try {
      const response = await askAIAssistant(content)
      
      // Extract natural_summary from the nested response structure
      let responseContent = "Sorry, I couldn't process your request."
      
      if (response && response.response && typeof response.response === 'object') {
        // Extract natural_summary from the response object
        const naturalSummary = (response.response as any).natural_summary
        if (naturalSummary && typeof naturalSummary === 'string') {
          // Remove quotes from the beginning and end if they exist
          responseContent = naturalSummary.replace(/^["']|["']$/g, '')
        }
      } else if (typeof response.response === 'string') {
        responseContent = response.response
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content: responseContent,
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (err) {
      setError("Failed to get response from AI assistant. Please try again.")
      console.error("Error in chat:", err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleQuickStart = (option: string) => {
    setShowQuickStart(false) // Hide quick start options when one is selected
    setInput(option)
    handleSendMessage(option)
  }

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    setSelectedFile(file)

    // Create preview URL for images
    if (file.type.startsWith("image/")) {
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
    }
  }

  const clearSelectedFile = () => {
    setSelectedFile(null)
    setPreviewUrl(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
  }

  const handlePromptSelect = (prompt: string) => {
    setInput(prompt)
    handleSendMessage(prompt)
  }

  return (
    <div className="flex gap-6 h-[calc(100vh-7rem)] bg-[#0a0a0a]">
      {/* Main Chat Interface */}
      <div className="flex-1 w-[85%] flex flex-col">
           <Card className="flex-1 flex flex-col bg-[#111111] border-[#1d1d1d]">
          <CardContent className="flex flex-col h-full p-4">
            <ScrollArea ref={scrollRef} className="flex-1 overflow-y-auto space-y-4 mb-4 p-2">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex items-start gap-3 ${
                    message.type === "user" ? "justify-end" : ""
                  }`}
                >
                  {message.type === "assistant" && (
                    <div className="h-8 w-8 rounded-full bg-gradient-to-br from-red-600 via-orange-500 to-yellow-500 flex items-center justify-center">
                      <Bot className="h-4 w-4 text-black" />
                    </div>
                  )}
                  <div
                    className={`rounded-lg p-3 max-w-[80%] ${
                      message.type === "user"
                        ? "bg-[#1a1a1a] text-white"
                        : "bg-[#0d0d0d] text-white"
                    }`}
                  >
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                    {message.attachments?.map((attachment, index) => (
                      <div key={index} className="mt-2">
                        {attachment.type === "image" ? (
                          <div className="mt-2 rounded-md overflow-hidden border border-[#1d1d1d]">
                            <img
                              src={attachment.url || "/placeholder.svg"}
                              alt={attachment.name}
                              className="max-w-full max-h-60 object-contain"
                            />
                          </div>
                        ) : (
                          <div className="flex items-center gap-2 p-2 bg-[#000000] rounded-md">
                            <FileText className="h-4 w-4" />
                            <span className="text-sm truncate">{attachment.name}</span>
                          </div>
                        )}
                      </div>
                    ))}
                    <span className="text-xs text-[#71717a] mt-1 block">
                      {message.timestamp.toLocaleTimeString()}
                    </span>
                  </div>
                  {message.type === "user" && (
                    <div className="h-8 w-8 rounded-full bg-[#1a1a1a] flex items-center justify-center">
                      <User className="h-4 w-4 text-white" />
                    </div>
                  )}
                </div>
              ))}

              {showQuickStart && !initialMessage && (
                <div className="space-y-3 my-6">
                  <p className="text-[#d4d4d8] text-sm font-medium">Quick Start Options:</p>
                  <div className="grid gap-3">
                    {quickStartOptions.map((option, index) => (
                      <Button
                        key={index}
                        variant="outline"
                        className={`h-auto p-4 bg-gradient-to-r from-red-600 to-orange-500 border-0 text-white hover:opacity-90 transition-all duration-200 hover:scale-[1.02]`}
                        onClick={() => handleQuickStart(option)}
                      >
                        {option}
                      </Button>
                    ))}
                  </div>
                </div>
              )}

              {isLoading && (
                <div className="flex gap-3 justify-start">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-orange-500 to-yellow-500 flex items-center justify-center">
                    <Bot className="h-4 w-4 text-black" />
                  </div>
                  <div className="bg-[#0d0d0d] border border-[#1d1d1d] rounded-lg p-3">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gradient-to-r from-red-500 to-orange-500 rounded-full animate-bounce"></div>
                      <div
                        className="w-2 h-2 bg-gradient-to-r from-orange-500 to-yellow-500 rounded-full animate-bounce"
                        style={{ animationDelay: "0.1s" }}
                      ></div>
                      <div
                        className="w-2 h-2 bg-gradient-to-r from-yellow-500 to-red-500 rounded-full animate-bounce"
                        style={{ animationDelay: "0.2s" }}
                      ></div>
                    </div>
                  </div>
                </div>
              )}
              {error && (
                <div className="flex items-center gap-2 text-red-500 bg-red-500/10 p-3 rounded-lg">
                  <AlertTriangle className="h-4 w-4" />
                  <p className="text-sm">{error}</p>
                </div>
              )}
              <div ref={messagesEndRef} />
            </ScrollArea>

            {selectedFile && (
              <div className="mb-4 p-3 bg-[#0d0d0d] rounded-lg border border-[#1d1d1d] relative">
                <Button
                  variant="ghost"
                  size="icon"
                  className="absolute top-1 right-1 h-6 w-6 rounded-full bg-[#1d1d1d] hover:bg-[#2d2d2d]"
                  onClick={clearSelectedFile}
                >
                  <X className="h-3 w-3" />
                </Button>
                <div className="flex items-center gap-2">
                  {selectedFile.type.startsWith("image/") && previewUrl ? (
                    <div className="w-full">
                      <p className="text-xs text-[#71717a] mb-2">Selected image:</p>
                      <div className="rounded-md overflow-hidden">
                        <img
                          src={previewUrl || "/placeholder.svg"}
                          alt="Preview"
                          className="max-h-40 object-contain mx-auto"
                        />
                      </div>
                    </div>
                  ) : (
                    <>
                      <FileText className="h-5 w-5 text-[#71717a]" />
                      <span className="text-sm text-[#d4d4d8] truncate">{selectedFile.name}</span>
                    </>
                  )}
                </div>
              </div>
            )}

            <div className="p-4 border-t border-[#1d1d1d]">
              <div className="flex gap-2">
                <Input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Type your message..."
                  className="flex-1 bg-[#0d0d0d] border-[#1d1d1d] text-white placeholder:text-[#71717a] focus:border-[#2d2d2d]"
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                      e.preventDefault()
                      handleSendMessage(input)
                    }
                  }}
                />
                <VoiceInterface onTranscription={(text) => {
                  setInput(text)
                  handleSendMessage(text)
                }} />
                <Button
                  variant="outline"
                  size="icon"
                  className="bg-[#0d0d0d] border-[#1d1d1d] text-[#d4d4d8] hover:bg-[#1a1a1a] hover:text-white transition-colors"
                >
                  <Paperclip className="h-4 w-4" />
                </Button>
                <Button
                  onClick={() => handleSendMessage(input)}
                  disabled={isLoading || !input.trim()}
                  className="bg-gradient-to-br from-red-600 via-orange-500 to-yellow-500 text-black hover:opacity-90 transition-opacity"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>

            <div className="mt-4 flex items-center gap-2">
              <Badge className="bg-gradient-to-r from-orange-500 to-red-500 text-white border-0">nlkit</Badge>
              <span className="text-xs text-[#71717a]">
                Powered by nlkit/nlux - Configure your chat adapter following the nlkit documentation
              </span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* SRE Prompt Suggestions Sidebar - Right Side */}
      <div className="w-[15%] flex-shrink-0">
        <SREPromptSuggestions onPromptSelect={handlePromptSelect} />
      </div>
    </div>
  )
}

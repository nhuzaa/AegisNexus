"use client"

import type React from "react"
import { useState, useRef, useEffect } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Send, ImageIcon, Bot, User, X, Paperclip, FileText, Shield, AlertTriangle, Search } from "lucide-react"
import { Textarea } from "@/components/ui/textarea"

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
  {
    id: 1,
    title: "Analyze Security Threats",
    description: "Get an overview of current security threats and vulnerabilities",
    prompt: "Can you analyze the current security threats in my system and provide recommendations for mitigation?",
    icon: Shield,
    gradient: "from-red-500 to-orange-500",
  },
  {
    id: 2,
    title: "Review System Logs",
    description: "Help me understand and analyze system security logs",
    prompt:
      "I need help reviewing my system security logs. What should I look for and how can I identify potential security issues?",
    icon: Search,
    gradient: "from-orange-500 to-yellow-500",
  },
  {
    id: 3,
    title: "Incident Response",
    description: "Guide me through security incident response procedures",
    prompt:
      "I think there might be a security incident. Can you guide me through the proper incident response procedures and what steps I should take immediately?",
    icon: AlertTriangle,
    gradient: "from-yellow-500 to-red-500",
  },
]

interface ChatInterfaceProps {
  initialMessage?: string | null
}

export function ChatInterface({ initialMessage }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      type: "assistant",
      content:
        "Hello! I'm your AegisNexus AI security assistant. I can help you analyze security threats, review logs, interpret security diagrams, and provide recommendations. Choose one of the options below to get started, or ask me anything!",
      timestamp: new Date(),
    },
  ])
  const [inputValue, setInputValue] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [showQuickStart, setShowQuickStart] = useState(true)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Add initial message from timeline analysis
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

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  // Simulated AI responses for demo purposes
  const getAIResponse = (userMessage: string, hasImage: boolean): string => {
    const lowerMessage = userMessage.toLowerCase()

    if (hasImage) {
      return "I've analyzed the uploaded image. This appears to be a security-related diagram or screenshot. Based on what I can see, there might be potential vulnerabilities in the configuration shown. I recommend reviewing the access controls and implementing additional security measures for the highlighted components."
    }

    if (lowerMessage.includes("analyze") && lowerMessage.includes("threat")) {
      return "🔍 **Security Threat Analysis Complete**\n\nI've identified several areas that need attention:\n\n**Critical Issues:**\n• 3 suspicious login attempts from IP 192.168.1.100\n• Outdated SSL certificates on 2 servers\n• Unusual network traffic patterns detected\n\n**Recommendations:**\n1. Implement IP blocking for suspicious addresses\n2. Update SSL certificates immediately\n3. Enable enhanced monitoring for network anomalies\n4. Review firewall rules and access controls\n\nWould you like me to provide detailed steps for any of these recommendations?"
    }

    if (lowerMessage.includes("logs") || lowerMessage.includes("review")) {
      return "📊 **Security Log Analysis Guide**\n\nHere's what to look for in your security logs:\n\n**Key Indicators:**\n• Failed login attempts (especially repeated ones)\n• Privilege escalation events\n• Unusual file access patterns\n• Network connection anomalies\n• System configuration changes\n\n**Red Flags:**\n🚨 Multiple failed logins from same IP\n🚨 Access attempts outside business hours\n🚨 Large data transfers\n🚨 New user account creations\n\n**Tools I recommend:**\n• SIEM solutions for automated analysis\n• Log aggregation tools\n• Real-time alerting systems\n\nWould you like me to help you set up automated log monitoring?"
    }

    if (lowerMessage.includes("incident") && lowerMessage.includes("response")) {
      return "🚨 **Incident Response Protocol Activated**\n\n**Immediate Actions (First 30 minutes):**\n\n1. **Contain the Threat**\n   • Isolate affected systems\n   • Preserve evidence\n   • Document everything\n\n2. **Assess the Damage**\n   • Identify compromised data\n   • Check system integrity\n   • Review access logs\n\n3. **Notify Stakeholders**\n   • Alert security team\n   • Inform management\n   • Contact relevant authorities if needed\n\n**Next Steps:**\n• Conduct forensic analysis\n• Implement recovery procedures\n• Review and update security policies\n\n**Need immediate help?** Tell me more about the incident and I'll provide specific guidance for your situation."
    }

    return "I understand your security concern. Based on the information provided, I recommend reviewing your current security protocols and implementing additional monitoring. Would you like me to provide more specific guidance on any particular area?"
  }

  const handleSendMessage = async (messageText?: string) => {
    const textToSend = messageText || inputValue
    if (!textToSend.trim() && !selectedFile) return

    // Hide quick start options after first message
    setShowQuickStart(false)

    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: textToSend || "Uploaded an image for analysis",
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
    setInputValue("")
    setSelectedFile(null)
    setPreviewUrl(null)
    setIsLoading(true)

    // Simulate AI processing delay
    setTimeout(() => {
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content: getAIResponse(textToSend, !!selectedFile),
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, aiResponse])
      setIsLoading(false)
    }, 1500)
  }

  const handleQuickStart = (prompt: string) => {
    handleSendMessage(prompt)
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

  return (
    <div className="flex flex-col h-[calc(100vh-7rem)]">
      <div className="mb-4">
        <h2 className="text-2xl font-bold text-white">AI Security Assistant</h2>
        <p className="text-[#71717a]">Upload images or ask questions about security</p>
      </div>

      <Card className="flex-1 flex flex-col bg-[#2d2d2d] border-[#3d3d3d]">
        <CardContent className="flex flex-col h-full p-4">
          {/* Messages Container */}
          <div className="flex-1 overflow-y-auto space-y-4 mb-4 p-2">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-3 ${message.type === "user" ? "justify-end" : "justify-start"}`}
              >
                <div className={`flex gap-3 max-w-[80%] ${message.type === "user" ? "flex-row-reverse" : "flex-row"}`}>
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center ${
                      message.type === "user"
                        ? "bg-gradient-to-br from-red-500 to-orange-500"
                        : "bg-gradient-to-br from-orange-500 to-yellow-500"
                    }`}
                  >
                    {message.type === "user" ? (
                      <User className="h-4 w-4 text-white" />
                    ) : (
                      <Bot className="h-4 w-4 text-black" />
                    )}
                  </div>
                  <div
                    className={`rounded-lg p-3 ${
                      message.type === "user"
                        ? "bg-gradient-to-br from-red-600 to-orange-600 text-white"
                        : "bg-[#1e1e1e] text-[#d4d4d8] border border-[#3d3d3d]"
                    }`}
                  >
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                    {message.attachments?.map((attachment, index) => (
                      <div key={index} className="mt-2">
                        {attachment.type === "image" ? (
                          <div className="mt-2 rounded-md overflow-hidden border border-[#3d3d3d]">
                            <img
                              src={attachment.url || "/placeholder.svg"}
                              alt={attachment.name}
                              className="max-w-full max-h-60 object-contain"
                            />
                          </div>
                        ) : (
                          <div className="flex items-center gap-2 p-2 bg-[#111111] rounded-md">
                            <FileText className="h-4 w-4" />
                            <span className="text-sm truncate">{attachment.name}</span>
                          </div>
                        )}
                      </div>
                    ))}
                    <p className="text-xs opacity-70 mt-1">{message.timestamp.toLocaleTimeString()}</p>
                  </div>
                </div>
              </div>
            ))}

            {/* Quick Start Options */}
            {showQuickStart && !initialMessage && (
              <div className="space-y-3 my-6">
                <p className="text-[#d4d4d8] text-sm font-medium">Quick Start Options:</p>
                <div className="grid gap-3">
                  {quickStartOptions.map((option) => (
                    <Button
                      key={option.id}
                      variant="outline"
                      className={`h-auto p-4 bg-gradient-to-r ${option.gradient} border-0 text-white hover:opacity-90 transition-all duration-200 hover:scale-[1.02]`}
                      onClick={() => handleQuickStart(option.prompt)}
                    >
                      <div className="flex items-start gap-3 w-full text-left">
                        <option.icon className="h-5 w-5 mt-0.5 flex-shrink-0" />
                        <div className="flex-1">
                          <h3 className="font-semibold text-sm">{option.title}</h3>
                          <p className="text-xs opacity-90 mt-1">{option.description}</p>
                        </div>
                      </div>
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
                <div className="bg-[#1e1e1e] border border-[#3d3d3d] rounded-lg p-3">
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
            <div ref={messagesEndRef} />
          </div>

          {/* File Preview */}
          {selectedFile && (
            <div className="mb-4 p-3 bg-[#1e1e1e] rounded-lg border border-[#3d3d3d] relative">
              <Button
                variant="ghost"
                size="icon"
                className="absolute top-1 right-1 h-6 w-6 rounded-full bg-[#3d3d3d] hover:bg-[#4d4d4d]"
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

          {/* Input Area */}
          <div className="flex flex-col gap-3">
            <Textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask about security threats or upload an image for analysis..."
              className="min-h-[80px] bg-[#1e1e1e] border-[#3d3d3d] text-white placeholder:text-[#71717a] resize-none"
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault()
                  handleSendMessage()
                }
              }}
            />

            <div className="flex gap-2">
              <input
                ref={fileInputRef}
                type="file"
                className="hidden"
                onChange={handleFileSelect}
                accept="image/*,.txt,.log,.json,.csv"
              />
              <Button
                variant="outline"
                size="icon"
                className="bg-[#1e1e1e] border-[#3d3d3d] text-[#d4d4d8] hover:bg-[#2d2d2d]"
                onClick={() => fileInputRef.current?.click()}
              >
                <Paperclip className="h-4 w-4" />
                <span className="sr-only">Attach file</span>
              </Button>
              <Button
                variant="outline"
                size="icon"
                className="bg-[#1e1e1e] border-[#3d3d3d] text-[#d4d4d8] hover:bg-[#2d2d2d]"
                onClick={() => fileInputRef.current?.click()}
              >
                <ImageIcon className="h-4 w-4" />
                <span className="sr-only">Upload image</span>
              </Button>
              <Button
                onClick={() => handleSendMessage()}
                disabled={(!inputValue.trim() && !selectedFile) || isLoading}
                className="flex-1 bg-gradient-to-r from-red-600 to-orange-500 hover:from-red-700 hover:to-orange-600 text-white border-0"
              >
                {isLoading ? "Processing..." : "Send"}
                {!isLoading && <Send className="ml-2 h-4 w-4" />}
              </Button>
            </div>
          </div>

          {/* nlkit Integration Note */}
          <div className="mt-4 flex items-center gap-2">
            <Badge className="bg-gradient-to-r from-orange-500 to-red-500 text-white border-0">nlkit</Badge>
            <span className="text-xs text-[#71717a]">
              Powered by nlkit/nlux - Configure your chat adapter following the nlkit documentation
            </span>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

"use client"

import type React from "react"

import { useState, useRef } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Send, Paperclip, Bot, User, ImageIcon, FileText, AlertCircle, CheckCircle } from "lucide-react"

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

export function ChatView() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      type: "assistant",
      content:
        "Hello! I'm your AegisNexus AI security assistant. I can help you analyze security threats, review logs, interpret security diagrams, and provide recommendations. How can I assist you today?",
      timestamp: new Date(),
    },
  ])
  const [inputValue, setInputValue] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Simulated AI responses for demo purposes
  const getAIResponse = (userMessage: string): string => {
    const lowerMessage = userMessage.toLowerCase()

    if (lowerMessage.includes("threat") || lowerMessage.includes("security")) {
      return "Based on current system analysis, I've detected 3 active threats that require attention. The most critical is a suspicious login pattern from IP range 192.168.1.x. I recommend implementing additional authentication measures and monitoring this IP range closely."
    }

    if (lowerMessage.includes("performance") || lowerMessage.includes("system")) {
      return "System performance is currently optimal with 98.5% uptime. CPU usage is at 67% which is within normal parameters. However, I notice memory usage has increased by 12% over the past week. Consider reviewing running processes for optimization opportunities."
    }

    if (lowerMessage.includes("compliance") || lowerMessage.includes("audit")) {
      return "Your current compliance score is 94%. SOC 2 compliance is at 98%, ISO 27001 at 95%. The main areas for improvement are in access control documentation and incident response procedures. I can help you generate the necessary documentation."
    }

    return "I understand your query. Based on the current security posture and system metrics, I recommend reviewing the latest security logs and implementing the suggested security patches. Would you like me to provide more specific guidance on any particular area?"
  }

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: inputValue,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInputValue("")
    setIsLoading(true)

    // Simulate AI processing delay
    setTimeout(() => {
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content: getAIResponse(inputValue),
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, aiResponse])
      setIsLoading(false)
    }, 1500)
  }

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    // Simulate file upload and analysis
    const fileMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: `Uploaded file: ${file.name}`,
      timestamp: new Date(),
      attachments: [
        {
          type: file.type.startsWith("image/") ? "image" : "file",
          name: file.name,
          url: URL.createObjectURL(file),
        },
      ],
    }

    setMessages((prev) => [...prev, fileMessage])

    // Simulate AI analysis of uploaded file
    setTimeout(() => {
      const analysisResponse: Message = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content: file.type.startsWith("image/")
          ? "I've analyzed the uploaded image. This appears to be a network diagram showing your current infrastructure. I notice potential security vulnerabilities in the DMZ configuration. The firewall rules could be strengthened, and I recommend implementing additional network segmentation."
          : "I've analyzed the uploaded file. The log entries show normal system behavior with a few anomalies that warrant investigation. I've identified 2 potential security events that require your attention.",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, analysisResponse])
    }, 2000)
  }

  const quickActions = [
    { label: "Analyze Current Threats", icon: AlertCircle },
    { label: "System Health Check", icon: CheckCircle },
    { label: "Compliance Report", icon: FileText },
    { label: "Performance Review", icon: Bot },
  ]

  const handleQuickAction = (action: string) => {
    setInputValue(action)
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-white mb-2">AI Security Assistant</h2>
        <p className="text-[#71717a]">Intelligent security analysis and recommendations powered by nlkit</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Quick Actions */}
        <Card className="bg-[#2d2d2d] border-[#3d3d3d]">
          <CardHeader>
            <CardTitle className="text-white text-lg">Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {quickActions.map((action, index) => (
              <Button
                key={index}
                variant="outline"
                className="w-full justify-start text-left bg-[#1e1e1e] border-[#3d3d3d] text-[#d4d4d8] hover:bg-[#2d2d2d] hover:text-white"
                onClick={() => handleQuickAction(action.label)}
              >
                <action.icon className="h-4 w-4 mr-2" />
                {action.label}
              </Button>
            ))}
          </CardContent>
        </Card>

        {/* Chat Interface */}
        <Card className="lg:col-span-3 bg-[#2d2d2d] border-[#3d3d3d]">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <Bot className="h-5 w-5" />
              Security Assistant Chat
              <Badge className="bg-[#22c55e] text-black">Online</Badge>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Messages Container */}
            <div className="h-96 overflow-y-auto space-y-4 p-4 bg-[#1e1e1e] rounded-lg border border-[#3d3d3d]">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex gap-3 ${message.type === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`flex gap-3 max-w-[80%] ${message.type === "user" ? "flex-row-reverse" : "flex-row"}`}
                  >
                    <div
                      className={`w-8 h-8 rounded-full flex items-center justify-center ${
                        message.type === "user" ? "bg-[#0ea5e9]" : "bg-[#22c55e]"
                      }`}
                    >
                      {message.type === "user" ? (
                        <User className="h-4 w-4 text-white" />
                      ) : (
                        <Bot className="h-4 w-4 text-white" />
                      )}
                    </div>
                    <div
                      className={`rounded-lg p-3 ${
                        message.type === "user"
                          ? "bg-[#0ea5e9] text-white"
                          : "bg-[#2d2d2d] text-[#d4d4d8] border border-[#3d3d3d]"
                      }`}
                    >
                      <p className="text-sm">{message.content}</p>
                      {message.attachments && (
                        <div className="mt-2 space-y-2">
                          {message.attachments.map((attachment, index) => (
                            <div key={index} className="flex items-center gap-2 text-xs">
                              {attachment.type === "image" ? (
                                <ImageIcon className="h-4 w-4" />
                              ) : (
                                <FileText className="h-4 w-4" />
                              )}
                              <span>{attachment.name}</span>
                            </div>
                          ))}
                        </div>
                      )}
                      <p className="text-xs opacity-70 mt-1">{message.timestamp.toLocaleTimeString()}</p>
                    </div>
                  </div>
                </div>
              ))}

              {isLoading && (
                <div className="flex gap-3 justify-start">
                  <div className="w-8 h-8 rounded-full bg-[#22c55e] flex items-center justify-center">
                    <Bot className="h-4 w-4 text-white" />
                  </div>
                  <div className="bg-[#2d2d2d] border border-[#3d3d3d] rounded-lg p-3">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-[#71717a] rounded-full animate-bounce"></div>
                      <div
                        className="w-2 h-2 bg-[#71717a] rounded-full animate-bounce"
                        style={{ animationDelay: "0.1s" }}
                      ></div>
                      <div
                        className="w-2 h-2 bg-[#71717a] rounded-full animate-bounce"
                        style={{ animationDelay: "0.2s" }}
                      ></div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Input Area */}
            <div className="flex gap-2">
              <input
                ref={fileInputRef}
                type="file"
                className="hidden"
                onChange={handleFileUpload}
                accept="image/*,.txt,.log,.json,.csv"
              />
              <Button
                variant="outline"
                size="icon"
                className="bg-[#1e1e1e] border-[#3d3d3d] text-[#d4d4d8] hover:bg-[#2d2d2d]"
                onClick={() => fileInputRef.current?.click()}
              >
                <Paperclip className="h-4 w-4" />
              </Button>
              <Input
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Ask about security threats, system performance, or upload files for analysis..."
                className="flex-1 bg-[#1e1e1e] border-[#3d3d3d] text-white placeholder:text-[#71717a]"
                onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
              />
              <Button
                onClick={handleSendMessage}
                disabled={!inputValue.trim() || isLoading}
                className="bg-[#0ea5e9] hover:bg-[#0ea5e9]/80 text-white"
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>

            {/* nlkit Integration Note */}
            <div className="text-xs text-[#71717a] p-3 bg-[#1e1e1e] rounded border border-[#3d3d3d]">
              <p className="font-medium mb-1">nlkit Integration:</p>
              <p>
                This chat interface is designed to integrate with nlkit/nlux. Configure your chat adapter following the
                nlkit documentation at docs.nlkit.com/nlux/examples/react-js-ai-assistant for production deployment.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

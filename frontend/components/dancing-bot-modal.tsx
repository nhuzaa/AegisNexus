"use client"

import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { X, Bot } from "lucide-react"

interface DancingBotModalProps {
  isOpen: boolean
  onClose: () => void
}

export function DancingBotModal({ isOpen, onClose }: DancingBotModalProps) {
  const [dots, setDots] = useState("")

  useEffect(() => {
    if (!isOpen) return

    const interval = setInterval(() => {
      setDots((prev) => {
        if (prev === "...") return ""
        return prev + "."
      })
    }, 500)

    return () => clearInterval(interval)
  }, [isOpen])

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center">
      <div className="bg-[#2d2d2d] border border-[#3d3d3d] rounded-lg p-8 max-w-md w-full mx-4 relative">
        <Button
          variant="ghost"
          size="icon"
          className="absolute top-2 right-2 text-[#71717a] hover:text-white hover:bg-[#3d3d3d]"
          onClick={onClose}
        >
          <X className="h-4 w-4" />
        </Button>

        <div className="text-center space-y-6">
          {/* Dancing Bot */}
          <div className="flex justify-center">
            <div className="relative">
              <div className="w-20 h-20 rounded-full bg-gradient-to-br from-orange-500 to-yellow-500 flex items-center justify-center animate-bounce">
                <Bot className="h-10 w-10 text-black animate-pulse" />
              </div>

              {/* Floating particles */}
              <div className="absolute -top-2 -right-2 w-3 h-3 bg-red-500 rounded-full animate-ping"></div>
              <div
                className="absolute -bottom-2 -left-2 w-2 h-2 bg-orange-500 rounded-full animate-ping"
                style={{ animationDelay: "0.5s" }}
              ></div>
              <div
                className="absolute top-1/2 -right-4 w-2 h-2 bg-yellow-500 rounded-full animate-ping"
                style={{ animationDelay: "1s" }}
              ></div>
            </div>
          </div>

          {/* Loading Text */}
          <div className="space-y-2">
            <h3 className="text-xl font-semibold text-white">Analyzing Security Timeline</h3>
            <p className="text-[#71717a]">AI is processing security events and generating insights{dots}</p>
          </div>

          {/* Progress Indicators */}
          <div className="space-y-3">
            <div className="flex justify-between text-sm text-[#d4d4d8]">
              <span>Processing events</span>
              <span className="text-orange-400">●●●○○</span>
            </div>
            <div className="flex justify-between text-sm text-[#d4d4d8]">
              <span>Analyzing patterns</span>
              <span className="text-yellow-400">●●○○○</span>
            </div>
            <div className="flex justify-between text-sm text-[#d4d4d8]">
              <span>Generating insights</span>
              <span className="text-red-400">●○○○○</span>
            </div>
          </div>

          {/* Animated Progress Bar */}
          <div className="w-full bg-[#1e1e1e] rounded-full h-2">
            <div
              className="bg-gradient-to-r from-red-500 via-orange-500 to-yellow-500 h-2 rounded-full animate-pulse"
              style={{ width: "60%" }}
            ></div>
          </div>

          <p className="text-xs text-[#71717a]">
            This may take a few moments. You can close this dialog and the analysis will continue in the background.
          </p>
        </div>
      </div>
    </div>
  )
}

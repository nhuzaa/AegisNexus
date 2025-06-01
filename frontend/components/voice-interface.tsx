"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Mic, MicOff, Volume2, VolumeX } from "lucide-react"
import { useToast } from "@/components/ui/use-toast"

interface VoiceInterfaceProps {
  onTranscription?: (text: string) => void
}

interface AudioMessage {
  type: "audio" | "text"
  data: string
  metadata: {
    voice_name?: string
    with_audio?: boolean
  }
}

interface ServerResponse {
  type: "transcription" | "sre_response" | "response_audio" | "error"
  data: string
  metadata: {
    confidence?: number
    enhanced_context?: boolean
    audio_length?: number
    voice_name?: string
    error_code?: string
  }
}

export function VoiceInterface({ onTranscription }: VoiceInterfaceProps) {
  const [isRecording, setIsRecording] = useState(false)
  const [isConnected, setIsConnected] = useState(false)
  const [isMuted, setIsMuted] = useState(false)
  const wsRef = useRef<WebSocket | null>(null)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const { toast } = useToast()

  useEffect(() => {
    return () => {
      cleanup()
    }
  }, [])

  const cleanup = () => {
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
      mediaRecorderRef.current.stop()
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop())
      mediaRecorderRef.current = null
    }
    if (audioRef.current) {
      audioRef.current.pause()
      audioRef.current.src = ""
      audioRef.current = null
    }
    setIsRecording(false)
    setIsConnected(false)
  }

  const connectWebSocket = () => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return wsRef.current
    }

    const ws = new WebSocket("ws://localhost:8000/speech-streaming/stream")
    wsRef.current = ws

    ws.onopen = () => {
      setIsConnected(true)
      toast({
        title: "Connected",
        description: "Voice streaming is now active",
        duration: 2000,
      })
    }

    ws.onclose = () => {
      setIsConnected(false)
      cleanup()
      toast({
        title: "Disconnected",
        description: "Voice streaming connection closed",
        duration: 2000,
      })
    }

    ws.onerror = (error) => {
      console.error("WebSocket error:", error)
      cleanup()
      toast({
        title: "Connection Error",
        description: "Failed to connect to voice server",
        variant: "destructive",
        duration: 3000,
      })
    }

    ws.onmessage = (event) => {
      try {
        const response: ServerResponse = JSON.parse(event.data)
        
        switch (response.type) {
          case "transcription":
            console.log("🎧 Transcription:", response.data)
            if (response.metadata.confidence) {
              console.log("Confidence:", response.metadata.confidence)
            }
            onTranscription?.(response.data)
            break

          case "sre_response":
            console.log("🤖 SRE Response:", response.data)
            if (response.metadata.enhanced_context) {
              console.log("Enhanced with SRE tools data")
            }
            break

          case "response_audio":
            console.log("🎤 Received audio response", response.metadata)
            playAudioResponse(response)
            break

          case "error":
            console.error("❌ Error:", response.data)
            console.error("Error Code:", response.metadata.error_code)
            toast({
              title: "Error",
              description: response.data,
              variant: "destructive",
              duration: 3000,
            })
            break

          default:
            console.log("📨 Unknown message type:", response.type)
            console.log("Content:", response.data)
        }
      } catch (error) {
        console.error("Error parsing WebSocket message:", error)
      }
    }

    return ws
  }

  const playAudioResponse = (response: ServerResponse) => {
    try {
      const audioBlob = new Blob([Buffer.from(response.data, 'base64')], { type: 'audio/wav' })
      const audioUrl = URL.createObjectURL(audioBlob)
      const audio = new Audio(audioUrl)
      audioRef.current = audio

      audio.onplay = () => {
        toast({
          title: "Playing Response",
          description: `Playing AI voice response (${response.metadata.voice_name})`,
          duration: 2000,
        })
      }

      audio.onended = () => {
        URL.revokeObjectURL(audioUrl)
      }

      audio.volume = isMuted ? 0 : 1
      audio.play().catch(error => {
        console.error("Error playing response:", error)
        toast({
          title: "Playback Error",
          description: "Failed to play AI response",
          variant: "destructive",
          duration: 3000,
        })
      })
    } catch (error) {
      console.error("Error playing audio response:", error)
      toast({
        title: "Playback Error",
        description: "Failed to process audio response",
        variant: "destructive",
        duration: 3000,
      })
    }
  }

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        } 
      })
      
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus',
        audioBitsPerSecond: 128000
      })
      mediaRecorderRef.current = mediaRecorder

      const ws = connectWebSocket()
      wsRef.current = ws

      mediaRecorder.ondataavailable = async (event) => {
        if (event.data.size > 0 && ws.readyState === WebSocket.OPEN) {
          try {
            const arrayBuffer = await event.data.arrayBuffer()
            const base64Audio = Buffer.from(arrayBuffer).toString('base64')
            
            const message: AudioMessage = {
              type: "audio",
              data: base64Audio,
              metadata: {
                voice_name: "en-US-AriaNeural"
              }
            }
            
            ws.send(JSON.stringify(message))
          } catch (error) {
            console.error("Error sending audio data:", error)
          }
        }
      }

      mediaRecorder.start(100)
      setIsRecording(true)
      
      toast({
        title: "Recording Started",
        description: "Microphone is active and recording",
        duration: 2000,
      })
    } catch (error) {
      console.error("Error accessing microphone:", error)
      toast({
        title: "Microphone Error",
        description: "Failed to access microphone. Please check permissions.",
        variant: "destructive",
        duration: 3000,
      })
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
      mediaRecorderRef.current.stop()
      toast({
        title: "Recording Stopped",
        description: "Microphone is now inactive",
        duration: 2000,
      })
    }
  }

  return (
    <div className="flex items-center gap-2">
      <Button
        variant="outline"
        size="icon"
        className={`${
          isRecording
            ? "bg-red-500 hover:bg-red-600 text-white"
            : "bg-[#1e1e1e] border-[#3d3d3d] text-[#d4d4d8] hover:bg-[#2d2d2d] hover:text-white"
        } transition-colors relative`}
        onClick={isRecording ? stopRecording : startRecording}
      >
        {isRecording ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
        {isRecording && (
          <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full animate-ping"></div>
        )}
      </Button>
      {isConnected && (
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-xs text-[#71717a]">Connected</span>
        </div>
      )}
      <Button
        variant="ghost"
        size="icon"
        className="h-6 w-6 p-0 hover:bg-[#2d2d2d]"
        onClick={() => setIsMuted(!isMuted)}
      >
        {isMuted ? <VolumeX className="h-3 w-3" /> : <Volume2 className="h-3 w-3" />}
      </Button>
    </div>
  )
} 
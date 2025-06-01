"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Mic, MicOff, Volume2, VolumeX } from "lucide-react"
import { useToast } from "@/components/ui/use-toast"
import * as SpeechSDK from "microsoft-cognitiveservices-speech-sdk"

interface VoiceInterfaceProps {
  onTranscription?: (text: string) => void
}

export function VoiceInterface({ onTranscription }: VoiceInterfaceProps) {
  const [isRecording, setIsRecording] = useState(false)
  const [isConnected, setIsConnected] = useState(false)
  const [isMuted, setIsMuted] = useState(false)
  const recognizerRef = useRef<SpeechSDK.SpeechRecognizer | null>(null)
  const synthesizerRef = useRef<SpeechSDK.SpeechSynthesizer | null>(null)
  const { toast } = useToast()

  useEffect(() => {
    initializeSpeechSDK()
    return () => {
      cleanup()
    }
  }, [])

  const initializeSpeechSDK = () => {
    try {
      // Get Azure Speech configuration from environment variables
      const speechKey = process.env.NEXT_PUBLIC_AZURE_SPEECH_KEY
      const speechRegion = process.env.NEXT_PUBLIC_AZURE_SPEECH_REGION

      if (!speechKey || !speechRegion) {
        console.error("Azure Speech credentials not found in environment variables")
        toast({
          title: "Configuration Error",
          description: "Azure Speech credentials not configured",
          variant: "destructive",
          duration: 3000,
        })
        return
      }

      // Create speech config
      const speechConfig = SpeechSDK.SpeechConfig.fromSubscription(speechKey, speechRegion)
      speechConfig.speechRecognitionLanguage = "en-US"
      speechConfig.speechSynthesisLanguage = "en-US"
      speechConfig.speechSynthesisVoiceName = "en-US-AriaNeural"

      // Create audio config for microphone input
      const audioConfig = SpeechSDK.AudioConfig.fromDefaultMicrophoneInput()

      // Create speech recognizer
      const recognizer = new SpeechSDK.SpeechRecognizer(speechConfig, audioConfig)
      recognizerRef.current = recognizer

      // Create speech synthesizer
      const synthesizer = new SpeechSDK.SpeechSynthesizer(speechConfig)
      synthesizerRef.current = synthesizer

      // Set up recognizer event handlers
      recognizer.recognizing = (s, e) => {
        console.log(`RECOGNIZING: Text=${e.result.text}`)
      }

      recognizer.recognized = (s, e) => {
        if (e.result.reason === SpeechSDK.ResultReason.RecognizedSpeech) {
          console.log(`RECOGNIZED: Text=${e.result.text}`)
          onTranscription?.(e.result.text)
          
          toast({
            title: "Speech Recognized",
            description: e.result.text,
            duration: 3000,
          })
        } else if (e.result.reason === SpeechSDK.ResultReason.NoMatch) {
          console.log("NOMATCH: Speech could not be recognized.")
        }
      }

      recognizer.canceled = (s, e) => {
        console.log(`CANCELED: Reason=${e.reason}`)
        if (e.reason === SpeechSDK.CancellationReason.Error) {
          console.log(`CANCELED: ErrorCode=${e.errorCode}`)
          console.log(`CANCELED: ErrorDetails=${e.errorDetails}`)
          toast({
            title: "Recognition Error",
            description: `Error: ${e.errorDetails}`,
            variant: "destructive",
            duration: 3000,
          })
        }
        setIsRecording(false)
      }

      recognizer.sessionStopped = (s, e) => {
        console.log("Session stopped event.")
        setIsRecording(false)
      }

      setIsConnected(true)
      toast({
        title: "Azure Speech Ready",
        description: "Speech services initialized successfully",
        duration: 2000,
      })

    } catch (error) {
      console.error("Error initializing Azure Speech SDK:", error)
      toast({
        title: "Initialization Error",
        description: "Failed to initialize Azure Speech services",
        variant: "destructive",
        duration: 3000,
      })
    }
  }

  const cleanup = () => {
    if (recognizerRef.current) {
      recognizerRef.current.stopContinuousRecognitionAsync()
      recognizerRef.current.close()
      recognizerRef.current = null
    }
    if (synthesizerRef.current) {
      synthesizerRef.current.close()
      synthesizerRef.current = null
    }
    setIsRecording(false)
    setIsConnected(false)
  }

  const startRecording = async () => {
    if (!recognizerRef.current) {
      toast({
        title: "Error",
        description: "Speech recognizer not initialized",
        variant: "destructive",
        duration: 3000,
      })
      return
    }

    try {
      await recognizerRef.current.startContinuousRecognitionAsync()
      setIsRecording(true)
      
      toast({
        title: "Recording Started",
        description: "Listening for speech input...",
        duration: 2000,
      })
    } catch (error) {
      console.error("Error starting recognition:", error)
      toast({
        title: "Recording Error",
        description: "Failed to start speech recognition",
        variant: "destructive",
        duration: 3000,
      })
    }
  }

  const stopRecording = async () => {
    if (!recognizerRef.current) return

    try {
      await recognizerRef.current.stopContinuousRecognitionAsync()
      setIsRecording(false)
      
      toast({
        title: "Recording Stopped",
        description: "Speech recognition stopped",
        duration: 2000,
      })
    } catch (error) {
      console.error("Error stopping recognition:", error)
      toast({
        title: "Error",
        description: "Failed to stop speech recognition",
        variant: "destructive",
        duration: 3000,
      })
    }
  }

  const speakText = async (text: string) => {
    if (!synthesizerRef.current || isMuted) return

    try {
      const result = await new Promise<SpeechSDK.SpeechSynthesisResult>((resolve, reject) => {
        synthesizerRef.current!.speakTextAsync(
          text,
          result => resolve(result),
          error => reject(error)
        )
      })

      if (result.reason === SpeechSDK.ResultReason.SynthesizingAudioCompleted) {
        toast({
          title: "Speech Synthesis",
          description: "AI response played successfully",
          duration: 2000,
        })
      } else {
        console.error("Speech synthesis failed:", result.errorDetails)
        toast({
          title: "Speech Error",
          description: "Failed to synthesize speech",
          variant: "destructive",
          duration: 3000,
        })
      }
    } catch (error) {
      console.error("Error in speech synthesis:", error)
      toast({
        title: "Speech Error",
        description: "Failed to play AI response",
        variant: "destructive",
        duration: 3000,
      })
    }
  }

  // Expose speak function for external use
  useEffect(() => {
    if (typeof window !== 'undefined') {
      (window as any).speakAIResponse = speakText
    }
  }, [isMuted])

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
        disabled={!isConnected}
      >
        {isRecording ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
        {isRecording && (
          <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full animate-ping"></div>
        )}
      </Button>
      
      {isConnected && (
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-xs text-[#71717a]">Azure Speech Ready</span>
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
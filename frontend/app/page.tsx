"use client"

import { useState, useEffect } from "react"
import { SidebarTrigger } from "@/components/ui/sidebar"
import { ChatInterface } from "@/components/chat-interface"
import { TimelineAnalysis } from "@/components/timeline-analysis"
import { DancingBotModal } from "@/components/dancing-bot-modal"
import { Flame } from "lucide-react"

export default function Home() {
  const [activeView, setActiveView] = useState<"chat" | "timeline" | "security" | "about" | "settings">("chat")
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisResult, setAnalysisResult] = useState<string | null>(null)

  useEffect(() => {
    const handleNavigation = (event: CustomEvent) => {
      setActiveView(event.detail.view)
    }

    window.addEventListener("navigate", handleNavigation as EventListener)

    return () => {
      window.removeEventListener("navigate", handleNavigation as EventListener)
    }
  }, [])

  const handleTimelineAnalysis = (timeframe: string, period: string) => {
    setIsAnalyzing(true)

    // Simulate API call to backend
    setTimeout(() => {
      const analysisPrompt = generateAnalysisPrompt(timeframe, period)
      setAnalysisResult(analysisPrompt)
      setIsAnalyzing(false)
      setActiveView("chat")
    }, 3000) // 3 second delay to show dancing bot
  }

  const generateAnalysisPrompt = (timeframe: string, period: string): string => {
    const prompts = {
      minutes: `🔍 **Real-Time Security Analysis (${timeframe})**\n\nI've analyzed the security events from the last ${timeframe}. Here's what I found:\n\n**Recent Activity:**\n• 12 authentication attempts\n• 3 network connections established\n• 1 file access event\n• 0 security alerts\n\n**Immediate Recommendations:**\n1. Monitor the authentication patterns\n2. Verify the legitimacy of new connections\n3. Continue real-time monitoring\n\n**Status:** ✅ All systems appear normal for this timeframe.\n\nWould you like me to dive deeper into any specific events?`,

      hours: `📊 **Hourly Security Analysis (${timeframe})**\n\nAnalyzing security patterns over the past ${timeframe}:\n\n**Key Findings:**\n• 45 total security events logged\n• 2 suspicious login attempts blocked\n• Network traffic: 15% above baseline\n• System performance: Normal\n\n**Trend Analysis:**\n📈 Increased activity during business hours\n🔒 All security protocols functioning correctly\n⚠️ Minor anomaly in network traffic patterns\n\n**Recommendations:**\n1. Investigate network traffic spike\n2. Review blocked login attempts\n3. Maintain current security posture\n\nShall I provide more details on any of these findings?`,

      days: `📅 **Daily Security Analysis (${timeframe})**\n\nComprehensive analysis of security events over ${timeframe}:\n\n**Security Summary:**\n• Total events: 1,247\n• Threats detected: 8\n• Threats mitigated: 8\n• System uptime: 99.8%\n\n**Notable Patterns:**\n🕐 Peak activity: 2-4 PM daily\n🌙 Minimal overnight activity\n📊 Consistent security posture\n\n**Areas of Interest:**\n• Recurring failed login from IP 192.168.1.100\n• Unusual file access patterns on weekends\n• Increased API calls from external sources\n\n**Action Items:**\n1. Block suspicious IP address\n2. Review weekend access policies\n3. Audit API usage patterns\n\nWould you like me to create a detailed incident report?`,

      weeks: `📈 **Weekly Security Analysis (${timeframe})**\n\nStrategic security overview for the past ${timeframe}:\n\n**Executive Summary:**\n• Overall security score: 94/100\n• Incidents resolved: 15\n• New vulnerabilities: 3\n• Patches applied: 12\n\n**Trend Analysis:**\n📊 Security posture improving (+5% from last period)\n🔄 Response time decreased by 23%\n🛡️ Zero successful breaches\n\n**Key Achievements:**\n✅ Implemented new firewall rules\n✅ Updated security protocols\n✅ Enhanced monitoring capabilities\n\n**Strategic Recommendations:**\n1. Continue current security initiatives\n2. Focus on vulnerability management\n3. Enhance user security training\n4. Consider additional monitoring tools\n\nShall I prepare a detailed security roadmap?`,

      months: `🗓️ **Monthly Security Analysis (${timeframe})**\n\nStrategic security assessment for ${timeframe}:\n\n**Executive Dashboard:**\n• Security maturity: Advanced (Level 4/5)\n• Compliance score: 96%\n• Risk reduction: 34% compared to last period\n• ROI on security investments: +127%\n\n**Major Accomplishments:**\n🎯 Zero critical security incidents\n📚 100% staff completed security training\n🔧 Deployed advanced threat detection\n📋 Achieved SOC 2 Type II compliance\n\n**Strategic Insights:**\n• Threat landscape evolution detected\n• Emerging risks in cloud infrastructure\n• Opportunity for AI-driven security automation\n\n**Long-term Recommendations:**\n1. Invest in next-generation SIEM\n2. Expand threat intelligence capabilities\n3. Develop incident response automation\n4. Plan for zero-trust architecture migration\n\nWould you like me to create a comprehensive security strategy document?`,
    }

    return prompts[period as keyof typeof prompts] || prompts.days
  }

  const closeAnalysis = () => {
    setIsAnalyzing(false)
  }

  const renderView = () => {
    switch (activeView) {
      case "chat":
        return <ChatInterface initialMessage={analysisResult} />
      case "timeline":
        return <TimelineAnalysis onAnalyze={handleTimelineAnalysis} />
      case "security":
        return <div className="text-white p-6">Security Info Page - Coming Soon</div>
      case "about":
        return <div className="text-white p-6">About Page - Coming Soon</div>
      case "settings":
        return <div className="text-white p-6">Settings Page - Coming Soon</div>
      default:
        return <ChatInterface />
    }
  }

  return (
    <div className="flex flex-1 flex-col">
      <header className="flex h-16 shrink-0 items-center gap-2 border-b border-[#3d3d3d] bg-[#1e1e1e] px-4">
        <SidebarTrigger className="text-white hover:bg-[#2d2d2d]" />
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded bg-gradient-to-br from-red-600 via-orange-500 to-yellow-500 flex items-center justify-center shadow-lg">
            <Flame className="h-4 w-4 text-black" />
          </div>
          <h1 className="text-xl font-semibold text-white">AegisNexus AI</h1>
        </div>
      </header>
      <main className="flex-1 bg-[#111111] p-4 md:p-6">{renderView()}</main>

      {/* Dancing Bot Modal */}
      <DancingBotModal isOpen={isAnalyzing} onClose={closeAnalysis} />
    </div>
  )
}

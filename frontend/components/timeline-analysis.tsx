"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Clock, Calendar, TrendingUp, Zap, BarChart3, Activity } from "lucide-react"

interface TimelineAnalysisProps {
  onAnalyze: (timeframe: string, period: string) => void
}

export function TimelineAnalysis({ onAnalyze }: TimelineAnalysisProps) {
  const [selectedPeriod, setSelectedPeriod] = useState<string | null>(null)
  const [selectedTimeframe, setSelectedTimeframe] = useState<string | null>(null)

  const timePeriods = [
    {
      id: "minutes",
      title: "Minutes",
      icon: Zap,
      description: "Real-time analysis",
      gradient: "from-yellow-500 to-orange-500",
      timeframes: ["Last 5 minutes", "Last 15 minutes", "Last 30 minutes", "Last 60 minutes"],
    },
    {
      id: "hours",
      title: "Hours",
      icon: Clock,
      description: "Hourly patterns",
      gradient: "from-orange-500 to-red-500",
      timeframes: ["Last 2 hours", "Last 6 hours", "Last 12 hours", "Last 24 hours"],
    },
    {
      id: "days",
      title: "Days",
      icon: Calendar,
      description: "Daily trends",
      gradient: "from-red-500 to-pink-500",
      timeframes: ["Last 2 days", "Last 3 days", "Last 7 days", "Last 14 days"],
    },
    {
      id: "weeks",
      title: "Weeks",
      icon: BarChart3,
      description: "Weekly analysis",
      gradient: "from-pink-500 to-purple-500",
      timeframes: ["Last 2 weeks", "Last 4 weeks", "Last 8 weeks", "Last 12 weeks"],
    },
    {
      id: "months",
      title: "Months",
      icon: TrendingUp,
      description: "Long-term insights",
      gradient: "from-purple-500 to-blue-500",
      timeframes: ["Last 2 months", "Last 3 months", "Last 6 months", "Last 12 months"],
    },
  ]

  const handlePeriodSelect = (periodId: string) => {
    setSelectedPeriod(periodId)
    setSelectedTimeframe(null)
  }

  const handleTimeframeSelect = (timeframe: string) => {
    setSelectedTimeframe(timeframe)
  }

  const handleAnalyze = () => {
    if (selectedTimeframe && selectedPeriod) {
      onAnalyze(selectedTimeframe, selectedPeriod)
    }
  }

  const selectedPeriodData = timePeriods.find((p) => p.id === selectedPeriod)

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-white mb-2">Timeline Security Analysis</h2>
        <p className="text-[#71717a]">Select a time period to analyze security events and get AI-powered insights</p>
      </div>

      {/* Time Period Selection */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        {timePeriods.map((period) => (
          <Card
            key={period.id}
            className={`cursor-pointer transition-all duration-200 hover:scale-105 ${
              selectedPeriod === period.id ? "ring-2 ring-orange-500 bg-[#2d2d2d]" : "bg-[#2d2d2d] hover:bg-[#3d3d3d]"
            } border-[#3d3d3d]`}
            onClick={() => handlePeriodSelect(period.id)}
          >
            <CardContent className="p-4">
              <div className="flex flex-col items-center text-center space-y-3">
                <div className={`p-3 rounded-lg bg-gradient-to-br ${period.gradient}`}>
                  <period.icon className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h3 className="font-semibold text-white">{period.title}</h3>
                  <p className="text-xs text-[#71717a] mt-1">{period.description}</p>
                </div>
                {selectedPeriod === period.id && (
                  <Badge className="bg-gradient-to-r from-orange-500 to-red-500 text-white">Selected</Badge>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Timeframe Selection */}
      {selectedPeriod && selectedPeriodData && (
        <Card className="bg-[#2d2d2d] border-[#3d3d3d]">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <selectedPeriodData.icon className="h-5 w-5" />
              Select {selectedPeriodData.title} Timeframe
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {selectedPeriodData.timeframes.map((timeframe) => (
                <Button
                  key={timeframe}
                  variant={selectedTimeframe === timeframe ? "default" : "outline"}
                  className={`h-auto p-4 ${
                    selectedTimeframe === timeframe
                      ? `bg-gradient-to-r ${selectedPeriodData.gradient} text-white border-0`
                      : "bg-[#1e1e1e] border-[#3d3d3d] text-[#d4d4d8] hover:bg-[#2d2d2d] hover:text-white"
                  }`}
                  onClick={() => handleTimeframeSelect(timeframe)}
                >
                  <div className="text-center">
                    <div className="font-medium text-sm">{timeframe}</div>
                  </div>
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Analysis Button */}
      {selectedTimeframe && selectedPeriod && (
        <Card className="bg-[#2d2d2d] border-[#3d3d3d]">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-white font-semibold">Ready to Analyze</h3>
                <p className="text-[#71717a] text-sm">
                  Analyzing security events for: <span className="text-orange-400">{selectedTimeframe}</span>
                </p>
              </div>
              <Button
                onClick={handleAnalyze}
                className="bg-gradient-to-r from-red-600 to-orange-500 hover:from-red-700 hover:to-orange-600 text-white border-0 px-8"
              >
                <Activity className="h-4 w-4 mr-2" />
                Start Analysis
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Info Card */}
      <Card className="bg-[#1e1e1e] border-[#3d3d3d]">
        <CardContent className="p-6">
          <div className="flex items-start gap-4">
            <div className="p-2 rounded-lg bg-gradient-to-br from-blue-500 to-purple-500">
              <Activity className="h-5 w-5 text-white" />
            </div>
            <div>
              <h3 className="text-white font-semibold mb-2">How Timeline Analysis Works</h3>
              <ul className="text-[#71717a] text-sm space-y-1">
                <li>• Select a time period (minutes to months)</li>
                <li>• Choose specific timeframe for analysis</li>
                <li>• AI analyzes security events and patterns</li>
                <li>• Get actionable insights and recommendations</li>
                <li>• Continue conversation with AI for deeper analysis</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

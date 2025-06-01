"use client"

import type React from "react"
import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { 
  Activity, 
  AlertTriangle, 
  BarChart3, 
  Cpu, 
  Database, 
  HardDrive, 
  FileText, 
  GitBranch, 
  Heart, 
  Globe, 
  ChevronDown, 
  ChevronRight,
  Zap
} from "lucide-react"

interface PromptSuggestionsProps {
  onPromptSelect: (prompt: string) => void
}

interface PromptCategory {
  id: string
  title: string
  icon: React.ComponentType<any>
  color: string
  prompts: string[]
  expanded?: boolean
}

const promptCategories: PromptCategory[] = [
  {
    id: "cpu",
    title: "CPU Metrics",
    icon: Cpu,
    color: "bg-red-500",
    prompts: [
      "What is the CPU usage?",
      "Show me CPU utilization",
      "How's the processor performance?"
    ]
  },
  {
    id: "traffic",
    title: "Traffic & Load",
    icon: Globe,
    color: "bg-cyan-500",
    prompts: [
      "Show me HTTP request rates",
      "What's the current traffic load?",
      "Check request volume"
    ]
  }
]

export function SREPromptSuggestions({ onPromptSelect }: PromptSuggestionsProps) {
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(
    new Set(["cpu", "traffic"])
  )

  const toggleCategory = (categoryId: string) => {
    const newExpanded = new Set(expandedCategories)
    if (newExpanded.has(categoryId)) {
      newExpanded.delete(categoryId)
    } else {
      newExpanded.add(categoryId)
    }
    setExpandedCategories(newExpanded)
  }

  return (
    <Card className="bg-[#111111] border-[#1d1d1d] h-auto">
      <CardHeader className="pb-2 px-2">
        <CardTitle className="text-white text-xs flex items-center gap-1">
          <BarChart3 className="h-3 w-3" />
          SRE
        </CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <div className="px-2 pb-2">
          <div className="space-y-2">
            {promptCategories.map((category) => {
              const isExpanded = expandedCategories.has(category.id)
              const IconComponent = category.icon
              
              return (
                <div key={category.id} className="space-y-1">
                  <Button
                    variant="ghost"
                    onClick={() => toggleCategory(category.id)}
                    className="w-full justify-between p-1.5 h-auto text-left bg-[#0d0d0d] border border-[#1d1d1d] hover:bg-[#1a1a1a] hover:border-[#2d2d2d]"
                  >
                    <div className="flex items-center gap-1.5">
                      <div className={`w-1.5 h-1.5 rounded-full ${category.color}`} />
                      <IconComponent className="h-3 w-3 text-[#d4d4d8]" />
                      <span className="text-[#d4d4d8] text-xs font-medium truncate">{category.title}</span>
                    </div>
                    {isExpanded ? (
                      <ChevronDown className="h-2.5 w-2.5 text-[#71717a] flex-shrink-0" />
                    ) : (
                      <ChevronRight className="h-2.5 w-2.5 text-[#71717a] flex-shrink-0" />
                    )}
                  </Button>
                  
                  {isExpanded && (
                    <div className="space-y-0.5 ml-1.5 pl-1.5 border-l border-[#1d1d1d]">
                      {category.prompts.map((prompt, index) => (
                        <Button
                          key={index}
                          variant="ghost"
                          onClick={() => onPromptSelect(prompt)}
                          className="w-full justify-start text-left p-1 h-auto text-xs bg-[#0a0a0a] hover:bg-[#1a1a1a] text-[#a1a1aa] hover:text-[#d4d4d8] border border-[#1d1d1d] hover:border-[#2d2d2d] rounded-sm"
                        >
                          <span className="text-[9px] leading-tight break-words">
                            {prompt.length > 25 ? `${prompt.substring(0, 25)}...` : prompt}
                          </span>
                        </Button>
                      ))}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      </CardContent>
    </Card>
  )
} 
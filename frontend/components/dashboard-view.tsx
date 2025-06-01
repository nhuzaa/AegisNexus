"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Shield, AlertTriangle, CheckCircle, Clock, TrendingUp, Users, Server, Zap } from "lucide-react"

export function DashboardView() {
  const securityMetrics = [
    {
      title: "Security Posture",
      value: "98.5%",
      change: "+2.1%",
      icon: Shield,
      color: "text-[#22c55e]",
      bgColor: "bg-[#22c55e]/10",
    },
    {
      title: "Active Threats",
      value: "3",
      change: "-5",
      icon: AlertTriangle,
      color: "text-[#f59e0b]",
      bgColor: "bg-[#f59e0b]/10",
    },
    {
      title: "System Uptime",
      value: "99.9%",
      change: "+0.1%",
      icon: CheckCircle,
      color: "text-[#22c55e]",
      bgColor: "bg-[#22c55e]/10",
    },
    {
      title: "Response Time",
      value: "1.2s",
      change: "-0.3s",
      icon: Clock,
      color: "text-[#0ea5e9]",
      bgColor: "bg-[#0ea5e9]/10",
    },
  ]

  const recentEvents = [
    {
      id: 1,
      type: "Critical",
      message: "Suspicious login attempt detected from IP 192.168.1.100",
      time: "2 minutes ago",
      status: "investigating",
    },
    {
      id: 2,
      type: "Warning",
      message: "High CPU usage detected on server-prod-01",
      time: "15 minutes ago",
      status: "resolved",
    },
    {
      id: 3,
      type: "Info",
      message: "Security patch applied to database cluster",
      time: "1 hour ago",
      status: "completed",
    },
    {
      id: 4,
      type: "Warning",
      message: "Failed authentication attempts threshold exceeded",
      time: "2 hours ago",
      status: "monitoring",
    },
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case "investigating":
        return "bg-[#f59e0b] text-black"
      case "resolved":
        return "bg-[#22c55e] text-black"
      case "completed":
        return "bg-[#0ea5e9] text-white"
      case "monitoring":
        return "bg-[#71717a] text-white"
      default:
        return "bg-[#71717a] text-white"
    }
  }

  const getTypeColor = (type: string) => {
    switch (type) {
      case "Critical":
        return "text-[#ef4444]"
      case "Warning":
        return "text-[#f59e0b]"
      case "Info":
        return "text-[#0ea5e9]"
      default:
        return "text-[#d4d4d8]"
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-white mb-2">Security Dashboard</h2>
        <p className="text-[#71717a]">Real-time security monitoring and threat detection</p>
      </div>

      {/* Security Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {securityMetrics.map((metric, index) => (
          <Card key={index} className="bg-[#2d2d2d] border-[#3d3d3d]">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-[#71717a] text-sm font-medium">{metric.title}</p>
                  <p className="text-2xl font-bold text-white mt-2">{metric.value}</p>
                  <p className={`text-sm mt-1 ${metric.color}`}>{metric.change} from last week</p>
                </div>
                <div className={`p-3 rounded-lg ${metric.bgColor}`}>
                  <metric.icon className={`h-6 w-6 ${metric.color}`} />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Security Events */}
        <Card className="lg:col-span-2 bg-[#2d2d2d] border-[#3d3d3d]">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <AlertTriangle className="h-5 w-5" />
              Recent Security Events
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentEvents.map((event) => (
                <div
                  key={event.id}
                  className="flex items-start gap-4 p-4 rounded-lg bg-[#1e1e1e] border border-[#3d3d3d]"
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`text-sm font-medium ${getTypeColor(event.type)}`}>{event.type}</span>
                      <Badge className={`text-xs ${getStatusColor(event.status)}`}>{event.status}</Badge>
                    </div>
                    <p className="text-[#d4d4d8] text-sm">{event.message}</p>
                    <p className="text-[#71717a] text-xs mt-1">{event.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* System Overview */}
        <Card className="bg-[#2d2d2d] border-[#3d3d3d]">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <Server className="h-5 w-5" />
              System Overview
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Users className="h-4 w-4 text-[#0ea5e9]" />
                  <span className="text-[#d4d4d8] text-sm">Active Users</span>
                </div>
                <span className="text-white font-medium">1,247</span>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <TrendingUp className="h-4 w-4 text-[#22c55e]" />
                  <span className="text-[#d4d4d8] text-sm">Network Traffic</span>
                </div>
                <span className="text-white font-medium">2.4 GB/s</span>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Zap className="h-4 w-4 text-[#f59e0b]" />
                  <span className="text-[#d4d4d8] text-sm">CPU Usage</span>
                </div>
                <span className="text-white font-medium">67%</span>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Server className="h-4 w-4 text-[#71717a]" />
                  <span className="text-[#d4d4d8] text-sm">Memory Usage</span>
                </div>
                <span className="text-white font-medium">4.2/8 GB</span>
              </div>
            </div>

            <div className="pt-4 border-t border-[#3d3d3d]">
              <div className="flex items-center gap-2 mb-2">
                <div className="h-2 w-2 rounded-full bg-[#22c55e]"></div>
                <span className="text-[#d4d4d8] text-sm">All systems operational</span>
              </div>
              <p className="text-[#71717a] text-xs">Last updated: 30 seconds ago</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

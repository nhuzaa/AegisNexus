"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  Area,
  AreaChart,
} from "recharts"
import { TrendingUp, Shield, AlertTriangle, CheckCircle, Activity } from "lucide-react"

export function MetricsView() {
  const threatData = [
    { name: "Mon", threats: 12, blocked: 11 },
    { name: "Tue", threats: 19, blocked: 18 },
    { name: "Wed", threats: 8, blocked: 8 },
    { name: "Thu", threats: 15, blocked: 14 },
    { name: "Fri", threats: 22, blocked: 20 },
    { name: "Sat", threats: 6, blocked: 6 },
    { name: "Sun", threats: 9, blocked: 9 },
  ]

  const performanceData = [
    { time: "00:00", response: 1.2, cpu: 45, memory: 62 },
    { time: "04:00", response: 1.1, cpu: 38, memory: 58 },
    { time: "08:00", response: 1.8, cpu: 72, memory: 75 },
    { time: "12:00", response: 2.1, cpu: 85, memory: 82 },
    { time: "16:00", response: 1.9, cpu: 78, memory: 79 },
    { time: "20:00", response: 1.4, cpu: 55, memory: 68 },
  ]

  const complianceData = [
    { name: "SOC 2", value: 98, color: "#22c55e" },
    { name: "ISO 27001", value: 95, color: "#0ea5e9" },
    { name: "GDPR", value: 92, color: "#f59e0b" },
    { name: "HIPAA", value: 89, color: "#ef4444" },
  ]

  const securityEvents = [
    { name: "Malware", value: 35, color: "#ef4444" },
    { name: "Phishing", value: 28, color: "#f59e0b" },
    { name: "DDoS", value: 20, color: "#0ea5e9" },
    { name: "Intrusion", value: 17, color: "#22c55e" },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-white mb-2">Security Metrics</h2>
        <p className="text-[#71717a]">Comprehensive analytics and performance insights</p>
      </div>

      {/* Key Performance Indicators */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="bg-[#2d2d2d] border-[#3d3d3d]">
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-lg bg-[#22c55e]/10">
                <Shield className="h-6 w-6 text-[#22c55e]" />
              </div>
              <div>
                <p className="text-[#71717a] text-sm">Threats Blocked</p>
                <p className="text-2xl font-bold text-white">1,247</p>
                <p className="text-[#22c55e] text-sm">+12% this week</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-[#2d2d2d] border-[#3d3d3d]">
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-lg bg-[#f59e0b]/10">
                <AlertTriangle className="h-6 w-6 text-[#f59e0b]" />
              </div>
              <div>
                <p className="text-[#71717a] text-sm">Active Alerts</p>
                <p className="text-2xl font-bold text-white">23</p>
                <p className="text-[#f59e0b] text-sm">-8% this week</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-[#2d2d2d] border-[#3d3d3d]">
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-lg bg-[#0ea5e9]/10">
                <CheckCircle className="h-6 w-6 text-[#0ea5e9]" />
              </div>
              <div>
                <p className="text-[#71717a] text-sm">Compliance Score</p>
                <p className="text-2xl font-bold text-white">94%</p>
                <p className="text-[#0ea5e9] text-sm">+3% this month</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-[#2d2d2d] border-[#3d3d3d]">
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-lg bg-[#ef4444]/10">
                <Activity className="h-6 w-6 text-[#ef4444]" />
              </div>
              <div>
                <p className="text-[#71717a] text-sm">Incidents</p>
                <p className="text-2xl font-bold text-white">5</p>
                <p className="text-[#ef4444] text-sm">+2 this week</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Threat Detection Trends */}
        <Card className="bg-[#2d2d2d] border-[#3d3d3d]">
          <CardHeader>
            <CardTitle className="text-white">Threat Detection Trends</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={threatData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#3d3d3d" />
                <XAxis dataKey="name" stroke="#71717a" />
                <YAxis stroke="#71717a" />
                <Bar dataKey="threats" fill="#ef4444" name="Threats Detected" />
                <Bar dataKey="blocked" fill="#22c55e" name="Threats Blocked" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* System Performance */}
        <Card className="bg-[#2d2d2d] border-[#3d3d3d]">
          <CardHeader>
            <CardTitle className="text-white">System Performance</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={performanceData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#3d3d3d" />
                <XAxis dataKey="time" stroke="#71717a" />
                <YAxis stroke="#71717a" />
                <Line type="monotone" dataKey="response" stroke="#0ea5e9" strokeWidth={2} name="Response Time (s)" />
                <Line type="monotone" dataKey="cpu" stroke="#f59e0b" strokeWidth={2} name="CPU Usage (%)" />
                <Line type="monotone" dataKey="memory" stroke="#22c55e" strokeWidth={2} name="Memory Usage (%)" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Compliance Scores */}
        <Card className="bg-[#2d2d2d] border-[#3d3d3d]">
          <CardHeader>
            <CardTitle className="text-white">Compliance Scores</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {complianceData.map((item, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-[#d4d4d8] text-sm font-medium">{item.name}</span>
                    <span className="text-white font-bold">{item.value}%</span>
                  </div>
                  <div className="w-full bg-[#1e1e1e] rounded-full h-2">
                    <div
                      className="h-2 rounded-full transition-all duration-300"
                      style={{
                        width: `${item.value}%`,
                        backgroundColor: item.color,
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Security Event Distribution */}
        <Card className="bg-[#2d2d2d] border-[#3d3d3d]">
          <CardHeader>
            <CardTitle className="text-white">Security Event Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={securityEvents}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="value"
                  label={({ name, value }) => `${name}: ${value}%`}
                >
                  {securityEvents.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Historical Trends */}
      <Card className="bg-[#2d2d2d] border-[#3d3d3d]">
        <CardHeader>
          <CardTitle className="text-white flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            Historical Security Trends (30 Days)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#3d3d3d" />
              <XAxis dataKey="time" stroke="#71717a" />
              <YAxis stroke="#71717a" />
              <Area type="monotone" dataKey="response" stackId="1" stroke="#0ea5e9" fill="#0ea5e9" fillOpacity={0.3} />
            </AreaChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}

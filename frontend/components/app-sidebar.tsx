"use client"

import { MessageSquare, Shield, Info, Settings, HelpCircle, Flame, Clock } from "lucide-react"
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarHeader,
  SidebarFooter,
} from "@/components/ui/sidebar"
import { useState } from "react"

const navItems = [
  {
    title: "AI Assistant",
    icon: MessageSquare,
    id: "chat",
  },
  {
    title: "Timeline Analysis",
    icon: Clock,
    id: "timeline",
  },
  {
    title: "Security Info",
    icon: Shield,
    id: "security",
  },
  {
    title: "About",
    icon: Info,
    id: "about",
  },
  {
    title: "Settings",
    icon: Settings,
    id: "settings",
  },
]

export function AppSidebar() {
  const [activeItem, setActiveItem] = useState("chat")

  const handleNavigation = (id: string) => {
    setActiveItem(id)
    // Dispatch custom event to update main view
    window.dispatchEvent(new CustomEvent("navigate", { detail: { view: id } }))
  }

  return (
    <Sidebar className="border-r border-[#3d3d3d]">
      <SidebarHeader className="border-b border-[#3d3d3d] p-4">
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded bg-gradient-to-br from-red-600 via-orange-500 to-yellow-500 flex items-center justify-center shadow-lg">
            <Flame className="h-4 w-4 text-black" />
          </div>
          <span className="font-semibold text-white">AegisNexus AI</span>
        </div>
      </SidebarHeader>

      <SidebarContent className="bg-[#1e1e1e]">
        <SidebarGroup>
          <SidebarGroupLabel className="text-[#71717a] text-xs uppercase tracking-wider">Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {navItems.map((item) => (
                <SidebarMenuItem key={item.id}>
                  <SidebarMenuButton
                    onClick={() => handleNavigation(item.id)}
                    isActive={activeItem === item.id}
                    className="text-[#d4d4d8] hover:text-white hover:bg-[#2d2d2d] data-[active=true]:bg-gradient-to-r data-[active=true]:from-red-600 data-[active=true]:to-orange-500 data-[active=true]:text-white"
                  >
                    <item.icon className="h-4 w-4" />
                    <span>{item.title}</span>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter className="border-t border-[#3d3d3d] p-4">
        <div className="flex items-center gap-2 text-[#71717a] text-sm">
          <HelpCircle className="h-4 w-4" />
          <span>Need help? Ask the AI</span>
        </div>
      </SidebarFooter>
    </Sidebar>
  )
}

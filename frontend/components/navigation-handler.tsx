"use client"

import { useEffect } from "react"

interface NavigationHandlerProps {
  onNavigate: (view: string) => void
}

export function NavigationHandler({ onNavigate }: NavigationHandlerProps) {
  useEffect(() => {
    const handleNavigation = (event: CustomEvent) => {
      onNavigate(event.detail.view)
    }

    window.addEventListener("navigate", handleNavigation as EventListener)

    return () => {
      window.removeEventListener("navigate", handleNavigation as EventListener)
    }
  }, [onNavigate])

  return null
}

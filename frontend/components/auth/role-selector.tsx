"use client"

import type React from "react"

import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { UserRound, Stethoscope, Pill, HeartPulse } from "lucide-react"
import type { HealthcareRole } from "@/types/auth"

interface RoleSelectorProps {
  onRoleSelect: (role: HealthcareRole) => void
}

interface RoleOption {
  id: HealthcareRole
  label: string
  icon: React.ReactNode
  color: string
}

export default function RoleSelector({ onRoleSelect }: RoleSelectorProps) {
  const [hoveredRole, setHoveredRole] = useState<HealthcareRole | null>(null)

  const roles: RoleOption[] = [
    {
      id: "doctor",
      label: "Doctor",
      icon: <Stethoscope size={24} />,
      color: "bg-green-100 border-green-300 hover:bg-green-200",
    },
    {
      id: "nurse",
      label: "Nurse",
      icon: <HeartPulse size={24} />,
      color: "bg-blue-100 border-blue-300 hover:bg-blue-200",
    },
    {
      id: "pharmacy",
      label: "Pharmacy",
      icon: <Pill size={24} />,
      color: "bg-purple-100 border-purple-300 hover:bg-purple-200",
    },
    {
      id: "patient",
      label: "Patient",
      icon: <UserRound size={24} />,
      color: "bg-amber-100 border-amber-300 hover:bg-amber-200",
    },
  ]

  return (
    <div className="grid grid-cols-2 gap-4">
      {roles.map((role) => (
        <Card
          key={role.id}
          className={`cursor-pointer border-2 transition-all ${
            hoveredRole === role.id ? `${role.color} scale-105` : "bg-white"
          }`}
          onClick={() => onRoleSelect(role.id)}
          onMouseEnter={() => setHoveredRole(role.id)}
          onMouseLeave={() => setHoveredRole(null)}
        >
          <CardContent className="flex flex-col items-center justify-center p-6">
            <div className={`p-2 rounded-full mb-2 ${role.color.split(" ")[0]}`}>{role.icon}</div>
            <span className="font-medium">{role.label}</span>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}


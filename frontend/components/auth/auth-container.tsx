"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import RoleSelector from "./role-selector"
import LoginForm from "./login-form"
import RegisterForm from "./register-form"
import type { HealthcareRole } from "@/types/auth"

export default function AuthContainer() {
  const [selectedRole, setSelectedRole] = useState<HealthcareRole | null>(null)
  const [activeTab, setActiveTab] = useState<"login" | "register">("login")

  return (
    <Card className="w-full max-w-md shadow-lg">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl font-bold text-center">Healthcare Platform</CardTitle>
        <CardDescription className="text-center">
          {selectedRole ? `Sign in or register as a ${selectedRole}` : "Select your role to continue"}
        </CardDescription>
      </CardHeader>
      <CardContent>
        {!selectedRole ? (
          <RoleSelector onRoleSelect={setSelectedRole} />
        ) : (
          <Tabs
            defaultValue={activeTab}
            onValueChange={(value) => setActiveTab(value as "login" | "register")}
            className="w-full"
          >
            <TabsList className="grid w-full grid-cols-2 mb-6">
              <TabsTrigger value="login">Login</TabsTrigger>
              <TabsTrigger value="register">Register</TabsTrigger>
            </TabsList>
            <TabsContent value="login">
              <LoginForm role={selectedRole} />
            </TabsContent>
            <TabsContent value="register">
              <RegisterForm role={selectedRole} />
            </TabsContent>
          </Tabs>
        )}

        {selectedRole && (
          <button
            onClick={() => setSelectedRole(null)}
            className="w-full text-sm text-blue-600 hover:text-blue-800 text-center mt-4"
          >
            Change role
          </button>
        )}
      </CardContent>
    </Card>
  )
}


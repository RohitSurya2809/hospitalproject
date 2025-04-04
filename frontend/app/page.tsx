import type { Metadata } from "next"
import AuthContainer from "@/components/auth/auth-container"

export const metadata: Metadata = {
  title: "Healthcare Platform - Authentication",
  description: "Login or register to access the healthcare platform",
}

export default function AuthPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex items-center justify-center p-4">
      <AuthContainer />
    </div>
  )
}


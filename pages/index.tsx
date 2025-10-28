import { useEffect } from 'react'
import { useRouter } from 'next/router'
import { useAuth } from '../lib/auth'
import LoadingSpinner from '../components/common/LoadingSpinner'

export default function Home() {
  const { user, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading) {
      if (user) {
        // User is authenticated, redirect to dashboard
        router.replace('/dashboard')
      } else {
        // User is not authenticated, redirect to login
        router.replace('/login')
      }
    }
  }, [user, isLoading, router])

  // Show loading spinner while checking authentication
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="mb-4">
            <div className="h-12 w-12 bg-primary-600 rounded-lg flex items-center justify-center mx-auto">
              <svg className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">Intelligent CRM</h1>
            <p className="text-gray-600">Loading your workspace...</p>
          </div>
          <LoadingSpinner />
        </div>
      </div>
    )
  }

  // This should not be reached due to the redirect, but just in case
  return null
}

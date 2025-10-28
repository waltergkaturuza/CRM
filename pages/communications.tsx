import Head from 'next/head'
import { useRouter } from 'next/router'
import { useEffect } from 'react'
import { useAuth } from '../lib/auth'
import Layout from '../components/layout/Layout'

export default function CommunicationsPage() {
  const { user, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && !user) {
      router.replace('/login')
    }
  }, [user, isLoading, router])

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!user) {
    return null
  }

  return (
    <>
      <Head>
        <title>Communications - Intelligent CRM</title>
        <meta name="description" content="Manage your customer communications" />
      </Head>
      
      <Layout>
        <div className="space-y-6">
          <div className="sm:flex sm:items-center sm:justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Communications</h1>
              <p className="mt-1 text-sm text-gray-500">
                Manage emails, calls, and other customer interactions.
              </p>
            </div>
            <div className="mt-4 sm:mt-0">
              <button
                type="button"
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                New Message
              </button>
            </div>
          </div>

          <div className="bg-white shadow rounded-lg p-6">
            <div className="text-center py-12">
              <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              <h3 className="mt-2 text-sm font-medium text-gray-900">No communications yet</h3>
              <p className="mt-1 text-sm text-gray-500">Start communicating with your customers.</p>
              <div className="mt-6">
                <button
                  type="button"
                  className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                >
                  Send Message
                </button>
              </div>
            </div>
          </div>
        </div>
      </Layout>
    </>
  )
}

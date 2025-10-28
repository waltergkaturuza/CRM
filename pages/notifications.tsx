import Head from 'next/head'
import { useRouter } from 'next/router'
import { useEffect } from 'react'
import { useAuth } from '../lib/auth'
import Layout from '../components/layout/Layout'

export default function NotificationsPage() {
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
        <title>Notifications - Intelligent CRM</title>
        <meta name="description" content="Manage your notifications and alerts" />
      </Head>
      
      <Layout>
        <div className="space-y-6">
          <div className="sm:flex sm:items-center sm:justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Notifications</h1>
              <p className="mt-1 text-sm text-gray-500">
                Stay updated with important alerts and messages.
              </p>
            </div>
            <div className="mt-4 sm:mt-0">
              <button
                type="button"
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                Mark All Read
              </button>
            </div>
          </div>

          <div className="bg-white shadow rounded-lg p-6">
            <div className="text-center py-12">
              <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-5 5v-5zM11 17H6l5 5v-5zM7 7h10v10H7V7z" />
              </svg>
              <h3 className="mt-2 text-sm font-medium text-gray-900">No notifications</h3>
              <p className="mt-1 text-sm text-gray-500">You're all caught up! No new notifications.</p>
            </div>
          </div>
        </div>
      </Layout>
    </>
  )
}

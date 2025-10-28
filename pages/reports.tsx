import Head from 'next/head'
import { useRouter } from 'next/router'
import { useEffect } from 'react'
import { useAuth } from '../lib/auth'
import Layout from '../components/layout/Layout'

export default function ReportsPage() {
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
        <title>Reports - Intelligent CRM</title>
        <meta name="description" content="Generate and view CRM reports" />
      </Head>
      
      <Layout>
        <div className="space-y-6">
          <div className="sm:flex sm:items-center sm:justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Reports</h1>
              <p className="mt-1 text-sm text-gray-500">
                Generate detailed reports on your CRM data.
              </p>
            </div>
            <div className="mt-4 sm:mt-0">
              <button
                type="button"
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                Generate Report
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Sales Report</h3>
              <p className="text-sm text-gray-500 mb-4">Overview of sales performance and revenue.</p>
              <button className="w-full bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
                Generate
              </button>
            </div>

            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Customer Report</h3>
              <p className="text-sm text-gray-500 mb-4">Detailed customer analysis and insights.</p>
              <button className="w-full bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
                Generate
              </button>
            </div>

            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Lead Report</h3>
              <p className="text-sm text-gray-500 mb-4">Lead conversion and pipeline analysis.</p>
              <button className="w-full bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
                Generate
              </button>
            </div>
          </div>
        </div>
      </Layout>
    </>
  )
}

import Head from 'next/head'
import Link from 'next/link'
import { HomeIcon } from '@heroicons/react/24/outline'

export default function Custom404() {
  return (
    <>
      <Head>
        <title>404 - Page Not Found | Intelligent CRM</title>
        <meta name="description" content="The page you're looking for doesn't exist." />
      </Head>
      
      <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <div className="text-center">
            <div className="mx-auto h-16 w-16 bg-primary-600 rounded-lg flex items-center justify-center mb-6">
              <svg className="h-10 w-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            
            <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>
            <h2 className="text-2xl font-semibold text-gray-700 mb-4">Page Not Found</h2>
            <p className="text-gray-600 mb-8 max-w-md mx-auto">
              Sorry, we couldn't find the page you're looking for. The page might have been moved, deleted, or you entered the wrong URL.
            </p>
            
            <div className="space-y-4">
              <Link 
                href="/dashboard"
                className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors duration-200"
              >
                <HomeIcon className="h-5 w-5 mr-2" />
                Go to Dashboard
              </Link>
              
              <div className="text-center">
                <button
                  onClick={() => window.history.back()}
                  className="text-primary-600 hover:text-primary-500 font-medium"
                >
                  ← Go back to previous page
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div className="mt-12 text-center">
          <p className="text-sm text-gray-500">
            Need help? Contact our support team or check our{' '}
            <Link 
              href="/help"
              className="text-primary-600 hover:text-primary-500"
            >
              help center
            </Link>
          </p>
        </div>
      </div>
    </>
  )
}

import Head from 'next/head'
import { useRouter } from 'next/router'
import { useEffect } from 'react'
import { useAuth } from '../lib/auth'
import Layout from '../components/layout/Layout'
import CustomerList from '../components/customers/CustomerList'

export default function CustomersPage() {
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
        <title>Customers - Intelligent CRM</title>
        <meta name="description" content="Manage your customers" />
      </Head>
      
      <Layout>
        <CustomerList />
      </Layout>
    </>
  )
}

// Removed getServerSideProps to avoid cookie/localStorage mismatch

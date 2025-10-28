import Head from 'next/head'
import { GetServerSideProps } from 'next'
import { useRouter } from 'next/router'
import { useEffect } from 'react'
import { useAuth } from '../lib/auth'
import Layout from '../components/layout/Layout'
import CustomerList from '../components/customers/CustomerList'

export default function CustomersPage() {
  const { user, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!user && !isLoading) {
      router.push('/login')
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

export const getServerSideProps: GetServerSideProps = async (context) => {
  // Check if user is logged in
  const token = context.req.cookies.token
  
  if (!token) {
    return {
      redirect: {
        destination: '/login',
        permanent: false,
      },
    }
  }

  return {
    props: {},
  }
}

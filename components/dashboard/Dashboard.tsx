import React from 'react'
import { useQuery } from 'react-query'
import apiClient from '../../lib/api'
import StatsCard from './StatsCard'
import RecentActivity from './RecentActivity'
import SalesChart from './SalesChart'
import TopCustomers from './TopCustomers'
import QuickActions from './QuickActions'

export default function Dashboard() {
  // Mock data for now since the API endpoints don't exist yet
  const mockDashboardData = {
    stats: {
      totalCustomers: 1234,
      totalLeads: 567,
      totalDeals: 89,
      totalRevenue: 45678
    },
    topCustomers: [
      { id: 1, name: 'John Doe', company: 'Acme Corp', revenue: 25000, status: 'active' },
      { id: 2, name: 'Jane Smith', company: 'Tech Solutions', revenue: 18000, status: 'active' },
      { id: 3, name: 'Bob Johnson', company: 'Global Inc', revenue: 32000, status: 'prospect' },
    ],
    salesChart: [
      { month: 'Jan', sales: 12000 },
      { month: 'Feb', sales: 15000 },
      { month: 'Mar', sales: 18000 },
      { month: 'Apr', sales: 22000 },
      { month: 'May', sales: 25000 },
      { month: 'Jun', sales: 28000 },
    ],
    recentActivity: [
      { 
        id: 1, 
        type: 'customer', 
        description: 'added a new customer', 
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(), // 2 hours ago
        user: 'Admin User',
        customer: 'John Doe'
      },
      { 
        id: 2, 
        type: 'deal', 
        description: 'closed a deal with', 
        timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(), // 4 hours ago
        user: 'Sales Rep',
        deal: 'Acme Corp'
      },
      { 
        id: 3, 
        type: 'lead', 
        description: 'received a new lead from website', 
        timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(), // 6 hours ago
        user: 'Marketing Team'
      },
    ]
  }

  const isLoading = false
  const error = null
  const dashboardData = mockDashboardData

  if (isLoading) {
    return (
      <div className="animate-pulse">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="bg-white rounded-lg shadow p-6">
              <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div className="h-8 bg-gray-200 rounded w-1/2"></div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">
              Error loading dashboard
            </h3>
            <div className="mt-2 text-sm text-red-700">
              <p>Unable to load dashboard data. Please try again later.</p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  const stats = dashboardData?.stats || {
    totalCustomers: 0,
    totalLeads: 0,
    totalDeals: 0,
    totalRevenue: 0,
  }

  return (
    <div className="space-y-8">
      {/* Page header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          Welcome back! Here's what's happening with your business today.
        </p>
      </div>

      {/* Stats cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Total Customers"
          value={stats.totalCustomers}
          change="+12%"
          changeType="positive"
          icon="users"
        />
        <StatsCard
          title="Active Leads"
          value={stats.totalLeads}
          change="+8%"
          changeType="positive"
          icon="user-group"
        />
        <StatsCard
          title="Open Deals"
          value={stats.totalDeals}
          change="-3%"
          changeType="negative"
          icon="currency-dollar"
        />
        <StatsCard
          title="Revenue"
          value={`$${stats.totalRevenue.toLocaleString()}`}
          change="+15%"
          changeType="positive"
          icon="chart-bar"
        />
      </div>

      {/* Charts and analytics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <SalesChart data={dashboardData?.salesChart || []} />
        <TopCustomers customers={dashboardData?.topCustomers || []} />
      </div>

      {/* Recent activity and quick actions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <RecentActivity activities={dashboardData?.recentActivity || []} />
        </div>
        <div>
          <QuickActions />
        </div>
      </div>
    </div>
  )
}

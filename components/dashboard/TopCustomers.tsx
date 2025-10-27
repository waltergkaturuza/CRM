import React from 'react'
import Link from 'next/link'

interface Customer {
  id: number
  name: string
  company: string
  revenue: number
  status: string
}

interface TopCustomersProps {
  customers: Customer[]
}

export default function TopCustomers({ customers }: TopCustomersProps) {
  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
        return 'bg-green-100 text-green-800'
      case 'inactive':
        return 'bg-gray-100 text-gray-800'
      case 'prospect':
        return 'bg-blue-100 text-blue-800'
      case 'churned':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-medium text-gray-900">Top Customers</h3>
        <Link href="/customers">
          <a className="text-sm text-primary-600 hover:text-primary-500">
            View all
          </a>
        </Link>
      </div>
      
      <div className="space-y-4">
        {customers.map((customer) => (
          <div key={customer.id} className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="flex-shrink-0 h-10 w-10">
                <div className="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                  <span className="text-sm font-medium text-gray-700">
                    {customer.name.split(' ').map(n => n[0]).join('')}
                  </span>
                </div>
              </div>
              <div className="ml-4">
                <div className="text-sm font-medium text-gray-900">{customer.name}</div>
                <div className="text-sm text-gray-500">{customer.company}</div>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <span className="text-sm font-medium text-gray-900">
                ${customer.revenue.toLocaleString()}
              </span>
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(customer.status)}`}>
                {customer.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

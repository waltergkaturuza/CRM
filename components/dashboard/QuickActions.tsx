import React from 'react'
import Link from 'next/link'
import { PlusIcon, UserGroupIcon, CurrencyDollarIcon, ChartBarIcon } from '@heroicons/react/24/outline'

export default function QuickActions() {
  const actions = [
    {
      name: 'Add Customer',
      href: '/customers/new',
      icon: PlusIcon,
      color: 'bg-blue-500',
    },
    {
      name: 'Create Lead',
      href: '/leads/new',
      icon: UserGroupIcon,
      color: 'bg-green-500',
    },
    {
      name: 'New Deal',
      href: '/deals/new',
      icon: CurrencyDollarIcon,
      color: 'bg-purple-500',
    },
    {
      name: 'View Reports',
      href: '/reports',
      icon: ChartBarIcon,
      color: 'bg-orange-500',
    },
  ]

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
      <div className="space-y-3">
        {actions.map((action) => (
          <Link 
            key={action.name} 
            href={action.href}
            className="flex items-center p-3 rounded-lg hover:bg-gray-50 transition-colors duration-200"
          >
            <div className={`flex-shrink-0 w-8 h-8 ${action.color} rounded-lg flex items-center justify-center`}>
              <action.icon className="h-5 w-5 text-white" />
            </div>
            <span className="ml-3 text-sm font-medium text-gray-900">{action.name}</span>
          </Link>
        ))}
      </div>
    </div>
  )
}

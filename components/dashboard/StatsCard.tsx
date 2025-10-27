import React from 'react'
import { 
  UsersIcon, 
  UserGroupIcon, 
  CurrencyDollarIcon, 
  ChartBarIcon 
} from '@heroicons/react/outline'

interface StatsCardProps {
  title: string
  value: string | number
  change: string
  changeType: 'positive' | 'negative' | 'neutral'
  icon: string
}

const iconMap = {
  users: UsersIcon,
  'user-group': UserGroupIcon,
  'currency-dollar': CurrencyDollarIcon,
  'chart-bar': ChartBarIcon,
}

export default function StatsCard({ title, value, change, changeType, icon }: StatsCardProps) {
  const IconComponent = iconMap[icon as keyof typeof iconMap] || ChartBarIcon

  const changeColor = {
    positive: 'text-green-600',
    negative: 'text-red-600',
    neutral: 'text-gray-600',
  }[changeType]

  const changeBgColor = {
    positive: 'bg-green-100',
    negative: 'bg-red-100',
    neutral: 'bg-gray-100',
  }[changeType]

  return (
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="p-5">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <IconComponent className="h-6 w-6 text-gray-400" aria-hidden="true" />
          </div>
          <div className="ml-5 w-0 flex-1">
            <dl>
              <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
              <dd className="flex items-baseline">
                <div className="text-2xl font-semibold text-gray-900">{value}</div>
                <div className={`ml-2 flex items-baseline text-sm font-semibold ${changeColor}`}>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${changeBgColor} ${changeColor}`}>
                    {change}
                  </span>
                </div>
              </dd>
            </dl>
          </div>
        </div>
      </div>
    </div>
  )
}

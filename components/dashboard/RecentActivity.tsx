import React from 'react'
import { formatDistanceToNow } from 'date-fns'

interface Activity {
  id: number
  type: string
  description: string
  user: string
  timestamp: string
  customer?: string
  lead?: string
  deal?: string
}

interface RecentActivityProps {
  activities: Activity[]
}

export default function RecentActivity({ activities }: RecentActivityProps) {
  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'customer_created':
        return '👤'
      case 'lead_created':
        return '🎯'
      case 'deal_created':
        return '💰'
      case 'email_sent':
        return '📧'
      case 'call_made':
        return '📞'
      case 'meeting_scheduled':
        return '📅'
      default:
        return '📝'
    }
  }

  const getActivityColor = (type: string) => {
    switch (type) {
      case 'customer_created':
        return 'bg-blue-100 text-blue-800'
      case 'lead_created':
        return 'bg-green-100 text-green-800'
      case 'deal_created':
        return 'bg-purple-100 text-purple-800'
      case 'email_sent':
        return 'bg-yellow-100 text-yellow-800'
      case 'call_made':
        return 'bg-red-100 text-red-800'
      case 'meeting_scheduled':
        return 'bg-indigo-100 text-indigo-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-medium text-gray-900">Recent Activity</h3>
        <a href="/activity" className="text-sm text-primary-600 hover:text-primary-500">
          View all
        </a>
      </div>
      
      <div className="flow-root">
        <ul className="-mb-8">
          {activities.map((activity, activityIdx) => (
            <li key={activity.id}>
              <div className="relative pb-8">
                {activityIdx !== activities.length - 1 ? (
                  <span
                    className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"
                    aria-hidden="true"
                  />
                ) : null}
                <div className="relative flex space-x-3">
                  <div>
                    <span className={`h-8 w-8 rounded-full flex items-center justify-center ring-8 ring-white ${getActivityColor(activity.type)}`}>
                      <span className="text-sm">{getActivityIcon(activity.type)}</span>
                    </span>
                  </div>
                  <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                    <div>
                      <p className="text-sm text-gray-500">
                        <span className="font-medium text-gray-900">{activity.user}</span>{' '}
                        {activity.description}
                        {activity.customer && (
                          <span className="font-medium text-gray-900"> {activity.customer}</span>
                        )}
                        {activity.lead && (
                          <span className="font-medium text-gray-900"> {activity.lead}</span>
                        )}
                        {activity.deal && (
                          <span className="font-medium text-gray-900"> {activity.deal}</span>
                        )}
                      </p>
                    </div>
                    <div className="text-right text-sm whitespace-nowrap text-gray-500">
                      <time dateTime={activity.timestamp}>
                        {formatDistanceToNow(new Date(activity.timestamp), { addSuffix: true })}
                      </time>
                    </div>
                  </div>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}

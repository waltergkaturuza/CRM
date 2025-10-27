import React from 'react'
import Link from 'next/link'
import { useRouter } from 'next/router'
import { 
  HomeIcon,
  UsersIcon,
  UserGroupIcon,
  CurrencyDollarIcon,
  ChartBarIcon,
  CogIcon,
  BellIcon,
  ChatAltIcon,
  DocumentTextIcon,
  CalendarIcon,
} from '@heroicons/react/outline'

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
}

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
  { name: 'Customers', href: '/customers', icon: UsersIcon },
  { name: 'Leads', href: '/leads', icon: UserGroupIcon },
  { name: 'Deals', href: '/deals', icon: CurrencyDollarIcon },
  { name: 'Analytics', href: '/analytics', icon: ChartBarIcon },
  { name: 'Tasks', href: '/tasks', icon: CalendarIcon },
  { name: 'Communications', href: '/communications', icon: ChatAltIcon },
  { name: 'Reports', href: '/reports', icon: DocumentTextIcon },
  { name: 'Notifications', href: '/notifications', icon: BellIcon },
  { name: 'Settings', href: '/settings', icon: CogIcon },
]

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  const router = useRouter()

  return (
    <>
      {/* Mobile sidebar overlay */}
      {isOpen && (
        <div className="fixed inset-0 flex z-40 md:hidden">
          <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={onClose} />
          <div className="relative flex-1 flex flex-col max-w-xs w-full bg-white">
            <div className="absolute top-0 right-0 -mr-12 pt-2">
              <button
                type="button"
                className="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
                onClick={onClose}
              >
                <span className="sr-only">Close sidebar</span>
                <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <SidebarContent />
          </div>
        </div>
      )}

      {/* Desktop sidebar */}
      <div className="hidden md:flex md:flex-shrink-0">
        <div className="flex flex-col w-64">
          <SidebarContent />
        </div>
      </div>
    </>
  )
}

function SidebarContent() {
  const router = useRouter()

  return (
    <div className="flex flex-col h-0 flex-1 border-r border-gray-200 bg-white">
      <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
        <div className="flex items-center flex-shrink-0 px-4">
          <div className="h-8 w-8 bg-primary-600 rounded-lg flex items-center justify-center">
            <svg className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <span className="ml-2 text-xl font-bold text-gray-900">Intelligent CRM</span>
        </div>
        <nav className="mt-5 flex-1 px-2 space-y-1">
          {navigation.map((item) => {
            const isActive = router.pathname === item.href
            return (
              <Link key={item.name} href={item.href}>
                <a
                  className={`${
                    isActive
                      ? 'bg-primary-100 text-primary-900'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  } group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors duration-200`}
                >
                  <item.icon
                    className={`${
                      isActive ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500'
                    } mr-3 flex-shrink-0 h-6 w-6 transition-colors duration-200`}
                    aria-hidden="true"
                  />
                  {item.name}
                </a>
              </Link>
            )
          })}
        </nav>
      </div>
      
      {/* User section */}
      <div className="flex-shrink-0 flex border-t border-gray-200 p-4">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="h-8 w-8 bg-gray-300 rounded-full flex items-center justify-center">
              <span className="text-sm font-medium text-gray-700">U</span>
            </div>
          </div>
          <div className="ml-3">
            <p className="text-sm font-medium text-gray-700">User Name</p>
            <p className="text-xs text-gray-500">Sales Rep</p>
          </div>
        </div>
      </div>
    </div>
  )
}

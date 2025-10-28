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
  ChatBubbleLeftRightIcon as ChatAltIcon,
  DocumentTextIcon,
  CalendarIcon,
} from '@heroicons/react/24/outline'

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
  onToggle: () => void
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

export default function Sidebar({ isOpen, onClose, onToggle }: SidebarProps) {
  const router = useRouter()

  return (
    <>
      {/* Mobile sidebar overlay */}
      <div className={`fixed inset-0 flex z-40 md:hidden transition-opacity duration-300 ${
        isOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'
      }`}>
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={onClose} />
        <div className={`relative flex-1 flex flex-col max-w-xs w-full bg-white transform transition-transform duration-300 ease-in-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}>
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
          <SidebarContent isCollapsed={false} />
        </div>
      </div>

      {/* Desktop sidebar */}
      <div className={`hidden md:flex md:flex-shrink-0 transition-all duration-300 ease-in-out ${
        isOpen ? 'w-64' : 'w-16'
      }`}>
        <div className="flex flex-col w-full">
          <SidebarContent isCollapsed={!isOpen} onToggle={onToggle} />
        </div>
      </div>
    </>
  )
}

interface SidebarContentProps {
  isCollapsed: boolean
  onToggle?: () => void
}

function SidebarContent({ isCollapsed, onToggle }: SidebarContentProps) {
  const router = useRouter()

  return (
    <div className="flex flex-col h-full border-r border-gray-200 bg-white">
      <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
        {/* Header with logo and toggle button */}
        <div className={`flex items-center flex-shrink-0 px-4 ${isCollapsed ? 'justify-center' : 'justify-between'}`}>
          <div className="flex items-center">
            <div className="h-8 w-8 bg-primary-600 rounded-lg flex items-center justify-center">
              <svg className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            {!isCollapsed && (
              <span className="ml-2 text-xl font-bold text-gray-900 whitespace-nowrap">Intelligent CRM</span>
            )}
          </div>
          {onToggle && !isCollapsed && (
            <button
              onClick={onToggle}
              className="p-1 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
              title="Collapse sidebar"
            >
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
              </svg>
            </button>
          )}
        </div>

        {/* Toggle button for collapsed state */}
        {onToggle && isCollapsed && (
          <div className="px-4 mt-2">
            <button
              onClick={onToggle}
              className="w-full p-2 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
              title="Expand sidebar"
            >
              <svg className="h-5 w-5 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        )}

        <nav className="mt-5 flex-1 px-2 space-y-1">
          {navigation.map((item) => {
            const isActive = router.pathname === item.href
            return (
              <Link 
                key={item.name} 
                href={item.href}
                className={`${
                  isActive
                    ? 'bg-primary-100 text-primary-900'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                } group flex items-center ${isCollapsed ? 'px-2 py-3 justify-center' : 'px-2 py-2'} text-sm font-medium rounded-md transition-all duration-200`}
                title={isCollapsed ? item.name : undefined}
              >
                <item.icon
                  className={`${
                    isActive ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500'
                  } ${isCollapsed ? 'h-6 w-6' : 'mr-3 h-6 w-6'} flex-shrink-0 transition-colors duration-200`}
                  aria-hidden="true"
                />
                {!isCollapsed && (
                  <span className="truncate">{item.name}</span>
                )}
              </Link>
            )
          })}
        </nav>
      </div>
      
      {/* User section */}
      <div className={`flex-shrink-0 flex border-t border-gray-200 p-4 ${isCollapsed ? 'justify-center' : ''}`}>
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="h-8 w-8 bg-gray-300 rounded-full flex items-center justify-center">
              <span className="text-sm font-medium text-gray-700">U</span>
            </div>
          </div>
          {!isCollapsed && (
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-700">User Name</p>
              <p className="text-xs text-gray-500">Sales Rep</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

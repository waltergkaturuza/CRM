import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import { PlusIcon, MagnifyingGlassIcon, FunnelIcon } from '@heroicons/react/24/outline'
import apiClient from '../../lib/api'
import CustomerTable from './CustomerTable'
import CustomerModal from './CustomerModal'
import LoadingSpinner from '../common/LoadingSpinner'

export default function CustomerList() {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingCustomer, setEditingCustomer] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [filters, setFilters] = useState({})
  
  const queryClient = useQueryClient()

  // Mock data for now since the API endpoints don't exist yet
  const mockCustomers = [
    {
      id: 1,
      name: 'John Doe',
      email: 'john.doe@acmecorp.com',
      company: 'Acme Corp',
      phone: '+1 (555) 123-4567',
      status: 'active',
      created_at: '2024-01-15T10:30:00Z',
      last_contact: '2024-10-20T14:22:00Z',
      total_value: 25000
    },
    {
      id: 2,
      name: 'Jane Smith',
      email: 'jane.smith@techsolutions.com',
      company: 'Tech Solutions',
      phone: '+1 (555) 987-6543',
      status: 'active',
      created_at: '2024-02-10T09:15:00Z',
      last_contact: '2024-10-18T11:45:00Z',
      total_value: 18000
    },
    {
      id: 3,
      name: 'Bob Johnson',
      email: 'bob.johnson@globalinc.com',
      company: 'Global Inc',
      phone: '+1 (555) 456-7890',
      status: 'prospect',
      created_at: '2024-03-05T16:20:00Z',
      last_contact: '2024-10-15T13:30:00Z',
      total_value: 32000
    },
    {
      id: 4,
      name: 'Alice Brown',
      email: 'alice.brown@startup.io',
      company: 'Startup.io',
      phone: '+1 (555) 321-0987',
      status: 'inactive',
      created_at: '2024-01-20T08:45:00Z',
      last_contact: '2024-09-30T10:15:00Z',
      total_value: 8500
    }
  ]

  // Filter mock data based on search term
  const filteredCustomers = mockCustomers.filter(customer => 
    !searchTerm || 
    customer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    customer.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    customer.company.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const customers = filteredCustomers
  const isLoading = false
  const error = null

  const deleteCustomerMutation = {
    mutate: (id: number) => {
      // Mock delete - in a real app this would call the API
      console.log('Mock delete customer:', id)
      // For now, just show a success message
      // In the future, this will call apiClient.deleteCustomer(id)
    },
    isLoading: false
  }

  const handleEdit = (customer: any) => {
    setEditingCustomer(customer)
    setIsModalOpen(true)
  }

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this customer?')) {
      try {
        await deleteCustomerMutation.mutateAsync(id)
      } catch (error) {
        console.error('Error deleting customer:', error)
      }
    }
  }

  const handleModalClose = () => {
    setIsModalOpen(false)
    setEditingCustomer(null)
  }

  if (isLoading) {
    return <LoadingSpinner />
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
              Error loading customers
            </h3>
            <div className="mt-2 text-sm text-red-700">
              <p>Unable to load customers. Please try again later.</p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Customers</h1>
          <p className="mt-1 text-sm text-gray-500">
            Manage your customer relationships and track their journey.
          </p>
        </div>
        <div className="mt-4 sm:mt-0">
          <button
            type="button"
            onClick={() => setIsModalOpen(true)}
            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            Add Customer
          </button>
        </div>
      </div>

      {/* Search and filters */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0 sm:space-x-4">
          <div className="flex-1 max-w-lg">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                placeholder="Search customers..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              />
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <button
              type="button"
              className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <FunnelIcon className="h-4 w-4 mr-2" />
              Filters
            </button>
          </div>
        </div>
      </div>

      {/* Customer table */}
      <CustomerTable
        customers={customers?.results || []}
        onEdit={handleEdit}
        onDelete={handleDelete}
        isLoading={isLoading}
      />

      {/* Customer modal */}
      <CustomerModal
        isOpen={isModalOpen}
        onClose={handleModalClose}
        customer={editingCustomer}
      />
    </div>
  )
}

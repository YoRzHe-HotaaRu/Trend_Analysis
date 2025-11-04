import { useQuery } from 'react-query'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('API Error:', error)
    
    if (error.response) {
      // Server responded with error status
      throw new Error(error.response.data?.message || 'Server error')
    } else if (error.request) {
      // Request was made but no response
      throw new Error('Network error - please check your connection')
    } else {
      // Something else happened
      throw new Error('Request failed')
    }
  }
)

export const useDataFetch = (endpoint, options = {}) => {
  return useQuery(
    ['data', endpoint, options.params],
    async () => {
      const response = await apiClient.get(endpoint, {
        params: options.params,
      })
      return response
    },
    {
      enabled: options.enabled !== false,
      refetchOnWindowFocus: options.refetchOnWindowFocus !== false,
      refetchInterval: options.refetchInterval,
      retry: options.retry || 1,
      staleTime: options.staleTime || 5 * 60 * 1000, // 5 minutes
      cacheTime: options.cacheTime || 10 * 60 * 1000, // 10 minutes
      onSuccess: options.onSuccess,
      onError: options.onError,
    }
  )
}

export const useMutation = (endpoint, options = {}) => {
  const mutation = useQueryClient()

  return useMutation(
    async (data) => {
      const response = await apiClient.post(endpoint, data)
      return response
    },
    {
      onSuccess: (data) => {
        // Invalidate and refetch related queries
        mutation.invalidateQueries(['data'])
        options.onSuccess?.(data)
      },
      onError: (error) => {
        console.error('Mutation error:', error)
        options.onError?.(error)
      },
    }
  )
}

export default apiClient
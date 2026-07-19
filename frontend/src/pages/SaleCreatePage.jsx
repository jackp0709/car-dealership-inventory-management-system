import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { apiClient } from '../api/client'
import SaleForm from '../components/SaleForm'

function SaleCreatePage() {
  const navigate = useNavigate()
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (payload) => {
    setError('')
    setIsSubmitting(true)
    try {
      await apiClient.post('/sales', payload)
      navigate('/sales', { state: { successMessage: 'Sale recorded successfully.' } })
    } catch (requestError) {
      const detail = requestError.response?.data?.detail
      setError(requestError.response?.status === 401 ? 'Your authentication has expired. Please sign in again.' : Array.isArray(detail) ? detail.map((item) => item.msg).join(' ') : detail ?? 'Unable to record the sale. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return <SaleForm error={error} isSubmitting={isSubmitting} onCancel={() => navigate('/sales')} onSubmit={handleSubmit} />
}

export default SaleCreatePage

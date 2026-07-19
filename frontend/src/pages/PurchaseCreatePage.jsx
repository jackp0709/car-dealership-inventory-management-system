import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { apiClient } from '../api/client'
import PurchaseForm from '../components/PurchaseForm'

function PurchaseCreatePage() {
  const navigate = useNavigate()
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (payload) => {
    setError('')
    setIsSubmitting(true)
    try {
      await apiClient.post('/purchases', payload)
      navigate('/purchases', { state: { successMessage: 'Purchase recorded successfully.' } })
    } catch (requestError) {
      const detail = requestError.response?.data?.detail
      setError(requestError.response?.status === 401 ? 'Your authentication has expired. Please sign in again.' : Array.isArray(detail) ? detail.map((item) => item.msg).join(' ') : detail ?? 'Unable to record the purchase. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return <PurchaseForm error={error} isSubmitting={isSubmitting} onCancel={() => navigate('/purchases')} onSubmit={handleSubmit} />
}

export default PurchaseCreatePage

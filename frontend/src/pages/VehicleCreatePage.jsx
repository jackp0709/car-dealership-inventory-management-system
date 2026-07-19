import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { apiClient } from '../api/client'
import VehicleForm from '../components/VehicleForm'

function VehicleCreatePage() {
  const navigate = useNavigate()
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (payload) => {
    setError('')
    setIsSubmitting(true)

    try {
      await apiClient.post('/vehicles', payload)
      navigate('/vehicles', { state: { successMessage: 'Vehicle added successfully.' } })
    } catch (requestError) {
      const detail = requestError.response?.data?.detail
      setError(
        requestError.response?.status === 401
          ? 'Your authentication has expired. Please sign in again.'
          : Array.isArray(detail)
            ? detail.map((item) => item.msg).join(' ')
            : detail ?? 'Unable to add the vehicle. Please try again.',
      )
    } finally {
      setIsSubmitting(false)
    }
  }

  return <VehicleForm error={error} isSubmitting={isSubmitting} onCancel={() => navigate('/vehicles')} onSubmit={handleSubmit} />
}

export default VehicleCreatePage

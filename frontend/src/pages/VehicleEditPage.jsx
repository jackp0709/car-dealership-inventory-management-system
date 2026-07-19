import { Alert, Box, CircularProgress } from '@mui/material'
import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

import { apiClient } from '../api/client'
import VehicleForm from '../components/VehicleForm'

function VehicleEditPage() {
  const navigate = useNavigate()
  const { vehicleId } = useParams()
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [vehicle, setVehicle] = useState(null)

  useEffect(() => {
    const loadVehicle = async () => {
      try {
        const response = await apiClient.get(`/vehicles/${vehicleId}`)
        setVehicle(response.data)
      } catch (requestError) {
        const detail = requestError.response?.data?.detail
        setError(
          requestError.response?.status === 401
            ? 'Your authentication has expired. Please sign in again.'
            : detail ?? 'Unable to load this vehicle. Please return to the vehicle list.',
        )
      } finally {
        setIsLoading(false)
      }
    }

    loadVehicle()
  }, [vehicleId])

  const handleSubmit = async ({ vin, ...payload }) => {
    setError('')
    setIsSubmitting(true)

    try {
      await apiClient.put(`/vehicles/${vehicleId}`, payload)
      navigate('/vehicles', { state: { successMessage: 'Vehicle updated successfully.' } })
    } catch (requestError) {
      const detail = requestError.response?.data?.detail
      setError(
        requestError.response?.status === 401
          ? 'Your authentication has expired. Please sign in again.'
          : Array.isArray(detail)
            ? detail.map((item) => item.msg).join(' ')
            : detail ?? 'Unable to update the vehicle. Please try again.',
      )
    } finally {
      setIsSubmitting(false)
    }
  }

  if (isLoading) {
    return <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}><CircularProgress /></Box>
  }

  if (!vehicle) {
    return <Alert severity="error">{error}</Alert>
  }

  return <VehicleForm error={error} initialVehicle={vehicle} isEditing isSubmitting={isSubmitting} onCancel={() => navigate('/vehicles')} onSubmit={handleSubmit} />
}

export default VehicleEditPage

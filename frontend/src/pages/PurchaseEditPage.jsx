import { Alert, Box, CircularProgress } from '@mui/material'
import { useEffect, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

import { apiClient } from '../api/client'
import PurchaseForm from '../components/PurchaseForm'

function PurchaseEditPage() {
  const navigate = useNavigate()
  const { purchaseId } = useParams()
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [purchase, setPurchase] = useState(null)
  const hasLoadedPurchase = useRef(false)

  useEffect(() => {
    if (hasLoadedPurchase.current) return
    hasLoadedPurchase.current = true
    const loadPurchase = async () => {
      try {
        const response = await apiClient.get(`/purchases/${purchaseId}`)
        setPurchase(response.data)
      } catch (requestError) {
        const detail = requestError.response?.data?.detail
        setError(requestError.response?.status === 401 ? 'Your authentication has expired. Please sign in again.' : detail ?? 'Unable to load this purchase. Please return to the purchase list.')
      } finally {
        setIsLoading(false)
      }
    }
    loadPurchase()
  }, [purchaseId])

  const handleSubmit = async ({ vehicle_id, ...payload }) => {
    setError('')
    setIsSubmitting(true)
    try {
      await apiClient.put(`/purchases/${purchaseId}`, payload)
      navigate('/purchases', { state: { successMessage: 'Purchase updated successfully.' } })
    } catch (requestError) {
      const detail = requestError.response?.data?.detail
      setError(requestError.response?.status === 401 ? 'Your authentication has expired. Please sign in again.' : Array.isArray(detail) ? detail.map((item) => item.msg).join(' ') : detail ?? 'Unable to update the purchase. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  if (isLoading) return <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}><CircularProgress /></Box>
  if (!purchase) return <Alert severity="error">{error}</Alert>

  return <PurchaseForm error={error} initialPurchase={purchase} isEditing isSubmitting={isSubmitting} onCancel={() => navigate('/purchases')} onSubmit={handleSubmit} />
}

export default PurchaseEditPage

import { Alert, Box, CircularProgress } from '@mui/material'
import { useEffect, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

import { apiClient } from '../api/client'
import SaleForm from '../components/SaleForm'

function SaleEditPage() {
  const navigate = useNavigate()
  const { saleId } = useParams()
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [sale, setSale] = useState(null)
  const hasLoadedSale = useRef(false)

  useEffect(() => {
    if (hasLoadedSale.current) return
    hasLoadedSale.current = true
    const loadSale = async () => {
      try {
        const response = await apiClient.get(`/sales/${saleId}`)
        setSale(response.data)
      } catch (requestError) {
        const detail = requestError.response?.data?.detail
        setError(requestError.response?.status === 401 ? 'Your authentication has expired. Please sign in again.' : detail ?? 'Unable to load this sale. Please return to the sales list.')
      } finally {
        setIsLoading(false)
      }
    }
    loadSale()
  }, [saleId])

  const handleSubmit = async (payload) => {
    setError('')
    setIsSubmitting(true)
    try {
      await apiClient.put(`/sales/${saleId}`, payload)
      navigate('/sales', { state: { successMessage: 'Sale updated successfully.' } })
    } catch (requestError) {
      const detail = requestError.response?.data?.detail
      setError(requestError.response?.status === 401 ? 'Your authentication has expired. Please sign in again.' : Array.isArray(detail) ? detail.map((item) => item.msg).join(' ') : detail ?? 'Unable to update the sale. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  if (isLoading) return <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}><CircularProgress /></Box>
  if (!sale) return <Alert severity="error">{error}</Alert>

  return <SaleForm error={error} initialSale={sale} isEditing isSubmitting={isSubmitting} onCancel={() => navigate('/sales')} onSubmit={handleSubmit} />
}

export default SaleEditPage

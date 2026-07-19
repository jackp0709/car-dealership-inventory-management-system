import { Alert, Box, Button, CircularProgress, Divider, Paper, Stack, Typography } from '@mui/material'
import { useEffect, useRef, useState } from 'react'
import { Link as RouterLink, useParams } from 'react-router-dom'

import { apiClient } from '../api/client'

const fields = [
  ['id', 'Purchase ID'], ['vehicle_id', 'Vehicle ID'], ['supplier_name', 'Supplier Name'],
  ['purchase_price', 'Purchase Price'], ['purchase_date', 'Purchase Date'], ['invoice_number', 'Invoice Number'],
  ['payment_status', 'Payment Status'], ['notes', 'Notes'], ['created_at', 'Created'], ['updated_at', 'Updated'],
]

function formatValue(purchase, field) {
  if (field === 'purchase_price') return Number(purchase[field]).toLocaleString(undefined, { style: 'currency', currency: 'USD' })
  if (field.endsWith('_at') || field === 'purchase_date') return new Date(purchase[field]).toLocaleString()
  return purchase[field] || '—'
}

function PurchaseDetailsPage() {
  const { purchaseId } = useParams()
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)
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

  if (isLoading) return <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}><CircularProgress /></Box>
  if (!purchase) return <Alert severity="error">{error}</Alert>

  return (
    <Paper elevation={1} sx={{ p: { xs: 2, md: 3 } }}>
      <Stack alignItems={{ sm: 'center' }} direction={{ xs: 'column', sm: 'row' }} justifyContent="space-between" spacing={2} sx={{ mb: 3 }}>
        <Box><Typography component="h1" variant="h4">Purchase Details</Typography><Typography color="text.secondary">Vehicle acquisition record #{purchase.id}</Typography></Box>
        <Stack direction="row" spacing={1}><Button component={RouterLink} to={`/purchases/${purchase.id}/edit`}>Edit</Button><Button component={RouterLink} to="/purchases" variant="outlined">Back to Purchases</Button></Stack>
      </Stack>
      <Stack divider={<Divider flexItem />} spacing={0}>
        {fields.map(([field, label]) => <Stack direction={{ xs: 'column', sm: 'row' }} key={field} spacing={1} sx={{ py: 1.5 }}><Typography sx={{ minWidth: 180 }} variant="subtitle2">{label}</Typography><Typography sx={{ whiteSpace: 'pre-wrap' }}>{formatValue(purchase, field)}</Typography></Stack>)}
      </Stack>
    </Paper>
  )
}

export default PurchaseDetailsPage

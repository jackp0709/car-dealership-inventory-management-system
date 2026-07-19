import { Alert, Box, Button, CircularProgress, Divider, Paper, Stack, Typography } from '@mui/material'
import { useEffect, useRef, useState } from 'react'
import { Link as RouterLink, useParams } from 'react-router-dom'

import { apiClient } from '../api/client'

const fields = [
  ['id', 'Sale ID'], ['vehicle_id', 'Vehicle ID'], ['seller_id', 'Seller ID'], ['customer_name', 'Customer Name'],
  ['customer_email', 'Customer Email'], ['customer_phone', 'Customer Phone'], ['sale_price', 'Sale Price'],
  ['sale_date', 'Sale Date'], ['created_at', 'Created'], ['updated_at', 'Updated'],
]

function formatValue(sale, field) {
  if (field === 'sale_price') return Number(sale[field]).toLocaleString(undefined, { style: 'currency', currency: 'USD' })
  if (field.endsWith('_at') || field === 'sale_date') return new Date(sale[field]).toLocaleString()
  return sale[field] || '—'
}

function SaleDetailsPage() {
  const { saleId } = useParams()
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)
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

  if (isLoading) return <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}><CircularProgress /></Box>
  if (!sale) return <Alert severity="error">{error}</Alert>

  return (
    <Paper elevation={1} sx={{ p: { xs: 2, md: 3 } }}>
      <Stack alignItems={{ sm: 'center' }} direction={{ xs: 'column', sm: 'row' }} justifyContent="space-between" spacing={2} sx={{ mb: 3 }}>
        <Box><Typography component="h1" variant="h4">Sale Details</Typography><Typography color="text.secondary">Completed sale record #{sale.id}</Typography></Box>
        <Stack direction="row" spacing={1}><Button component={RouterLink} to={`/sales/${sale.id}/edit`}>Edit</Button><Button component={RouterLink} to="/sales" variant="outlined">Back to Sales</Button></Stack>
      </Stack>
      <Stack divider={<Divider flexItem />} spacing={0}>{fields.map(([field, label]) => <Stack direction={{ xs: 'column', sm: 'row' }} key={field} spacing={1} sx={{ py: 1.5 }}><Typography sx={{ minWidth: 180 }} variant="subtitle2">{label}</Typography><Typography>{formatValue(sale, field)}</Typography></Stack>)}</Stack>
    </Paper>
  )
}

export default SaleDetailsPage

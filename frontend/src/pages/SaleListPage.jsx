import { Alert, Box, Button, CircularProgress, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Paper, Snackbar, Stack, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material'
import { useEffect, useRef, useState } from 'react'
import { Link as RouterLink, useLocation } from 'react-router-dom'

import { apiClient } from '../api/client'

const columns = [
  ['id', 'ID'], ['customer_name', 'Customer'], ['customer_email', 'Email'], ['customer_phone', 'Phone'],
  ['vehicle_id', 'Vehicle ID'], ['sale_price', 'Sale Price'], ['sale_date', 'Sale Date'], ['seller_id', 'Seller ID'],
]

function formatValue(sale, field) {
  if (field === 'sale_price') return Number(sale[field]).toLocaleString(undefined, { style: 'currency', currency: 'USD' })
  if (field === 'sale_date') return new Date(sale[field]).toLocaleString()
  return sale[field] || '—'
}

function SaleListPage() {
  const location = useLocation()
  const [error, setError] = useState('')
  const [isDeleting, setIsDeleting] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [sales, setSales] = useState([])
  const [selectedSale, setSelectedSale] = useState(null)
  const [successMessage, setSuccessMessage] = useState(location.state?.successMessage ?? '')
  const hasLoadedSales = useRef(false)

  const loadSales = async () => {
    setError('')
    setIsLoading(true)
    try {
      const response = await apiClient.get('/sales')
      setSales(response.data)
    } catch (requestError) {
      setError(requestError.response?.status === 401 ? 'Your authentication has expired. Please sign in again.' : 'Unable to load sales. Please check your connection and try again.')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    if (hasLoadedSales.current) return
    hasLoadedSales.current = true
    loadSales()
  }, [])

  const handleDelete = async () => {
    if (!selectedSale) return
    setIsDeleting(true)
    setError('')
    try {
      await apiClient.delete(`/sales/${selectedSale.id}`)
      setSales((currentSales) => currentSales.filter((sale) => sale.id !== selectedSale.id))
      setSelectedSale(null)
      setSuccessMessage('Sale deleted successfully.')
    } catch (requestError) {
      const detail = requestError.response?.data?.detail
      setError(requestError.response?.status === 401 ? 'Your authentication has expired. Please sign in again.' : detail ?? 'Unable to delete the sale. Please try again.')
      setSelectedSale(null)
    } finally {
      setIsDeleting(false)
    }
  }

  if (isLoading) return <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}><CircularProgress /></Box>

  return (
    <Stack spacing={3}>
      <Stack alignItems={{ sm: 'center' }} direction={{ xs: 'column', sm: 'row' }} justifyContent="space-between" spacing={2}>
        <Box><Typography component="h1" variant="h4">Sales Management</Typography><Typography color="text.secondary">Track completed vehicle sales and customer records.</Typography></Box>
        <Button component={RouterLink} to="/sales/new" variant="contained">Record Sale</Button>
      </Stack>
      {error && <Alert action={<Button color="inherit" onClick={loadSales}>Retry</Button>} severity="error">{error}</Alert>}
      {sales.length === 0 ? (
        <Paper sx={{ p: 5, textAlign: 'center' }}>
          <Typography gutterBottom variant="h6">No sales records</Typography>
          <Typography color="text.secondary" sx={{ mb: 3 }}>Record a completed vehicle sale to begin tracking sales.</Typography>
          <Button component={RouterLink} to="/sales/new" variant="contained">Record Sale</Button>
        </Paper>
      ) : (
        <TableContainer component={Paper}>
          <Table aria-label="Sales records" size="small" sx={{ minWidth: 1100 }}>
            <TableHead><TableRow>{columns.map(([, label]) => <TableCell key={label}>{label}</TableCell>)}<TableCell>Actions</TableCell></TableRow></TableHead>
            <TableBody>{sales.map((sale) => <TableRow key={sale.id}>
              {columns.map(([field]) => <TableCell key={field}>{formatValue(sale, field)}</TableCell>)}
              <TableCell><Stack direction="row" spacing={1}>
                <Button component={RouterLink} size="small" to={`/sales/${sale.id}`}>Details</Button>
                <Button component={RouterLink} size="small" to={`/sales/${sale.id}/edit`}>Edit</Button>
                <Button color="error" onClick={() => setSelectedSale(sale)} size="small">Delete</Button>
              </Stack></TableCell>
            </TableRow>)}</TableBody>
          </Table>
        </TableContainer>
      )}
      <Dialog onClose={() => !isDeleting && setSelectedSale(null)} open={Boolean(selectedSale)}>
        <DialogTitle>Delete Sale?</DialogTitle>
        <DialogContent><DialogContentText>Permanently delete the sale for {selectedSale?.customer_name}? The vehicle will return to available inventory.</DialogContentText></DialogContent>
        <DialogActions><Button disabled={isDeleting} onClick={() => setSelectedSale(null)}>Cancel</Button><Button color="error" disabled={isDeleting} onClick={handleDelete} variant="contained">{isDeleting ? 'Deleting…' : 'Delete Sale'}</Button></DialogActions>
      </Dialog>
      <Snackbar autoHideDuration={4000} onClose={() => setSuccessMessage('')} open={Boolean(successMessage)}><Alert onClose={() => setSuccessMessage('')} severity="success" variant="filled">{successMessage}</Alert></Snackbar>
    </Stack>
  )
}

export default SaleListPage

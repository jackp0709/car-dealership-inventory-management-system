import {
  Alert, Box, Button, Chip, CircularProgress, Dialog, DialogActions, DialogContent,
  DialogContentText, DialogTitle, Paper, Snackbar, Stack, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, Typography,
} from '@mui/material'
import { useEffect, useRef, useState } from 'react'
import { Link as RouterLink, useLocation } from 'react-router-dom'

import { apiClient } from '../api/client'

const columns = [
  ['id', 'ID'], ['vehicle_id', 'Vehicle ID'], ['supplier_name', 'Supplier'],
  ['purchase_price', 'Purchase Price'], ['purchase_date', 'Purchase Date'],
  ['invoice_number', 'Invoice Number'], ['payment_status', 'Payment Status'],
  ['notes', 'Notes'], ['created_at', 'Created'], ['updated_at', 'Updated'],
]

function formatValue(purchase, field) {
  if (field === 'purchase_price') {
    return Number(purchase[field]).toLocaleString(undefined, { style: 'currency', currency: 'USD' })
  }
  if (field.endsWith('_at') || field === 'purchase_date') return new Date(purchase[field]).toLocaleString()
  return purchase[field] || '—'
}

function PurchaseListPage() {
  const location = useLocation()
  const [error, setError] = useState('')
  const [isDeleting, setIsDeleting] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [purchases, setPurchases] = useState([])
  const [selectedPurchase, setSelectedPurchase] = useState(null)
  const [successMessage, setSuccessMessage] = useState(location.state?.successMessage ?? '')
  const hasLoadedPurchases = useRef(false)

  const loadPurchases = async () => {
    setError('')
    setIsLoading(true)
    try {
      const response = await apiClient.get('/purchases')
      setPurchases(response.data)
    } catch (requestError) {
      setError(
        requestError.response?.status === 401
          ? 'Your authentication has expired. Please sign in again.'
          : 'Unable to load purchases. Please check your connection and try again.',
      )
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    if (hasLoadedPurchases.current) return
    hasLoadedPurchases.current = true
    loadPurchases()
  }, [])

  const handleDelete = async () => {
    if (!selectedPurchase) return
    setIsDeleting(true)
    setError('')
    try {
      await apiClient.delete(`/purchases/${selectedPurchase.id}`)
      setPurchases((currentPurchases) => currentPurchases.filter((purchase) => purchase.id !== selectedPurchase.id))
      setSelectedPurchase(null)
      setSuccessMessage('Purchase deleted successfully.')
    } catch (requestError) {
      const detail = requestError.response?.data?.detail
      setError(
        requestError.response?.status === 401
          ? 'Your authentication has expired. Please sign in again.'
          : detail ?? 'Unable to delete the purchase. Please try again.',
      )
      setSelectedPurchase(null)
    } finally {
      setIsDeleting(false)
    }
  }

  if (isLoading) return <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}><CircularProgress /></Box>

  return (
    <Stack spacing={3}>
      <Stack alignItems={{ sm: 'center' }} direction={{ xs: 'column', sm: 'row' }} justifyContent="space-between" spacing={2}>
        <Box>
          <Typography component="h1" variant="h4">Purchase Management</Typography>
          <Typography color="text.secondary">Track vehicle acquisitions and supplier records.</Typography>
        </Box>
        <Button component={RouterLink} to="/purchases/new" variant="contained">Record Purchase</Button>
      </Stack>
      {error && <Alert action={<Button color="inherit" onClick={loadPurchases}>Retry</Button>} severity="error">{error}</Alert>}
      {purchases.length === 0 ? (
        <Paper sx={{ p: 5, textAlign: 'center' }}>
          <Typography gutterBottom variant="h6">No purchase records</Typography>
          <Typography color="text.secondary" sx={{ mb: 3 }}>Record a vehicle acquisition to begin tracking purchases.</Typography>
          <Button component={RouterLink} to="/purchases/new" variant="contained">Record Purchase</Button>
        </Paper>
      ) : (
        <TableContainer component={Paper}>
          <Table aria-label="Purchase records" size="small" sx={{ minWidth: 1600 }}>
            <TableHead><TableRow>{columns.map(([, label]) => <TableCell key={label}>{label}</TableCell>)}<TableCell>Actions</TableCell></TableRow></TableHead>
            <TableBody>
              {purchases.map((purchase) => (
                <TableRow key={purchase.id}>
                  {columns.map(([field]) => <TableCell key={field}>{field === 'payment_status' ? <Chip color={purchase.payment_status === 'PAID' ? 'success' : 'warning'} label={purchase.payment_status} size="small" /> : formatValue(purchase, field)}</TableCell>)}
                  <TableCell><Stack direction="row" spacing={1}>
                    <Button component={RouterLink} size="small" to={`/purchases/${purchase.id}`}>Details</Button>
                    <Button component={RouterLink} size="small" to={`/purchases/${purchase.id}/edit`}>Edit</Button>
                    <Button color="error" onClick={() => setSelectedPurchase(purchase)} size="small">Delete</Button>
                  </Stack></TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      <Dialog onClose={() => !isDeleting && setSelectedPurchase(null)} open={Boolean(selectedPurchase)}>
        <DialogTitle>Delete Purchase?</DialogTitle>
        <DialogContent><DialogContentText>Permanently delete purchase invoice {selectedPurchase?.invoice_number}? This action cannot be undone.</DialogContentText></DialogContent>
        <DialogActions><Button disabled={isDeleting} onClick={() => setSelectedPurchase(null)}>Cancel</Button><Button color="error" disabled={isDeleting} onClick={handleDelete} variant="contained">{isDeleting ? 'Deleting…' : 'Delete Purchase'}</Button></DialogActions>
      </Dialog>
      <Snackbar autoHideDuration={4000} onClose={() => setSuccessMessage('')} open={Boolean(successMessage)}><Alert onClose={() => setSuccessMessage('')} severity="success" variant="filled">{successMessage}</Alert></Snackbar>
    </Stack>
  )
}

export default PurchaseListPage

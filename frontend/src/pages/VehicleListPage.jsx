import {
  Alert,
  Box,
  Button,
  Chip,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Paper,
  Snackbar,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from '@mui/material'
import { useEffect, useRef, useState } from 'react'
import { Link as RouterLink, useLocation } from 'react-router-dom'

import { apiClient } from '../api/client'

const columns = [
  ['manufacturer', 'Manufacturer'], ['model', 'Model'], ['vin', 'VIN'], ['year', 'Year'],
  ['purchase_price', 'Purchase Price'], ['selling_price', 'Selling Price'], ['color', 'Color'],
  ['mileage', 'Mileage'], ['fuel_type', 'Fuel Type'], ['transmission', 'Transmission'],
  ['condition', 'Condition'], ['description', 'Description'], ['status', 'Status'],
  ['created_at', 'Created'], ['updated_at', 'Updated'],
]

function formatValue(vehicle, field) {
  if (field === 'purchase_price' || field === 'selling_price') {
    return Number(vehicle[field]).toLocaleString(undefined, { style: 'currency', currency: 'USD' })
  }
  if (field === 'created_at' || field === 'updated_at') {
    return new Date(vehicle[field]).toLocaleString()
  }
  return vehicle[field] || '—'
}

function VehicleListPage() {
  const location = useLocation()
  const [vehicles, setVehicles] = useState([])
  const [error, setError] = useState('')
  const [isDeleting, setIsDeleting] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const hasLoadedVehicles = useRef(false)
  const [selectedVehicle, setSelectedVehicle] = useState(null)
  const [successMessage, setSuccessMessage] = useState(location.state?.successMessage ?? '')

  const loadVehicles = async () => {
    setError('')
    setIsLoading(true)

    try {
      const response = await apiClient.get('/vehicles')
      setVehicles(response.data)
    } catch (requestError) {
      setError(
        requestError.response?.status === 401
          ? 'Your authentication has expired. Please sign in again.'
          : 'Unable to load vehicles. Please check your connection and try again.',
      )
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    if (hasLoadedVehicles.current) return
    hasLoadedVehicles.current = true
    loadVehicles()
  }, [])

  const handleDelete = async () => {
    if (!selectedVehicle) return

    setIsDeleting(true)
    setError('')

    try {
      await apiClient.delete(`/vehicles/${selectedVehicle.id}`)
      setVehicles((currentVehicles) => currentVehicles.filter((vehicle) => vehicle.id !== selectedVehicle.id))
      setSelectedVehicle(null)
      setSuccessMessage('Vehicle deleted successfully.')
    } catch (requestError) {
      const detail = requestError.response?.data?.detail
      setError(
        requestError.response?.status === 401
          ? 'Your authentication has expired. Please sign in again.'
          : detail ?? 'Unable to delete the vehicle. Please try again.',
      )
      setSelectedVehicle(null)
    } finally {
      setIsDeleting(false)
    }
  }

  if (isLoading) {
    return <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}><CircularProgress /></Box>
  }

  return (
    <Stack spacing={3}>
      <Stack alignItems={{ sm: 'center' }} direction={{ xs: 'column', sm: 'row' }} justifyContent="space-between" spacing={2}>
        <Box>
          <Typography component="h1" variant="h4">Vehicle Management</Typography>
          <Typography color="text.secondary">Manage the dealership inventory.</Typography>
        </Box>
        <Button component={RouterLink} to="/vehicles/new" variant="contained">Add Vehicle</Button>
      </Stack>

      {error && <Alert action={<Button color="inherit" onClick={loadVehicles}>Retry</Button>} severity="error">{error}</Alert>}

      {vehicles.length === 0 ? (
        <Paper sx={{ p: 5, textAlign: 'center' }}>
          <Typography gutterBottom variant="h6">No vehicles in inventory</Typography>
          <Typography color="text.secondary" sx={{ mb: 3 }}>Add the first vehicle to begin managing inventory.</Typography>
          <Button component={RouterLink} to="/vehicles/new" variant="contained">Add Vehicle</Button>
        </Paper>
      ) : (
        <TableContainer component={Paper}>
          <Table aria-label="Vehicle inventory" size="small" sx={{ minWidth: 1800 }}>
            <TableHead>
              <TableRow>
                {columns.map(([, label]) => <TableCell key={label}>{label}</TableCell>)}
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {vehicles.map((vehicle) => (
                <TableRow key={vehicle.id}>
                  {columns.map(([field]) => (
                    <TableCell key={field}>
                      {field === 'status'
                        ? <Chip color={vehicle.status === 'AVAILABLE' ? 'success' : 'default'} label={vehicle.status} size="small" />
                        : formatValue(vehicle, field)}
                    </TableCell>
                  ))}
                  <TableCell>
                    <Stack direction="row" spacing={1}>
                      <Button component={RouterLink} size="small" to={`/vehicles/${vehicle.id}/edit`}>Edit</Button>
                      <Button color="error" onClick={() => setSelectedVehicle(vehicle)} size="small">Delete</Button>
                    </Stack>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      <Dialog onClose={() => !isDeleting && setSelectedVehicle(null)} open={Boolean(selectedVehicle)}>
        <DialogTitle>Delete Vehicle?</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Permanently delete {selectedVehicle?.manufacturer} {selectedVehicle?.model}? This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button disabled={isDeleting} onClick={() => setSelectedVehicle(null)}>Cancel</Button>
          <Button color="error" disabled={isDeleting} onClick={handleDelete} variant="contained">
            {isDeleting ? 'Deleting…' : 'Delete Vehicle'}
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar autoHideDuration={4000} onClose={() => setSuccessMessage('')} open={Boolean(successMessage)}>
        <Alert onClose={() => setSuccessMessage('')} severity="success" variant="filled">{successMessage}</Alert>
      </Snackbar>
    </Stack>
  )
}

export default VehicleListPage

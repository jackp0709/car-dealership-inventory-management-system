import { Alert, Box, Button, CircularProgress, Grid, MenuItem, Paper, TextField, Typography } from '@mui/material'
import { useEffect, useRef, useState } from 'react'

import { apiClient } from '../api/client'

const paymentStatuses = ['PENDING', 'PAID']

function toLocalDateTime(value) {
  if (!value) return ''

  const date = new Date(value)
  const offset = date.getTimezoneOffset() * 60_000
  return new Date(date.getTime() - offset).toISOString().slice(0, 16)
}

function PurchaseForm({ error, initialPurchase, isEditing, isSubmitting, onCancel, onSubmit }) {
  const [isLoadingVehicles, setIsLoadingVehicles] = useState(!isEditing)
  const [vehicleError, setVehicleError] = useState('')
  const [vehicles, setVehicles] = useState([])
  const hasLoadedVehicles = useRef(false)
  const fields = isEditing
    ? initialPurchase
    : {
        vehicle_id: '',
        supplier_name: '',
        purchase_price: '',
        purchase_date: toLocalDateTime(new Date()),
        invoice_number: '',
        payment_status: 'PENDING',
        notes: '',
      }

  useEffect(() => {
    if (isEditing || hasLoadedVehicles.current) return
    hasLoadedVehicles.current = true

    const loadVehicles = async () => {
      try {
        const response = await apiClient.get('/vehicles')
        setVehicles(response.data)
      } catch (requestError) {
        setVehicleError(
          requestError.response?.status === 401
            ? 'Your authentication has expired. Please sign in again.'
            : 'Unable to load vehicles. Please return to the purchase list and try again.',
        )
      } finally {
        setIsLoadingVehicles(false)
      }
    }

    loadVehicles()
  }, [isEditing])

  const handleSubmit = (event) => {
    event.preventDefault()
    const formData = new FormData(event.currentTarget)
    const payload = Object.fromEntries(formData.entries())

    if (isEditing) {
      onSubmit(payload)
      return
    }

    onSubmit({
      ...payload,
      vehicle_id: Number(payload.vehicle_id),
      purchase_date: new Date(payload.purchase_date).toISOString(),
    })
  }

  if (isLoadingVehicles) {
    return <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}><CircularProgress /></Box>
  }

  return (
    <Paper component="form" elevation={1} onSubmit={handleSubmit} sx={{ p: { xs: 2, md: 3 } }}>
      <Typography component="h1" gutterBottom variant="h4">
        {isEditing ? 'Edit Purchase' : 'Record Purchase'}
      </Typography>
      <Typography color="text.secondary" sx={{ mb: 3 }}>
        {isEditing
          ? 'Update the supported vehicle acquisition details.'
          : 'Record the dealership acquisition of an inventory vehicle.'}
      </Typography>
      {(error || vehicleError) && <Alert severity="error" sx={{ mb: 2 }}>{error || vehicleError}</Alert>}
      <Grid container spacing={2}>
        <Grid size={{ xs: 12, sm: 6 }}>
          {isEditing ? (
            <TextField defaultValue={fields.vehicle_id} disabled fullWidth label="Vehicle ID" name="vehicle_id" />
          ) : (
            <TextField defaultValue={fields.vehicle_id} fullWidth label="Vehicle" name="vehicle_id" required select>
              {vehicles.map((vehicle) => (
                <MenuItem key={vehicle.id} value={vehicle.id}>
                  #{vehicle.id} — {vehicle.manufacturer} {vehicle.model} ({vehicle.vin})
                </MenuItem>
              ))}
            </TextField>
          )}
        </Grid>
        <Grid size={{ xs: 12, sm: 6 }}>
          <TextField defaultValue={fields.supplier_name} fullWidth label="Supplier Name" name="supplier_name" required />
        </Grid>
        {!isEditing && (
          <>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField defaultValue={fields.purchase_price} fullWidth inputProps={{ min: '0.01', step: '0.01' }} label="Purchase Price" name="purchase_price" required type="number" />
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField defaultValue={fields.purchase_date} fullWidth inputProps={{ max: toLocalDateTime(new Date()) }} label="Purchase Date" name="purchase_date" required type="datetime-local" />
            </Grid>
          </>
        )}
        <Grid size={{ xs: 12, sm: 6 }}>
          <TextField defaultValue={fields.invoice_number} fullWidth label="Invoice Number" name="invoice_number" required />
        </Grid>
        <Grid size={{ xs: 12, sm: 6 }}>
          <TextField defaultValue={fields.payment_status} fullWidth label="Payment Status" name="payment_status" select>
            {paymentStatuses.map((paymentStatus) => <MenuItem key={paymentStatus} value={paymentStatus}>{paymentStatus}</MenuItem>)}
          </TextField>
        </Grid>
        <Grid size={12}>
          <TextField defaultValue={fields.notes ?? ''} fullWidth label="Notes" minRows={3} multiline name="notes" />
        </Grid>
      </Grid>
      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end', mt: 3 }}>
        <Button disabled={isSubmitting} onClick={onCancel} variant="outlined">Cancel</Button>
        <Button disabled={isSubmitting || Boolean(vehicleError)} type="submit" variant="contained">
          {isSubmitting ? 'Saving…' : isEditing ? 'Update Purchase' : 'Record Purchase'}
        </Button>
      </Box>
    </Paper>
  )
}

export default PurchaseForm

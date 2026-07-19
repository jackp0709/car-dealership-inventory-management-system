import { Alert, Box, Button, CircularProgress, Grid, MenuItem, Paper, TextField, Typography } from '@mui/material'
import { useEffect, useRef, useState } from 'react'

import { apiClient } from '../api/client'

function toLocalDateTime(value) {
  if (!value) return ''

  const date = new Date(value)
  const offset = date.getTimezoneOffset() * 60_000
  return new Date(date.getTime() - offset).toISOString().slice(0, 16)
}

function SaleForm({ error, initialSale, isEditing, isSubmitting, onCancel, onSubmit }) {
  const [isLoadingOptions, setIsLoadingOptions] = useState(!isEditing)
  const [optionsError, setOptionsError] = useState('')
  const [sellers, setSellers] = useState([])
  const [vehicles, setVehicles] = useState([])
  const hasLoadedOptions = useRef(false)
  const fields = isEditing
    ? initialSale
    : {
        vehicle_id: '', seller_id: '', customer_name: '', customer_email: '', customer_phone: '',
        sale_price: '', sale_date: toLocalDateTime(new Date()),
      }

  useEffect(() => {
    if (isEditing || hasLoadedOptions.current) return
    hasLoadedOptions.current = true

    const loadOptions = async () => {
      try {
        const [vehiclesResponse, usersResponse] = await Promise.all([
          apiClient.get('/vehicles'),
          apiClient.get('/users'),
        ])
        setVehicles(vehiclesResponse.data.filter((vehicle) => vehicle.status === 'AVAILABLE'))
        setSellers(usersResponse.data)
      } catch (requestError) {
        setOptionsError(
          requestError.response?.status === 401
            ? 'Your authentication has expired. Please sign in again.'
            : 'Unable to load sale options. Please return to the sales list and try again.',
        )
      } finally {
        setIsLoadingOptions(false)
      }
    }

    loadOptions()
  }, [isEditing])

  const handleSubmit = (event) => {
    event.preventDefault()
    const payload = Object.fromEntries(new FormData(event.currentTarget).entries())

    if (isEditing) {
      onSubmit(payload)
      return
    }

    onSubmit({
      ...payload,
      vehicle_id: Number(payload.vehicle_id),
      seller_id: Number(payload.seller_id),
      sale_date: new Date(payload.sale_date).toISOString(),
    })
  }

  if (isLoadingOptions) return <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}><CircularProgress /></Box>

  return (
    <Paper component="form" elevation={1} onSubmit={handleSubmit} sx={{ p: { xs: 2, md: 3 } }}>
      <Typography component="h1" gutterBottom variant="h4">{isEditing ? 'Edit Sale' : 'Record Sale'}</Typography>
      <Typography color="text.secondary" sx={{ mb: 3 }}>
        {isEditing ? 'Update the supported customer details for this sale.' : 'Record a completed vehicle sale.'}
      </Typography>
      {(error || optionsError) && <Alert severity="error" sx={{ mb: 2 }}>{error || optionsError}</Alert>}
      <Grid container spacing={2}>
        {isEditing ? (
          <>
            <Grid size={{ xs: 12, sm: 6 }}><TextField defaultValue={fields.vehicle_id} disabled fullWidth label="Vehicle ID" /></Grid>
            <Grid size={{ xs: 12, sm: 6 }}><TextField defaultValue={fields.seller_id} disabled fullWidth label="Seller ID" /></Grid>
          </>
        ) : (
          <>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField defaultValue={fields.vehicle_id} fullWidth label="Vehicle" name="vehicle_id" required select>
                {vehicles.map((vehicle) => <MenuItem key={vehicle.id} value={vehicle.id}>#{vehicle.id} — {vehicle.manufacturer} {vehicle.model} ({vehicle.vin})</MenuItem>)}
              </TextField>
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField defaultValue={fields.seller_id} fullWidth label="Seller" name="seller_id" required select>
                {sellers.map((seller) => <MenuItem key={seller.id} value={seller.id}>{seller.full_name} ({seller.email})</MenuItem>)}
              </TextField>
            </Grid>
          </>
        )}
        <Grid size={{ xs: 12, sm: 6 }}><TextField defaultValue={fields.customer_name} fullWidth label="Customer Name" name="customer_name" required /></Grid>
        <Grid size={{ xs: 12, sm: 6 }}><TextField defaultValue={fields.customer_email} fullWidth label="Customer Email" name="customer_email" required type="email" /></Grid>
        <Grid size={{ xs: 12, sm: 6 }}><TextField defaultValue={fields.customer_phone} fullWidth label="Customer Phone" name="customer_phone" required /></Grid>
        {!isEditing && <>
          <Grid size={{ xs: 12, sm: 6 }}><TextField defaultValue={fields.sale_price} fullWidth inputProps={{ min: '0.01', step: '0.01' }} label="Sale Price" name="sale_price" required type="number" /></Grid>
          <Grid size={{ xs: 12, sm: 6 }}><TextField defaultValue={fields.sale_date} fullWidth inputProps={{ max: toLocalDateTime(new Date()) }} label="Sale Date" name="sale_date" required type="datetime-local" /></Grid>
        </>}
      </Grid>
      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end', mt: 3 }}>
        <Button disabled={isSubmitting} onClick={onCancel} variant="outlined">Cancel</Button>
        <Button disabled={isSubmitting || Boolean(optionsError)} type="submit" variant="contained">{isSubmitting ? 'Saving…' : isEditing ? 'Update Sale' : 'Record Sale'}</Button>
      </Box>
    </Paper>
  )
}

export default SaleForm

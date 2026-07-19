import { Box, Button, Grid, MenuItem, Paper, TextField, Typography } from '@mui/material'

const fuelTypes = ['PETROL', 'DIESEL', 'CNG', 'ELECTRIC', 'HYBRID']
const transmissions = ['MANUAL', 'AUTOMATIC']
const conditions = ['NEW', 'USED']

function VehicleForm({ error, initialVehicle, isEditing, isSubmitting, onCancel, onSubmit }) {
  const fields = isEditing
    ? initialVehicle
    : {
        manufacturer: '',
        model: '',
        vin: '',
        year: '',
        purchase_price: '',
        selling_price: '',
        color: '',
        mileage: '',
        fuel_type: 'PETROL',
        transmission: 'MANUAL',
        condition: 'NEW',
        description: '',
      }

  const handleSubmit = (event) => {
    event.preventDefault()
    const formData = new FormData(event.currentTarget)
    const payload = Object.fromEntries(formData.entries())

    onSubmit({
      ...payload,
      year: Number(payload.year),
      mileage: Number(payload.mileage),
    })
  }

  return (
    <Paper component="form" elevation={1} onSubmit={handleSubmit} sx={{ p: { xs: 2, md: 3 } }}>
      <Typography component="h1" gutterBottom variant="h4">
        {isEditing ? 'Edit Vehicle' : 'Add Vehicle'}
      </Typography>
      <Typography color="text.secondary" sx={{ mb: 3 }}>
        {isEditing
          ? 'Update the inventory details for this vehicle.'
          : 'Add a vehicle to the dealership inventory.'}
      </Typography>
      {error && (
        <Typography color="error" role="alert" sx={{ mb: 2 }}>
          {error}
        </Typography>
      )}
      <Grid container spacing={2}>
        <Grid item size={{ xs: 12, sm: 6 }}>
          <TextField defaultValue={fields.manufacturer} fullWidth label="Manufacturer" name="manufacturer" required />
        </Grid>
        <Grid item size={{ xs: 12, sm: 6 }}>
          <TextField defaultValue={fields.model} fullWidth label="Model" name="model" required />
        </Grid>
        <Grid item size={{ xs: 12, sm: 6 }}>
          <TextField defaultValue={fields.vin} disabled={isEditing} fullWidth label="VIN" name="vin" required={!isEditing} />
        </Grid>
        <Grid item size={{ xs: 12, sm: 6 }}>
          <TextField defaultValue={fields.year} fullWidth label="Year" name="year" required type="number" />
        </Grid>
        <Grid item size={{ xs: 12, sm: 6 }}>
          <TextField defaultValue={fields.purchase_price} fullWidth label="Purchase Price" name="purchase_price" required type="number" />
        </Grid>
        <Grid item size={{ xs: 12, sm: 6 }}>
          <TextField defaultValue={fields.selling_price} fullWidth label="Selling Price" name="selling_price" required type="number" />
        </Grid>
        <Grid item size={{ xs: 12, sm: 6 }}>
          <TextField defaultValue={fields.color} fullWidth label="Color" name="color" required />
        </Grid>
        <Grid item size={{ xs: 12, sm: 6 }}>
          <TextField defaultValue={fields.mileage} fullWidth label="Mileage" name="mileage" required type="number" />
        </Grid>
        <Grid item size={{ xs: 12, sm: 4 }}>
          <TextField defaultValue={fields.fuel_type} fullWidth label="Fuel Type" name="fuel_type" select>
            {fuelTypes.map((fuelType) => <MenuItem key={fuelType} value={fuelType}>{fuelType}</MenuItem>)}
          </TextField>
        </Grid>
        <Grid item size={{ xs: 12, sm: 4 }}>
          <TextField defaultValue={fields.transmission} fullWidth label="Transmission" name="transmission" select>
            {transmissions.map((transmission) => <MenuItem key={transmission} value={transmission}>{transmission}</MenuItem>)}
          </TextField>
        </Grid>
        <Grid item size={{ xs: 12, sm: 4 }}>
          <TextField defaultValue={fields.condition} fullWidth label="Condition" name="condition" select>
            {conditions.map((condition) => <MenuItem key={condition} value={condition}>{condition}</MenuItem>)}
          </TextField>
        </Grid>
        <Grid item size={12}>
          <TextField defaultValue={fields.description ?? ''} fullWidth label="Description" minRows={3} multiline name="description" />
        </Grid>
      </Grid>
      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end', mt: 3 }}>
        <Button disabled={isSubmitting} onClick={onCancel} variant="outlined">Cancel</Button>
        <Button disabled={isSubmitting} type="submit" variant="contained">
          {isSubmitting ? 'Saving…' : isEditing ? 'Update Vehicle' : 'Add Vehicle'}
        </Button>
      </Box>
    </Paper>
  )
}

export default VehicleForm

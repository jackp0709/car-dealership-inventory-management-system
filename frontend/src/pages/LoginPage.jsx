import { Alert, Box, Button, Paper, Stack, TextField, Typography } from '@mui/material'
import { useState } from 'react'
import { Navigate, useLocation, useNavigate } from 'react-router-dom'

import { apiClient } from '../api/client'

function LoginPage() {
  const location = useLocation()
  const navigate = useNavigate()
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  if (localStorage.getItem('access_token')) {
    return <Navigate replace to="/vehicles" />
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setIsSubmitting(true)

    const formData = new FormData(event.currentTarget)

    try {
      const response = await apiClient.post('/auth/login', Object.fromEntries(formData.entries()))
      localStorage.setItem('access_token', response.data.access_token)
      navigate(location.state?.from?.pathname ?? '/vehicles', { replace: true })
    } catch (requestError) {
      setError(
        requestError.response?.status === 401
          ? 'Incorrect email or password.'
          : requestError.response?.data?.detail ?? 'Unable to sign in. Please check your connection and try again.',
      )
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Box sx={{ alignItems: 'center', bgcolor: 'grey.50', display: 'flex', minHeight: '100vh', px: 2 }}>
      <Paper component="form" elevation={1} onSubmit={handleSubmit} sx={{ mx: 'auto', p: { xs: 3, sm: 4 }, width: '100%', maxWidth: 440 }}>
        <Typography component="h1" gutterBottom variant="h4">Sign in</Typography>
        <Typography color="text.secondary" sx={{ mb: 3 }}>Sign in to manage the dealership inventory.</Typography>
        <Stack spacing={2}>
          {error && <Alert severity="error">{error}</Alert>}
          <TextField autoComplete="email" autoFocus fullWidth label="Email" name="email" required type="email" />
          <TextField autoComplete="current-password" fullWidth label="Password" name="password" required type="password" />
          <Button disabled={isSubmitting} size="large" type="submit" variant="contained">
            {isSubmitting ? 'Signing in…' : 'Sign in'}
          </Button>
        </Stack>
      </Paper>
    </Box>
  )
}

export default LoginPage

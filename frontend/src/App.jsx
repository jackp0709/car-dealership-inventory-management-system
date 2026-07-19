import { AppBar, Box, Button, Container, Toolbar, Typography } from '@mui/material'
import { Link as RouterLink, Outlet } from 'react-router-dom'

function App() {
  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'grey.50' }}>
      <AppBar position="sticky" elevation={1}>
        <Toolbar>
          <Typography component="div" sx={{ flexGrow: 1 }} variant="h6">
            Car Dealership Inventory
          </Typography>
          <Button color="inherit" component={RouterLink} to="/vehicles">
            Vehicles
          </Button>
        </Toolbar>
      </AppBar>
      <Container component="main" maxWidth="xl" sx={{ py: { xs: 3, md: 4 } }}>
        <Outlet />
      </Container>
    </Box>
  )
}

export default App

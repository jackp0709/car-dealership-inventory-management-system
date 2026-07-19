import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Divider,
  Paper,
  Stack,
  Typography,
} from '@mui/material'
import { useEffect, useRef, useState } from 'react'

import { getDashboardSummary } from '../api/dashboard'

function MetricCard({ label, value }) {
  return (
    <Card variant="outlined">
      <CardContent>
        <Typography color="text.secondary" variant="body2">{label}</Typography>
        <Typography component="p" sx={{ mt: 1 }} variant="h4">{value}</Typography>
      </CardContent>
    </Card>
  )
}

function formatCurrency(value) {
  return Number(value).toLocaleString(undefined, { style: 'currency', currency: 'USD' })
}

function formatRecordedAt(value) {
  return new Date(value).toLocaleString()
}

function ActivityList({ activities, activityType, title }) {
  const matchingActivities = activities.filter((activity) => activity.activity_type === activityType)

  return (
    <Paper sx={{ p: 3 }} variant="outlined">
      <Typography component="h3" gutterBottom variant="h6">{title}</Typography>
      <Divider sx={{ mb: 1 }} />
      {matchingActivities.length === 0 ? (
        <Typography color="text.secondary">No recent {activityType.toLowerCase()}s available.</Typography>
      ) : (
        <Stack divider={<Divider flexItem />} spacing={0}>
          {matchingActivities.map((activity) => (
            <Box key={`${activity.activity_type}-${activity.record_id}`} sx={{ py: 1.5 }}>
              <Typography>{activity.counterparty_name}</Typography>
              <Typography color="text.secondary" variant="body2">
                Vehicle #{activity.vehicle_id} · {formatRecordedAt(activity.recorded_at)}
              </Typography>
            </Box>
          ))}
        </Stack>
      )}
    </Paper>
  )
}

function DashboardPage() {
  const [dashboard, setDashboard] = useState(null)
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const hasLoadedDashboard = useRef(false)

  const loadDashboard = async () => {
    setError('')
    setIsLoading(true)

    try {
      setDashboard(await getDashboardSummary())
    } catch (requestError) {
      setError(
        requestError.response?.status === 401
          ? 'Your authentication has expired. Please sign in again.'
          : 'Unable to load dashboard information.',
      )
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    if (hasLoadedDashboard.current) return
    hasLoadedDashboard.current = true
    loadDashboard()
  }, [])

  if (isLoading) {
    return <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}><CircularProgress /></Box>
  }

  if (error) {
    return <Alert action={<Button color="inherit" onClick={loadDashboard}>Retry</Button>} severity="error">{error}</Alert>
  }

  const { financial_metrics: financialMetrics, operational_metrics: operationalMetrics, recent_activity: recentActivity } = dashboard
  const operationalCards = [
    ['Total Vehicles', operationalMetrics.total_vehicles],
    ['Available Vehicles', operationalMetrics.available_vehicles],
    ['Sold Vehicles', operationalMetrics.sold_vehicles],
    ['Total Purchases', operationalMetrics.total_purchases],
    ['Completed Sales', operationalMetrics.total_completed_sales],
  ]
  const financialCards = [
    ['Total Purchase Cost', formatCurrency(financialMetrics.total_purchase_cost)],
    ['Total Sales Revenue', formatCurrency(financialMetrics.total_sales_revenue)],
    ['Gross Profit', formatCurrency(financialMetrics.estimated_gross_profit)],
  ]

  return (
    <Stack spacing={4}>
      <Box>
        <Typography component="h1" variant="h4">Dashboard</Typography>
        <Typography color="text.secondary">Overview of dealership operations and recent activity.</Typography>
      </Box>

      <Box>
        <Typography component="h2" gutterBottom variant="h6">Summary Metrics</Typography>
        <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))' }}>
          {operationalCards.map(([label, value]) => <MetricCard key={label} label={label} value={value} />)}
        </Box>
      </Box>

      <Box>
        <Typography component="h2" gutterBottom variant="h6">Financial Summary</Typography>
        <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))' }}>
          {financialCards.map(([label, value]) => <MetricCard key={label} label={label} value={value} />)}
        </Box>
      </Box>

      <Box>
        <Typography component="h2" gutterBottom variant="h6">Recent Activity</Typography>
        {recentActivity.length === 0 ? (
          <Paper sx={{ p: 3 }} variant="outlined">
            <Typography color="text.secondary">No recent activity available.</Typography>
          </Paper>
        ) : (
          <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: { md: 'repeat(2, minmax(0, 1fr))' } }}>
            <ActivityList activities={recentActivity} activityType="PURCHASE" title="Recent Purchases" />
            <ActivityList activities={recentActivity} activityType="SALE" title="Recent Sales" />
          </Box>
        )}
      </Box>
    </Stack>
  )
}

export default DashboardPage

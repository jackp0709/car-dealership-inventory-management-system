import { createBrowserRouter, Navigate } from 'react-router-dom'

import App from '../App'
import ProtectedRoute from '../components/ProtectedRoute'
import LoginPage from '../pages/LoginPage'
import VehicleCreatePage from '../pages/VehicleCreatePage'
import VehicleEditPage from '../pages/VehicleEditPage'
import VehicleListPage from '../pages/VehicleListPage'

export const router = createBrowserRouter([
  {
    element: <LoginPage />,
    path: '/login',
  },
  {
    element: <ProtectedRoute />,
    children: [
      {
        element: <App />,
        path: '/',
        children: [
          {
            element: <Navigate replace to="/vehicles" />,
            index: true,
          },
          {
            element: <VehicleListPage />,
            path: 'vehicles',
          },
          {
            element: <VehicleCreatePage />,
            path: 'vehicles/new',
          },
          {
            element: <VehicleEditPage />,
            path: 'vehicles/:vehicleId/edit',
          },
          {
            element: <Navigate replace to="/vehicles" />,
            path: '*',
          },
        ],
      },
    ],
  },
])

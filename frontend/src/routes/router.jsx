import { createBrowserRouter, Navigate } from 'react-router-dom'

import App from '../App'
import VehicleCreatePage from '../pages/VehicleCreatePage'
import VehicleEditPage from '../pages/VehicleEditPage'
import VehicleListPage from '../pages/VehicleListPage'

export const router = createBrowserRouter([
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
    ],
  },
])

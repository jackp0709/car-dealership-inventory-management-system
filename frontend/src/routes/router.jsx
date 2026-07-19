import { createBrowserRouter, Navigate } from 'react-router-dom'

import App from '../App'
import ProtectedRoute from '../components/ProtectedRoute'
import LoginPage from '../pages/LoginPage'
import PurchaseCreatePage from '../pages/PurchaseCreatePage'
import PurchaseDetailsPage from '../pages/PurchaseDetailsPage'
import PurchaseEditPage from '../pages/PurchaseEditPage'
import PurchaseListPage from '../pages/PurchaseListPage'
import SaleCreatePage from '../pages/SaleCreatePage'
import SaleDetailsPage from '../pages/SaleDetailsPage'
import SaleEditPage from '../pages/SaleEditPage'
import SaleListPage from '../pages/SaleListPage'
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
            element: <PurchaseListPage />,
            path: 'purchases',
          },
          {
            element: <PurchaseCreatePage />,
            path: 'purchases/new',
          },
          {
            element: <PurchaseDetailsPage />,
            path: 'purchases/:purchaseId',
          },
          {
            element: <PurchaseEditPage />,
            path: 'purchases/:purchaseId/edit',
          },
          {
            element: <SaleListPage />,
            path: 'sales',
          },
          {
            element: <SaleCreatePage />,
            path: 'sales/new',
          },
          {
            element: <SaleDetailsPage />,
            path: 'sales/:saleId',
          },
          {
            element: <SaleEditPage />,
            path: 'sales/:saleId/edit',
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

import { Navigate, Route, BrowserRouter as Router, Routes } from 'react-router-dom';

import Login from './components/auth/Login';
import Logout from './components/auth/Logout';

import Layout from './components/common/Layout';
import Dashboard from './pages/Dashboard';

// Módulos implementados
import BitacoraList from './components/bitacora/BitacoraList';
import CuotaList from './components/cuotas/CuotaList';
import PrivilegeList from './components/privileges/PrivilegeList';
import RoleList from './components/roles/RoleList';
import UnidadList from './components/unidades/UnidadList';
import UserList from './components/users/UserList';

import { AuthProvider, useAuth } from './contexts/AuthContext';

function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" replace />;
}

function AppRoutes() {
  return (
    <Routes>
      {/* Público */}
      <Route path="/login" element={<Login />} />

      {/* Privado con Layout */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Layout>
              <Dashboard />
            </Layout>
          </ProtectedRoute>
        }
      />

      {/* === Rutas que faltaban (causaban No routes matched) === */}
      <Route
        path="/usuarios"
        element={
          <ProtectedRoute>
            <Layout>
              <UserList />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/roles"
        element={
          <ProtectedRoute>
            <Layout>
              <RoleList />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/privilegios"
        element={
          <ProtectedRoute>
            <Layout>
              <PrivilegeList />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/logout"
        element={
          <ProtectedRoute>
            <Layout>
              <Logout />
            </Layout>
          </ProtectedRoute>
        }
      />

      {/* Rutas que ya tenías */}
      <Route
        path="/unidades"
        element={
          <ProtectedRoute>
            <Layout>
              <UnidadList />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/cuotas"
        element={
          <ProtectedRoute>
            <Layout>
              <CuotaList />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/bitacora"
        element={
          <ProtectedRoute>
            <Layout>
              <BitacoraList />
            </Layout>
          </ProtectedRoute>
        }
      />

      {/* Home → Dashboard */}
      <Route path="/" element={<Navigate to="/dashboard" replace />} />

      {/* 404 */}
      <Route path="*" element={<div style={{ padding: 24 }}>404 - Recurso no encontrado</div>} />
    </Routes>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
}

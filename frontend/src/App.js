import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Layout from './components/common/Layout';
import Login from './components/auth/Login';
import Dashboard from './pages/Dashboard';
import UserList from './components/users/UserList';
import RoleList from './components/roles/RoleList';
import PrivilegeList from './components/privileges/PrivilegeList';
import UnidadList from './components/unidades/UnidadList';
import CuotaList from './components/cuotas/CuotaList';


function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" />;
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
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
      <Route
        path="/users"
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
        path="/privileges"
        element={
          <ProtectedRoute>
            <Layout>
              <PrivilegeList />
            </Layout>
          </ProtectedRoute>
        }
      />
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
      <Route path="/" element={<Navigate to="/dashboard" />} />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
}

export default App;
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Layout from './components/common/Layout';
import Login from './components/auth/Login';

// Componentes implementados
import Dashboard from './pages/Dashboard';
import UserList from './components/users/UserList';
import RoleList from './components/roles/RoleList';
import PrivilegeList from './components/privileges/PrivilegeList';
import UnidadList from './components/unidades/UnidadList';
import CuotaList from './components/cuotas/CuotaList';

// Componentes placeholder (no implementados)
import PagoList from './components/placeholders/PagoList';
import HistorialPagos from './components/placeholders/HistorialPagos';
import ReportesFinancieros from './components/placeholders/ReportesFinancieros';
import Morosidad from './components/placeholders/Morosidad';
import QRPagos from './components/placeholders/QRPagos';
import Camaras from './components/placeholders/Camaras';
import ReconocimientoFacial from './components/placeholders/ReconocimientoFacial';
import DetectarVisitantes from './components/placeholders/DetectarVisitantes';
import ReconocimientoVehiculos from './components/placeholders/ReconocimientoVehiculos';
import DeteccionAnomalias from './components/placeholders/DeteccionAnomalias';
import RegistroVisitantes from './components/placeholders/RegistroVisitantes';
import ReportesSeguridad from './components/placeholders/ReportesSeguridad';
import GestionInvitados from './components/placeholders/GestionInvitados';
import Avisos from './components/placeholders/Avisos';
import TareasMantenimiento from './components/placeholders/TareasMantenimiento';
import ReportesMantenimiento from './components/placeholders/ReportesMantenimiento';
import Notificaciones from './components/placeholders/Notificaciones';
import Configuracion from './components/placeholders/Configuracion';
import AreasComunes from './components/placeholders/AreasComunes';
import ReportesAreas from './components/placeholders/ReportesAreas';

function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" />;
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      
      {/* Rutas protegidas */}
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <Layout>
            <Dashboard />
          </Layout>
        </ProtectedRoute>
      } />
      
      {/* Identidad & Unidades */}
      <Route path="/usuarios" element={
        <ProtectedRoute>
          <Layout>
            <UserList />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/roles" element={
        <ProtectedRoute>
          <Layout>
            <RoleList />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/privilegios" element={
        <ProtectedRoute>
          <Layout>
            <PrivilegeList />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/unidades" element={
        <ProtectedRoute>
          <Layout>
            <UnidadList />
          </Layout>
        </ProtectedRoute>
      } />
      
      {/* Finanzas & Cobranza */}
      <Route path="/cuotas" element={
        <ProtectedRoute>
          <Layout>
            <CuotaList />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/pagos" element={
        <ProtectedRoute>
          <Layout>
            <PagoList />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/historial-pagos" element={
        <ProtectedRoute>
          <Layout>
            <HistorialPagos />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/reportes-financieros" element={
        <ProtectedRoute>
          <Layout>
            <ReportesFinancieros />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/morosidad" element={
        <ProtectedRoute>
          <Layout>
            <Morosidad />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/qr-pagos" element={
        <ProtectedRoute>
          <Layout>
            <QRPagos />
          </Layout>
        </ProtectedRoute>
      } />
      
      {/* IA & Seguridad */}
      <Route path="/camaras" element={
        <ProtectedRoute>
          <Layout>
            <Camaras />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/reconocimiento-facial" element={
        <ProtectedRoute>
          <Layout>
            <ReconocimientoFacial />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/detectar-visitantes" element={
        <ProtectedRoute>
          <Layout>
            <DetectarVisitantes />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/reconocimiento-vehiculos" element={
        <ProtectedRoute>
          <Layout>
            <ReconocimientoVehiculos />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/deteccion-anomalias" element={
        <ProtectedRoute>
          <Layout>
            <DeteccionAnomalias />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/registro-visitantes" element={
        <ProtectedRoute>
          <Layout>
            <RegistroVisitantes />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/reportes-seguridad" element={
        <ProtectedRoute>
          <Layout>
            <ReportesSeguridad />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/gestion-invitados" element={
        <ProtectedRoute>
          <Layout>
            <GestionInvitados />
          </Layout>
        </ProtectedRoute>
      } />
      
      {/* Operaciones & Notificaciones */}
      <Route path="/avisos" element={
        <ProtectedRoute>
          <Layout>
            <Avisos />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/tareas-mantenimiento" element={
        <ProtectedRoute>
          <Layout>
            <TareasMantenimiento />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/reportes-mantenimiento" element={
        <ProtectedRoute>
          <Layout>
            <ReportesMantenimiento />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/notificaciones" element={
        <ProtectedRoute>
          <Layout>
            <Notificaciones />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/configuracion" element={
        <ProtectedRoute>
          <Layout>
            <Configuracion />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/areas-comunes" element={
        <ProtectedRoute>
          <Layout>
            <AreasComunes />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/reportes-areas" element={
        <ProtectedRoute>
          <Layout>
            <ReportesAreas />
          </Layout>
        </ProtectedRoute>
      } />
      
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
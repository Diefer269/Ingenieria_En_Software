import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';

import Login from './components/Login';
import Register from './components/Register';
import Home from './pages/Home';
import PrivateRoute from './components/PrivateRoutes';
import PublicRoute from './components/PublicRoutes';
import AuthNavbar from "./components/AuthNavBar";
import HomeNavbar from "./components/HomeNavBar";
import Habitaciones from "./pages/Habitaciones";
import CrearHabitacion from './pages/CrearHabitacion';
import EditarHabitacion from './pages/EditarHabitacion';
import Clientes from './pages/Clientes';
import CrearCliente from './pages/CrearCliente';
import EditarCliente from './pages/EditarCliente';
import Reservas from './pages/Reservas';
import CrearReserva from './pages/CrearReserva';
import EditarReserva from './pages/EditarReserva'; 
import Pagos from './pages/Pagos';
import CrearPago from './pages/CrearPago';
import EditarPago from './pages/EditarPago';
import Reportes from './pages/Reportes';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));

  // Función para actualizar token al login o logout
  const handleLogin = (newToken) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  return (
    <Router>
      {/* Navbar condicional según si hay token */}
      {token ? <HomeNavbar onLogout={handleLogout} /> : <AuthNavbar />}

      <Routes>
        <Route
          path="/login"
          element={
            <PublicRoute>
              <Login onLogin={handleLogin} />
            </PublicRoute>
          }
        />
        <Route
          path="/register"
          element={
            <PublicRoute>
              <Register />
            </PublicRoute>
          }
        />
        <Route
          path="/"
          element={
            <PrivateRoute>
              <Home />
            </PrivateRoute>
          }
        />
        <Route path="*" element={<Navigate to={token ? '/' : '/login'} />} />

        <Route
          path="/habitaciones"
          element={
            <PrivateRoute>
              <Habitaciones />
            </PrivateRoute>
          }
        />
        <Route 
          path="/crear-habitacion"
          element={
            <PrivateRoute>
              <CrearHabitacion/>
            </PrivateRoute>
          } 
          />
        <Route
          path="/editar-habitacion/:id" 
          element={
            <PrivateRoute>
              <EditarHabitacion />
            </PrivateRoute>
          } 
          />

        <Route
         path="/clientes" 
         element={
          <PrivateRoute>
            <Clientes />
          </PrivateRoute>
          } 
          />
        <Route
         path="/crear-cliente" 
         element={
         <PrivateRoute>
                <CrearCliente />
                </PrivateRoute>
                } 
                />
        <Route
         path="/editar-cliente/:id" 
         element={
         <PrivateRoute>
                <EditarCliente />
                </PrivateRoute>
                } 
                />

        <Route
         path="/reservas" 
         element={
         <PrivateRoute>
                <Reservas />
                </PrivateRoute>
                } 
                />
        <Route
         path="/crear-reserva" 
         element={
         <PrivateRoute>
                <CrearReserva />
                </PrivateRoute>
                } 
                />
        <Route
         path="/editar-reserva/:id" 
         element={
         <PrivateRoute>
                <EditarReserva />
                </PrivateRoute>
                } 
                />

        <Route
         path="/pagos" 
         element={
         <PrivateRoute>
                <Pagos />
                </PrivateRoute>
                } 
                />
        <Route
         path="/crear-pago" 
         element={
         <PrivateRoute>
                <CrearPago />
                </PrivateRoute>
                } 
                />
        <Route
         path="/editar-pago/:id" 
         element={
         <PrivateRoute>
                <EditarPago />
                </PrivateRoute>
                } 
                />

        <Route
         path="/reportes" 
         element={
         <PrivateRoute>
                <Reportes />
                </PrivateRoute>
                } 
                />
      </Routes>
    </Router>
    
  );
}

export default App;

import { createContext, useContext, useEffect, useState } from 'react';
import { authService } from '../services/authService';

import api from '../services/api';
const AuthContext = createContext();

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      authService.getCurrentUser()
        .then(response => {
          setCurrentUser(response.data);
          setLoading(false);
        })
        .catch(error => {
          console.error('Error getting current user:', error);
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (credentials) => {
    try {
      const response = await authService.login(credentials);
      const { access, refresh, user } = response.data;
      
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      setCurrentUser(user);
      
      return response;
    } catch (error) {
      throw error;
    }
  };

const logout = async () => {
  try {
    const refresh = localStorage.getItem('refresh_token');
    if (refresh) {
      await api.post('auth/logout/', { refresh }); // también acepta { refresh_token: refresh }
    }
  } catch (e) {
    // opcional: console.warn('Logout server error', e);
  } finally {
    // limpia estado y tokens
    setCurrentUser(null);
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }
};
  const value = {
    currentUser,
    login,
    logout,
    isAuthenticated: !!currentUser
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};
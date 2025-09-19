import axios from 'axios';

const RAW_API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
// fuerza una sola barra final: .../api/
const API_BASE_URL = RAW_API_BASE_URL.replace(/\/+$/, '') + '/';

const api = axios.create({ baseURL: API_BASE_URL });

// Interceptor para agregar el token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor para refresh del token (ajusta la ruta si tu backend la tiene bajo /auth/)
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        // ⬇usa la que corresponda en tu backend: 'token/refresh/' (SimpleJWT por defecto)
        // o 'auth/token/refresh/' si configuraste ese prefijo.
        const refreshPath = 'token/refresh/'; // o 'auth/token/refresh/'
        const { data } = await axios.post(API_BASE_URL + refreshPath, { refresh: refreshToken });

        const { access } = data;
        localStorage.setItem('access_token', access);
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;

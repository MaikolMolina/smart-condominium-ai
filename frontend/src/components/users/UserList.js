import React, { useState, useEffect, useCallback } from 'react';
import {
  IconButton,
  Button,
  Box,
  Typography,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Alert,
  Snackbar,
  MenuItem
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Add as AddIcon
} from '@mui/icons-material';
import { userService } from '../../services/userService';
import { unidadService } from '../../services/unidadService';

const UserList = () => {
  const [users, setUsers] = useState([]);
  const [unidades, setUnidades] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingUser, setEditingUser] = useState(null);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    ci: '',
    telefono: '',
    tipo_usuario: 'residente',
    unidad_habitacional: '',
    password: ''
  });
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  const showSnackbar = useCallback((message, severity = 'success') => {
    setSnackbar({ open: true, message, severity });
  }, []);

  const loadUsers = useCallback(async () => {
    try {
      const response = await userService.getAll();
      setUsers(response.data);
    } catch (error) {
      console.error('Error loading users:', error);
      showSnackbar('Error al cargar usuarios', 'error');
    }
  }, [showSnackbar]);

  const loadUnidades = useCallback(async () => {
    try {
      const response = await unidadService.getAll();
      setUnidades(response.data);
    } catch (error) {
      console.error('Error loading unidades:', error);
    }
  }, []);

  useEffect(() => {
    loadUsers();
    loadUnidades();
  }, [loadUsers, loadUnidades]);

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  const handleOpenDialog = (user = null) => {
    if (user) {
      setEditingUser(user);
      setFormData({
        username: user.username,
        email: user.email,
        first_name: user.first_name,
        last_name: user.last_name,
        ci: user.ci,
        telefono: user.telefono,
        tipo_usuario: user.tipo_usuario,
        unidad_habitacional: user.unidad_habitacional?.id || '',
        password: ''
      });
    } else {
      setEditingUser(null);
      setFormData({
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        ci: '',
        telefono: '',
        tipo_usuario: 'residente',
        unidad_habitacional: '',
        password: ''
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingUser) {
        await userService.update(editingUser.id, formData);
        showSnackbar('Usuario actualizado correctamente');
      } else {
        await userService.create(formData);
        showSnackbar('Usuario creado correctamente');
      }
      loadUsers();
      handleCloseDialog();
    } catch (error) {
      console.error('Error saving user:', error);
      showSnackbar('Error al guardar usuario', 'error');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de que desea eliminar este usuario?')) {
      try {
        await userService.delete(id);
        showSnackbar('Usuario eliminado correctamente');
        loadUsers();
      } catch (error) {
        console.error('Error deleting user:', error);
        showSnackbar('Error al eliminar usuario', 'error');
      }
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h4" gutterBottom>
          Gestión de Usuarios
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Nuevo Usuario
        </Button>
      </Box>

      {/* Tabla de usuarios - Reemplaza con tu implementación actual */}
      <Box>
        {users.map(user => (
          <Box key={user.id} sx={{ p: 2, border: '1px solid #ccc', mb: 1 }}>
            <Typography>{user.first_name} {user.last_name}</Typography>
            <Typography variant="body2">{user.email}</Typography>
            <Box>
              <IconButton
                color="primary"
                onClick={() => handleOpenDialog(user)}
              >
                <EditIcon />
              </IconButton>
              <IconButton
                color="error"
                onClick={() => handleDelete(user.id)}
              >
                <DeleteIcon />
              </IconButton>
            </Box>
          </Box>
        ))}
      </Box>

      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingUser ? 'Editar Usuario' : 'Crear Usuario'}
        </DialogTitle>
        <form onSubmit={handleSubmit}>
          <DialogContent>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
              <TextField
                label="Username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
                fullWidth
              />
              <TextField
                label="Email"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                required
                fullWidth
              />
              <Box sx={{ display: 'flex', gap: 2 }}>
                <TextField
                  label="Nombre"
                  name="first_name"
                  value={formData.first_name}
                  onChange={handleChange}
                  required
                  fullWidth
                />
                <TextField
                  label="Apellido"
                  name="last_name"
                  value={formData.last_name}
                  onChange={handleChange}
                  required
                  fullWidth
                />
              </Box>
              <Box sx={{ display: 'flex', gap: 2 }}>
                <TextField
                  label="CI"
                  name="ci"
                  value={formData.ci}
                  onChange={handleChange}
                  required
                  fullWidth
                />
                <TextField
                  label="Teléfono"
                  name="telefono"
                  value={formData.telefono}
                  onChange={handleChange}
                  required
                  fullWidth
                />
              </Box>
              <TextField
                label="Tipo de Usuario"
                name="tipo_usuario"
                value={formData.tipo_usuario}
                onChange={handleChange}
                select
                required
                fullWidth
              >
                <MenuItem value="admin">Administrador</MenuItem>
                <MenuItem value="residente">Residente</MenuItem>
                <MenuItem value="inquilino">Inquilino</MenuItem>
                <MenuItem value="mantenimiento">Mantenimiento</MenuItem>
                <MenuItem value="seguridad">Seguridad</MenuItem>
              </TextField>
              <TextField
                label="Unidad Habitacional"
                name="unidad_habitacional"
                value={formData.unidad_habitacional}
                onChange={handleChange}
                select
                required
                fullWidth
              >
                {unidades.map((unidad) => (
                  <MenuItem key={unidad.id} value={unidad.id}>
                    {unidad.torre} - {unidad.piso} - {unidad.numero}
                  </MenuItem>
                ))}
              </TextField>
              <TextField
                label="Contraseña"
                name="password"
                type="password"
                value={formData.password}
                onChange={handleChange}
                required={!editingUser}
                fullWidth
              />
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog}>Cancelar</Button>
            <Button type="submit" variant="contained">
              {editingUser ? 'Actualizar' : 'Crear'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default UserList;
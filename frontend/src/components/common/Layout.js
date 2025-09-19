// src/components/common/Layout.js
import {
  Dashboard as DashboardIcon,
  ExitToApp as ExitToAppIcon,
  Home as HomeIcon,
  Lock as LockIcon,
  Menu as MenuIcon,
  AttachMoney as MoneyIcon,
  People as PeopleIcon,
  Security as SecurityIcon
} from '@mui/icons-material';
import ListAltIcon from '@mui/icons-material/ListAlt'; // Ícono para Bitácora
import {
  AppBar,
  Avatar,
  Box,
  CssBaseline,
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Menu,
  MenuItem,
  Toolbar,
  Typography,
  useMediaQuery,
  useTheme
} from '@mui/material';
import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const drawerWidth = 240;

// Menú lateral
const menuItems = [
  { text: 'Dashboard', path: '/dashboard', icon: <DashboardIcon /> },
  { text: 'Usuarios', path: '/users', icon: <PeopleIcon /> },
  { text: 'Unidades', path: '/unidades', icon: <HomeIcon /> },
  { text: 'Roles', path: '/roles', icon: <LockIcon /> },
  { text: 'Privilegios', path: '/privileges', icon: <SecurityIcon /> },
  { text: 'Bitácora', path: '/bitacora', icon: <ListAltIcon /> },
  { text: 'Cuotas', path: '/cuotas', icon: <MoneyIcon /> },
];

const Layout = ({ children }) => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();
  const { currentUser, logout } = useAuth();

  // 🔹 breakpoints: compactamos en pantallas < 600px
  const theme = useTheme();
  const isSmDown = useMediaQuery(theme.breakpoints.down('sm'));

  const handleDrawerToggle = () => setMobileOpen(!mobileOpen);
  const handleMenu = (event) => setAnchorEl(event.currentTarget);
  const handleClose = () => setAnchorEl(null);

  const handleLogout = async () => {
    handleClose();
    await logout();
    navigate('/login');
  };

  const drawer = (
    <div>
      <Toolbar variant={isSmDown ? 'dense' : 'regular'}>
        <Typography variant={isSmDown ? 'subtitle1' : 'h6'} noWrap component="div">
          Smart Condo
        </Typography>
      </Toolbar>
      {/* Lista en modo "dense" para móviles */}
      <List dense={isSmDown}>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => navigate(item.path)}
              sx={{ py: isSmDown ? 0.5 : 1 }}
            >
              <ListItemIcon
                sx={{
                  minWidth: isSmDown ? 36 : 40,
                  '& .MuiSvgIcon-root': { fontSize: isSmDown ? 20 : 24 }
                }}
              >
                {item.icon}
              </ListItemIcon>
              <ListItemText
                primary={item.text}
                primaryTypographyProps={{
                  variant: isSmDown ? 'body2' : 'body1',
                  noWrap: true
                }}
              />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </div>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        <Toolbar variant={isSmDown ? 'dense' : 'regular'}>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography
            variant={isSmDown ? 'h6' : 'h5'}
            noWrap
            component="div"
            sx={{ flexGrow: 1 }}
          >
            {menuItems.find(item => item.path === location.pathname)?.text || 'Dashboard'}
          </Typography>
          <div>
            <IconButton
              size={isSmDown ? 'small' : 'large'}
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleMenu}
              color="inherit"
            >
              <Avatar sx={{ width: isSmDown ? 28 : 32, height: isSmDown ? 28 : 32 }}>
                {currentUser?.first_name?.[0]}{currentUser?.last_name?.[0]}
              </Avatar>
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorEl}
              anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
              keepMounted
              transformOrigin={{ vertical: 'top', horizontal: 'right' }}
              open={Boolean(anchorEl)}
              onClose={handleClose}
            >
              <MenuItem onClick={handleClose}>Perfil</MenuItem>
              <MenuItem onClick={handleLogout}>
                <ListItemIcon>
                  <ExitToAppIcon fontSize="small" />
                </ListItemIcon>
                Cerrar Sesión
              </MenuItem>
            </Menu>
          </div>
        </Toolbar>
      </AppBar>

      <Box component="nav" sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}>
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{ keepMounted: true }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      <Box
        component="main"
        sx={{ flexGrow: 1, p: isSmDown ? 2 : 3, width: { sm: `calc(100% - ${drawerWidth}px)` } }}
      >
        <Toolbar variant={isSmDown ? 'dense' : 'regular'} />
        {children}
      </Box>
    </Box>
  );
};

export default Layout;

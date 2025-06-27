---
applyTo: ["ui", "frontend", "react", "components", "firebase", "design-system"]
description: "Instructions for UI component development and frontend implementation"
priority: "high"
---

# **Task: UI Development (React & Material Design)**

Develop modern, responsive, and accessible user interfaces using React and Google's Material Design system, integrated with GCP services.

## **Component Development Standards**

### **1. Component Structure**
```typescript
// Component file structure example
import React, { useState, useEffect, memo } from 'react';
import { 
  Button, 
  TextField, 
  Typography, 
  Box,
  Alert 
} from '@mui/material';
import { styled } from '@mui/material/styles';

interface ComponentProps {
  title: string;
  onSubmit: (data: FormData) => Promise<void>;
  loading?: boolean;
  error?: string;
}

// Styled components for custom styling
const StyledContainer = styled(Box)(({ theme }) => ({
  padding: theme.spacing(3),
  borderRadius: theme.shape.borderRadius,
  backgroundColor: theme.palette.background.paper,
  boxShadow: theme.shadows[1],
}));

// Main component with proper TypeScript typing
const UserForm: React.FC<ComponentProps> = memo(({ 
  title, 
  onSubmit, 
  loading = false, 
  error 
}) => {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: ''
  });

  // Component logic here...

  return (
    <StyledContainer>
      <Typography variant="h5" component="h2" gutterBottom>
        {title}
      </Typography>
      {/* Form implementation */}
    </StyledContainer>
  );
});

UserForm.displayName = 'UserForm';
export default UserForm;
```

### **2. Component Design Patterns**

#### **Container/Presentation Pattern**
```typescript
// Container Component (Logic)
const UserListContainer: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchUsers()
      .then(setUsers)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const handleDeleteUser = async (userId: string) => {
    try {
      await deleteUser(userId);
      setUsers(prev => prev.filter(user => user.id !== userId));
    } catch (err) {
      setError('Failed to delete user');
    }
  };

  return (
    <UserListPresentation
      users={users}
      loading={loading}
      error={error}
      onDeleteUser={handleDeleteUser}
    />
  );
};

// Presentation Component (UI Only)
interface UserListPresentationProps {
  users: User[];
  loading: boolean;
  error: string | null;
  onDeleteUser: (userId: string) => void;
}

const UserListPresentation: React.FC<UserListPresentationProps> = ({
  users,
  loading,
  error,
  onDeleteUser
}) => {
  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <List>
      {users.map(user => (
        <UserListItem 
          key={user.id} 
          user={user} 
          onDelete={() => onDeleteUser(user.id)} 
        />
      ))}
    </List>
  );
};
```

## **Material Design Implementation**

### **1. Theme Configuration**
```typescript
// theme.ts
import { createTheme, ThemeOptions } from '@mui/material/styles';

const themeOptions: ThemeOptions = {
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#dc004e',
      light: '#ff5983',
      dark: '#9a0036',
      contrastText: '#ffffff',
    },
    background: {
      default: '#fafafa',
      paper: '#ffffff',
    },
    text: {
      primary: 'rgba(0, 0, 0, 0.87)',
      secondary: 'rgba(0, 0, 0, 0.6)',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 300,
      lineHeight: 1.2,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 400,
      lineHeight: 1.3,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.5,
    },
  },
  spacing: 8,
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 500,
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 8,
          },
        },
      },
    },
  },
};

export const theme = createTheme(themeOptions);

// App.tsx
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {/* Your app components */}
    </ThemeProvider>
  );
}
```

### **2. Responsive Design Patterns**
```typescript
import { useMediaQuery, useTheme, Grid, Container } from '@mui/material';

const ResponsiveLayout: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isTablet = useMediaQuery(theme.breakpoints.down('lg'));

  return (
    <Container maxWidth="xl">
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <MainContent />
        </Grid>
        {!isMobile && (
          <Grid item xs={12} md={4}>
            <Sidebar />
          </Grid>
        )}
      </Grid>
    </Container>
  );
};

// Responsive styling with sx prop
const ResponsiveComponent = () => (
  <Box
    sx={{
      display: 'flex',
      flexDirection: { xs: 'column', md: 'row' },
      gap: { xs: 2, md: 4 },
      padding: { xs: 2, md: 3, lg: 4 },
      backgroundColor: { xs: 'grey.100', md: 'white' },
    }}
  >
    <Typography
      variant="h4"
      sx={{
        fontSize: { xs: '1.5rem', md: '2rem', lg: '2.5rem' },
        textAlign: { xs: 'center', md: 'left' },
      }}
    >
      Responsive Title
    </Typography>
  </Box>
);
```

## **Firebase Integration**

### **1. Authentication Setup**
```typescript
// firebase/auth.ts
import { 
  getAuth, 
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  User
} from 'firebase/auth';
import { app } from './config';

const auth = getAuth(app);

export const authService = {
  // Sign in with email and password
  signIn: async (email: string, password: string) => {
    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      return userCredential.user;
    } catch (error) {
      throw new Error(`Sign in failed: ${error.message}`);
    }
  },

  // Create new user account
  signUp: async (email: string, password: string) => {
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      return userCredential.user;
    } catch (error) {
      throw new Error(`Sign up failed: ${error.message}`);
    }
  },

  // Sign out current user
  signOut: async () => {
    try {
      await signOut(auth);
    } catch (error) {
      throw new Error(`Sign out failed: ${error.message}`);
    }
  },

  // Get current user
  getCurrentUser: () => auth.currentUser,

  // Listen to auth state changes
  onAuthStateChanged: (callback: (user: User | null) => void) => {
    return onAuthStateChanged(auth, callback);
  }
};

// hooks/useAuth.ts
import { useState, useEffect, createContext, useContext } from 'react';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = authService.onAuthStateChanged((user) => {
      setUser(user);
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  const value = {
    user,
    loading,
    signIn: authService.signIn,
    signUp: authService.signUp,
    signOut: authService.signOut,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
```

### **2. Firestore Data Management**
```typescript
// firebase/firestore.ts
import {
  getFirestore,
  collection,
  doc,
  getDocs,
  getDoc,
  addDoc,
  updateDoc,
  deleteDoc,
  query,
  where,
  orderBy,
  limit,
  onSnapshot,
} from 'firebase/firestore';
import { app } from './config';

const db = getFirestore(app);

export const firestoreService = {
  // Create document
  create: async <T>(collectionName: string, data: T) => {
    try {
      const docRef = await addDoc(collection(db, collectionName), data);
      return docRef.id;
    } catch (error) {
      throw new Error(`Failed to create document: ${error.message}`);
    }
  },

  // Get document by ID
  getById: async <T>(collectionName: string, id: string): Promise<T | null> => {
    try {
      const docRef = doc(db, collectionName, id);
      const docSnap = await getDoc(docRef);
      
      if (docSnap.exists()) {
        return { id: docSnap.id, ...docSnap.data() } as T;
      }
      return null;
    } catch (error) {
      throw new Error(`Failed to get document: ${error.message}`);
    }
  },

  // Get all documents from collection
  getAll: async <T>(collectionName: string): Promise<T[]> => {
    try {
      const querySnapshot = await getDocs(collection(db, collectionName));
      return querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      })) as T[];
    } catch (error) {
      throw new Error(`Failed to get documents: ${error.message}`);
    }
  },

  // Query documents with conditions
  query: async <T>(
    collectionName: string,
    conditions: { field: string; operator: any; value: any }[],
    orderByField?: string,
    limitCount?: number
  ): Promise<T[]> => {
    try {
      let q = collection(db, collectionName);
      
      // Apply where conditions
      conditions.forEach(condition => {
        q = query(q, where(condition.field, condition.operator, condition.value));
      });
      
      // Apply ordering
      if (orderByField) {
        q = query(q, orderBy(orderByField));
      }
      
      // Apply limit
      if (limitCount) {
        q = query(q, limit(limitCount));
      }
      
      const querySnapshot = await getDocs(q);
      return querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      })) as T[];
    } catch (error) {
      throw new Error(`Failed to query documents: ${error.message}`);
    }
  },

  // Real-time listener
  listen: <T>(
    collectionName: string,
    callback: (data: T[]) => void,
    errorCallback?: (error: Error) => void
  ) => {
    return onSnapshot(
      collection(db, collectionName),
      (snapshot) => {
        const data = snapshot.docs.map(doc => ({
          id: doc.id,
          ...doc.data()
        })) as T[];
        callback(data);
      },
      (error) => {
        if (errorCallback) {
          errorCallback(new Error(`Firestore listener error: ${error.message}`));
        }
      }
    );
  }
};
```

## **API Integration Patterns**

### **1. HTTP Client Setup**
```typescript
// api/client.ts
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { authService } from '../firebase/auth';

class ApiClient {
  private client: AxiosInstance;

  constructor(baseURL: string) {
    this.client = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor - add auth token
    this.client.interceptors.request.use(
      async (config) => {
        const user = authService.getCurrentUser();
        if (user) {
          const token = await user.getIdToken();
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor - handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Handle unauthorized - redirect to login
          authService.signOut();
        }
        return Promise.reject(error);
      }
    );
  }

  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.get(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.post(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.put(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.delete(url, config);
    return response.data;
  }
}

export const apiClient = new ApiClient(process.env.REACT_APP_API_BASE_URL || '');
```

### **2. React Query Integration**
```typescript
// hooks/useUsers.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../api/client';

interface User {
  id: string;
  name: string;
  email: string;
  createdAt: string;
}

// Fetch users
export const useUsers = () => {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => apiClient.get<User[]>('/users'),
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
  });
};

// Fetch user by ID
export const useUser = (userId: string) => {
  return useQuery({
    queryKey: ['users', userId],
    queryFn: () => apiClient.get<User>(`/users/${userId}`),
    enabled: !!userId,
  });
};

// Create user mutation
export const useCreateUser = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (userData: Omit<User, 'id' | 'createdAt'>) =>
      apiClient.post<User>('/users', userData),
    onSuccess: () => {
      // Invalidate and refetch users list
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
};

// Update user mutation
export const useUpdateUser = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, ...userData }: Partial<User> & { id: string }) =>
      apiClient.put<User>(`/users/${id}`, userData),
    onSuccess: (data) => {
      // Update specific user in cache
      queryClient.setQueryData(['users', data.id], data);
      // Invalidate users list
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
};
```

## **Performance Optimization**

### **1. Code Splitting and Lazy Loading**
```typescript
// App.tsx
import { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { CircularProgress, Box } from '@mui/material';

// Lazy load components
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Users = lazy(() => import('./pages/Users'));
const Settings = lazy(() => import('./pages/Settings'));

const LoadingFallback = () => (
  <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
    <CircularProgress />
  </Box>
);

function App() {
  return (
    <Router>
      <Suspense fallback={<LoadingFallback />}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/users" element={<Users />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Suspense>
    </Router>
  );
}
```

### **2. Memoization and Optimization**
```typescript
import { memo, useMemo, useCallback } from 'react';

interface ExpensiveComponentProps {
  data: any[];
  onItemClick: (id: string) => void;
  filter: string;
}

const ExpensiveComponent = memo<ExpensiveComponentProps>(({ 
  data, 
  onItemClick, 
  filter 
}) => {
  // Memoize expensive calculations
  const filteredData = useMemo(() => {
    return data.filter(item => 
      item.name.toLowerCase().includes(filter.toLowerCase())
    );
  }, [data, filter]);

  const sortedData = useMemo(() => {
    return filteredData.sort((a, b) => a.name.localeCompare(b.name));
  }, [filteredData]);

  // Memoize event handlers
  const handleItemClick = useCallback((id: string) => {
    onItemClick(id);
  }, [onItemClick]);

  return (
    <List>
      {sortedData.map(item => (
        <ListItem 
          key={item.id}
          onClick={() => handleItemClick(item.id)}
        >
          <ListItemText primary={item.name} />
        </ListItem>
      ))}
    </List>
  );
});
```

## **Accessibility Standards**

### **1. ARIA Implementation**
```typescript
const AccessibleForm = () => {
  const [error, setError] = useState<string>('');
  const errorId = 'form-error';

  return (
    <form 
      role="form" 
      aria-labelledby="form-title"
      aria-describedby={error ? errorId : undefined}
    >
      <Typography id="form-title" variant="h2">
        User Registration
      </Typography>
      
      {error && (
        <Alert 
          id={errorId}
          severity="error" 
          role="alert"
          aria-live="polite"
        >
          {error}
        </Alert>
      )}
      
      <TextField
        label="Email"
        type="email"
        required
        aria-required="true"
        aria-describedby="email-help"
        error={!!error}
      />
      
      <Typography id="email-help" variant="caption">
        Enter a valid email address
      </Typography>
      
      <Button 
        type="submit"
        aria-describedby="submit-help"
      >
        Register
      </Button>
    </form>
  );
};
```

### **2. Keyboard Navigation**
```typescript
const KeyboardNavigationComponent = () => {
  const [focusedIndex, setFocusedIndex] = useState(0);
  const itemRefs = useRef<(HTMLElement | null)[]>([]);

  const handleKeyDown = useCallback((event: KeyboardEvent) => {
    switch (event.key) {
      case 'ArrowDown':
        event.preventDefault();
        const nextIndex = Math.min(focusedIndex + 1, items.length - 1);
        setFocusedIndex(nextIndex);
        itemRefs.current[nextIndex]?.focus();
        break;
        
      case 'ArrowUp':
        event.preventDefault();
        const prevIndex = Math.max(focusedIndex - 1, 0);
        setFocusedIndex(prevIndex);
        itemRefs.current[prevIndex]?.focus();
        break;
        
      case 'Enter':
      case ' ':
        event.preventDefault();
        // Handle selection
        break;
    }
  }, [focusedIndex, items.length]);

  return (
    <Box role="listbox" onKeyDown={handleKeyDown}>
      {items.map((item, index) => (
        <Box
          key={item.id}
          ref={el => itemRefs.current[index] = el}
          role="option"
          tabIndex={index === focusedIndex ? 0 : -1}
          aria-selected={index === focusedIndex}
        >
          {item.name}
        </Box>
      ))}
    </Box>
  );
};
```

## **Testing Standards**

### **1. Component Testing**
```typescript
// __tests__/UserForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ThemeProvider } from '@mui/material/styles';
import { theme } from '../theme';
import UserForm from '../components/UserForm';

const renderWithTheme = (component: React.ReactElement) => {
  return render(
    <ThemeProvider theme={theme}>
      {component}
    </ThemeProvider>
  );
};

describe('UserForm', () => {
  const mockOnSubmit = jest.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  it('renders form fields correctly', () => {
    renderWithTheme(
      <UserForm title="Test Form" onSubmit={mockOnSubmit} />
    );

    expect(screen.getByRole('textbox', { name: /name/i })).toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: /email/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /submit/i })).toBeInTheDocument();
  });

  it('validates email format', async () => {
    const user = userEvent.setup();
    
    renderWithTheme(
      <UserForm title="Test Form" onSubmit={mockOnSubmit} />
    );

    const emailInput = screen.getByRole('textbox', { name: /email/i });
    await user.type(emailInput, 'invalid-email');
    
    const submitButton = screen.getByRole('button', { name: /submit/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/invalid email format/i)).toBeInTheDocument();
    });

    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('submits form with valid data', async () => {
    const user = userEvent.setup();
    
    renderWithTheme(
      <UserForm title="Test Form" onSubmit={mockOnSubmit} />
    );

    await user.type(screen.getByRole('textbox', { name: /name/i }), 'John Doe');
    await user.type(screen.getByRole('textbox', { name: /email/i }), 'john@example.com');
    await user.click(screen.getByRole('button', { name: /submit/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        name: 'John Doe',
        email: 'john@example.com'
      });
    });
  });
});
```

## **Deployment Configuration**

### **1. Firebase Hosting**
```json
// firebase.json
{
  "hosting": {
    "public": "build",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ],
    "headers": [
      {
        "source": "/static/**",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "public, max-age=31536000, immutable"
          }
        ]
      }
    ]
  }
}

// .firebaserc
{
  "projects": {
    "development": "your-dev-project",
    "staging": "your-staging-project",
    "production": "your-prod-project"
  }
}
```

### **2. Environment Configuration**
```typescript
// config/environment.ts
interface EnvironmentConfig {
  apiBaseUrl: string;
  firebaseConfig: {
    apiKey: string;
    authDomain: string;
    projectId: string;
    storageBucket: string;
    messagingSenderId: string;
    appId: string;
  };
  enableAnalytics: boolean;
  logLevel: 'debug' | 'info' | 'warn' | 'error';
}

const environments: Record<string, EnvironmentConfig> = {
  development: {
    apiBaseUrl: 'http://localhost:8080/api',
    firebaseConfig: {
      // Development Firebase config
    },
    enableAnalytics: false,
    logLevel: 'debug',
  },
  production: {
    apiBaseUrl: 'https://api.yourapp.com',
    firebaseConfig: {
      // Production Firebase config
    },
    enableAnalytics: true,
    logLevel: 'error',
  },
};

const env = process.env.NODE_ENV || 'development';
export const config = environments[env];
```

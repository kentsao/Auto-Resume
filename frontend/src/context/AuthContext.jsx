import { createContext, useState, useEffect, useContext } from 'react';
import api from '../api/axios';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          // We don't have a dedicated /me endpoint yet, but we can decode the token 
          // or assume valid if we have it. For now, let's just set a flag or decode it.
          // Ideally, we should fetch the user profile.
          // Let's assume we can decode the token payload if needed, 
          // but for now we'll just set the user as "authenticated" and maybe store the username if we had it.
          
          // Since we don't have a /me endpoint, let's just trust the token for now 
          // or try to fetch a protected resource.
          // Actually, the backend returns the user info in the callback, 
          // so we can store it in localStorage too.
          
          const storedUser = localStorage.getItem('user');
          if (storedUser) {
            setUser(JSON.parse(storedUser));
          }
        } catch (error) {
          console.error("Auth check failed", error);
          localStorage.removeItem('token');
          localStorage.removeItem('user');
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = (token, userData) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(userData));
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);

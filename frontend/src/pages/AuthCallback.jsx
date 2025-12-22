import React, { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { jwtDecode } from 'jwt-decode';

const AuthCallback = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { login } = useAuth();

  useEffect(() => {
    const token = searchParams.get('token');
    if (token) {
      try {
        const decoded = jwtDecode(token);
        // The token payload structure depends on backend/app/auth/jwt_utils.py
        // Assuming it has 'sub' as username.
        const userData = {
          username: decoded.sub,
          email: decoded.email,
          github_id: decoded.id
        };
        login(token, userData);
        navigate('/dashboard');
      } catch (error) {
        console.error('Invalid token', error);
        navigate('/login');
      }
    } else {
      navigate('/login');
    }
  }, [searchParams, login, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900"></div>
    </div>
  );
};

export default AuthCallback;

import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../api/axios';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  
  const [targetUsername, setTargetUsername] = useState('');
  const [githubToken, setGithubToken] = useState('');
  const [resumeHtml, setResumeHtml] = useState('');
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState('ui'); // 'ui' or 'formal'
  const [showSettings, setShowSettings] = useState(true);

  useEffect(() => {
    if (user?.username) {
      setTargetUsername(user.username);
    }
  }, [user]);

  const fetchResume = async (currentMode = mode) => {
    if (!targetUsername) return;
    
    setLoading(true);
    try {
      const params = {};
      if (githubToken) params.token = githubToken;
      
      const response = await api.get(`/generate/${targetUsername}/${currentMode}`, { params });
      setResumeHtml(response.data);
    } catch (error) {
      console.error("Failed to fetch resume", error);
      setResumeHtml(`<div class="p-4 text-red-600">Error: ${error.response?.data?.detail || error.message}</div>`);
    } finally {
      setLoading(false);
    }
  };

  const handleSummarize = async () => {
    if (!targetUsername) return;

    setLoading(true);
    try {
      const params = { format: mode };
      if (githubToken) params.token = githubToken;

      const response = await api.get(`/generate/${targetUsername}/summarized`, { params });
      setResumeHtml(response.data);
    } catch (error) {
      console.error("Failed to summarize resume", error);
      setResumeHtml(`<div class="p-4 text-red-600">Error: ${error.response?.data?.detail || error.message}</div>`);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPdf = async () => {
    if (!targetUsername) return;
    
    setLoading(true);
    try {
      const params = {};
      if (githubToken) params.token = githubToken;

      const response = await api.get(`/generate/${targetUsername}/pdf`, {
        params,
        responseType: 'blob',
      });
      
      // Create a blob from the response data
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      
      // Create a temporary link element
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${targetUsername}_resume.pdf`);
      
      // Append to body, click, and remove
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      // Clean up the URL object
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Failed to download PDF", error);
      alert(`Failed to download PDF: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Auto-Resume Dashboard</h1>
          <div className="flex items-center space-x-4">
            {user ? (
              <>
                <span className="text-gray-700">Welcome, {user.username}</span>
                <button
                  onClick={logout}
                  className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
                >
                  Logout
                </button>
              </>
            ) : (
              <button
                onClick={() => navigate('/login')}
                className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-gray-800 hover:bg-gray-900"
              >
                Login with GitHub
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto py-6 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row gap-6 h-full">
          {/* Controls Sidebar */}
          <div className="w-full md:w-80 bg-white p-4 rounded-lg shadow space-y-6 h-fit">
            
            {/* Configuration Section */}
            <div className="space-y-4 border-b pb-4">
              <h2 className="text-lg font-medium text-gray-900 flex justify-between items-center cursor-pointer" onClick={() => setShowSettings(!showSettings)}>
                Configuration
                <span className="text-sm text-gray-500">{showSettings ? '▼' : '▶'}</span>
              </h2>
              
              {showSettings && (
                <div className="space-y-3">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">GitHub Username</label>
                    <input
                      type="text"
                      value={targetUsername}
                      onChange={(e) => setTargetUsername(e.target.value)}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                      placeholder="e.g. kentsao"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      GitHub Token <span className="text-xs text-gray-500">(Optional)</span>
                    </label>
                    <input
                      type="password"
                      value={githubToken}
                      onChange={(e) => setGithubToken(e.target.value)}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                      placeholder="ghp_..."
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      Required for private repos or higher rate limits.
                    </p>
                  </div>

                  <button
                    onClick={() => fetchResume(mode)}
                    disabled={loading || !targetUsername}
                    className="w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
                  >
                    {loading ? 'Generating...' : 'Generate Resume'}
                  </button>
                </div>
              )}
            </div>

            {/* Actions Section */}
            <div className="space-y-4">
              <h2 className="text-lg font-medium text-gray-900">Actions</h2>
              
              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">Template Mode</label>
                <div className="flex space-x-2">
                  <button
                    onClick={() => { setMode('ui'); fetchResume('ui'); }}
                    className={`flex-1 px-3 py-2 text-sm rounded-md ${
                      mode === 'ui' 
                        ? 'bg-blue-600 text-white' 
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                  >
                    Creative
                  </button>
                  <button
                    onClick={() => { setMode('formal'); fetchResume('formal'); }}
                    className={`flex-1 px-3 py-2 text-sm rounded-md ${
                      mode === 'formal' 
                        ? 'bg-blue-600 text-white' 
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                  >
                    Formal
                  </button>
                </div>
              </div>

              <button
                onClick={handleSummarize}
                disabled={loading || !targetUsername}
                className="w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700 disabled:opacity-50"
              >
                {loading ? 'Processing...' : 'Summarize with AI'}
              </button>

              <button
                onClick={handleDownloadPdf}
                disabled={loading || !targetUsername}
                className="w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 disabled:opacity-50"
              >
                Download PDF
              </button>
            </div>
          </div>

          {/* Preview Area */}
          <div className="flex-1 bg-white rounded-lg shadow overflow-hidden min-h-[600px] relative">
            {loading && (
              <div className="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center z-10">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              </div>
            )}
            <div className="w-full h-full overflow-auto p-4">
               {resumeHtml ? (
                 <iframe 
                   srcDoc={resumeHtml} 
                   title="Resume Preview"
                   className="w-full h-full min-h-[800px] border-0"
                 />
               ) : (
                 <div className="flex flex-col items-center justify-center h-full text-gray-500">
                   <svg className="w-16 h-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                   </svg>
                   <p className="text-lg">Enter a GitHub username to generate a resume</p>
                 </div>
               )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;

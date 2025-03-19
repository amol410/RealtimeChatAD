import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000';

// Function to retrieve CSRF token from cookies
function getCSRFToken() {
  const cookie = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='));
  return cookie ? cookie.split('=')[1] : '';
}

// Function to check if the user is authenticated
export const isAuthenticated = async () => {
  try {
    const response = await axiosInstance.get('/auth/status/');
    return response.data.authenticated;  // Ensure your backend provides this route
  } catch (error) {
    console.error('Authentication check failed:', error);
    return false;
  }
};

// Create an Axios instance with session authentication
const axiosInstance = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,  // ✅ Ensures session cookies are sent with requests
});

// Function to handle API errors gracefully
const handleError = (error) => {
  console.error('API Error:', error.response?.data || error.message);
  throw error.response?.data || error.message;
};

// GET request (No CSRF needed)
export const get = (url) => {
  return axiosInstance.get(url)
    .then(response => response.data)
    .catch(handleError);
};

// POST request
export const post = (url, data) => {
  return axiosInstance.post(url, data, {
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken(),  // ✅ Ensures CSRF protection
    }
  })
    .then(response => response.data)
    .catch(handleError);
};

// PUT request
export const put = (url, data) => {
  return axiosInstance.put(url, data, {
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken(),
    }
  })
    .then(response => response.data)
    .catch(handleError);
};

// DELETE request
export const del = (url) => {
  return axiosInstance.delete(url, {
    headers: {
      'X-CSRFToken': getCSRFToken(),
    }
  })
    .then(response => response.data)
    .catch(handleError);
};

export default axiosInstance;

import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000'; // Ensure Django runs on this

// Create an Axios instance with default settings
const axiosInstance = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCSRFToken(), // ✅ CSRF token for Django
  },
  withCredentials: true, // ✅ Helps with session-based auth
});

// Function to retrieve CSRF token from cookies
function getCSRFToken() {
  const cookie = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='));
  return cookie ? cookie.split('=')[1] : '';
}

// Function to handle API errors gracefully
const handleError = (error) => {
  console.error('API Error:', error.response?.data || error.message);
  throw error.response?.data || error.message;
};

// GET request
export const get = (url) => {
  return axiosInstance.get(url)
    .then(response => response.data)
    .catch(handleError);
};

// POST request
export const post = (url, data) => {
  return axiosInstance.post(url, data)
    .then(response => response.data)
    .catch(handleError);
};

// PUT request
export const put = (url, data) => {
  return axiosInstance.put(url, data)
    .then(response => response.data)
    .catch(handleError);
};

// DELETE request
export const del = (url) => {
  return axiosInstance.delete(url)
    .then(response => response.data)
    .catch(handleError);
};

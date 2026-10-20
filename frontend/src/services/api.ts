import axios, { AxiosError, AxiosInstance } from 'axios';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export const apiClient: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
});

export interface FormattedError {
  message: string;
  statusCode?: number;
  detail?: string;
  isNetworkError: boolean;
  isTimeout: boolean;
}

export function parseApiError(error: unknown): FormattedError {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<{ detail?: string; message?: string }>;

    if (axiosError.code === 'ECONNABORTED') {
      return {
        message: 'Request timed out. The AI model or server took too long to respond.',
        statusCode: 408,
        isNetworkError: false,
        isTimeout: true,
      };
    }

    if (!axiosError.response) {
      return {
        message: `Unable to connect to backend at ${BASE_URL}. Ensure the FastAPI server is running on port 8000.`,
        statusCode: 0,
        isNetworkError: true,
        isTimeout: false,
      };
    }

    const status = axiosError.response.status;
    const data = axiosError.response.data;
    const detail = typeof data === 'object' && data !== null ? data.detail || data.message : undefined;

    let message = detail || axiosError.message;
    if (status === 404) {
      message = detail || 'Resource not found.';
    } else if (status === 409) {
      message = detail || 'State conflict: this item has already been modified.';
    } else if (status === 422) {
      message = detail || 'Validation error: invalid request payload or parameters.';
    } else if (status >= 500) {
      message = detail || 'Internal backend server error.';
    }

    return {
      message,
      statusCode: status,
      detail: typeof detail === 'string' ? detail : JSON.stringify(detail),
      isNetworkError: false,
      isTimeout: false,
    };
  }

  if (error instanceof Error) {
    return {
      message: error.message,
      isNetworkError: false,
      isTimeout: false,
    };
  }

  return {
    message: 'An unexpected error occurred.',
    isNetworkError: false,
    isTimeout: false,
  };
}

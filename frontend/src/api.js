import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/secret';

// Создаем экземпляр axios с базовыми настройками
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Обработчик ошибок
const handleError = (error) => {
  if (error.response) {
    // Для 422 ошибки возвращаем весь объект ошибки
    if (error.response.status === 422) {
      throw error; // Передаем как есть для специальной обработки
    }
    // Сервер ответил с кодом ошибки
    throw new Error(error.response.data.detail || 'An error occurred');
  } else if (error.request) {
    // Запрос был сделан, но ответ не получен
    throw new Error('No response from server');
  } else {
    // Ошибка при настройке запроса
    throw new Error('Request setup error');
  }
};

export default {
  async createSecret(data) {
    try {
      const response = await api.post('/', data);
      return response.data;
    } catch (error) {
      handleError(error);
    }
  },

  async getSecret(accessKey) {
    try {
      const response = await api.get(`/${accessKey}`);
      return response.data;
    } catch (error) {
      handleError(error);
    }
  },

  async updateSecret(accessKey, data) {
    try {
      // Для PATCH запроса с необязательными полями
      const response = await api.patch(`/${accessKey}`, data);
      return response.status === 204;
    } catch (error) {
      handleError(error);
    }
  },

  async deleteSecret(accessKey) {
    try {
      const response = await api.delete(`/${accessKey}`);
      return response.status === 204;
    } catch (error) {
      handleError(error);
    }
  },

  async getSecretLifetime(accessKey) {
    try {
      const response = await api.get(`/lifetime/${accessKey}`);
      return response.data;
    } catch (error) {
      handleError(error);
    }
  },
};
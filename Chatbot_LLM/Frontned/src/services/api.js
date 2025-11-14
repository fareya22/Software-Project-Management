const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

export const chatAPI = {
  async sendMessage(message) {
    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data.response;
    } catch (error) {
      console.error('API Error:', error);
      throw new Error('Failed to send message. Please try again.');
    }
  },

  async checkHealth() {
    try {
      const response = await fetch(`${API_BASE_URL}/`);
      return response.ok;
    } catch (error) {
      return false;
    }
  }
};
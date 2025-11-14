# 🤖 LLM Chatbot - Assignment-1

A modern, responsive AI-powered chatbot application built with React frontend and FastAPI backend, featuring real-time messaging and neural network integration.

## 👥 Group Members

| Name | Roll |
|------|----|
| Mosamma Sultana Trina | BSSE-1313 |
| Md. Mostafizur Rahaman | BSSE-1320 |
| Fareya Azam | BSSE-1331 |

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Real-time Chat Interface**: Modern, responsive UI with smooth animations
- **AI-Powered Responses**: Integrated with Google Gemini AI for intelligent, well-formatted conversations
- **Code Explanation**: Clean formatting for technical code explanations with syntax highlighting

## 🛠 Technology Stack

### Frontend
- **React 18** - Modern JavaScript library for building user interfaces
- **Tailwind CSS** - Utility-first CSS framework for styling
- **Lucide React** - Beautiful icon library
- **Custom Hooks** - For state management and API calls

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Google Gemini AI** - Google's latest AI model (Gemini 1.5 Flash) for natural language processing
- **python-dotenv** - Environment variable management
- **CORS Middleware** - Cross-origin resource sharing support

### Development Tools
- **Node.js** - JavaScript runtime for frontend
- **Python 3.13** - Programming language for backend
- **Git** - Version control system

## 📋 Prerequisites

Before running this project, ensure you have the following installed:

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **Git**
- **Gemini Api key** (for AI functionality)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/MdMostafizurRahaman/Software-Project-Management.git
cd Chatbot
```

### 2. Backend Setup
```bash
cd Backend

# Install Python dependencies
pip install fastapi uvicorn google-generativeai python-dotenv

# Create .env file with your Gemini API key
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
```

### 3. Frontend Setup
```bash
cd ../Frontned

# Install Node.js dependencies
npm install

# Create .env file
echo "REACT_APP_BACKEND_URL=http://localhost:8000" > .env
```

## 🎯 Usage

### Running the Application

1. **Start Backend Server:**
   ```bash
   cd Backend
   python main.py
   ```
   Backend will run on `http://localhost:8000`

2. **Start Frontend Server:**
   ```bash
   cd Frontned
   npm start
   ```
   Frontend will run on `http://localhost:3000`

3. **Access the Application:**
   Open your browser and navigate to `http://localhost:3000`

### Using the Chatbot

1. Type your message in the input field
2. Press Enter or click the Send button
3. Wait for the AI response
4. Continue the conversation!

## 📁 Project Structure

```
ChatBot/
├── Backend/
│   ├── main.py              # FastAPI application
│   ├── .env                 # Environment variables
│   └── .gitignore          # Git ignore rules
├── Frontned/
│   ├── public/
│   │   └── index.html      # HTML template
│   ├── src/
│   │   ├── components/
│   │   │   └── ChatbotMessenger.js  # Main chat component
│   │   ├── hooks/
│   │   │   └── useChat.js           # Custom chat hook
│   │   ├── services/
│   │   │   └── api.js               # API service layer
│   │   ├── App.js                   # Root component
│   │   ├── index.js                 # React entry point
│   │   └── index.css                # Global styles
│   ├── package.json         # Node dependencies
│   ├── tailwind.config.js   # Tailwind configuration
│   └── .env                 # Frontend environment variables
└── README.md                # Project documentation
```

## 📚 API Documentation

### Backend Endpoints

#### GET `/`
Returns server status information.

**Response:**
```json
{
  "message": "Chatbot API is running"
}
```

#### POST `/chat`
Sends a message to the AI and receives a response.

**Request Body:**
```json
{
  "message": "Hello, how are you?"
}
```

**Response:**
```json
{
  "response": "Hi there! I'm doing well, thank you for asking. How can I help you today?"
}
```

**Error Response:**
```json
{
  "response": "Error: [error message]"
}
```

<img src="./Screenshort/image%20copy.png" width="300" alt="Screenshot 1"/> <img src="./Screenshort/image.png" width="300" alt="Screenshot 2"/>


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments
- **OpenAI** for the Python client library
- **FastAPI** for the excellent web framework
- **React** for the powerful frontend library
- **Tailwind CSS** for the utility-first styling approach

---

**Assignment 1 - LLM Chatbot** | **Submitted by Group: Mostafizur Rahaman, Mosamma Sultana Trina, Fareya Azam**


For any questions or support, please contact the group members.



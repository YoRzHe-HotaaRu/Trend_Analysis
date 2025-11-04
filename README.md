# 🚆 KV Transit Analytics

<div align="center">

**Advanced transportation and attractions visualization platform for Klang Valley**

[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=for-the-badge&logo=react&logoColor=white)](https://reactjs.org/)
[![Material-UI](https://img.shields.io/badge/Material--UI-5.14.18-1976d2?style=for-the-badge&logo=mui&logoColor=white)](https://mui.com/)
[![Leaflet](https://img.shields.io/badge/Leaflet-1.9.4-199D48?style=for-the-badge&logo=leaflet&logoColor=white)](https://leafletjs.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Latest-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

## 📋 Table of Contents

- [Overview](#-overview)
- [🎯 Features](#-features)
- [🛠️ Technology Stack](#️-technology-stack)
- [⚡ Quick Start](#️-quick-start)
- [📁 Project Structure](#-project-structure)
- [🔧 API Documentation](#-api-documentation)
- [👨‍💻 Author](#-author)
- [📄 License](#-license)

## 🌟 Overview

**KV Transit Analytics** is a comprehensive web application that provides real-time visualization and analysis of transportation networks and attractions across the Klang Valley region in Malaysia. This platform combines interactive mapping, real-time data analytics, and trend analysis to offer valuable insights for urban planning, transportation management, and public awareness.

### 🎯 Key Objectives

- **Real-time Transit Monitoring**: Track live transit data and system performance
- **Interactive Visualization**: Explore transportation networks and attractions through dynamic maps
- **Data Analytics**: Analyze patterns, trends, and performance metrics
- **User-Friendly Interface**: Provide intuitive navigation and responsive design
- **Academic Excellence**: Showcase Computer Science skills at UiTM level

## 🎯 Features

### 🗺️ Interactive Map View
- **Real-time Transit Data**: Live monitoring of LRT, MRT, BRT, and KTM systems
- **Attraction Layer**: Shopping malls, restaurants, and entertainment venues
- **Dynamic Layer Controls**: Toggle different data layers on/off
- **Responsive Design**: Optimized for desktop and mobile devices

### 📊 Real-time Dashboard
- **Live Statistics**: Active routes, passenger counts, and system metrics
- **Performance Indicators**: On-time performance, efficiency rates, and delay tracking
- **Transit Distribution**: Visual breakdown of different transportation modes
- **Trend Monitoring**: Real-time updates every 30 seconds

### 📈 Trend Analysis
- **Historical Data**: Analyze transportation patterns over time
- **Comparative Analytics**: Compare different time periods and routes
- **Visual Charts**: Interactive graphs powered by Chart.js

### ⏰ Time Controls
- **Flexible Time Ranges**: Real-time, hourly, daily, weekly, and monthly views
- **Custom Date Selection**: Choose specific dates for historical analysis
- **Dynamic Updates**: Automatic data refresh based on selected time range

</div>

## 🛠️ Technology Stack

### Frontend Technologies
- **React 18.2.0** - Modern JavaScript library for building user interfaces
- **Material-UI (MUI) 5.14.18** - Comprehensive React component library
- **React-Leaflet 4.2.1** - Interactive maps integration
- **Chart.js 4.4.0** - Beautiful charts and data visualization
- **Axios, React-Query** - Data fetching and state management
- **Vite 5.0.2** - Fast build tool and development server

### Backend Technologies
- **Python Flask** - Lightweight web framework
- **SQLite** - Database management
- **SQLAlchemy** - Python SQL toolkit and ORM
- **External APIs** - Real-time data integration (Foursquare, Google Places, Grab, OSM)

## ⚡ Quick Start

### Prerequisites
- **Node.js** v16.0.0 or higher
- **Python** v3.8 or higher
- **npm** package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/kv-transit-analytics.git
   cd kv-transit-analytics
   ```

2. **Setup Frontend**
   ```bash
   npm install
   ```

3. **Setup Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Start Development Servers**
   ```bash
   # Terminal 1 - Backend
   cd backend
   python app.py

   # Terminal 2 - Frontend
   npm run dev
   ```

5. **Access the Application**
   - **Frontend**: http://localhost:5173
   - **Backend API**: http://localhost:5000

### Build for Production
```bash
npm run build
npm run preview
```

## 📁 Project Structure

```
kv-transit-analytics/
├── src/                          # Frontend source code
│   ├── components/
│   │   ├── Dashboard/            # Dashboard components
│   │   │   ├── RealTimeStats.jsx
│   │   │   └── TrendCharts.jsx
│   │   └── Map/                  # Map-related components
│   │       ├── AttractionLayer.jsx
│   │       ├── InteractiveMap.jsx
│   │       ├── TemporalController.jsx
│   │       └── TransitLayer.jsx
│   ├── hooks/
│   │   └── useDataFetch.js
│   ├── theme/
│   │   └── lightTheme.js
│   ├── App.jsx                   # Main application component
│   └── main.jsx                  # Application entry point
├── backend/                      # Backend source code
│   ├── api/                      # API routes and handlers
│   ├── models/                   # Data models
│   ├── utils/                    # Utility functions
│   ├── external_apis/            # External API integrations
│   └── app.py                    # Flask application entry point
├── package.json
└── README.md
```

## 🔧 API Documentation

### Base URL
```
Development: http://localhost:5000/api
```

### Key Endpoints

#### Transit Data
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/transit/real-time` | Get real-time transit data |
| GET | `/transit/stations` | Get all transit stations |
| GET | `/transit/routes` | Get transit route information |

#### Attractions Data
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/attractions/active` | Get active attractions data |
| GET | `/attractions/categories` | Get attraction categories |
| GET | `/attractions/search` | Search attractions by query |

#### Dashboard Statistics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dashboard/stats` | Get real-time dashboard statistics |

### Example Response

**Real-time Transit Data:**
```json
{
  "success": true,
  "data": [
    {
      "id": "station_001",
      "name": "KLCC Station",
      "type": "LRT",
      "latitude": 3.1478,
      "longitude": 101.6953,
      "passenger_count": 1247,
      "status": "operational",
      "last_updated": "2025-11-04T10:30:00Z"
    }
  ]
}
```

## 👨‍💻 Author

<div align="center">

**Amir Hafizi Bin Musa**  
*UiTM Computer Science Student*

[![📧 Email](https://img.shields.io/badge/Email-amir.hafizi.uitm%40student.com-blue?style=for-the-badge&logo=gmail&logoColor=white)](mailto:amir.hafizi.uitm@student.com)
[![💼 LinkedIn](https://img.shields.io/badge/LinkedIn-amir-hafizi-musa-5530b9364?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/amir-hafizi-musa-5530b9364/)
[![🐙 GitHub](https://img.shields.io/badge/GitHub-@YoRzHe-HotaaRu?style=for-the-badge&logo=github&logoColor=white)](https://github.com/amirhafizi)

</div>

### 🎓 Academic Information
- **Institution**: Universiti Teknologi MARA (UiTM)
- **Program**: Bachelor of Computer Science (Hons.)
- **Year**: 2025
- **Specialization**: LLMs & Web Development

### 🏆 Skills Demonstrated
- **Frontend Development**: React, Material-UI, Responsive Design
- **Backend Development**: Python Flask, RESTful APIs
- **Database Management**: SQLite, SQLAlchemy
- **Data Visualization**: Chart.js, Leaflet, Interactive Maps
- **Version Control**: Git, GitHub Workflow

### 🚀 Future Enhancements
- [ ] Mobile app development (React Native)
- [ ] Machine learning integration for predictive analytics
- [ ] Integration with live transit APIs
- [ ] Multi-language support (English, Bahasa Malaysia, Chinese)
- [ ] Advanced filtering and search capabilities
- [ ] User authentication and personalization

## 📄 License

<div align="center">

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**MIT License - see the [LICENSE](LICENSE) file for details**

</div>

---

<div align="center">

[![Made with ❤️ in Malaysia](https://img.shields.io/badge/Made%20with%20%E2%9D%A4%EF%B8%8F-in%20Malaysia-red?style=for-the-badge)](https://www.uitm.edu.my/)
[![Built with Modern Tech](https://img.shields.io/badge/Built%20with-React%20%7C%20MUI%20%7C%20Python-61DAFB%20%26%201976d2%20%26%203776AB?style=for-the-badge&logo=react&logoColor=white)](https://reactjs.org/)
[![Academic Project](https://img.shields.io/badge/Academic%20Project-UiTM%20Computer%20Science-FF6B35?style=for-the-badge)](https://www.uitm.edu.my/)

**© 2025 Amir Hafizi Bin Musa. All rights reserved.**

*This project demonstrates advanced full-stack web development skills as part of my Computer Science studies at UiTM.*

</div>

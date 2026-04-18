# 🐄 IoT-Based Cattle Health Monitoring System

<div align="center">

![GitHub Repo stars](https://img.shields.io/github/stars/yourusername/cattle-health-monitoring?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/yourusername/cattle-health-monitoring?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/yourusername/cattle-health-monitoring?style=for-the-badge)
![GitHub license](https://img.shields.io/github/license/yourusername/cattle-health-monitoring?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)
![Flask](https://img.shields.io/badge/Flask-Backend-black?style=for-the-badge\&logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge\&logo=mysql)
![Bootstrap](https://img.shields.io/badge/Bootstrap-Frontend-purple?style=for-the-badge\&logo=bootstrap)

### 🚀 Smart Livestock Monitoring Through IoT & Web Technology

A **production-ready full-stack web application** that monitors cattle health using IoT sensors and displays **real-time analytics, alerts, reports, cattle records, device status, and predictive insights** through a modern dashboard.

</div>

---

# 📖 Project Overview

The **IoT-Based Cattle Health Monitoring System** is designed to help farmers and veterinarians monitor the health of cattle remotely using wearable IoT devices.

The system collects sensor data such as:

* 🌡 Body Temperature
* ❤️ Heart Rate
* 🫁 Blood Oxygen (SpO₂)
* 🐾 Motion / Activity Tracking

This data is stored in a **MySQL database** and visualized in a **modern web dashboard** built using Flask + Bootstrap.

It helps detect:

* Fever
* Low oxygen level
* Inactivity
* Potential illness
* Device failures

---

# ✨ Features

## 🔐 Authentication & Roles

* Farmer Registration / Login
* Veterinarian Login
* Role-Based Access
* Secure Password Hashing
* Session Management
* Logout System

---

## 📊 Smart Dashboard

* Total Cattle Count
* Active Devices Count
* Healthy Animals
* At Risk Animals
* Alerts Summary
* Last Sync Time
* Real-Time Temperature Graph
* Recent Alerts Panel
* Auto Refresh Every 30 Seconds

---

## 🐄 Cattle Management

* Add New Cattle
* Edit Cattle Details
* Delete Cattle
* Upload Cattle Photo
* Breed / Age / Weight Tracking
* Individual Cattle Profile

---

## 📈 Health Monitoring

* Live Temperature
* Heart Rate
* SpO₂ Levels
* Motion Status
* Historical Graphs
* Health Trend Analysis

---

## 🚨 Alerts Engine

Automatic alerts when:

| Condition     | Alert            |
| ------------- | ---------------- |
| Temp > 39.5°C | Fever            |
| SpO₂ < 90%    | Risk             |
| Low Movement  | Possible Illness |

---

## 📄 Reports System

* Export CSV Reports
* Export PDF Reports
* Temperature Analytics
* Cattle Performance Reports

---

## 📱 Responsive UI

* Mobile Friendly
* Tablet Compatible
* Desktop Optimized
* Sidebar Navigation
* SaaS Style Dashboard
* Soft Gradient Cards

---

# 🧠 Hardware Sensors Used

| Sensor          | Purpose                |
| --------------- | ---------------------- |
| DS18B20         | Body Temperature       |
| MAX30102        | Heart Rate + SpO₂      |
| MPU6050         | Motion / Accelerometer |
| ESP32 / NodeMCU | Data Transmission      |

---

# 🛠 Tech Stack

## Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript
* Chart.js
* Font Awesome

## Backend

* Python
* Flask
* Flask Login
* Flask SQLAlchemy
* Flask Bcrypt

## Database

* MySQL

## Optional IoT Layer

* MQTT
* ESP32
* REST API

---

# 📁 Folder Structure

```bash
cattle-health-monitoring/
│── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── templates/
│   └── static/
│       ├── css/
│       ├── js/
│       └── uploads/
│
│── sql/
│   └── schema.sql
│
│── requirements.txt
│── run.py
│── README.md
```

---

# 🗄 Database Schema

## Tables Used

### users

* id
* name
* email
* password
* role

### cattle

* id
* cattle_tag
* breed
* age
* weight
* photo
* owner_id

### devices

* id
* device_id
* device_serial
* cattle_id
* install_date
* status

### health_data
* id
* cattle_id
* temp
* heart_rate
* spo2
* motion
* timestamp

### alerts
* id
* cattle_id
* device_id
* message
* severity
* timestamp

---

# 📊 Dashboard Modules

## Main Cards

* 🐄 Total Cattle
* 🔗 Connected Devices
* 💚 Healthy
* ⚠ Alerts
* 🔴 At Risk

## Graphs

* Temperature Trend
* Health Trends
* Reports Charts

## Other Sections

* Latest Alerts
* Notification Center
* Data Sync Status

---

# 🔐 Authentication System

```python
Login
Register
Session Management
Password Hashing
Logout
Protected Routes
```

---

# 📡 API Endpoints

| Endpoint               | Method | Description        |
| ---------------------- | ------ | ------------------ |
| /login                 | POST   | User Login         |
| /register              | POST   | Register User      |
| /api/cattle            | GET    | Get All Cattle     |
| /api/health-data       | GET    | Latest Health Data |
| /api/alerts            | GET    | Alerts List        |
| /api/dashboard/summary | GET    | Dashboard Stats    |

---

# ⚙️ Installation Guide

## 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/cattle-health-monitoring.git
cd cattle-health-monitoring
```

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

## 3️⃣ Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

## 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 5️⃣ Configure Database

Create MySQL database:

```sql
CREATE DATABASE cattle_health_db;
```

Import schema:

```bash
mysql -u root -p cattle_health_db < sql/schema.sql
```

## 6️⃣ Run Server

```bash
python run.py
```

---

# ▶️ Run Project

Open Browser:

```bash
http://127.0.0.1:5000
```

---

# 📷 Screenshots

> Add your project screenshots here

```md
/assets/dashboard.png
/assets/login.png
/assets/reports.png
```

---

# 📈 Future Enhancements

* AI-Based Disease Prediction
* SMS Alerts
* MQTT Live Sensor Feed
* GPS Tracking
* Milk Yield Prediction

---

# 🤝 Contributing

Contributions are welcome.

```bash
1. Fork Repository
2. Create Feature Branch
3. Commit Changes
4. Push Branch
5. Create Pull Request
```

---

# 📜 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

### Wahid Jamadar (Software Developer & AI Enthusiast)
* Full Stack Developer
* Python & Flask Developer

---

<div align="center">

### ⭐ If you like this project, give it a Star on GitHub ⭐

### 🚀 Built with Passion + Code + Innovation

</div>

# Afya-Sentinel
# Afya Sentinel 🌍🩺
**AI-Powered Healthcare Crisis Prediction for Kenya**

[![Azure](https://img.shields.io/badge/Microsoft_Azure-0089D6?logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

<div align="center">
  <img src="https://github.com/yourusername/afya-sentinel/raw/main/images/logo.png" width="300" alt="Afya Sentinel Logo">
</div>

## 🚀 Key Features
- **Early Outbreak Detection**: Predict disease surges 2-4 weeks before they occur
- **Hospital Capacity Forecasting**: AI models track bed/ICU availability in real-time
- **Multilingual Alerts**: Swahili/English recommendations for health workers
- **Azure AI Integration**: Anomaly detection + NLP for social media monitoring
- **Kenya-First Design**: Tailored to county-level health protocols

## 📊 Live Demo
[![Demo Video](https://img.shields.io/badge/Watch_Demo-FF0000?logo=youtube&logoColor=white)](https://youtu.be/demo-link)

Access our test dashboard:  
🔗 [https://afya-sentinel.azurewebsites.net](https://afya-sentinel.azurewebsites.net)  
*(Test credentials: guest/Pass1234)*

## 🔧 Tech Stack
| Component               | Technology Used                          |
|-------------------------|-----------------------------------------|
| **Backend**             | Python Flask, Azure Functions           |
| **AI/ML**               | Azure Anomaly Detector, Gemini API      |
| **Data Pipeline**       | Microsoft Fabric, Azure Data Factory    |
| **Frontend**            | HTML5, Tailwind CSS, Chart.js           |
| **Deployment**          | Azure App Service, Docker               |

## 📂 Repository Structure


## 🛠️ Setup Guide

### Prerequisites
- Azure account with credits
- Python 3.9+
- Azure CLI installed

### Installation
```bash
# Clone repo
git clone https://github.com/yourusername/afya-sentinel.git
cd afya-sentinel

# Install dependencies
pip install -r requirements.txt

# Set environment variables
echo "AZURE_KEY=your_key" > .env

# Run locally
python app/main.py

az login
az webapp up --name afya-sentinel --resource-group kenya-health-rg --runtime "PYTHON:3.9"

🤝 How to Contribute
Fork the repository

Create a feature branch (git checkout -b feature/improvement)

Submit a Pull Request


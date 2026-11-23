# 📦 SupplyChainTracker

A lightweight web-based **Supply Chain Tracking and Inventory Management System** built with **Python, Flask, SQLite, HTML, CSS, and JavaScript**.

SupplyChainTracker helps users manage shipments, track shipment status, monitor inventory, and manage basic system settings through a simple and user-friendly dashboard.

## 🚀 Features

- 📊 **Dashboard** — View an overview of supply chain activities.
- 🚚 **Shipment Management** — Add, view, and manage shipment records.
- 🔎 **Track Shipment** — Search shipments using a shipment tracking code.
- 📦 **Inventory Management** — Manage and monitor inventory items.
- ⚙️ **Settings** — Manage basic application settings.
- ⚠️ **Error Handling** — User-friendly error page for invalid or unavailable requests.
- 💾 **SQLite Database** — Lightweight local database for storing application data.
- 🖥️ **Responsive Web Interface** — Clean and simple interface for easy navigation.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| 🐍 Python | Backend development |
| 🌐 Flask | Web application framework |
| 🗄️ SQLite | Database management |
| 🎨 HTML5 | Web page structure |
| 🎨 CSS3 | Styling and layout |
| ⚡ JavaScript | Client-side functionality |

## 📁 Project Structure

```text
SupplyChainTracker/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── static/
│   ├── script.js
│   └── style.css
│
└── templates/
    ├── index.html
    ├── shipments.html
    ├── track.html
    ├── inventory.html
    ├── settings.html
    └── error.html
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/chinmay05886/SupplyChainTracker.git
```

### 2. Navigate to the project directory

```bash
cd SupplyChainTracker
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python app.py
```

### 7. Open the application

Open the local Flask server in your browser:

```text
http://127.0.0.1:5000
```

## 🔄 How It Works

```text
User
  ↓
Web Interface
  ↓
Flask Application
  ↓
Application Logic
  ↓
SQLite Database
  ↓
Data displayed on Web Interface
```

Users interact with the web interface to manage shipments and inventory. Flask processes the requests and communicates with the SQLite database to store and retrieve information.

## 🧩 Main Modules

### 🚚 Shipments
Manage shipment information and monitor shipment progress through tracking codes and shipment statuses.

### 🔎 Tracking
Search for a shipment using its tracking code and view its current information.

### 📦 Inventory
Maintain inventory records and monitor available stock.

### 📊 Dashboard
Provides a centralized overview of the application's supply-chain information.

### ⚙️ Settings
Provides basic application configuration options.

## 🗃️ Database

SupplyChainTracker uses **SQLite** as its database.

The application maintains data such as:

- Shipment records
- Shipment status
- Tracking codes
- Inventory information
- Customer-related shipment information

The SQLite database is stored locally and is excluded from version control where appropriate.

## 🧪 Testing

The application was tested locally to verify:

- ✅ Shipment creation and management
- ✅ Shipment tracking
- ✅ Inventory operations
- ✅ Navigation between pages
- ✅ Database operations
- ✅ Invalid request/error handling
- ✅ Application startup and routing

## 🔐 Error Handling

The application includes basic error handling to provide a better user experience when an invalid route or unavailable resource is requested.

A custom `error.html` page is used to display user-friendly error information instead of exposing technical details.

## 🎯 Project Objective

The main objective of SupplyChainTracker is to demonstrate how a **Python Flask web application** can be used to build a simple supply-chain management system with database integration and a user-friendly frontend.

## 📚 Learning Outcomes

Through this project, the following practical concepts were implemented:

- Python web development
- Flask routing
- HTML/CSS/JavaScript integration
- SQLite database operations
- CRUD-based application logic
- Form handling
- Request and response handling
- Error handling
- Frontend-backend integration
- Git and GitHub version control

## 🔮 Future Improvements

Possible future enhancements include:

- 🔐 User authentication and role-based access
- 📱 Improved mobile responsiveness
- 📈 Advanced analytics and reporting
- 📊 Shipment and inventory charts
- 🔔 Shipment status notifications
- ☁️ Cloud database integration
- 🚀 Deployment to a production hosting platform
- 🔗 REST API integration

## 👨‍💻 Author

**Chinmay Deshpande**

B.E. Computer Science Engineering Student

GitHub: [chinmay05886](https://github.com/chinmay05886)

---

⭐ If you find this project useful, consider giving the repository a star!
# ☕ First Cup Coffee - Full-Stack Cafe Ordering System

First Cup Coffee is a modern, full-stack web application designed for a cafe environment. It allows customers to easily browse a dynamic menu, add items to their cart, and place orders directly from their table. The system also includes a backend component to manage orders and a simple kitchen display interface to view incoming requests.


---

## ✨ Features

* **Dynamic Menu:** Menu items and categories are fetched from a backend API, allowing for easy updates without changing the frontend code.
* **Interactive Cart:** A persistent shopping cart that uses `localStorage` to remember a user's items even if they refresh the page.
* **Seamless Ordering:** Customers can place orders by providing their table number. The order is then sent to a persistent SQLite database.
* **Backend API:** A robust Flask API handles all business logic, including menu management, order processing, and data persistence.
* **Kitchen Display System:** A dedicated `/kitchen.html` page that fetches and displays active orders in real-time for the kitchen staff.
* **Responsive Design:** A clean, mobile-first interface built with vanilla HTML, CSS, and JavaScript.

---

## 🛠️ Technology Stack

### Backend
* **Python 3**: Core programming language.
* **Flask**: A lightweight web framework for building the API.
* **Flask-CORS**: Handles Cross-Origin Resource Sharing to allow the frontend and backend to communicate.
* **SQLite3**: A serverless, file-based database for storing orders and menu items.

### Frontend
* **HTML5**: Standard markup for the web pages.
* **CSS3**: Custom styling for a modern look and feel.
* **Vanilla JavaScript (ES6+)**: Handles all client-side logic, interactivity, and API communication using the `fetch` API.

---

## 📂 Project Structure

The project is organized into two main folders for clear separation of concerns.
.
├── backend/
│   ├── app.py              # Main Flask application with all API endpoints
│   └── cafe_orders.db      # SQLite database (created automatically)
│
├── frontend/
│   ├── index.html          # Main customer ordering interface
│   ├── kitchen.html        # Kitchen Display System interface
│   ├── style.css           # All CSS styles
│   └── app.js              # JavaScript for the customer interface (index.html)
│   └── kitchen.js          # JavaScript for the KDS (kitchen.html)
│
├── README.md               # This file
└── script.py               # Python Flask backend

---

## 🚀 Setup and Installation

To run this project locally, follow these steps.

### Prerequisites
* Python 3.8+
* `pip` (Python package installer)
* A code editor like VS Code with the **Live Server** extension (recommended for the frontend).

### 1. Backend Setup

First, set up a virtual environment and install the required packages.

```bash
# 1. Clone the repository
git clone https://github.com/PreetishMajumdar/Coffee-Ordering-System.git
cd Coffee-Ordering-System

# 2. Navigate to the backend directory
cd backend

# 3. Create a virtual environment
python -m venv venv

# 4. Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 5. Install the required packages
pip install Flask Flask-CORS

# 6. Run the Flask server
python app.py
Your backend API should now be running at http://localhost:5000.
2. Frontend Setup
The frontend is served as a set of static files. The easiest way to run it is with the Live Server extension in VS Code.

Open the frontend folder in Visual Studio Code.
Right-click the index.html file.
Select "Open with Live Server".

A browser window will open, usually at http://127.0.0.1:5500, where you can use the application. To view the kitchen display, open kitchen.html with Live Server.

📋 API Endpoints
The Flask backend provides the following RESTful API endpoints:
MethodEndpointDescriptionGET/api/menuGet the complete menu with all categories.POST/api/ordersCreate a new order.GET/api/ordersGet a list of all orders.GET/api/orders/<order_id>Get details for a specific order by ID.PUT/api/orders/<order_id>/statusUpdate the status of an existing order.GET/api/statsGet daily statistics (total orders, revenue).

🔮 Future Improvements
This project serves as a solid foundation. Future enhancements could include:

Real-time Order Updates: Implement WebSockets to push new orders to the kitchen display instantly.
Admin Dashboard: A secure admin panel to add, edit, or delete menu items directly from the browser.
User Authentication: Allow regular customers to create accounts and view their order history.
Payment Gateway Integration: Integrate a payment provider like Stripe or Razorpay.
Order History: Add functionality to view past orders and reorder favorite items.
Inventory Management: Track ingredient availability and automatically disable unavailable items.


🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

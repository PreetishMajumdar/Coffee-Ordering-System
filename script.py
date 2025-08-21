# Create a comprehensive Python Flask backend for the First Cup Coffee ordering system
import os

# Create the main Flask application file
app_py_content = '''
from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import json
import uuid
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database initialization
def init_db():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect('cafe_orders.db')
    cursor = conn.cursor()
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            customer_name TEXT,
            table_number INTEGER,
            items TEXT,  -- JSON string of items
            total_amount REAL,
            status TEXT DEFAULT 'pending',
            order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            estimated_time INTEGER DEFAULT 15
        )
    ''')
    
    # Create menu_items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu_items (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            available BOOLEAN DEFAULT 1,
            image_url TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Menu data - same as frontend
MENU_DATA = {
    "coffee": {
        "title": "Coffee & Espresso",
        "icon": "☕",
        "items": [
            {"id": "americano", "name": "Americano", "description": "Rich espresso with hot water", "price": 120, "image": "☕"},
            {"id": "latte", "name": "Latte", "description": "Creamy espresso with steamed milk", "price": 150, "image": "🥛"},
            {"id": "cappuccino", "name": "Cappuccino", "description": "Perfect balance of espresso, steamed milk and foam", "price": 140, "image": "☕"},
            {"id": "mocha", "name": "Mocha", "description": "Chocolate and espresso blend with steamed milk", "price": 170, "image": "🍫"},
            {"id": "espresso", "name": "Espresso", "description": "Pure, concentrated coffee shot", "price": 100, "image": "☕"},
            {"id": "flatwhite", "name": "Flat White", "description": "Double espresso with microfoam milk", "price": 160, "image": "🥛"}
        ]
    },
    "cold": {
        "title": "Cold Beverages",
        "icon": "🧊",
        "items": [
            {"id": "iced-americano", "name": "Iced Americano", "description": "Chilled espresso with cold water", "price": 130, "image": "🧊"},
            {"id": "iced-latte", "name": "Iced Latte", "description": "Cold espresso with milk over ice", "price": 160, "image": "🥤"},
            {"id": "cold-brew", "name": "Cold Brew", "description": "Smooth, slow-brewed cold coffee", "price": 140, "image": "🧊"},
            {"id": "frappe", "name": "Frappe", "description": "Blended iced coffee drink", "price": 180, "image": "🥤"},
            {"id": "iced-mocha", "name": "Iced Mocha", "description": "Cold chocolate coffee delight", "price": 190, "image": "🍫"}
        ]
    },
    "tea": {
        "title": "Tea & Other Drinks",
        "icon": "🍵",
        "items": [
            {"id": "masala-chai", "name": "Masala Chai", "description": "Traditional spiced Indian tea", "price": 80, "image": "🍵"},
            {"id": "green-tea", "name": "Green Tea", "description": "Light and refreshing antioxidant tea", "price": 70, "image": "🍃"},
            {"id": "earl-grey", "name": "Earl Grey", "description": "Classic black tea with bergamot", "price": 90, "image": "🍵"},
            {"id": "hot-chocolate", "name": "Hot Chocolate", "description": "Rich cocoa with steamed milk", "price": 120, "image": "☕"},
            {"id": "matcha-latte", "name": "Matcha Latte", "description": "Japanese green tea with steamed milk", "price": 180, "image": "🍃"}
        ]
    },
    "pastries": {
        "title": "Pastries & Baked Goods",
        "icon": "🥐",
        "items": [
            {"id": "chocolate-croissant", "name": "Chocolate Croissant", "description": "Buttery croissant with chocolate", "price": 80, "image": "🥐"},
            {"id": "blueberry-muffin", "name": "Blueberry Muffin", "description": "Fresh baked with real blueberries", "price": 70, "image": "🧁"},
            {"id": "chocolate-chip-cookie", "name": "Chocolate Chip Cookie", "description": "Warm, gooey classic cookie", "price": 50, "image": "🍪"},
            {"id": "red-velvet-cupcake", "name": "Red Velvet Cupcake", "description": "Moist cake with cream cheese frosting", "price": 90, "image": "🧁"},
            {"id": "banana-bread", "name": "Banana Bread", "description": "Homemade moist banana bread slice", "price": 60, "image": "🍞"}
        ]
    },
    "breakfast": {
        "title": "Breakfast & Light Meals",
        "icon": "🍽️",
        "items": [
            {"id": "avocado-toast", "name": "Avocado Toast", "description": "Smashed avocado on artisan bread", "price": 180, "image": "🥑"},
            {"id": "grilled-sandwich", "name": "Grilled Sandwich", "description": "Cheese and vegetable grilled sandwich", "price": 120, "image": "🥪"},
            {"id": "caesar-salad", "name": "Caesar Salad", "description": "Crisp lettuce with parmesan and croutons", "price": 160, "image": "🥗"},
            {"id": "breakfast-bagel", "name": "Breakfast Bagel", "description": "Everything bagel with cream cheese", "price": 100, "image": "🥯"},
            {"id": "pancakes", "name": "Pancakes", "description": "Fluffy pancakes with maple syrup", "price": 140, "image": "🥞"}
        ]
    }
}

@app.route('/')
def index():
    """Serve a simple API documentation page"""
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>First Cup Coffee - API Backend</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { color: #007bff; font-weight: bold; }
            h1 { color: #333; text-align: center; }
            code { background: #e9ecef; padding: 2px 4px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>☕ First Cup Coffee - Backend API</h1>
        <p>Welcome to the First Cup Coffee ordering system backend. This Flask server provides REST API endpoints for the cafe ordering system.</p>
        
        <h2>🚀 Available Endpoints:</h2>
        
        <div class="endpoint">
            <div class="method">GET</div>
            <h3>/api/menu</h3>
            <p>Get the complete menu with all categories and items</p>
        </div>
        
        <div class="endpoint">
            <div class="method">GET</div>
            <h3>/api/menu/&lt;category&gt;</h3>
            <p>Get menu items for a specific category (coffee, cold, tea, pastries, breakfast)</p>
        </div>
        
        <div class="endpoint">
            <div class="method">POST</div>
            <h3>/api/orders</h3>
            <p>Create a new order</p>
            <p>Body: <code>{"items": [...], "table_number": 5, "customer_name": "Optional"}</code></p>
        </div>
        
        <div class="endpoint">
            <div class="method">GET</div>
            <h3>/api/orders</h3>
            <p>Get all orders (for admin/kitchen display)</p>
        </div>
        
        <div class="endpoint">
            <div class="method">GET</div>
            <h3>/api/orders/&lt;order_id&gt;</h3>
            <p>Get specific order details</p>
        </div>
        
        <div class="endpoint">
            <div class="method">PUT</div>
            <h3>/api/orders/&lt;order_id&gt;/status</h3>
            <p>Update order status (pending, preparing, ready, completed)</p>
            <p>Body: <code>{"status": "preparing"}</code></p>
        </div>
        
        <h2>📊 Database Status:</h2>
        <p>Database initialized successfully with orders and menu_items tables.</p>
        
        <h2>🔧 Usage:</h2>
        <p>Start the server with: <code>python app.py</code></p>
        <p>Access the web frontend at: <code>/frontend</code></p>
        <p>This backend is designed to work with the First Cup Coffee web ordering interface.</p>
    </body>
    </html>
    '''
    return html_content

@app.route('/api/menu')
def get_menu():
    """Get the complete menu"""
    return jsonify(MENU_DATA)

@app.route('/api/menu/<category>')
def get_category_menu(category):
    """Get menu items for a specific category"""
    if category in MENU_DATA:
        return jsonify(MENU_DATA[category])
    else:
        return jsonify({"error": "Category not found"}), 404

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new order"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'items' not in data or 'table_number' not in data:
            return jsonify({"error": "Missing required fields: items, table_number"}), 400
        
        # Validate table number
        table_number = data.get('table_number')
        if not isinstance(table_number, int) or table_number < 1 or table_number > 50:
            return jsonify({"error": "Table number must be between 1 and 50"}), 400
        
        # Generate unique order ID
        order_id = str(uuid.uuid4())[:8].upper()
        
        # Calculate total amount
        total_amount = 0
        for item in data['items']:
            total_amount += item.get('price', 0) * item.get('quantity', 1)
        
        # Estimate preparation time (base: 5 min + 2 min per item)
        item_count = sum(item.get('quantity', 1) for item in data['items'])
        estimated_time = 5 + (item_count * 2)
        
        # Save to database
        conn = sqlite3.connect('cafe_orders.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO orders (id, customer_name, table_number, items, total_amount, estimated_time)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            order_id,
            data.get('customer_name', ''),
            table_number,
            json.dumps(data['items']),
            total_amount,
            estimated_time
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "success": True,
            "order_id": order_id,
            "total_amount": total_amount,
            "estimated_time": estimated_time,
            "message": "Order placed successfully!"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Get all orders (for kitchen display)"""
    try:
        conn = sqlite3.connect('cafe_orders.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, customer_name, table_number, items, total_amount, status, order_time, estimated_time
            FROM orders
            ORDER BY order_time DESC
        ''')
        
        orders = []
        for row in cursor.fetchall():
            orders.append({
                "id": row[0],
                "customer_name": row[1],
                "table_number": row[2],
                "items": json.loads(row[3]),
                "total_amount": row[4],
                "status": row[5],
                "order_time": row[6],
                "estimated_time": row[7]
            })
        
        conn.close()
        return jsonify(orders)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders/<order_id>')
def get_order(order_id):
    """Get specific order details"""
    try:
        conn = sqlite3.connect('cafe_orders.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, customer_name, table_number, items, total_amount, status, order_time, estimated_time
            FROM orders
            WHERE id = ?
        ''', (order_id,))
        
        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "Order not found"}), 404
        
        order = {
            "id": row[0],
            "customer_name": row[1],
            "table_number": row[2],
            "items": json.loads(row[3]),
            "total_amount": row[4],
            "status": row[5],
            "order_time": row[6],
            "estimated_time": row[7]
        }
        
        conn.close()
        return jsonify(order)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update order status"""
    try:
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({"error": "Status is required"}), 400
        
        valid_statuses = ['pending', 'preparing', 'ready', 'completed', 'cancelled']
        if data['status'] not in valid_statuses:
            return jsonify({"error": f"Status must be one of: {valid_statuses}"}), 400
        
        conn = sqlite3.connect('cafe_orders.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE orders
            SET status = ?
            WHERE id = ?
        ''', (data['status'], order_id))
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Order not found"}), 404
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": f"Order status updated to {data['status']}"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Get basic statistics for the cafe"""
    try:
        conn = sqlite3.connect('cafe_orders.db')
        cursor = conn.cursor()
        
        # Total orders today
        cursor.execute('''
            SELECT COUNT(*), SUM(total_amount)
            FROM orders
            WHERE date(order_time) = date('now')
        ''')
        today_stats = cursor.fetchone()
        
        # Orders by status
        cursor.execute('''
            SELECT status, COUNT(*)
            FROM orders
            WHERE date(order_time) = date('now')
            GROUP BY status
        ''')
        status_stats = dict(cursor.fetchall())
        
        conn.close()
        
        return jsonify({
            "today": {
                "total_orders": today_stats[0] or 0,
                "total_revenue": today_stats[1] or 0
            },
            "status_breakdown": status_stats
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("🚀 Starting First Cup Coffee Backend Server...")
    print("📱 Frontend web app should be served separately")
    print("🔧 API endpoints available at /api/")
    print("📊 Visit / for API documentation")
    app.run(debug=True, host='0.0.0.0', port=5000)
'''

# Write the Flask application to file
with open('app.py', 'w') as f:
    f.write(app_py_content)

print("✅ Flask backend app.py created successfully!")
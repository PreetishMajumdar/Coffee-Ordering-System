// NEW: API base URL
const API_BASE_URL = 'http://localhost:5000/api';

// NEW: This will be populated by the API call
let menuData = {}; 

// Global state
let cart = [];
let currentCategory = null;

// NEW: Function to fetch menu from the backend
async function loadMenuData() {
    console.log('Fetching menu data from API...');
    try {
        const response = await fetch(`${API_BASE_URL}/menu`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        menuData = await response.json();
        console.log('Menu data loaded successfully.');
    } catch (error) {
        console.error('Failed to load menu data:', error);
        showToast('Error: Could not load the menu.');
    }
}

// MODIFIED: App initialization is now async
document.addEventListener('DOMContentLoaded', async () => {
    console.log('DOM Content Loaded - Initializing app...');
    
    await loadMenuData(); // Wait for menu to load first!
    
    loadCart();
    updateCartBadge();
    setupEventListeners();
    
    // Hide loading screen
    const loadingScreen = document.getElementById('loadingScreen');
    if (loadingScreen) loadingScreen.classList.add('hidden');
    
    console.log('App initialization complete');
});

// MODIFIED: This function now correctly handles clicks using data-attributes
function setupEventListeners() {
    // Category cards
    document.querySelectorAll('.category-card').forEach(card => {
        card.addEventListener('click', () => {
            const categoryKey = card.dataset.category; // Read the data-category attribute
            if (categoryKey) showCategory(categoryKey);
        });
    });
    
    // Header controls
    document.querySelector('.logo').addEventListener('click', showHome);
    document.querySelector('.cart-icon').addEventListener('click', showCart);

    // Page navigation buttons
    document.getElementById('backToHomeBtn').addEventListener('click', showHome);
    document.getElementById('backToHomeFromCartBtn').addEventListener('click', showHome);
    document.getElementById('browseMenuBtn').addEventListener('click', showHome);
    document.getElementById('placeOrderBtn').addEventListener('click', showOrderConfirmation);
    document.getElementById('clearCartBtn').addEventListener('click', clearCart);
    document.getElementById('confirmOrderBtn').addEventListener('click', confirmOrder);
    document.getElementById('newOrderBtn').addEventListener('click', newOrder);
}


// --- All functions below are the final, working versions ---

// Cart management
function loadCart() { try { const s = localStorage.getItem('FirstCupCart'); if(s){cart=JSON.parse(s);} } catch(e){cart=[];} }
function saveCart() { localStorage.setItem('FirstCupCart', JSON.stringify(cart)); }
function addToCart(itemId, categoryKey) { const item = menuData[categoryKey].items.find(i=>i.id===itemId); if (!item) return; const qtyEl = document.querySelector(`[data-item-id="${itemId}"] .quantity-display`); const quantity = parseInt(qtyEl.textContent) || 1; const existing = cart.find(ci=>ci.id===itemId); if (existing) { existing.quantity += quantity; } else { cart.push({ ...item, quantity }); } qtyEl.textContent = '1'; saveCart(); updateCartBadge(); showToast(`${item.name} added!`); }
function removeFromCart(itemId) { cart=cart.filter(i=>i.id!==itemId); saveCart(); updateCartBadge(); renderCart(); }
function updateCartQuantity(itemId, change) { const item=cart.find(i=>i.id===itemId); if (item) { item.quantity+=change; if (item.quantity<=0) { removeFromCart(itemId); } else { saveCart(); updateCartBadge(); renderCart(); } } }
function clearCart() { cart=[]; saveCart(); updateCartBadge(); renderCart(); }
function updateCartBadge() { const badge=document.getElementById('cartBadge'); if (!badge) return; const total=cart.reduce((s,i)=>s+i.quantity, 0); badge.textContent=total; badge.style.display=total>0?'flex':'none'; }

// Navigation
function hideAllPages() { document.querySelectorAll('.page').forEach(p=>p.classList.add('hidden')); }
function showHome() { hideAllPages(); document.getElementById('homePage').classList.remove('hidden'); }
function showCategory(key) { currentCategory=key; const cat=menuData[key]; if (!cat) return; hideAllPages(); document.getElementById('categoryTitle').textContent=cat.title; renderCategoryItems(cat); document.getElementById('categoryPage').classList.remove('hidden'); }
function showCart() { hideAllPages(); renderCart(); document.getElementById('cartPage').classList.remove('hidden'); }
function showOrderConfirmation() { if(cart.length===0){showToast('Your cart is empty'); return;} hideAllPages(); renderOrderSummary(); document.getElementById('orderPage').classList.remove('hidden'); document.querySelector('.table-number-section').classList.remove('hidden'); document.getElementById('orderConfirmed').classList.add('hidden'); document.getElementById('tableNumber').value = ''; }

// Rendering
function renderCategoryItems(cat) { 
    const grid = document.getElementById('itemsGrid'); 
    grid.innerHTML = ''; 
    cat.items.forEach(item => { 
        const el = document.createElement('div'); 
        el.className = 'item-card'; 
        el.dataset.itemId = item.id; 
        
        // MODIFIED: Changed this line to use an <img> tag for the image
        el.innerHTML = `<div class="item-image"><img src="${item.image}" alt="${item.name}"></div><div class="item-content"><h3 class="item-name">${item.name}</h3><p class="item-description">${item.description}</p><p class="item-price">₹${item.price}</p><div class="item-controls"><div class="quantity-controls"><button class="quantity-btn" onclick="updateItemQuantity('${item.id}',-1)">-</button><span class="quantity-display">1</span><button class="quantity-btn" onclick="updateItemQuantity('${item.id}',1)">+</button></div><button class="add-to-cart-btn" onclick="addToCart('${item.id}','${currentCategory}')">Add to Cart</button></div></div>`; 
        
        grid.appendChild(el); 
    }); 
}
function renderCart() { const cont=document.getElementById('cartItems'); const summ=document.getElementById('cartSummary'); const empty=document.getElementById('cartEmpty'); if(cart.length===0){cont.innerHTML=''; summ.style.display='none'; empty.classList.remove('hidden'); return;} empty.classList.add('hidden'); summ.style.display='block'; cont.innerHTML=''; let total=0; cart.forEach(item=>{ total+=item.price*item.quantity; const el=document.createElement('div'); el.className='cart-item'; el.innerHTML=`<div class="cart-item-info"><div class="cart-item-name">${item.name}</div><div class="cart-item-price">₹${item.price}</div></div><div class="cart-item-controls"><div class="quantity-controls"><button class="quantity-btn" onclick="updateCartQuantity('${item.id}',-1)">-</button><span class="quantity-display">${item.quantity}</span><button class="quantity-btn" onclick="updateCartQuantity('${item.id}',1)">+</button></div></div>`; cont.appendChild(el); }); document.getElementById('cartTotal').textContent=total; }
function renderOrderSummary() { const cont=document.getElementById('orderSummary'); let total=0; cont.innerHTML=''; cart.forEach(item=>{ total+=item.price*item.quantity; const el=document.createElement('div'); el.className='order-summary-item'; el.innerHTML=`<span>${item.name} × ${item.quantity}</span><span>₹${item.price*item.quantity}</span>`; cont.appendChild(el); }); document.getElementById('orderTotal').textContent=total; }
function updateItemQuantity(itemId, change) { const el=document.querySelector(`[data-item-id="${itemId}"] .quantity-display`); let q=parseInt(el.textContent); q+=change; if(q<1)q=1; if(q>99)q=99; el.textContent=q; }

// NEW: Order function integrated with backend
async function confirmOrder() {
    const tableInput = document.getElementById('tableNumber');
    const tableNumber = parseInt(tableInput.value);
    if (!tableNumber || tableNumber < 1 || tableNumber > 50) {
        showToast('Please enter a valid table number (1-50)');
        return;
    }
    const btn = document.getElementById('confirmOrderBtn');
    btn.disabled = true;
    btn.textContent = 'Placing...';

    try {
        const response = await fetch(`${API_BASE_URL}/orders`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ table_number: tableNumber, items: cart }),
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'Failed to place order');

        document.getElementById('orderId').textContent = result.order_id;
        document.getElementById('estimatedTime').textContent = result.estimated_time;
        document.querySelector('.table-number-section').classList.add('hidden');
        document.getElementById('orderConfirmed').classList.remove('hidden');
        
        cart = [];
        saveCart();
        updateCartBadge();
        showToast(`Order #${result.order_id} confirmed!`);
    } catch (error) {
        showToast(`Error: ${error.message}`);
    } finally {
        btn.disabled = false;
        btn.textContent = 'Confirm Order';
    }
}
function newOrder() { showHome(); }

// Utility function
function showToast(message) { const t=document.getElementById('toast'); const m=document.getElementById('toastMessage'); m.textContent=message; t.classList.remove('hidden'); t.classList.add('show'); setTimeout(()=>{t.classList.remove('show');setTimeout(()=>t.classList.add('hidden'),300)},3000); }

// Make essential functions globally available for inline onclicks in dynamically generated HTML
window.updateItemQuantity=updateItemQuantity; window.addToCart=addToCart; window.updateCartQuantity=updateCartQuantity; window.removeFromCart=removeFromCart;
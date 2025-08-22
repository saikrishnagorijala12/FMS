# 📌 Franchise Management System (FMS)

![License](https://img.shields.io/badge/license-MIT-blue.svg)  
![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)  
![Tech](https://img.shields.io/badge/stack-Angular%20%7C%20Python%20Flask%20%7C%20PostgreSQL-orange)  

## 📖 Overview  
The **Franchise Management System (FMS)** is a full-stack web application that streamlines **franchise operations** for businesses.  
It provides separate roles for:  
- **Franchisor (Owner)** → Manages franchises, products, commissions, and global analytics.  
- **Franchisee** → Manages inventory, orders, earnings, and requests stock.  
- **Customer** → Browses locations, buys products, and tracks orders.  

This system ensures **scalability, transparency, and efficiency** in managing multi-location franchise businesses.  

---

## ✨ Features  

### 🔑 Authentication & User Management  
- Secure **JWT-based login & registration**.  
- Role-based access control (**Franchisor, Franchisee, Customer**).  
- Profile management & password reset.  

### 🏢 Franchisor Features  
- Approve/reject franchise applications.  
- Add, update, delete products.  
- Manage commissions & earnings.  
- View global sales, analytics, and reports.  

### 🏪 Franchisee Features  
- Apply for a franchise.  
- Manage inventory & submit stock requests.  
- Process customer orders (Processing → Shipped → Delivered).  
- Withdraw earnings & pay commissions.  
- Dashboard with real-time sales & stock analytics.  

### 🛒 Customer Features  
- Browse franchises by location.  
- Search products & place orders.  
- Secure payments via card.  
- Track order history & status.  

### 📊 Reports & Analytics  
- Performance summary per franchise.  
- Financial analytics (growth, commissions, outstanding payments).  
- Exportable reports (CSV/Excel).  

### ⚡ Technical Highlights  
- **Frontend:** Angular, Bootstrap, RxJS  
- **Backend:** Python Flask (REST API)  
- **Database:** PostgreSQL  
- **Authentication:** JWT  
- **Deployment Ready:** Docker  

---

## 🛠️ Installation & Setup  

### Prerequisites  
- Node.js (>=16) & Angular CLI  
- Python (>=3.10) + pip  
- PostgreSQL (>=13)  
- Docker (optional for containerized deployment)  

### Frontend (Angular)  
```bash
cd frontend
npm install
ng serve -o
```

### Backend (Flask)  
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Database Setup  
```sql
CREATE DATABASE fms;
-- Run provided migrations
```

---

## 📂 Project Structure  

```
FMS/
│── frontend/           # Angular Frontend
│   ├── src/app/        # Components, services, guards
│── backend/            # Flask Backend
│   ├── models/         # SQLAlchemy models
│   ├── routes/         # API endpoints
│   ├── services/       # Business logic
│── docs/               # Documentation (RTM, Test Cases, Diagrams)
│── docker-compose.yml  # For containerized deployment
│── README.md           # Project Documentation
```

---

## 📸 Screenshots  

> _(Add actual screenshots later – placeholders below)_  

- **Franchisor Dashboard**  
  ![Dashboard Screenshot](docs/screenshots/franchisor_dashboard.png)  

- **Franchisee Inventory**  
  ![Inventory Screenshot](docs/screenshots/franchisee_inventory.png)  

- **Customer Ordering**  
  ![Customer Screenshot](docs/screenshots/customer_order.png)  

---

## ✅ Testing  

- **Manual Test Cases:** See [Test Cases Document](docs/FMS_Test_Cases.xlsx)  
- **Automation (Future Scope):** Cypress for UI, PyTest for API  

---

## 📌 Roadmap  
- [ ] Multi-language support 🌍  
- [ ] Mobile app integration 📱  
- [ ] AI-driven franchise performance prediction 🤖  
- [ ] Cloud deployment on AWS  

---

## 🤝 Contribution  

Contributions are welcome! 🎉  

1. Fork the repo  
2. Create a feature branch (`git checkout -b feature/new-feature`)  
3. Commit changes (`git commit -m "Add new feature"`)  
4. Push branch (`git push origin feature/new-feature`)  
5. Open a Pull Request  

---

## 📜 License  
This project is licensed under the **MIT License**.  

---

⚡ Built with ❤️ by **Sai Krishna Gorijala**

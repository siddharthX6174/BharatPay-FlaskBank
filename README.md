<div align="center">

# 🏦 Bharat Pay - Modern Banking Application

<p align="center">
  <img src="https://img.shields.io/badge/Flask-3.0.0-blue?style=for-the-badge&logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/Python-3.11+-green?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0-red?style=for-the-badge&logo=postgresql" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/TailwindCSS-3.0-38B2AC?style=for-the-badge&logo=tailwind-css" alt="Tailwind">
</p>

![Project img](app/static/root/assets/images/home.png)

<p align="center">
  A full-stack, production-ready banking web application with modern UI/UX, real-time insights, secure transactions, and comprehensive admin controls.
</p>

[Features](#-features) • [Quick Start](#-quick-start) • [Tech Stack](#-tech-stack) • [Documentation](#-documentation) • [Screenshots](#-screenshots)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [User Roles](#-user-roles)
- [API Routes](#-api-routes)
- [Database Schema](#-database-schema)
- [Security Features](#-security-features)
- [Screenshots](#-screenshots)
- [Development](#-development)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

**Bharat Pay** is a modern, full-stack banking application built with Flask and designed for educational purposes and rapid prototyping. It features a beautiful, responsive UI built with Tailwind CSS, comprehensive transaction management, real-time financial insights, and a powerful admin dashboard.

### Why Bharat Pay?

- ✅ **Production-Ready**: Secure authentication, CSRF protection, and validated transactions
- ✅ **Modern UI/UX**: Responsive design with Tailwind CSS, smooth animations, and intuitive navigation
- ✅ **Real-Time Insights**: Dynamic charts, transaction analytics, and financial trends
- ✅ **Admin Controls**: User management, profile approvals, and transaction monitoring
- ✅ **Beneficiary System**: Save frequent recipients for quick transfers
- ✅ **One-Command Setup**: Automated initialization script handles everything

---

## ✨ Features

### 🔐 Authentication & Security
- **Secure Registration**: Email validation, password strength requirements, bcrypt hashing
- **Login System**: Session-based authentication with remember-me functionality
- **Profile Management**: User onboarding with business details (PAN, GST, Aadhaar)
- **Account Verification**: Admin approval system for profile changes
- **CSRF Protection**: Form security with Flask-WTF tokens

### 💳 Banking Operations
- **Account Management**: Unique 13-digit account numbers (ACC format) and 16-digit card numbers
- **Deposits**: Add funds with transaction history tracking
- **Transfers**: Account-to-account money transfers with validation
- **Withdrawals**: Secure cash-out functionality with balance verification
- **Mobile Recharge**: Direct recharge with transaction logging
- **Receipt Generation**: Downloadable transaction receipts with templates

### 👥 Beneficiary System
- **Save Recipients**: Store frequently used transfer recipients
- **Quick Send**: One-click transfers to saved beneficiaries
- **Nickname Support**: Custom names for easy identification
- **Favorites**: Mark important beneficiaries
- **Usage Tracking**: Automatic tracking of last used date and transaction count

### 📊 Financial Insights Dashboard
- **Real-Time Balance**: Live balance updates with growth indicators
- **Transaction Analytics**: Category breakdown (deposits, transfers, withdrawals, recharges)
- **Weekly Activity Graph**: 7-day volume trend with SVG visualization
- **Monthly Reports**: Month-over-month comparisons
- **Virtual Card Display**: Interactive card with show/hide functionality

### 👨‍💼 Admin Dashboard
- **User Management**: View, search, and manage all users
- **Profile Approvals**: Review and approve user profile changes
- **Transaction Monitoring**: Track all transactions system-wide
- **Statistics Overview**: Total users, pending approvals, transaction volumes
- **Responsive Layout**: Mobile-friendly admin panel with hamburger menu

### 🎨 User Experience
- **Responsive Design**: Mobile-first approach, works on all devices
- **Modern UI**: Gradient cards, glass morphism, smooth transitions
- **Quick Actions**: Easy access to Send Money, Add Funds, Withdraw
- **Recent Transactions**: At-a-glance transaction history
- **Dark Mode Ready**: Prepared for theme switching (future enhancement)

---

## 🛠 Tech Stack

### Backend
- **Flask 3.0.0** - Modern Python web framework
- **SQLAlchemy 2.0** - ORM for database interactions
- **PostgreSQL/SQLite** - Flexible database support
- **Bcrypt** - Password hashing and security
- **Flask-Login** - Session management
- **Flask-WTF** - Form validation and CSRF protection

### Frontend
- **Tailwind CSS 3.x** - Utility-first CSS framework
- **Font Awesome 6** - Icon library
- **Vanilla JavaScript** - Interactive UI components
- **Jinja2** - Server-side templating engine

### Development Tools
- **Python 3.11+** - Modern Python features
- **pip** - Package management
- **Virtual Environment** - Isolated dependencies

---

## 📁 Project Structure

```
Flask-Banking-App/
├── 📄 start.py                      # Unified initialization & startup script
├── 📄 run.py                        # Flask application entrypoint
├── 📄 config.py                     # Configuration management
├── 📄 create_db.py                  # Database creation script
├── 📄 tables.py                     # Database table inspector
├── 📄 requirements.txt              # Python dependencies
├── 📄 README.md                     # This file
│
├── 📂 app/
│   ├── 📄 __init__.py               # Flask app initialization
│   ├── 📄 decorators.py             # Custom decorators (@approved_required, @admin_required)
│   │
│   ├── 📂 models/
│   │   └── 📂 user/
│   │       ├── 📄 user.py           # User model (account_number, card_number, balance)
│   │       ├── 📄 transaction.py    # Transaction model (transfers, deposits, etc.)
│   │       └── 📄 beneficiary.py    # Beneficiary model (saved recipients)
│   │
│   ├── 📂 routes/
│   │   ├── 📂 root/                 # Public routes
│   │   │   ├── 📄 index.py          # Homepage
│   │   │   ├── 📄 login.py          # User login
│   │   │   ├── 📄 register.py       # User registration
│   │   │   ├── 📄 about.py          # About page
│   │   │   ├── 📄 contact.py        # Contact page
│   │   │   └── 📄 services.py       # Services page
│   │   │
│   │   ├── 📂 user/                 # Protected user routes
│   │   │   ├── 📄 dashboard.py      # Main dashboard with insights
│   │   │   ├── 📄 deposit.py        # Add funds
│   │   │   ├── 📄 transfer.py       # Money transfers
│   │   │   ├── 📄 withdraw.py       # Cash withdrawals
│   │   │   ├── 📄 recharge.py       # Mobile recharges
│   │   │   ├── 📄 transaction_history.py  # Transaction logs
│   │   │   ├── 📄 receipt.py        # Receipt generation
│   │   │   ├── 📄 beneficiaries.py  # Manage beneficiaries
│   │   │   └── 📄 profile.py        # User profile management
│   │   │
│   │   └── 📂 admin/                # Admin-only routes
│   │       ├── 📄 dashboard.py      # Admin overview
│   │       ├── 📄 users.py          # User management
│   │       ├── 📄 profile_changes.py # Profile approval system
│   │       └── 📄 transactions.py   # Transaction monitoring
│   │
│   ├── 📂 static/
│   │   ├── 📂 root/assets/          # Public assets (CSS, JS, images)
│   │   └── 📂 user/assets/          # User dashboard assets
│   │
│   └── 📂 templates/
│       ├── 📂 root/                 # Public templates
│       │   ├── 📄 default.html      # Base layout
│       │   ├── 📄 index.html
│       │   ├── 📄 login.html
│       │   └── 📄 register.html
│       │
│       ├── 📂 user/                 # User templates
│       │   ├── 📄 default.html      # User base layout
│       │   ├── 📄 index.html        # Dashboard
│       │   ├── 📄 transfer.html
│       │   └── 📄 ...
│       │
│       └── 📂 admin/                # Admin templates
│           ├── 📄 default.html      # Admin base layout
│           ├── 📄 dashboard.html
│           └── 📄 ...
│
└── 📂 instance/
    └── 📄 banking.db                # SQLite database (auto-generated)
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git (optional)

### One-Command Setup (Recommended)

```bash
# Clone the repository (or download ZIP)
git clone <repository-url>
cd Flask-Banking-App

# Run the unified startup script
python start.py
```

**That's it!** The script will:
1. ✅ Install all dependencies from requirements.txt
2. ✅ Create the database and tables
3. ✅ Create default admin user (`admin@bwavebank.com` / `admin123`)
4. ✅ Start the Flask development server

Open your browser to: **http://127.0.0.1:5000**

### Manual Setup (Alternative)

```bash
# 1. Clone the repository
git clone <repository-url>
cd Flask-Banking-App

# 2. Create virtual environment (optional but recommended)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create database and tables
python create_db.py

# 5. Run the application
python3 start.py
```

### Default Admin Credentials
```
Email: admin@bwavebank.com
Password: admin123
```

> ⚠️ **Security Note**: Change the admin password immediately after first login in production environments.

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory (optional, defaults work for development):

```env
# Database Configuration
DB_URI=sqlite:///instance/banking.db
# For PostgreSQL:
# DB_URI=postgresql+psycopg2://user:password@localhost:5432/banking_db

# Flask Configuration
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True

# Optional Settings
AUTO_CREATE_TABLES=True
FLASK_ENV=development
```

### Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_URI` | Database connection string | `sqlite:///instance/banking.db` |
| `SECRET_KEY` | Flask session encryption key | Auto-generated |
| `DEBUG` | Enable debug mode | `True` |
| `AUTO_CREATE_TABLES` | Auto-create missing tables | `True` |

### Database Configuration

**SQLite (Default - Development)**
```python
DB_URI = "sqlite:///instance/banking.db"
```

**PostgreSQL (Production)**
```python
DB_URI = "postgresql+psycopg2://username:password@localhost:5432/banking_db"
```

---

## 👥 User Roles

### Regular User
- View personal dashboard with financial insights
- Perform transactions (deposit, transfer, withdraw, recharge)
- Manage beneficiaries
- View transaction history
- Generate transaction receipts
- Update profile (requires admin approval)

### Administrator
- Access admin dashboard with system statistics
- Manage all users (view, search, delete)
- Approve/reject profile change requests
- Monitor all transactions system-wide
- View pending approvals and alerts

---

## 🔌 API Routes

### Public Routes
```
GET  /                    - Homepage
GET  /about               - About page
GET  /services            - Services page
GET  /contact             - Contact page
GET  /login               - Login page
POST /login               - Process login
GET  /register            - Registration page
POST /register            - Process registration
GET  /logout              - Logout user
```

### User Routes (Protected)
```
GET  /dashboard           - Main dashboard with insights
GET  /deposit             - Deposit page
POST /deposit             - Process deposit
GET  /transfer            - Transfer money page
POST /transfer            - Process transfer
GET  /withdraw            - Withdrawal page
POST /withdraw            - Process withdrawal
GET  /recharge            - Recharge page
POST /recharge            - Process recharge
GET  /transaction-history - View all transactions
GET  /receipt/<id>        - Generate transaction receipt
GET  /beneficiaries       - Manage beneficiaries
POST /beneficiaries/add   - Add new beneficiary
POST /beneficiaries/delete/<id> - Remove beneficiary
GET  /profile             - User profile
POST /profile             - Update profile
```

### Admin Routes (Admin Only)
```
GET  /admin/dashboard     - Admin overview
GET  /admin/users         - User management
GET  /admin/profile-changes - Profile approval queue
POST /admin/approve/<id>  - Approve profile change
POST /admin/reject/<id>   - Reject profile change
GET  /admin/transactions  - Transaction monitoring
POST /admin/delete-user/<id> - Delete user
```

---

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    account_number VARCHAR(16) UNIQUE,  -- ACC1234567890123
    card_number VARCHAR(16) UNIQUE,     -- 16-digit card
    balance NUMERIC(12, 2) DEFAULT 0.00,
    is_admin BOOLEAN DEFAULT FALSE,
    is_approved BOOLEAN DEFAULT TRUE,
    
    -- Onboarding Fields
    business_name VARCHAR(150),
    pan_card VARCHAR(10),
    gst_number VARCHAR(15),
    aadhaar_number VARCHAR(12),
    address TEXT,
    
    created_at DATETIME DEFAULT NOW
);
```

### Transactions Table
```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    recipient_id INTEGER,
    recipient_name VARCHAR(100),
    recipient_card_number VARCHAR(16),  -- Stores account_number
    amount NUMERIC(12, 2) NOT NULL,
    type VARCHAR(25) NOT NULL,  -- transfer, deposit, withdrawal, recharge
    description TEXT,
    timestamp DATETIME DEFAULT NOW,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Beneficiaries Table
```sql
CREATE TABLE beneficiaries (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    beneficiary_name VARCHAR(100) NOT NULL,
    beneficiary_card_number VARCHAR(16) NOT NULL,  -- Stores account_number
    nickname VARCHAR(50),
    is_favorite BOOLEAN DEFAULT FALSE,
    last_used DATETIME,
    total_transactions INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT NOW,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Profile Change Log Table
```sql
CREATE TABLE profile_change_log (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    field_name VARCHAR(50) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    status VARCHAR(20) DEFAULT 'pending',  -- pending, approved, rejected
    requested_at DATETIME DEFAULT NOW,
    reviewed_at DATETIME,
    reviewed_by INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 🔒 Security Features

### Authentication
- ✅ **Bcrypt Password Hashing** - Industry-standard password encryption
- ✅ **Session Management** - Secure Flask sessions with secret key
- ✅ **Login Required Decorator** - Protected routes with `@login_required`
- ✅ **Approved User Decorator** - Additional layer with `@approved_required`
- ✅ **Admin Only Decorator** - Admin route protection with `@admin_required`

### Transaction Security
- ✅ **Balance Validation** - Prevents overdrafts and negative balances
- ✅ **Account Verification** - Validates recipient accounts exist
- ✅ **Atomic Transactions** - Database commits ensure consistency
- ✅ **Amount Validation** - Decimal precision and minimum checks
- ✅ **CSRF Protection** - Form tokens prevent cross-site attacks

### Data Protection
- ✅ **SQL Injection Prevention** - SQLAlchemy ORM parameterized queries
- ✅ **XSS Protection** - Jinja2 auto-escaping
- ✅ **Unique Constraints** - Email, account_number, card_number uniqueness
- ✅ **Audit Logging** - Profile change tracking with timestamps

### Best Practices
- Environment variables for sensitive data
- Separate admin and user permissions
- Profile change approval workflow
- Transaction history immutability
- Password strength requirements (implemented in forms)

---

## 📸 Screenshots

### User Dashboard
![Dashboard](app/static/root/assets/images/dashboard.png)

### Transfer Money
![transfer](app/static/root/assets/images/transfer.png)

### Admin Dashboard
![admin](app/static/root/assets/images/admin.png)

---

## 💻 Development

### Running Tests
```bash
# Unit tests
python -m pytest tests/

# Coverage report
python -m pytest --cov=app tests/
```

### Database Management

**View Tables**
```bash
python tables.py
```

**Reset Database**
```bash
# Delete database file
rm instance/banking.db

# Recreate
python create_db.py
```

**Migrations (Recommended for Production)**
```bash
# Install Flask-Migrate
pip install Flask-Migrate

# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

### Code Style
```bash
# Format with Black
black app/

# Lint with Flake8
flake8 app/

# Type checking with MyPy
mypy app/
```

---

## 🌐 Deployment

### Production Checklist
- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `DEBUG=False`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure proper WSGI server (Gunicorn, uWSGI)
- [ ] Set up reverse proxy (Nginx, Apache)
- [ ] Enable HTTPS with SSL certificate
- [ ] Configure environment variables securely
- [ ] Set up database backups
- [ ] Change default admin password
- [ ] Configure logging and monitoring

### Deploy with Gunicorn
```bash
# Install Gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Deploy with Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

### Deploy to Cloud Platforms
- **Heroku**: Add `Procfile` with `web: gunicorn run:app`
- **AWS Elastic Beanstalk**: Use `application.py` entrypoint
- **Google Cloud Run**: Containerize with Docker
- **Azure App Service**: Use Python 3.11 runtime

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Write descriptive commit messages
- Add tests for new features
- Update documentation as needed
- Keep code modular and reusable

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Flask** - Excellent Python web framework
- **Tailwind CSS** - Utility-first CSS framework
- **Font Awesome** - Beautiful icon library
- **SQLAlchemy** - Powerful ORM
- **Community** - All contributors and users

---

## 📞 Support

For questions, issues, or feature requests:

- 🐛 [Report Bug](https://github.com/yourusername/flask-banking-app/issues)
- 💡 [Request Feature](https://github.com/yourusername/flask-banking-app/issues)
- 📧 Email: support@bharatpay.com
- 💬 Discord: [Join our community](#)

---

<div align="center">

### ⭐ Star this repository if you find it helpful!

**Made with ❤️ by Your Team**

[Website](#) • [Documentation](#) • [Changelog](#) • [FAQ](#)

</div>


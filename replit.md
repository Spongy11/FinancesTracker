# Personal Finance Tracker

## Overview

A Streamlit-based personal finance tracking application that enables users to monitor their income, expenses, and investments with persistent PostgreSQL database storage. The application provides real-time financial metrics, visualizations, personalized insights, goal tracking, budget management, and expense forecasting to help users manage their finances effectively. Built with a focus on simplicity and user experience, it offers interactive dashboards for tracking financial health through key metrics like savings rate, spending patterns, and investment allocation.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit for rapid web application development with minimal frontend code
- **Layout**: Wide layout with expandable sidebar for navigation and input forms
- **Visualization**: Plotly (Express and Graph Objects) for interactive charts and financial dashboards
- **File Upload**: Support for CSV and Excel file imports for bulk transaction entry

### Database Architecture
- **Database**: PostgreSQL (Neon-backed) for persistent data storage
- **Connection**: psycopg2-binary for database connectivity
- **Tables**:
  - `income`: Stores income transactions (id, amount, category, date, description, created_at)
  - `expenses`: Stores expense transactions (id, amount, category, date, description, created_at)
  - `investments`: Stores investment transactions (id, amount, type, date, description, created_at)
  - `goals`: Stores financial goals (id, name, target_amount, current_amount, target_date, category, description, created_at)
  - `budgets`: Stores budget limits (id, category, monthly_limit, alert_threshold, active, created_at)

### Data Structure
- **Persistent Storage**: All financial data stored in PostgreSQL database
- **Data Categories**:
  - Income: 7 predefined categories (Salary, Freelance, Business, etc.)
  - Expenses: 12 predefined categories (Housing, Transportation, Food & Dining, etc.)
  - Investments: 9 predefined types (Stocks, Bonds, Mutual Funds, etc.)
- **Data Schema**: Each transaction contains:
  - amount: Numeric value (DECIMAL)
  - category/type: String from predefined lists
  - date: Timestamp for temporal analysis
  - description: Optional text field
  - created_at: Automatic timestamp

### Core Features

#### 1. Transaction Management
- Manual entry forms for income, expenses, and investments
- Data persists across sessions in PostgreSQL database
- Real-time data loading from database on each page load

#### 2. Dashboard & Visualizations
- Financial metrics calculation (income, expenses, investments, savings rate)
- Interactive charts:
  - Pie charts for expense breakdown
  - Bar charts for category spending
  - Line charts for income vs expenses timeline
  - Investment portfolio visualization
  - Gauge charts for savings rate

#### 3. CSV/Excel Import
- Bulk transaction upload from CSV or Excel files
- Support for importing income, expenses, and investments
- Preview data before import
- Validation and error handling

#### 4. Goal Tracking
- Create financial goals with target amounts and dates
- Track progress with visual progress bars
- Update current amounts toward goals
- Category-based goal organization
- Overall progress metrics

#### 5. Budget Management
- Set monthly spending limits by category
- Configurable alert thresholds (50-100%)
- Real-time budget tracking against current month spending
- Visual alerts when thresholds exceeded
- Budget vs actual comparison

#### 6. Expense Forecasting
- Historical trend analysis
- Monthly spending averages
- Next month expense predictions
- Category-level forecasts
- Trend visualization with line charts

#### 7. Reports & Insights
- Personalized savings tips based on spending patterns
- Detailed expense and income analysis
- CSV export for reports
- Savings rate tracking with goals

### Design Patterns
- **Database-Driven Architecture**: All data stored in PostgreSQL with CRUD operations
- **Modular Function Design**: Separated database functions for clean code organization
- **Category-Based Classification**: Predefined categories ensure consistent data entry
- **Real-time Data Loading**: Fresh data loaded from database on each interaction

### Pros and Cons

**Pros**:
- Persistent data storage across sessions
- Multi-user capable with database backend
- Scalable for large transaction volumes
- Data backup and recovery possible
- CSV/Excel import for bulk data entry
- Goal tracking and budget management
- Expense forecasting capabilities

**Cons**:
- Requires database connection
- Slightly slower than pure in-memory operations
- Database must be maintained
- No user authentication (single-user currently)

## External Dependencies

### Core Libraries
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive visualization library
- **numpy**: Numerical computing support
- **psycopg2-binary**: PostgreSQL database adapter
- **openpyxl**: Excel file reading support

### Python Standard Library
- **datetime**: Date and time handling
- **timedelta**: Time-based calculations
- **os**: Environment variable access

### Database
- **PostgreSQL**: Primary data storage (via Replit Neon integration)
- **Environment Variables**: DATABASE_URL, PGPORT, PGUSER, PGPASSWORD, PGDATABASE, PGHOST

## Recent Changes (November 2025)

### Database Integration
- Migrated from session-based storage to PostgreSQL database
- Created database schema with 5 tables (income, expenses, investments, goals, budgets)
- Implemented CRUD operations for all data types
- Added database initialization script (db_setup.py)

### New Features Added
- **CSV/Excel Import**: Bulk transaction upload with file validation and preview
- **Goal Tracking**: Create and monitor financial goals with progress visualization
- **Budget Management**: Set spending limits with threshold alerts
- **Expense Forecasting**: Predict future expenses based on historical trends
- **Enhanced Reports**: Added category-level forecasting and trend analysis

### UI Updates
- Added new navigation pages: Import Data, Goals, Budgets
- Updated sidebar with persistence indicator
- Improved data visualization with forecasting charts
- Added budget alert system with visual indicators

## Future Enhancement Considerations
- User authentication for multi-user support
- Bank API integrations for automatic transaction imports
- More sophisticated forecasting models (ML-based)
- Recurring transaction templates
- Custom report generation
- Data export to PDF
- Mobile-responsive design improvements
- Budget categories customization

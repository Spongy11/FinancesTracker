import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import psycopg2
import os

st.set_page_config(page_title="Personal Finance Tracker", layout="wide", initial_sidebar_state="expanded")

def get_db_connection():
    return psycopg2.connect(os.environ['DATABASE_URL'])

def load_income_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, amount, category, date, description FROM income ORDER BY date DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{'id': row[0], 'amount': float(row[1]), 'category': row[2], 'date': row[3], 'description': row[4]} for row in rows]

def load_expense_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, amount, category, date, description FROM expenses ORDER BY date DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{'id': row[0], 'amount': float(row[1]), 'category': row[2], 'date': row[3], 'description': row[4]} for row in rows]

def load_investment_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, amount, type, date, description FROM investments ORDER BY date DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{'id': row[0], 'amount': float(row[1]), 'type': row[2], 'date': row[3], 'description': row[4]} for row in rows]

def add_income(amount, category, date, description):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO income (amount, category, date, description) VALUES (%s, %s, %s, %s)",
                (amount, category, date, description))
    conn.commit()
    cur.close()
    conn.close()

def add_expense(amount, category, date, description):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO expenses (amount, category, date, description) VALUES (%s, %s, %s, %s)",
                (amount, category, date, description))
    conn.commit()
    cur.close()
    conn.close()

def add_investment(amount, type_name, date, description):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO investments (amount, type, date, description) VALUES (%s, %s, %s, %s)",
                (amount, type_name, date, description))
    conn.commit()
    cur.close()
    conn.close()

def clear_all_income():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM income")
    conn.commit()
    cur.close()
    conn.close()

def clear_all_expenses():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses")
    conn.commit()
    cur.close()
    conn.close()

def clear_all_investments():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM investments")
    conn.commit()
    cur.close()
    conn.close()

def delete_income(income_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM income WHERE id = %s", (income_id,))
    conn.commit()
    cur.close()
    conn.close()

def delete_expense(expense_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
    conn.commit()
    cur.close()
    conn.close()

def delete_investment(investment_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM investments WHERE id = %s", (investment_id,))
    conn.commit()
    cur.close()
    conn.close()

EXPENSE_CATEGORIES = [
    "Housing", "Transportation", "Food & Dining", "Utilities", 
    "Healthcare", "Entertainment", "Shopping", "Education", 
    "Personal Care", "Insurance", "Debt Payments", "Other"
]

INCOME_CATEGORIES = [
    "Salary", "Freelance", "Business", "Investment Returns", 
    "Rental Income", "Gifts", "Other"
]

INVESTMENT_TYPES = [
    "Stocks", "Bonds", "Mutual Funds", "ETFs", "Real Estate", 
    "Cryptocurrency", "Savings Account", "Retirement Account", "Other"
]

def calculate_financial_metrics(income_data, expense_data, investment_data):
    total_income = sum([item['amount'] for item in income_data])
    total_expenses = sum([item['amount'] for item in expense_data])
    total_investments = sum([item['amount'] for item in investment_data])
    
    net_savings = total_income - total_expenses - total_investments
    savings_rate = (net_savings / total_income * 100) if total_income > 0 else 0
    
    return {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'total_investments': total_investments,
        'net_savings': net_savings,
        'savings_rate': savings_rate
    }

def generate_financial_tips(metrics, expense_df):
    tips = []
    
    if metrics['savings_rate'] < 10:
        tips.append("⚠️ Your savings rate is below 10%. Experts recommend saving at least 20% of your income.")
    elif metrics['savings_rate'] < 20:
        tips.append("💡 Your savings rate is decent, but try to increase it to 20% or more for better financial security.")
    else:
        tips.append("✅ Great job! You're saving over 20% of your income, which is excellent.")
    
    if not expense_df.empty:
        expense_by_category = expense_df.groupby('category')['amount'].sum().sort_values(ascending=False)
        
        if len(expense_by_category) > 0:
            top_category = expense_by_category.index[0]
            top_amount = expense_by_category.iloc[0]
            top_percentage = (top_amount / metrics['total_expenses'] * 100) if metrics['total_expenses'] > 0 else 0
            
            if top_percentage > 30:
                tips.append(f"💰 {top_category} accounts for {top_percentage:.1f}% of your expenses. Consider reviewing this category for potential savings.")
            
            if 'Food & Dining' in expense_by_category.index:
                food_expense = expense_by_category['Food & Dining']
                food_percentage = (food_expense / metrics['total_expenses'] * 100) if metrics['total_expenses'] > 0 else 0
                if food_percentage > 15:
                    tips.append(f"🍽️ Food & Dining is {food_percentage:.1f}% of expenses. Meal planning and cooking at home could save you money.")
            
            if 'Entertainment' in expense_by_category.index:
                entertainment_expense = expense_by_category['Entertainment']
                entertainment_percentage = (entertainment_expense / metrics['total_expenses'] * 100) if metrics['total_expenses'] > 0 else 0
                if entertainment_percentage > 10:
                    tips.append(f"🎬 Entertainment expenses are {entertainment_percentage:.1f}% of total spending. Look for free or low-cost alternatives.")
    
    if metrics['total_investments'] == 0 and metrics['total_income'] > 0:
        tips.append("📈 You haven't logged any investments yet. Consider investing for long-term wealth building.")
    elif metrics['total_income'] > 0:
        investment_rate = (metrics['total_investments'] / metrics['total_income'] * 100)
        if investment_rate < 10:
            tips.append("📊 Try to invest at least 10-15% of your income for long-term financial growth.")
    
    if metrics['net_savings'] < 0:
        tips.append("🚨 You're spending more than you earn! Review your expenses immediately and create a budget.")
    
    tips.append("💡 Track your expenses regularly to identify spending patterns and areas for improvement.")
    tips.append("🎯 Set specific financial goals (emergency fund, retirement, vacation) to stay motivated.")
    
    return tips

income_data = load_income_data()
expense_data = load_expense_data()
investment_data = load_investment_data()

st.sidebar.title("💰 Finance Tracker")
page = st.sidebar.radio("Navigate", ["Home", "Dashboard", "Add Income", "Add Expense", "Add Investment", "Reports & Tips", "Import Data", "Goals", "Budgets"])

if page == "Home":
    st.title("🏠 Personal Finance Tracker")
    st.write("### Welcome to your Financial Management Dashboard")
    st.write("Track your income, expenses, investments, and achieve your financial goals!")
    
    st.divider()
    
    metrics = calculate_financial_metrics(income_data, expense_data, investment_data)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Income", f"${metrics['total_income']:,.2f}")
    with col2:
        st.metric("Total Expenses", f"${metrics['total_expenses']:,.2f}")
    with col3:
        st.metric("Total Investments", f"${metrics['total_investments']:,.2f}")
    with col4:
        st.metric("Net Savings", f"${metrics['net_savings']:,.2f}")
    
    st.divider()
    
    st.write("### Quick Navigation")
    st.write("Click on any button below to navigate to different sections:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 View Dashboard", use_container_width=True):
            st.session_state.nav_page = "Dashboard"
            st.rerun()
        
        if st.button("💵 Add Income", use_container_width=True):
            st.session_state.nav_page = "Add Income"
            st.rerun()
        
        if st.button("💳 Add Expense", use_container_width=True):
            st.session_state.nav_page = "Add Expense"
            st.rerun()
    
    with col2:
        if st.button("📈 Add Investment", use_container_width=True):
            st.session_state.nav_page = "Add Investment"
            st.rerun()
        
        if st.button("📥 Import Data", use_container_width=True):
            st.session_state.nav_page = "Import Data"
            st.rerun()
        
        if st.button("🎯 Manage Goals", use_container_width=True):
            st.session_state.nav_page = "Goals"
            st.rerun()
    
    with col3:
        if st.button("💰 Set Budgets", use_container_width=True):
            st.session_state.nav_page = "Budgets"
            st.rerun()
        
        if st.button("📋 Reports & Tips", use_container_width=True):
            st.session_state.nav_page = "Reports & Tips"
            st.rerun()
    
    st.divider()
    
    if income_data or expense_data or investment_data:
        st.write("### Recent Activity")
        
        recent_col1, recent_col2, recent_col3 = st.columns(3)
        
        with recent_col1:
            st.write("**Recent Income**")
            if income_data[:3]:
                for item in income_data[:3]:
                    st.write(f"• ${item['amount']:.2f} - {item['category']}")
            else:
                st.write("No income entries yet")
        
        with recent_col2:
            st.write("**Recent Expenses**")
            if expense_data[:3]:
                for item in expense_data[:3]:
                    st.write(f"• ${item['amount']:.2f} - {item['category']}")
            else:
                st.write("No expense entries yet")
        
        with recent_col3:
            st.write("**Recent Investments**")
            if investment_data[:3]:
                for item in investment_data[:3]:
                    st.write(f"• ${item['amount']:.2f} - {item['type']}")
            else:
                st.write("No investment entries yet")
    else:
        st.info("👋 Start by adding your first transaction using the navigation buttons above!")

elif page == "Dashboard":
    st.title("📊 Financial Dashboard")
    
    metrics = calculate_financial_metrics(income_data, expense_data, investment_data)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Income", f"${metrics['total_income']:,.2f}")
    with col2:
        st.metric("Total Expenses", f"${metrics['total_expenses']:,.2f}")
    with col3:
        st.metric("Total Investments", f"${metrics['total_investments']:,.2f}")
    with col4:
        st.metric("Net Savings", f"${metrics['net_savings']:,.2f}", 
                 delta=f"{metrics['savings_rate']:.1f}% savings rate")
    
    st.divider()
    
    if expense_data:
        st.subheader("💳 Expense Breakdown by Category")
        
        expense_df = pd.DataFrame(expense_data)
        expense_by_category = expense_df.groupby('category')['amount'].sum().reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pie = px.pie(expense_by_category, values='amount', names='category', 
                            title='Expenses by Category',
                            color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            fig_bar = px.bar(expense_by_category.sort_values('amount', ascending=True), 
                            x='amount', y='category', orientation='h',
                            title='Spending by Category',
                            color='amount',
                            color_continuous_scale='Reds')
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No expense data yet. Add some expenses to see visualizations!")
    
    st.divider()
    
    if income_data or expense_data:
        st.subheader("📈 Income vs Expenses Over Time")
        
        all_transactions = []
        
        for item in income_data:
            all_transactions.append({
                'date': item['date'],
                'type': 'Income',
                'amount': item['amount']
            })
        
        for item in expense_data:
            all_transactions.append({
                'date': item['date'],
                'type': 'Expense',
                'amount': item['amount']
            })
        
        if all_transactions:
            trans_df = pd.DataFrame(all_transactions)
            trans_df['date'] = pd.to_datetime(trans_df['date'])
            trans_df = trans_df.sort_values('date')
            
            daily_summary = trans_df.groupby(['date', 'type'])['amount'].sum().reset_index()
            
            fig_line = px.line(daily_summary, x='date', y='amount', color='type',
                             title='Income vs Expenses Timeline',
                             labels={'amount': 'Amount ($)', 'date': 'Date'},
                             color_discrete_map={'Income': '#2ecc71', 'Expense': '#e74c3c'})
            st.plotly_chart(fig_line, use_container_width=True)
    
    if investment_data:
        st.divider()
        st.subheader("💼 Investment Portfolio")
        
        investment_df = pd.DataFrame(investment_data)
        investment_by_type = investment_df.groupby('type')['amount'].sum().reset_index()
        
        fig_investment = px.bar(investment_by_type, x='type', y='amount',
                               title='Investments by Type',
                               color='amount',
                               color_continuous_scale='Blues')
        st.plotly_chart(fig_investment, use_container_width=True)

elif page == "Add Income":
    st.title("💵 Add Income")
    
    with st.form("income_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            income_amount = st.number_input("Amount ($)", min_value=0.0, step=0.01, format="%.2f")
            income_category = st.selectbox("Category", INCOME_CATEGORIES)
        
        with col2:
            income_date = st.date_input("Date", value=datetime.now())
            income_description = st.text_input("Description (Optional)")
        
        submitted = st.form_submit_button("Add Income")
        
        if submitted and income_amount > 0:
            add_income(income_amount, income_category, income_date, income_description)
            st.success(f"✅ Added ${income_amount:.2f} to {income_category}")
            st.rerun()
    
    st.divider()
    
    if income_data:
        st.subheader("Recent Income Entries")
        
        for idx, item in enumerate(income_data):
            col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 3, 1, 1])
            with col1:
                st.write(f"**${item['amount']:.2f}**")
            with col2:
                st.write(item['category'])
            with col3:
                st.write(str(item['date']))
            with col4:
                st.write(item['description'] if item['description'] else '-')
            with col5:
                if st.button("🗑️", key=f"del_income_{item['id']}"):
                    delete_income(item['id'])
                    st.success("Deleted!")
                    st.rerun()
            with col6:
                st.write("")
        
        st.divider()
        
        if st.button("Clear All Income Data"):
            clear_all_income()
            st.rerun()

elif page == "Add Expense":
    st.title("💳 Add Expense")
    
    with st.form("expense_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            expense_amount = st.number_input("Amount ($)", min_value=0.0, step=0.01, format="%.2f")
            expense_category = st.selectbox("Category", EXPENSE_CATEGORIES)
        
        with col2:
            expense_date = st.date_input("Date", value=datetime.now())
            expense_description = st.text_input("Description (Optional)")
        
        submitted = st.form_submit_button("Add Expense")
        
        if submitted and expense_amount > 0:
            add_expense(expense_amount, expense_category, expense_date, expense_description)
            st.success(f"✅ Added ${expense_amount:.2f} expense in {expense_category}")
            st.rerun()
    
    st.divider()
    
    if expense_data:
        st.subheader("Recent Expense Entries")
        
        for idx, item in enumerate(expense_data):
            col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 3, 1, 1])
            with col1:
                st.write(f"**${item['amount']:.2f}**")
            with col2:
                st.write(item['category'])
            with col3:
                st.write(str(item['date']))
            with col4:
                st.write(item['description'] if item['description'] else '-')
            with col5:
                if st.button("🗑️", key=f"del_expense_{item['id']}"):
                    delete_expense(item['id'])
                    st.success("Deleted!")
                    st.rerun()
            with col6:
                st.write("")
        
        st.divider()
        
        if st.button("Clear All Expense Data"):
            clear_all_expenses()
            st.rerun()

elif page == "Add Investment":
    st.title("📈 Add Investment")
    
    with st.form("investment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            investment_amount = st.number_input("Amount ($)", min_value=0.0, step=0.01, format="%.2f")
            investment_type = st.selectbox("Investment Type", INVESTMENT_TYPES)
        
        with col2:
            investment_date = st.date_input("Date", value=datetime.now())
            investment_description = st.text_input("Description (Optional)")
        
        submitted = st.form_submit_button("Add Investment")
        
        if submitted and investment_amount > 0:
            add_investment(investment_amount, investment_type, investment_date, investment_description)
            st.success(f"✅ Added ${investment_amount:.2f} investment in {investment_type}")
            st.rerun()
    
    st.divider()
    
    if investment_data:
        st.subheader("Investment Portfolio")
        
        for idx, item in enumerate(investment_data):
            col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 3, 1, 1])
            with col1:
                st.write(f"**${item['amount']:.2f}**")
            with col2:
                st.write(item['type'])
            with col3:
                st.write(str(item['date']))
            with col4:
                st.write(item['description'] if item['description'] else '-')
            with col5:
                if st.button("🗑️", key=f"del_investment_{item['id']}"):
                    delete_investment(item['id'])
                    st.success("Deleted!")
                    st.rerun()
            with col6:
                st.write("")
        
        st.divider()
        
        total_invested = sum([item['amount'] for item in investment_data])
        st.metric("Total Invested", f"${total_invested:,.2f}")
        
        if st.button("Clear All Investment Data"):
            clear_all_investments()
            st.rerun()

elif page == "Import Data":
    st.title("📥 Import Transactions from CSV/Excel")
    
    st.info("Upload a CSV or Excel file with your transactions. The file should have columns: amount, category, date, description (optional)")
    
    tab1, tab2, tab3 = st.tabs(["Import Income", "Import Expenses", "Import Investments"])
    
    with tab1:
        st.subheader("Import Income Data")
        income_file = st.file_uploader("Upload Income CSV/Excel", type=['csv', 'xlsx'], key='income_upload')
        
        if income_file:
            try:
                if income_file.name.endswith('.csv'):
                    df = pd.read_csv(income_file)
                else:
                    df = pd.read_excel(income_file)
                
                st.write("Preview of uploaded data:")
                st.dataframe(df.head())
                
                if st.button("Import Income Data"):
                    conn = get_db_connection()
                    cur = conn.cursor()
                    count = 0
                    for _, row in df.iterrows():
                        amount = float(row.get('amount', 0))
                        category = str(row.get('category', 'Other'))
                        date = pd.to_datetime(row.get('date', datetime.now())).date()
                        description = str(row.get('description', ''))
                        
                        cur.execute("INSERT INTO income (amount, category, date, description) VALUES (%s, %s, %s, %s)",
                                   (amount, category, date, description))
                        count += 1
                    
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success(f"✅ Successfully imported {count} income entries!")
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Error importing file: {str(e)}")
    
    with tab2:
        st.subheader("Import Expense Data")
        expense_file = st.file_uploader("Upload Expense CSV/Excel", type=['csv', 'xlsx'], key='expense_upload')
        
        if expense_file:
            try:
                if expense_file.name.endswith('.csv'):
                    df = pd.read_csv(expense_file)
                else:
                    df = pd.read_excel(expense_file)
                
                st.write("Preview of uploaded data:")
                st.dataframe(df.head())
                
                if st.button("Import Expense Data"):
                    conn = get_db_connection()
                    cur = conn.cursor()
                    count = 0
                    for _, row in df.iterrows():
                        amount = float(row.get('amount', 0))
                        category = str(row.get('category', 'Other'))
                        date = pd.to_datetime(row.get('date', datetime.now())).date()
                        description = str(row.get('description', ''))
                        
                        cur.execute("INSERT INTO expenses (amount, category, date, description) VALUES (%s, %s, %s, %s)",
                                   (amount, category, date, description))
                        count += 1
                    
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success(f"✅ Successfully imported {count} expense entries!")
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Error importing file: {str(e)}")
    
    with tab3:
        st.subheader("Import Investment Data")
        investment_file = st.file_uploader("Upload Investment CSV/Excel", type=['csv', 'xlsx'], key='investment_upload')
        
        if investment_file:
            try:
                if investment_file.name.endswith('.csv'):
                    df = pd.read_csv(investment_file)
                else:
                    df = pd.read_excel(investment_file)
                
                st.write("Preview of uploaded data:")
                st.dataframe(df.head())
                
                if st.button("Import Investment Data"):
                    conn = get_db_connection()
                    cur = conn.cursor()
                    count = 0
                    for _, row in df.iterrows():
                        amount = float(row.get('amount', 0))
                        inv_type = str(row.get('type', 'Other'))
                        date = pd.to_datetime(row.get('date', datetime.now())).date()
                        description = str(row.get('description', ''))
                        
                        cur.execute("INSERT INTO investments (amount, type, date, description) VALUES (%s, %s, %s, %s)",
                                   (amount, inv_type, date, description))
                        count += 1
                    
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success(f"✅ Successfully imported {count} investment entries!")
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Error importing file: {str(e)}")

elif page == "Goals":
    st.title("🎯 Financial Goals")
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, target_amount, current_amount, target_date, category, description FROM goals ORDER BY target_date")
    goals = cur.fetchall()
    cur.close()
    conn.close()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Add New Goal")
        with st.form("goal_form"):
            goal_name = st.text_input("Goal Name", placeholder="e.g., Emergency Fund, Vacation, New Car")
            gcol1, gcol2 = st.columns(2)
            with gcol1:
                target_amount = st.number_input("Target Amount ($)", min_value=0.0, step=100.0, format="%.2f")
                current_amount = st.number_input("Current Amount ($)", min_value=0.0, step=100.0, format="%.2f")
            with gcol2:
                target_date = st.date_input("Target Date")
                goal_category = st.text_input("Category (Optional)")
            goal_description = st.text_area("Description (Optional)")
            
            if st.form_submit_button("Create Goal"):
                if goal_name and target_amount > 0:
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute("""INSERT INTO goals (name, target_amount, current_amount, target_date, category, description) 
                                VALUES (%s, %s, %s, %s, %s, %s)""",
                               (goal_name, target_amount, current_amount, target_date, goal_category, goal_description))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success(f"✅ Goal '{goal_name}' created!")
                    st.rerun()
    
    with col2:
        st.subheader("Quick Stats")
        if goals:
            total_target = sum([float(g[2]) for g in goals])
            total_current = sum([float(g[3]) for g in goals])
            st.metric("Total Goal Target", f"${total_target:,.2f}")
            st.metric("Total Saved", f"${total_current:,.2f}")
            progress = (total_current / total_target * 100) if total_target > 0 else 0
            st.metric("Overall Progress", f"{progress:.1f}%")
    
    st.divider()
    
    if goals:
        st.subheader("Your Goals")
        for goal in goals:
            goal_id, name, target, current, target_date, category, description = goal
            target = float(target)
            current = float(current)
            progress = (current / target * 100) if target > 0 else 0
            
            with st.expander(f"🎯 {name} - {progress:.1f}% complete", expanded=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Target:** ${target:,.2f}")
                    st.write(f"**Current:** ${current:,.2f}")
                with col2:
                    st.write(f"**Remaining:** ${target - current:,.2f}")
                    st.write(f"**Target Date:** {target_date}")
                with col3:
                    if category:
                        st.write(f"**Category:** {category}")
                    if description:
                        st.write(f"**Description:** {description}")
                
                st.progress(min(progress / 100, 1.0))
                
                ucol1, ucol2 = st.columns([3, 1])
                with ucol1:
                    new_amount = st.number_input(f"Update amount for {name}", min_value=0.0, value=current, step=10.0, key=f"update_{goal_id}")
                with ucol2:
                    st.write("")
                    st.write("")
                    if st.button("Update", key=f"btn_{goal_id}"):
                        conn = get_db_connection()
                        cur = conn.cursor()
                        cur.execute("UPDATE goals SET current_amount = %s WHERE id = %s", (new_amount, goal_id))
                        conn.commit()
                        cur.close()
                        conn.close()
                        st.success("Updated!")
                        st.rerun()
    else:
        st.info("No goals yet. Create your first financial goal above!")

elif page == "Budgets":
    st.title("💰 Budget Management")
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, category, monthly_limit, alert_threshold, active FROM budgets WHERE active = TRUE ORDER BY category")
    budgets = cur.fetchall()
    cur.close()
    conn.close()
    
    current_month = datetime.now().replace(day=1).date()
    next_month = (datetime.now().replace(day=28) + timedelta(days=4)).replace(day=1).date()
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT category, SUM(amount) FROM expenses WHERE date >= %s AND date < %s GROUP BY category", 
                (current_month, next_month))
    spending_this_month = {row[0]: float(row[1]) for row in cur.fetchall()}
    cur.close()
    conn.close()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Create Budget")
        with st.form("budget_form"):
            budget_category = st.selectbox("Category", EXPENSE_CATEGORIES)
            bcol1, bcol2 = st.columns(2)
            with bcol1:
                monthly_limit = st.number_input("Monthly Limit ($)", min_value=0.0, step=50.0, format="%.2f")
            with bcol2:
                alert_threshold = st.slider("Alert Threshold (%)", min_value=50, max_value=100, value=80)
            
            if st.form_submit_button("Create Budget"):
                if monthly_limit > 0:
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute("""INSERT INTO budgets (category, monthly_limit, alert_threshold) 
                                VALUES (%s, %s, %s)""",
                               (budget_category, monthly_limit, alert_threshold))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success(f"✅ Budget for {budget_category} created!")
                    st.rerun()
    
    with col2:
        st.subheader("This Month")
        total_budgeted = sum([float(b[2]) for b in budgets])
        total_spent = sum(spending_this_month.values())
        st.metric("Total Budget", f"${total_budgeted:,.2f}")
        st.metric("Total Spent", f"${total_spent:,.2f}")
        remaining = total_budgeted - total_spent
        st.metric("Remaining", f"${remaining:,.2f}")
    
    st.divider()
    
    if budgets:
        st.subheader("Your Budgets")
        
        for budget in budgets:
            budget_id, category, limit, threshold, active = budget
            limit = float(limit)
            spent = spending_this_month.get(category, 0.0)
            percentage = (spent / limit * 100) if limit > 0 else 0
            remaining = limit - spent
            
            alert_msg = ""
            if percentage >= 100:
                alert_msg = "🚨 OVER BUDGET!"
            elif percentage >= threshold:
                alert_msg = f"⚠️ {threshold}% threshold reached!"
            
            with st.container():
                st.write(f"### {category} {alert_msg}")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Budget", f"${limit:,.2f}")
                with col2:
                    st.metric("Spent", f"${spent:,.2f}")
                with col3:
                    st.metric("Remaining", f"${remaining:,.2f}")
                with col4:
                    st.metric("Used", f"{percentage:.1f}%")
                
                if percentage >= 100:
                    st.progress(1.0, text=f"Over budget by ${spent - limit:,.2f}")
                else:
                    st.progress(percentage / 100)
                
                st.divider()
    else:
        st.info("No budgets set yet. Create your first budget above!")

elif page == "Reports & Tips":
    st.title("📋 Financial Reports & Savings Tips")
    
    metrics = calculate_financial_metrics(income_data, expense_data, investment_data)
    
    st.header("Monthly Financial Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Income & Spending")
        summary_data = {
            'Category': ['Total Income', 'Total Expenses', 'Total Investments', 'Net Savings'],
            'Amount': [
                f"${metrics['total_income']:,.2f}",
                f"${metrics['total_expenses']:,.2f}",
                f"${metrics['total_investments']:,.2f}",
                f"${metrics['net_savings']:,.2f}"
            ]
        }
        st.table(pd.DataFrame(summary_data))
    
    with col2:
        st.subheader("Key Metrics")
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=metrics['savings_rate'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Savings Rate (%)"},
            delta={'reference': 20},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 10], 'color': "lightgray"},
                    {'range': [10, 20], 'color': "gray"},
                    {'range': [20, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 20
                }
            }
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    st.divider()
    
    st.header("💡 Personalized Savings Tips")
    
    expense_df = pd.DataFrame(expense_data) if expense_data else pd.DataFrame()
    tips = generate_financial_tips(metrics, expense_df)
    
    for tip in tips:
        st.info(tip)
    
    st.divider()
    
    st.header("📊 Expense Forecasting")
    
    if len(expense_data) >= 3:
        expense_df = pd.DataFrame(expense_data)
        expense_df['date'] = pd.to_datetime(expense_df['date'])
        expense_df['month'] = expense_df['date'].dt.to_period('M')
        
        monthly_expenses = expense_df.groupby('month')['amount'].sum().reset_index()
        monthly_expenses['month'] = monthly_expenses['month'].astype(str)
        
        if len(monthly_expenses) >= 2:
            avg_monthly = monthly_expenses['amount'].mean()
            trend = monthly_expenses['amount'].diff().mean()
            
            next_month_forecast = avg_monthly + trend
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Average Monthly Spending", f"${avg_monthly:,.2f}")
                st.metric("Trend", f"${trend:,.2f}" + (" 📈" if trend > 0 else " 📉"))
            with col2:
                st.metric("Next Month Forecast", f"${next_month_forecast:,.2f}")
            
            fig_forecast = px.line(monthly_expenses, x='month', y='amount',
                                 title='Monthly Spending Trend',
                                 labels={'amount': 'Amount ($)', 'month': 'Month'})
            st.plotly_chart(fig_forecast, use_container_width=True)
            
            st.subheader("Category Forecasts")
            category_forecasts = []
            for category in EXPENSE_CATEGORIES:
                cat_expenses = expense_df[expense_df['category'] == category]
                if len(cat_expenses) > 0:
                    cat_monthly = cat_expenses.groupby('month')['amount'].sum()
                    if len(cat_monthly) > 0:
                        avg_cat = cat_monthly.mean()
                        category_forecasts.append({
                            'Category': category,
                            'Avg Monthly': f"${avg_cat:.2f}",
                            'Forecast Next Month': f"${avg_cat:.2f}"
                        })
            
            if category_forecasts:
                st.dataframe(pd.DataFrame(category_forecasts), use_container_width=True)
    else:
        st.info("Add more expense data (at least 3 entries) to see forecasting predictions!")
    
    st.divider()
    
    if expense_data:
        st.header("📊 Detailed Expense Analysis")
        
        expense_df = pd.DataFrame(expense_data)
        expense_summary = expense_df.groupby('category')['amount'].agg(['sum', 'count', 'mean']).round(2)
        expense_summary.columns = ['Total Spent', 'Number of Transactions', 'Average Amount']
        expense_summary['% of Total'] = (expense_summary['Total Spent'] / metrics['total_expenses'] * 100).round(1)
        expense_summary = expense_summary.sort_values(by='Total Spent', ascending=False)
        
        st.dataframe(expense_summary, use_container_width=True)
    
    if income_data:
        st.divider()
        st.header("💵 Income Analysis")
        
        income_df = pd.DataFrame(income_data)
        income_summary = income_df.groupby('category')['amount'].agg(['sum', 'count']).round(2)
        income_summary.columns = ['Total Income', 'Number of Entries']
        income_summary['% of Total'] = (income_summary['Total Income'] / metrics['total_income'] * 100).round(1)
        income_summary = income_summary.sort_values(by='Total Income', ascending=False)
        
        st.dataframe(income_summary, use_container_width=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        report_data = {
            'Metric': ['Total Income', 'Total Expenses', 'Total Investments', 'Net Savings', 'Savings Rate (%)'],
            'Value': [
                metrics['total_income'],
                metrics['total_expenses'],
                metrics['total_investments'],
                metrics['net_savings'],
                metrics['savings_rate']
            ]
        }
        report_df = pd.DataFrame(report_data)
        csv = report_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Financial Report (CSV)",
            data=csv,
            file_name=f"financial_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        if expense_data:
            expense_df = pd.DataFrame(expense_data)
            csv_expenses = expense_df.to_csv(index=False)
            st.download_button(
                label="📥 Download All Expenses (CSV)",
                data=csv_expenses,
                file_name=f"expenses_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

st.sidebar.divider()
st.sidebar.success("💾 Data is persisted in the database across sessions!")

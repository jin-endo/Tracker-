
import streamlit as st
import sqlite3
import pandas as pd

#  Replace with your full local path 
#still not working even with a full ass path to db im done pplaying with this
db_path = r'C:\Users\andre\Downloads\personal_finance_tracker_final_fixed\finance.db'
conn = sqlite3.connect(db_path) #streamlit makes another Db connects to it not the one that has the data)
cursor = conn.cursor()

query = """
SELECT t.amount, t.category, t.type, t.date, u.first_name
FROM "transaction" t
JOIN user u ON t.user_id = u.id
"""
try:
    df = pd.read_sql_query(query, conn)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

st.title("📊 Personal Finance Dashboard")

if df.empty:
    st.warning("No transactions found. Add some data in the Flask app first.")
else:
    st.subheader("Summary Table")
    st.dataframe(df)

    st.subheader("Income vs. Expenses")
    summary = df.groupby('type')['amount'].sum()
    st.bar_chart(summary)

    st.subheader("Spending by Category")
    expense_df = df[df['type'] == 'expense']
    if not expense_df.empty:
        category_summary = expense_df.groupby('category')['amount'].sum()
        st.pie_chart(category_summary)
    else:
        st.info("No expenses yet to show category breakdown.")
#this would have been graphes and stuff but doesn't wanna connect to right db
conn.close()

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load datasets
@st.cache_data
def load_data():
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
    if not os.path.exists(data_path):
        st.error(f"Folder dataset tidak ditemukan: {data_path}")
        st.stop()
    
    try:
        sellers = pd.read_csv(os.path.join(data_path, "sellers_dataset.csv"))
        orders = pd.read_csv(os.path.join(data_path, "orders_dataset.csv"))
        order_items = pd.read_csv(os.path.join(data_path, "order_items_dataset.csv"))
        order_reviews = pd.read_csv(os.path.join(data_path, "order_reviews_dataset.csv"))
        order_payments = pd.read_csv(os.path.join(data_path, "order_payments_dataset.csv"))
    except FileNotFoundError as e:
        st.error(f"File dataset tidak ditemukan: {e}")
        st.stop()
    
    return sellers, orders, order_items, order_reviews, order_payments

sellers, orders, order_items, order_reviews, order_payments = load_data()

# Convert order_purchase_timestamp ke datetime
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

# Sidebar untuk filter tanggal
st.sidebar.header("Filter Tanggal")
min_date = orders['order_purchase_timestamp'].min().date()
max_date = orders['order_purchase_timestamp'].max().date()
start_date, end_date = st.sidebar.date_input(
    "Rentang Waktu", [min_date, max_date], min_value=min_date, max_value=max_date
)

# Filter dataset berdasarkan tanggal
filtered_orders = orders[(orders['order_purchase_timestamp'].dt.date >= start_date) &
                         (orders['order_purchase_timestamp'].dt.date <= end_date)]

# Merge order items dengan sellers untuk mendapatkan jumlah pesanan per seller
order_items_sellers = order_items.merge(sellers, on='seller_id')
seller_orders = order_items_sellers.groupby('seller_id').order_id.nunique().reset_index()
seller_orders.columns = ['seller_id', 'total_orders']

# Scatter plot antara nilai pembayaran dan rating
payments_reviews = order_payments.merge(order_reviews, on='order_id')

# --- TAMPILAN DASHBOARD ---
st.title("E-Commerce Dashboard")

# Chart 1: Bar Chart - Jumlah Pesanan per Penjual
st.subheader("Total Pesanan per Penjual")
fig, ax = plt.subplots()
top_sellers = seller_orders.sort_values(by='total_orders', ascending=False).head(10)
sns.barplot(y=top_sellers['seller_id'], x=top_sellers['total_orders'], ax=ax)
ax.set_xlabel("Jumlah Pesanan")
ax.set_ylabel("ID Penjual")
st.pyplot(fig)

# Chart 2: Scatter Plot - Hubungan Nilai Pembayaran vs Rating
st.subheader("Hubungan Nilai Pembayaran dan Rating Pelanggan")
fig, ax = plt.subplots()
sns.scatterplot(x=payments_reviews['payment_value'], y=payments_reviews['review_score'], alpha=0.5, ax=ax)
ax.set_xlabel("Nilai Pembayaran")
ax.set_ylabel("Rating Pelanggan")
st.pyplot(fig)

# Menampilkan dataset setelah filter
st.subheader("Data Pesanan Setelah Filter")
st.dataframe(filtered_orders)

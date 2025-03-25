import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load datasets
@st.cache_data
def load_data():
    data_path = os.path.dirname(__file__)
    sellers = pd.read_csv(os.path.join(data_path, "sellers_dataset.csv"))
    orders = pd.read_csv(os.path.join(data_path, "orders_dataset.csv"))
    order_items = pd.read_csv(os.path.join(data_path, "order_items_dataset.csv"))
    order_reviews = pd.read_csv(os.path.join(data_path, "order_reviews_dataset.csv"))
    products = pd.read_csv(os.path.join(data_path, "products_dataset.csv"))
    order_payments = pd.read_csv(os.path.join(data_path, "order_payments_dataset.csv"))
    return sellers, orders, order_items, order_reviews, products, order_payments

sellers, orders, order_items, order_reviews, products, order_payments = load_data()

# Convert timestamps
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

# Merge data untuk analisis produk
order_items_products = order_items.merge(products, on='product_id')
order_items_products['order_month'] = pd.to_datetime(order_items_products['shipping_limit_date']).dt.to_period('M')

# Agregasi kategori produk terlaris per bulan
category_sales = order_items_products.groupby(['order_month', 'product_category_name'])['order_id'].count().reset_index()
category_sales = category_sales.sort_values(by=['order_month', 'order_id'], ascending=[True, False])

# Faktor kepuasan pelanggan
review_analysis = order_reviews.merge(order_payments, on='order_id')

# --- TAMPILAN DASHBOARD ---
st.title("E-Commerce Dashboard")

# Chart 1: Produk Kategori Terlaris per Bulan
st.subheader("Produk Kategori Terlaris per Bulan")
st.sidebar.subheader("Filter Kategori Produk")
selected_category = st.sidebar.selectbox("Pilih Kategori Produk", category_sales['product_category_name'].unique())
filtered_category_sales = category_sales[category_sales['product_category_name'] == selected_category]

fig, ax = plt.subplots(figsize=(10, 6))
category_sales['order_month'] = category_sales['order_month'].astype(str)
filtered_category_sales['order_month'] = filtered_category_sales['order_month'].astype(str)
category_sales['order_id'] = pd.to_numeric(category_sales['order_id'], errors='coerce')
category_sales = category_sales.dropna()
sns.lineplot(data=filtered_category_sales, x='order_month', y='order_id', marker='o', ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penjualan")
st.pyplot(fig)

# Chart 2: Analisis Kepuasan Pelanggan
st.subheader("Faktor yang Mempengaruhi Kepuasan Pelanggan")
st.sidebar.subheader("Filter Rentang Rating")
review_range = st.sidebar.slider("Pilih Rentang Rating", 1, 5, (1, 5))
filtered_reviews = review_analysis[(review_analysis['review_score'] >= review_range[0]) &
                                     (review_analysis['review_score'] <= review_range[1])]

fig, ax = plt.subplots()
sns.boxplot(data=filtered_reviews, x='review_score', y='payment_value', ax=ax)
ax.set_xlabel("Rating Pelanggan")
ax.set_ylabel("Nilai Pembayaran")
st.pyplot(fig)

# Menampilkan dataset setelah filter
st.subheader("Data Pesanan Setelah Filter")
st.dataframe(filtered_orders)

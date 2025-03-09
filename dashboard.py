import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === SETUP APLIKASI ===
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# === LOAD DATASET ===
@st.cache_data
def load_data():
    sellers_df = pd.read_csv("sellers_dataset.csv")
    orders_df = pd.read_csv("orders_dataset.csv")
    order_items_df = pd.read_csv("order_items_dataset.csv")
    order_reviews_df = pd.read_csv("order_reviews_dataset.csv")
    order_payments_df = pd.read_csv("order_payments_dataset.csv")
    return sellers_df, orders_df, order_items_df, order_reviews_df, order_payments_df

sellers_df, orders_df, order_items_df, order_reviews_df, order_payments_df = load_data()

# === TITLE & INTRO ===
st.title("Dashboard Analisis E-Commerce Dataset")
st.markdown("Dashboard ini menampilkan analisis data penjualan dan kepuasan pelanggan dari dataset E-Commerce Public.")

st.divider()

# === METRIC CARD (RINGKASAN DATA) ===
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Pesanan", f"{orders_df.shape[0]:,}")
col2.metric("Total Produk Terjual", f"{order_items_df.shape[0]:,}")
col3.metric("Total Penjual", f"{sellers_df.shape[0]:,}")
col4.metric("Total Pembayaran", f"${order_payments_df['payment_value'].sum():,.2f}")

st.divider()

# === FILTER DATA (SIDEBAR) ===
st.sidebar.header("Filter Data")

# Menghitung performa penjual berdasarkan jumlah pesanan
seller_performance = order_items_df.groupby('seller_id').agg(
    total_orders=('order_id', 'count')
).reset_index()
seller_performance = seller_performance.merge(sellers_df, on='seller_id', how='left')

# Mengklasifikasikan performa penjual ke dalam kategori
seller_performance['performance_category'] = pd.qcut(
    seller_performance['total_orders'], q=4, labels=['Low', 'Medium', 'High', 'Top']
)

# Sidebar untuk memilih kategori performa penjual
performance_filter = st.sidebar.multiselect("Pilih Kategori Kinerja Penjual", 
                                            seller_performance['performance_category'].unique(), 
                                            default=seller_performance['performance_category'].unique())

# Filter data berdasarkan pilihan pengguna
filtered_sellers = seller_performance[seller_performance['performance_category'].isin(performance_filter)]

# === VISUALISASI DENGAN POP-UP INSIGHT ===

col1, col2 = st.columns(2)

# Distribusi Kinerja Penjual (dikembalikan ke tampilan awal)
with col1:
    st.subheader("Distribusi Kinerja Penjual")
    fig, ax = plt.subplots(figsize=(4, 2.5))
    sns.countplot(data=filtered_sellers, x="performance_category", palette="Blues", ax=ax)
    ax.set_title("Distribusi Kinerja Penjual")
    ax.set_xlabel("Kategori Kinerja")
    ax.set_ylabel("Jumlah Penjual")
    st.pyplot(fig, use_container_width=False)

    # Insight Pop-up
    with st.expander("Lihat Insight"):
        st.write("""
        - Kinerja yang Merata: Penjualan terlihat cukup merata di berbagai kategori kinerja, dari "Low" hingga "Top". Hal ini menunjukkan bahwa ada sejumlah penjual di setiap kategori, meskipun tidak ada kategori yang sangat dominan.
        - Kategori Medium dan Top Menonjol: Kategori "Medium" dan "Top" memiliki jumlah penjualan yang cukup tinggi. Ini bisa berarti bahwa banyak penjual berada di tingkat kinerja yang baik, dan ada potensi untuk mendorong mereka menuju kategori "Top".
        - Peluang untuk Peningkatan: Kategori "Low" menunjukkan jumlah penjualan yang lebih sedikit. Ini bisa jadi tanda bahwa ada penjual yang mungkin memerlukan dukungan atau pelatihan tambahan untuk meningkatkan kinerja mereka.
        - Strategi Pengembangan: Dengan banyaknya penjual di kategori "Medium", perusahaan dapat fokus pada strategi untuk membantu mereka naik ke kategori "Top", misalnya melalui insentif atau pelatihan.
        """)

# Distribusi Rating Kepuasan Pelanggan
with col2:
    st.subheader("Distribusi Rating Kepuasan Pelanggan")
    fig, ax = plt.subplots(figsize=(4, 2.5))
    sns.histplot(order_reviews_df['review_score'], bins=20, kde=True, color='blue', ax=ax)
    ax.set_title("Distribusi Rating Kepuasan Pelanggan")
    ax.set_xlabel("Rata-rata Skor Review")
    ax.set_ylabel("Frekuensi")
    st.pyplot(fig, use_container_width=False)

    # Insight Pop-up
    with st.expander("Lihat Insight"):
        st.write("""
        - Konsentrasi pada Rating Tinggi: Terlihat bahwa sebagian besar pelanggan memberikan rating yang tinggi, terutama di sekitar skor 5. Ini menunjukkan bahwa banyak pelanggan merasa puas dengan pengalaman belanja mereka.
        - Kurangnya Rating Rendah: Rating di bawah 3 (misalnya, 1 dan 2) tampaknya sangat sedikit, menunjukkan bahwa masalah kepuasan pelanggan mungkin tidak umum terjadi, atau bahwa pelanggan yang tidak puas memilih untuk tidak memberikan ulasan.
        - Puncak di Skor 4 dan 5: Terdapat puncak signifikan di rata-rata skor 4 dan 5, yang bisa mengindikasikan adanya loyalitas pelanggan yang tinggi atau produk yang berkualitas.
        - Distribusi yang Mencolok: Garis kurva menunjukkan distribusi yang halus, yang menunjukkan bahwa meskipun ada beberapa variasi dalam rating, mayoritas pelanggan cenderung memberikan nilai yang positif.
        - Peluang untuk Meningkatkan Rating: Meskipun banyak rating tinggi, perusahaan bisa berfokus pada meningkatkan pengalaman pelanggan untuk lebih banyak rating 5, dengan memperhatikan umpan balik dari pelanggan yang memberikan rating 4.
                """)

col3, col4 = st.columns(2)

# Tren Jumlah Pesanan per Bulan
with col3:
    st.subheader("Tren Jumlah Pesanan per Bulan")
    orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
    orders_df['order_purchase_month'] = orders_df['order_purchase_timestamp'].dt.to_period('M')

    monthly_orders = orders_df.groupby('order_purchase_month').size()
    fig, ax = plt.subplots(figsize=(4, 2.5))
    monthly_orders.plot(marker='o', linestyle='-', ax=ax)
    ax.set_title("Tren Jumlah Pesanan per Bulan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Pesanan")
    ax.grid()
    st.pyplot(fig, use_container_width=False)

    # Insight Pop-up
    with st.expander("Lihat Insight"):
        st.write("""
        - Peningkatan Pesanan yang Stabil: Dari akhir 2016 hingga pertengahan 2017, terlihat adanya peningkatan yang stabil dalam jumlah pesanan. Ini menunjukkan pertumbuhan yang positif dalam aktivitas penjualan selama periode tersebut.
        - Lonjakan Pesanan: Ada lonjakan signifikan pada bulan Juli 2017, yang menunjukkan kemungkinan adanya promosi, peluncuran produk baru, atau faktor lain yang menarik perhatian pelanggan.
        - Penurunan yang Drastis: Namun, setelah bulan Juli, terdapat penurunan tajam pada bulan Oktober. Ini bisa mengindikasikan masalah musiman, kurangnya promosi, atau persaingan yang lebih ketat pada periode tersebut.
        - Konsistensi Bulan Lain: Sebelum lonjakan, jumlah pesanan cukup konsisten, yang menunjukkan bahwa bisnis memiliki basis pelanggan yang stabil.        
                 """)

# Hubungan Total Pembayaran dan Rating Kepuasan Pelanggan
with col4:
    st.subheader("Hubungan Total Pembayaran dan Rating Kepuasan Pelanggan")
    customer_satisfaction = order_reviews_df.groupby('order_id').agg(
        avg_review_score=('review_score', 'mean')
    ).reset_index()

    payment_review = order_payments_df.groupby('order_id').agg(
        total_payment=('payment_value', 'sum')
    ).reset_index()

    customer_satisfaction = customer_satisfaction.merge(payment_review, on='order_id', how='left')

    fig, ax = plt.subplots(figsize=(4, 2.5))
    sns.scatterplot(data=customer_satisfaction, x="total_payment", y="avg_review_score", ax=ax)
    ax.set_title("Hubungan Total Pembayaran dan Rata-rata Skor Review")
    ax.set_xlabel("Total Pembayaran")
    ax.set_ylabel("Rata-rata Skor Review")
    ax.grid()
    st.pyplot(fig, use_container_width=False)

    # Insight Pop-up
    with st.expander("Lihat Insight"):
        st.write("""
        - Variasi Skor Review: Terdapat variasi yang signifikan dalam skor review, terutama pada total pembayaran yang lebih rendah. Beberapa pelanggan memberikan skor rendah meskipun total pembayaran mereka bervariasi.
        - Kecenderungan Positif pada Pembayaran Tinggi: Skor review yang tinggi (mendekati 5) tampak lebih banyak terjadi pada total pembayaran yang lebih tinggi. Ini mungkin menunjukkan bahwa pelanggan yang mengeluarkan lebih banyak uang cenderung lebih puas dengan produk atau layanan.
        - Konsistensi di Pembayaran Rendah: Pada total pembayaran yang rendah, banyak skor review berada di sekitar angka 1 dan 2. Ini bisa mengindikasikan bahwa pelanggan merasa tidak puas ketika mereka mengeluarkan sedikit uang, mungkin karena ekspektasi yang tidak terpenuhi.
        - Peluang untuk Meningkatkan Pengalaman Pelanggan: Dengan adanya pelanggan yang memberikan skor rendah meskipun melakukan pembayaran, perusahaan dapat mengeksplorasi faktor-faktor yang mempengaruhi kepuasan pelanggan dan berusaha untuk memperbaiki pengalaman mereka.
        """)

st.divider()

# === KESIMPULAN ===
st.header("Kesimpulan Analisis")
st.markdown("""
- Tren Jumlah Pesanan: Terjadi fluktuasi setiap bulan dengan periode puncak tertentu.
- Kinerja Penjual: Penjual dikategorikan dalam 4 tingkat performa berdasarkan total pesanan yang diterima.
- Kepuasan Pelanggan: Distribusi rating ulasan menunjukkan sebagian besar pelanggan memberikan rating tinggi.
- Pembayaran & Kepuasan: Tidak ada korelasi yang kuat antara total pembayaran dan rating ulasan pelanggan.
""")

# Tambahkan Footer
st.caption("Dibuat oleh: Muhammad Ridho Abidin Damanik | Belajar Analisis Data dengan Python (Dicoding x LaskarAI) ")

# E-Commerce Data Dashboard

Dashboard ini dibuat menggunakan **Streamlit** untuk menganalisis data e-commerce terkait penjualan dan kepuasan pelanggan.  
Menampilkan **ringkasan metrik utama**, **filter interaktif**, serta berbagai **visualisasi data**.

---

## Fitur Utama
✅ **Ringkasan Data**: Total pesanan, produk terjual, penjual, dan total pembayaran.  
✅ **Filter Interaktif**: Memilih kategori performa penjual.  
✅ **Visualisasi Data**: Tren penjualan, distribusi rating pelanggan, dan analisis kepuasan pelanggan.  
✅ **Tampilan Interaktif**: Dibuat dengan **Streamlit** agar mudah digunakan.

---

## **Setup Environment**

### **1. Menggunakan Anaconda**
Jika menggunakan **Anaconda**, buat environment baru dan install dependencies:
```sh
conda create --name ecommerce-dashboard python=3.9
conda activate ecommerce-dashboard
pip install -r requirements.txt
```
### **2. Setup Environment - Shell/Terminal**
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt

### **3. Run steamlit app**
streamlit run dashboard.py

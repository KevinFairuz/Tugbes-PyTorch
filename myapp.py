import streamlit as st
import pandas as pd
import folium
import datetime
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import seaborn as sns
from streamlit_option_menu import option_menu
# Loading the CSV file into a DataFrame
file_path = 'geolocation_dataset.csv'
df_geo_data = pd.read_csv(file_path)

# reading the data from excel file
df_data_review = pd.read_csv('order_reviews_dataset.csv')
df_sellers = pd.read_csv('sellers_dataset.csv')
df_data_review = pd.read_csv('order_reviews_dataset.csv')
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:')
st.markdown(
    '<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
image = Image.open('shopee-logo-1.jpg')

seller = list(df_sellers['seller_state'])

col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image(image, width=100)

html_title = """
    <style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:6px;
    }
    </style>
    <center><h1 class="title-test">Online Shop</h1></center>"""

with col2:
    st.markdown(html_title, unsafe_allow_html=True)

col3, col4, col5 = st.columns([0.5, 0.45, 0.45])
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by:  \n {box_date}")


@st.cache_data
# Load Data CSV
def load_data(url):
    df = pd.read_csv(url)
    return df


with col4:
    def Analisis_Pengiriman(df_orders):
        # Mengabil data order dengan status 'delivered'
        df_orders_delivered = df_orders[df_orders['order_status']
                                        == 'delivered']

    # Menghapus nilai null pada atribut 'order_delivered_customer_date' pada dataframe
        df_orders_delivered = df_orders_delivered.dropna(
            subset=['order_delivered_customer_date'])

    # Mengubah tipe data pada 'order_delivered_customer_date' dan 'order_estimated_delivery_date'
        df_orders_delivered['order_delivered_customer_date'] = pd.to_datetime(
            df_orders_delivered['order_delivered_customer_date'])

    # Mengkonversi Datetime ke format Date untuk atribut 'order_delivered_customer_date'
        df_orders_delivered['order_delivered_customer_date'] = df_orders_delivered['order_delivered_customer_date'].dt.date

        df_orders_delivered['order_delivered_customer_date'] = pd.to_datetime(
            df_orders_delivered['order_delivered_customer_date'])
        df_orders_delivered['order_estimated_delivery_date'] = pd.to_datetime(
            df_orders_delivered['order_estimated_delivery_date'])

    # Perhitungan value_count() untuk status 'processing','shipped','delivered'
        jumlah_processing = df_orders['order_status'].value_counts()[
            'processing']
        jumlah_shipped = df_orders['order_status'].value_counts()['shipped']
        jumlah_delivered = df_orders['order_status'].value_counts()[
            'delivered']

    # Perhitungan pengiriman tepat waktu dan terlambat
        jml_order_terlambat = len(df_orders_delivered[(
            df_orders_delivered["order_estimated_delivery_date"] < df_orders_delivered[
                "order_delivered_customer_date"])])
        jml_order_tepat_waktu = len(df_orders_delivered[(
            df_orders_delivered["order_estimated_delivery_date"] > df_orders_delivered[
                "order_delivered_customer_date"])])
        jml_order_diterima = jml_order_tepat_waktu + jml_order_terlambat

    # Menghitung selisih hari
        df_orders_delivered["Selisih Hari"] = df_orders_delivered["order_delivered_customer_date"] - df_orders_delivered[
            "order_estimated_delivery_date"]

    # Mengganti nilai selisih hari negatif dengan 0
        df_orders_delivered["Selisih Hari"] = np.where(df_orders_delivered['Selisih Hari'].dt.days < 0, 0,
                                                       df_orders_delivered['Selisih Hari'].dt.days)

    # Grafik Status Pengiriman
        data_pengiriman = pd.DataFrame({
            'Kategori': ['Processing', 'Shipped', 'Delivered'],
            'Jumlah': [jumlah_processing, jumlah_shipped, jumlah_delivered]
        })

    # Perkembangan Pengiriman
        st.header("Grafik Perkembangan Pengiriman")
        st.dataframe(data_pengiriman)

    # Buat bar chart
        label = data_pengiriman['Kategori']
        data = data_pengiriman['Jumlah']

        fig, ax = plt.subplots()
        ax.bar(label, data, color=['green' if kategori ==
               'Delivered' else 'red' for kategori in label])
        ax.set_xlabel('Kategori')
        ax.set_ylabel('Jumlah')

    # Menambahkan Label Pada Setiap Bar
        for i in range(len(label)):
            ax.text(label[i], data[i], str(data[i]), ha='center', va='bottom')

    # Rotasi Label 45 derajat
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Expander Grafik
        with st.expander("Penjelasan Perkembangan Pengiriman"):
            st.write(
                'Dilihat dari grafik diatas, terlihat dari proses pengiriman sudah sangat baik, terdapat 96.478 paket terkirim, dan perbandingannya sangat signifikan dibanding dengan proses yang lain. namun perlu dianalisa kembali untuk pengirimannya apakah sudah tepat waktu atau tidak')

        st.write('<hr>', unsafe_allow_html=True)  # hr Garis Pemisah

        st.header("Grafik Ketepatan Jasa Pengiriman")
        # Pengiriman Tepat Waktu dan Terlambat
        data_keterlambatan = pd.DataFrame({
            'Kategori': ['Tepat Waktu', 'Terlambat'],
            'Jumlah': [jml_order_tepat_waktu, jml_order_terlambat]
        })

        st.dataframe(data_keterlambatan)

        # Grafik Keterlambatan
        label = data_keterlambatan['Kategori']
        size = data_keterlambatan['Jumlah']

        fig, ax = plt.subplots()
        ax.pie(size, labels=label, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Mengatur aspek rasio agar lingkaran tampak sempurna

        st.pyplot(fig)

        # Expander Grafik
        with st.expander("Penjelasan Ketepatan Pengiriman"):
            st.write(
                'Dilihat dari grafik pie tersebut, dapat dilihat bahwa dari total pengiriman, keterlambatan hanya berjumlah 6.534 pengiriman atau sejumlah 6.9% dari total pengiriman yang sudah dilakukan')

        st.write('<hr>', unsafe_allow_html=True)  # hr Garis Pemisah

        # Grafik Keterlambatan
        # Membuat histogram
        jumlah_bins = 4
        nilai_min = 1
        nilai_max = df_orders_delivered['Selisih Hari'].max()

        fig, ax = plt.subplots()
        hist, edges = np.histogram(
            df_orders_delivered['Selisih Hari'], bins=jumlah_bins, range=(nilai_min, nilai_max))
        ax.hist(df_orders_delivered['Selisih Hari'],
                bins=edges, color='skyblue', edgecolor='k')

        # Buat list rentang berdasarkan nilai bins (DataFrame)
        rentang = [
            f'{int(edges[i])}-{int(edges[i + 1])}' for i in range(len(edges) - 1)]
        jml_keterlambatan = []

        # Tambahkan jumlah frekuensi di atas setiap bin histogram
        for i in range(len(hist)):
            ax.text((edges[i] + edges[i + 1]) / 2, hist[i],
                    str(hist[i]), ha='center', va='bottom')
            jml_keterlambatan.append(str(hist[i]))  # Untuk DataFrame

        waktu_keterlambatan = pd.DataFrame({
            'Kategori': rentang,
            'Jumlah': jml_keterlambatan
        })

        st.dataframe(waktu_keterlambatan)

        ax.set_xlabel('Rentang')
        ax.set_ylabel('Frekuensi')

        # Menampilkan histogram di Streamlit
        st.pyplot(fig)

     # Expander Grafik
        with st.expander("Penjelasan Waktu Keterlambatan"):
            st.write(
                'Dilihat dari grafik tersebut, terlihat bahwa sebanyak 6.394 pengiriman terlambat dengan range waktu 1-47 hari, disini cukup lumayan banyak, namun untuk pengiriman ke luar negeri mungkin masih dapat di toleransi')


def Analisis_Review(df_Order_Items, df_Order_Reviews, df_sellers):
    # Menghitung jumlah pesanan untuk masing-masing bintang 1-5
    count_reviews = df_Order_Reviews['review_score'].value_counts(
    ).reset_index()
    count_reviews.columns = ['Review_Score', 'Jumlah']

    # Join antara dataset Order_Reviews dengan Order_Items
    df_Reviews_Items = pd.merge(
        left=df_Order_Reviews,
        right=df_Order_Items,
        how='inner',
        left_on='order_id',
        right_on='order_id'
    )

    # Join antara dataframe Review_Items dengan dataset sellers
    df_Reviews_Items_Sellers = pd.merge(
        left=df_Reviews_Items,
        right=df_sellers,
        how='inner',
        left_on='seller_id',
        right_on='seller_id'
    )

    # Ambil penilaian 1 untuk proses analisis lebih lanjut
    df_Review_1 = df_Reviews_Items_Sellers.loc[df_Reviews_Items_Sellers['review_score'] == 1]

    # Count berdasarkan kota untuk dataframe penilaian 1
    count_review_city = df_Review_1['seller_city'].value_counts().reset_index()
    count_review_city.columns = ['Seller_City', 'Jumlah']

    Lima_Terendah = count_review_city.head()

    # Analisis Data Review Penilaian
    st.header("Grafik Review Terhadap Order Konsumen")
    count_reviews_sorted = count_reviews.sort_values(by='Review_Score')

    st.dataframe(count_reviews_sorted)

    # Buat bar chart
    label = count_reviews['Review_Score']
    data = count_reviews['Jumlah']

    fig, ax = plt.subplots()
    ax.bar(label, data, color=['skyblue' if kategori !=
           1 else 'red' for kategori in label])
    ax.set_xlabel('Review_Score')
    ax.set_ylabel('Jumlah')

    # Menambahkan Label Pada Setiap Bar
    for i in range(len(label)):
        ax.text(label[i], data[i], str(data[i]), ha='center', va='bottom')

    st.pyplot(fig)
    # Expander Grafik
    with st.expander("Penjelasan Review Order"):
        st.write(
            'Pada grafik penilaian oleh konsumen terhadap order yang pernah dilakukan, diketahui terdapat 11.424 order yang mendapatkan penilaian 1, namun dibandingkan dengan hasil review yang lain, dapat dilihat masih banyak yang memberikan penilaian 5 dengan total penilaian sebanyak 57.328. walaupun penilaian 1 masih rendah, diharapkan perusahaan mampu memperbaikin performa dari penjualan atau kualitas produk yang dijual')

    st.write('<hr>', unsafe_allow_html=True)  # hr Garis Pemisah
    # Analisis Cabang / Kota Terendah
    st.header("Grafik 5 Cabang Terendah")
    st.dataframe(Lima_Terendah)

    # Buat bar chart
    label = Lima_Terendah['Seller_City']
    data = Lima_Terendah['Jumlah']

    fig, ax = plt.subplots()
    ax.bar(label, data, color=['skyblue' if jumlah <=
           999 else 'red' for jumlah in data])
    ax.set_xlabel('Seller_City')
    ax.set_ylabel('Jumlah')

    # Menambahkan Label Pada Setiap Bar
    for i in range(len(label)):
        ax.text(label[i], data[i], str(data[i]), ha='center', va='bottom')

    # Rotasi Label 45 derajat
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Expander Grafik
    with st.expander("Penjelasan Cabang Terendah"):
        st.write(
            'Analisis selanjutnya untuk menambah wawasan pengguna, terlihat terdapat 2 cabang yang memiliki penilaian 1 terbanyak, diantaranya Sao Paulo sebanyak 3.571 dan ibitinga sebangayk 1.241. dari sini perusahaan dapat mengambil keputusan apakah barang dari cabang tersebut perlu di cek kembali kualitasnya atau menutup pengiriman dari cabang tersebut')


def Analisis_Geoanalisis(df_geo_data):
    # Create a map
    m = folium.Map(location=[df_geo_data['geolocation_lat'].mean(), df_geo_data['geolocation_lng'].mean()],
                   zoom_start=5)

    # Add points to the map
    for idx, row in df_geo_data.iterrows():
        folium.CircleMarker(
            [row['geolocation_lat'], row['geolocation_lng']], radius=3, fill=True).add_to(m)

    # Display the map
    st.write(m._repr_html_(), unsafe_allow_html=True)

    # Using KMeans for clustering
    kmeans = KMeans(n_clusters=5)
    df_geo_data['cluster'] = kmeans.fit_predict(
        df_geo_data[['geolocation_lat', 'geolocation_lng']])

    # Plotting the clusters
    # Plotting the clusters
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='geolocation_lng', y='geolocation_lat', hue='cluster', data=df_geo_data, palette='viridis',
                    ax=ax)
    plt.title('Cluster Analysis of Geolocations')
    st.pyplot(fig)


df_Order_Items = load_data(
    "https://raw.githubusercontent.com/palafk/Tubes-PYTORCH/main/order_items_dataset.csv")
df_Order_Reviews = load_data(
    "https://raw.githubusercontent.com/palafk/Tubes-PYTORCH/main/order_reviews_dataset.csv")
df_orders = load_data(
    "https://raw.githubusercontent.com/palafk/Tubes-PYTORCH/main/orders_dataset.csv")
df_sellers = load_data(
    "https://raw.githubusercontent.com/palafk/Tubes-PYTORCH/main/sellers_dataset.csv")

with st.sidebar:
    selected = option_menu('Menu', ['Dashboard'],
                           icons=["easel2", "graph-up"],
                           menu_icon="cast",
                           default_index=0)

if (selected == 'Dashboard'):
    st.header(f"E-Commerce Shopee")
    tab1, tab2, tab3 = st.tabs(
        ["Data Pengiriman", "Data Review", "Data Geografi"])

    with tab1:
        Analisis_Pengiriman(df_orders)
    with tab2:
        Analisis_Review(df_Order_Items, df_Order_Reviews, df_sellers)
    with tab3:
        Analisis_Geoanalisis(df_geo_data)

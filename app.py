import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from helper.analysis import run_analysis
import io
from matplotlib.backends.backend_pdf import PdfPages

st.set_page_config(page_title="Greedy Optimization Dashboard", layout="wide")

st.title("⚡ Dashboard Optimasi Konsumsi Daya Listrik - Greedy Algorithm")

st.markdown("""
Aplikasi ini menganalisis dan mengoptimasi konsumsi daya listrik rumah tangga 
berdasarkan algoritma Greedy menggunakan dataset dari Kaggle.
""")

# --- Upload File ---
uploaded_file = st.file_uploader("📤 Upload Dataset Listrik (*.txt atau *.csv)", type=['txt', 'csv'])

if uploaded_file:
    try:
        with st.spinner("📂 Membaca dan memproses data..."):
            # Hanya baca sekali
            df = pd.read_csv(uploaded_file, sep=';', low_memory=False)
            row_count = df.shape[0]

        st.success("✅ Data berhasil dimuat.")
        st.info(f"📊 Jumlah data yang diimpor: **{row_count:,} baris**")

        with st.spinner("⚙️ Menjalankan analisis optimasi Greedy..."):
            # Lempar DataFrame, bukan file
            fig1, fig2, fig3, summary_df = run_analysis(df)

        # --- Visualisasi Hasil ---
        st.subheader("📈 Visualisasi Konsumsi Sebelum dan Sesudah Optimasi")
        st.pyplot(fig1)

        st.subheader("📊 Pola Konsumsi Rata-rata per Jam")
        st.pyplot(fig2)

        st.subheader("📉 Penghematan Harian (%)")
        st.pyplot(fig3)

        st.subheader("📋 Ringkasan Hasil dan IKE")
        st.dataframe(summary_df)

        st.subheader("📤 Ekspor Hasil Analisis")

        # --- Ekspor CSV (Ringkasan) ---
        csv = summary_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Ringkasan (CSV)",
            data=csv,
            file_name='ringkasan_optimasi_listrik.csv',
            mime='text/csv'
        )

        # --- Ekspor PDF (Visualisasi + Ringkasan) ---
        pdf_buffer = io.BytesIO()
        with PdfPages(pdf_buffer) as pdf:
            # Tambah grafik
            pdf.savefig(fig1, bbox_inches='tight')
            pdf.savefig(fig2, bbox_inches='tight')
            pdf.savefig(fig3, bbox_inches='tight')
            
            # Tambah halaman ringkasan (format tabel)
            import matplotlib.pyplot as plt
            fig_summary, ax_summary = plt.subplots(figsize=(8, 4))
            ax_summary.axis('off')
            table = ax_summary.table(cellText=summary_df.values, colLabels=summary_df.columns, loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1, 1.5)
            pdf.savefig(fig_summary, bbox_inches='tight')

        pdf_buffer.seek(0)
        st.download_button(
            label="⬇️ Download Visualisasi + Ringkasan (PDF)",
            data=pdf_buffer,
            file_name="hasil_optimasi_listrik.pdf",
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat memproses data: {e}")
else:
    st.warning("Silakan unggah file dataset terlebih dahulu.")

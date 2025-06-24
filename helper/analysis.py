import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run_analysis(df):
    # --- Validasi kolom penting ---
    required_columns = ['Date', 'Time', 'Global_active_power']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Kolom '{col}' tidak ditemukan dalam dataset.")

    # --- Preprocessing ---
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].replace('?', np.nan)
            try:
                df[col] = pd.to_numeric(df[col])
            except:
                pass
    df.dropna(inplace=True)
    df.set_index('Datetime', inplace=True)

    # --- Konversi ke data per jam ---
    hourly_data = df['Global_active_power'].resample('h').mean().dropna()

    # --- Greedy Optimization ---
    def apply_greedy_optimization(data_series, days_to_analyze=28,
                                  strategy='daily_average', reduction_factor=0.7,
                                  shift_factor=0.2):
        sample_data = data_series.head(24 * days_to_analyze)
        optimized_simulated = sample_data.copy()
        thresholds = pd.Series(dtype=float)

        for date in np.unique(sample_data.index.date):
            daily = sample_data[sample_data.index.date == date]
            if len(daily) == 0:
                continue
            threshold = daily.mean() if strategy == 'daily_average' else daily.quantile(0.25)
            thresholds[date] = threshold
            inefficient = daily >= threshold
            reduced = daily[inefficient] * (1 - reduction_factor)
            optimized_simulated.loc[daily.index[inefficient]] = daily[inefficient] * reduction_factor
            total_shift = reduced.sum() * shift_factor
            efficient = daily < threshold
            if total_shift > 0 and efficient.any():
                per_hour = total_shift / efficient.sum()
                optimized_simulated.loc[daily.index[efficient]] += per_hour
        return optimized_simulated, thresholds, sample_data

    # --- Analisis Utama ---
    days = 28
    optimized, thresholds, original = apply_greedy_optimization(hourly_data, days_to_analyze=days)
    asum_area = 77
    ike_limit = 3.4
    total_ori = original.sum()
    total_opt = optimized.sum()
    ike_ori = total_ori / asum_area
    ike_opt = total_opt / asum_area
    saving = (total_ori - total_opt) / total_ori * 100

    # --- Summary Tabel ---
    summary_df = pd.DataFrame({
        "Metrik": [
            "Total Konsumsi Asli (kWh)",
            "Total Konsumsi Setelah Optimasi (kWh)",
            "IKE Asli",
            "IKE Setelah Optimasi",
            "Potensi Penghematan (%)"
        ],
        "Nilai": [
            f"{total_ori:.2f}",
            f"{total_opt:.2f}",
            f"{ike_ori:.2f}",
            f"{ike_opt:.2f}",
            f"{saving:.2f}%"
        ]
    })

    # --- Grafik 1: Konsumsi Total ---
    fig1, ax1 = plt.subplots(figsize=(14, 6))
    ax1.plot(original.index, original, label='Asli', color='blue')
    ax1.plot(optimized.index, optimized, label='Optimasi', color='green', linestyle='--')
    ax1.set_title('Konsumsi Daya Sebelum vs Sesudah Optimasi')
    ax1.set_ylabel("Daya (kW)")
    ax1.legend()
    ax1.grid(True)

    # --- Grafik 2: Pola Jam ---
    fig2, ax2 = plt.subplots()
    ori_pattern = original.groupby(original.index.hour).mean()
    opt_pattern = optimized.groupby(optimized.index.hour).mean()
    ax2.plot(ori_pattern, label='Asli', marker='o')
    ax2.plot(opt_pattern, label='Optimasi', marker='x')
    ax2.set_title("Pola Konsumsi Rata-rata per Jam")
    ax2.set_xlabel("Jam")
    ax2.set_ylabel("Daya (kW)")
    ax2.grid(True)
    ax2.legend()

    # --- Grafik 3: Penghematan Harian ---
    daily_ori = original.groupby(original.index.date).sum()
    daily_opt = optimized.groupby(optimized.index.date).sum()
    daily_save = ((daily_ori - daily_opt) / daily_ori) * 100
    fig3, ax3 = plt.subplots()
    daily_save.plot(kind='bar', ax=ax3, color='purple', alpha=0.7)
    ax3.set_title("Persentase Penghematan Harian")
    ax3.set_ylabel("Penghematan (%)")
    ax3.grid(axis='y')

    return fig1, fig2, fig3, summary_df

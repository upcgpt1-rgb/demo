import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="Dashboard Predictivo - Contrans S.A.C.", layout="wide")

st.title("📊 Sistema Predictivo de Demanda Logística – Contrans S.A.C.")

# Simulación de datos
fechas = pd.date_range("2024-11-01", periods=30)
real = np.random.randint(1200, 1900, size=30)
pred = real + np.random.randint(-100, 100, size=30)
df = pd.DataFrame({"Fecha": fechas, "Demanda Real": real, "Demanda Predicha": pred})

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Precisión del Modelo", "87 %")
col2.metric("Tiempo de Respuesta", "4.2 s")
col3.metric("Ocupación Actual", "92 %")

# Gráfico de líneas
chart = (
    alt.Chart(df)
    .mark_line(point=True)
    .encode(
        x="Fecha:T",
        y=alt.Y("Demanda Real", title="Movimientos de contenedores"),
        color=alt.value("steelblue")
    )
)
chart_pred = (
    alt.Chart(df)
    .mark_line(point=True, strokeDash=[5,5], color="orange")
    .encode(x="Fecha:T", y="Demanda Predicha")
)
st.altair_chart(chart + chart_pred, use_container_width=True)

# Alertas de saturación
st.subheader("🔔 Alertas de Demanda")
for i in range(len(df)):
    if df["Demanda Predicha"][i] > 1800:
        st.warning(f"{df['Fecha'][i].date()}: Posible saturación de almacén ({df['Demanda Predicha'][i]} unidades)")

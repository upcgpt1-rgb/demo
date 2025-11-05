import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="Dashboard Predictivo - Contrans S.A.C.", layout="wide")

st.title("📊 Sistema Predictivo de Demanda Logística – Contrans S.A.C.")
st.markdown("**Versión demo interactiva** con simulación de predicción y planificación operativa.")

# --- Datos simulados ---
fechas = pd.date_range("2024-11-01", periods=10)
real = np.random.randint(1200, 1900, size=10)
pred = real + np.random.randint(-100, 100, size=10)
df = pd.DataFrame({"Fecha": fechas, "Demanda Real": real, "Demanda Predicha": pred})

# --- KPIs ---
col1, col2, col3 = st.columns(3)
col1.metric("Precisión del Modelo", "87 %")
col2.metric("Tiempo de Respuesta", "4.2 s")
col3.metric("Ocupación Actual", "92 %")

# --- Gráfico de demanda ---
st.subheader("📈 Predicción de demanda diaria (LSTM)")
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

# --- NUEVA SECCIÓN: Planificación operativa ---
st.subheader("🕓 Planificación de Disponibilidad por Día/Hora")
st.markdown("El operador de planning puede definir cuántos cupos disponibles ofrecer por día y hora, según la predicción del sistema.")

# Seleccionar día
selected_date = st.selectbox("Seleccionar fecha:", df["Fecha"].dt.strftime("%Y-%m-%d"))
filtered = df[df["Fecha"].dt.strftime("%Y-%m-%d") == selected_date]

# Generar horas simuladas
hours = [f"{h}:00" for h in range(6, 21)]  # 6 AM a 8 PM
pred_hourly = np.random.randint(60, 120, size=len(hours))
plan_hourly = []

st.write(f"### Predicción para {selected_date}")
for i, h in enumerate(hours):
    col1, col2 = st.columns(2)
    col1.write(f"**{h}** — Predicción: {pred_hourly[i]} movimientos")
    plan_value = col2.number_input(f"Cupos disponibles {h}", min_value=0, max_value=200, value=int(pred_hourly[i]*0.9))
    plan_hourly.append(plan_value)

# --- Comparación y alertas ---
st.subheader("🚨 Comparativo Predicción vs Disponibilidad")
comparison = pd.DataFrame({
    "Hora": hours,
    "Predicción": pred_hourly,
    "Disponibilidad": plan_hourly
})

st.dataframe(comparison, use_container_width=True)

# Gráfico comparativo
chart_compare = (
    alt.Chart(comparison)
    .transform_fold(["Predicción", "Disponibilidad"], as_=["Tipo", "Valor"])
    .mark_bar()
    .encode(
        x="Hora:N",
        y="Valor:Q",
        color="Tipo:N"
    )
)
st.altair_chart(chart_compare, use_container_width=True)

# --- Alertas automáticas ---
st.subheader("🔔 Alertas de Saturación")
for i in range(len(comparison)):
    if comparison["Disponibilidad"][i] < comparison["Predicción"][i]:
        st.warning(f"⚠️ {comparison['Hora'][i]}: Capacidad insuficiente (Predicción {comparison['Predicción'][i]} > Cupos {comparison['Disponibilidad'][i]})")
    else:
        st.success(f"✅ {comparison['Hora'][i]}: Capacidad adecuada.")

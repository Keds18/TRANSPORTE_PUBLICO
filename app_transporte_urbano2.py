import streamlit as st
import pandas as pd
from func_dimen_ruta import *
from graficas_rutas2 import graficar_recorrido_vehiculos2, graficar_oferta_acumulada

st.set_page_config(page_title="Dimensionamiento de Ruta Básica", layout="wide", page_icon="KDS_COMPANY.png")
st.title("🚍 Dimensionamiento de Ruta de Transporte Público")

st.markdown("""
### Herramienta para dimensionamiento de una ruta de transporte urbano
-Ingrese los parámetros correspondientes para la **Hora de Máxima Demanda** y la **Hora Valle**.
""")

st.sidebar.image("KDS_COMPANY.png", width=100)
st.sidebar.header("🔧 Parámetros de Entrada")
st.sidebar.markdown("Completa los siguientes campos para cada período horario:")

# Crear pestañas para cada horario
tab1, tab2 = st.tabs(["🕛 Hora de Máxima Demanda", "🌙 Hora Valle"])

# Función general para cada pestaña
def interfaz(tab, nombre_seccion):
    with tab:
        st.subheader(f"📋 Parámetros - {nombre_seccion}")

        col1, col2 = st.columns(2)
        with col1:
            longitud = st.number_input("📏 Longitud de ruta (km):", min_value=0.1, value=10.0, step=0.1, key=f"long_{nombre_seccion}")
            usuarios = st.number_input("👥 Usuarios por hora:", min_value=1, value=375, step=1, key=f"usuarios_{nombre_seccion}")
            capacidad = st.number_input("🚌 Capacidad por vehículo (sentados + de pie):", min_value=1, value=70, step=1, key=f"capacidad_{nombre_seccion}")
            ocupacion = st.slider("🔄 Factor de ocupación:", min_value=0.1, max_value=1.0, value=0.7, step=0.05, key=f"ocupacion_{nombre_seccion}")

        with col2:
            tiempo = st.number_input("⏱ Tiempo de recorrido (min):", min_value=1.0, value=45.0, step=1.0, key=f"tiempo_{nombre_seccion}")
            terminal = st.number_input("🏁 Tiempo en terminal (min):", min_value=0.0, value=6.0, step=0.5, key=f"terminal_{nombre_seccion}")
            hora_inicio = st.slider("🕓 Hora de inicio:", 0, 23, 7, key=f"ini_{nombre_seccion}")
            hora_fin = st.slider("🕗 Hora de fin:", 1, 24, 8, key=f"fin_{nombre_seccion}")

        # Calcular variables
        try:
            vop = calcular_velocidad_operacion(longitud, tiempo)
            intervalo = calcular_intervalo_despacho(capacidad, usuarios, ocupacion)
            tciclo = calcular_tiempo_ciclo(tiempo, terminal)
            N = calcular_numero_vehiculos(tciclo, intervalo)
            tciclo_corr = calcular_tiempo_ciclo_corregido(N, intervalo)
            tterm_corr = calcular_tiempo_terminal_corregido(tciclo_corr, tiempo)
            vcom = calcular_velocidad_comercial(longitud, tciclo_corr)
            eficiencia = calcular_eficiencia_sistema(vcom, N)
            frecuencia = calcular_frecuencia_paso(intervalo)
            capacidad_linea = calcular_capacidad_linea(frecuencia, capacidad)
            capacidad_ajustada = calcular_capacidad_linea_con_factor(capacidad_linea, ocupacion)
            reserva = calcular_vehiculos_reserva(N)
            itinerario = calcular_itinerario_despacho(hora_inicio, hora_fin, intervalo)

            # Control de estado
            if f"mostrar_resultados_{nombre_seccion}" not in st.session_state:
                st.session_state[f"mostrar_resultados_{nombre_seccion}"] = False
            if f"mostrar_graf_{nombre_seccion}" not in st.session_state:
                st.session_state[f"mostrar_graf_{nombre_seccion}"] = False

            # Botón para mostrar resultados
            if st.button("✅ Calcular resultados", key=f"calcular_{nombre_seccion}"):
                st.session_state[f"mostrar_resultados_{nombre_seccion}"] = True

            if st.session_state[f"mostrar_resultados_{nombre_seccion}"]:
                st.markdown("### 📊 Resultados del Cálculo")
                st.dataframe(pd.DataFrame({
                    "Parámetro": [
                        "Velocidad Operación (km/h)", "Intervalo (min)", "Tiempo Ciclo (min)",
                        "N° Vehículos requeridos", "Tiempo Ciclo Corregido (min)",
                        "Tiempo Terminal Corregido (min)", "Velocidad Comercial (km/h)",
                        "Eficiencia (km/h/veh)", "Frecuencia (veh/h)",
                        "Capacidad de Línea (pas/h)", "Capacidad Ajustada (pas/h)", "Vehículos de Reserva"
                    ],
                    "Valor": [
                        round(vop, 2), intervalo, tciclo, N, tciclo_corr,
                        round(tterm_corr, 2), round(vcom, 2), round(eficiencia, 2),
                        round(frecuencia, 2), round(capacidad_linea, 2),
                        round(capacidad_ajustada, 2), reserva
                    ]
                }))

            # Botón para mostrar gráficas
            if st.button("📉 Mostrar gráficas", key=f"mostrar_btn_{nombre_seccion}"):
                st.session_state[f"mostrar_graf_{nombre_seccion}"] = True

            if st.session_state[f"mostrar_graf_{nombre_seccion}"]:
                st.markdown("### 🚌 Gráfica de Recorrido de Vehículos")
                graficar_recorrido_vehiculos2(
                    tciclo_corr, intervalo, longitud, tiempo, tiempo, tterm_corr,
                    key=f"recorrido_{nombre_seccion}"
                )

                st.markdown("### 📈 Gráfica de Oferta Acumulada")
                graficar_oferta_acumulada(
                    intervalo, capacidad, ocupacion, usuarios,
                    key=f"oferta_{nombre_seccion}"
                )

                st.markdown("### 🕒 Itinerario de Despacho")
                st.code("\n".join(itinerario))

        except DimensionamientoError as e:
            st.error(f"❌ Error: {e}")

# Crear interfaces para ambas pestañas
interfaz(tab1, "HMD")
interfaz(tab2, "HV")

# Pie de pagina
st.markdown("""
<hr>
<div style='text-align: center; font-size: 0.9em; color: gray;'>
    <p>© 2025 <strong>Public_Transport_Kevin_Galindo_Antezana</strong> | All rights reserved, please reference.</p>
    <p>📧 Contact: <a href="mailto:keds1810@gmail.com">keds1810@gmail.com</a></p>
    <p>Developed with Python + Streamlit</p>
    </div>

""", unsafe_allow_html=True)

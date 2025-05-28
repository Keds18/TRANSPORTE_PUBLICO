import numpy as np
import plotly.graph_objects as go
import streamlit as st

# GRAFICA DE RECORRIDO DE VEHICULOS
def graficar_recorrido_vehiculos2(tiempo_ciclo, intervalo, longitud_ruta_km,
                                  tiempo_ida, tiempo_retorno, tiempo_terminal,
                                  key=None):
    """
    Gráfica los recorridos de ida y retorno de los buses durante un ciclo de operación,
    con estilo profesional y leyendas organizadas.

    Parámetros:
    - tiempo_ciclo: Duración total del ciclo de servicio (en minutos).
    - intervalo: Intervalo entre salidas de buses (en minutos).
    - longitud_ruta_km: Longitud de la ruta de ida (en kilómetros).
    - tiempo_ida: Duración del trayecto de ida (en minutos).
    - tiempo_retorno: Duración del trayecto de retorno (en minutos).
    - tiempo_terminal: Tiempo de permanencia en el terminal antes del retorno (en minutos).
    """
    
    # Colores profesionales
    color_ida = "#1f77b4"      # azul
    color_retorno = "#d62728"  # rojo
    color_terminal = "#4d4d4d" # gris oscuro (texto)

    # Tiempos de salida de los buses
    salidas = np.arange(0, tiempo_ciclo, intervalo)
    fig = go.Figure()

    for idx, salida in enumerate(salidas):
        bus = f'Bus {idx + 1}'

        # Trayecto de ida
        t_ida = np.linspace(salida, salida + tiempo_ida, 50)
        d_ida = np.linspace(0, longitud_ruta_km, 50)
        fig.add_trace(go.Scatter(
            x=t_ida, y=d_ida,
            mode='lines',
            line=dict(color=color_ida, width=2),
            name=f'{bus} - Ida',
            hovertemplate=f'<b>{bus}</b><br>Tiempo: %{{x:.1f}} min<br>Distancia: %{{y:.1f}} km',
            showlegend=False
        ))

        # Etiqueta final de ida
        fig.add_trace(go.Scatter(
            x=[t_ida[-1] + 3], y=[d_ida[-1]],
            mode='text',
            text=[bus],
            textposition="top center",
            textfont=dict(color=color_ida, size=9),
            showlegend=False
        ))

        # Trayecto de retorno
        inicio_retorno = salida + tiempo_ida + tiempo_terminal
        t_retorno = np.linspace(inicio_retorno, inicio_retorno + tiempo_retorno, 50)
        d_retorno = np.linspace(longitud_ruta_km, 0, 50)
        fig.add_trace(go.Scatter(
            x=t_retorno, y=d_retorno,
            mode='lines',
            line=dict(color=color_retorno, width=2),
            name=f'{bus} - Retorno',
            hovertemplate=f'<b>{bus}</b><br>Tiempo: %{{x:.1f}} min<br>Distancia: %{{y:.1f}} km',
            showlegend=False
        ))

    # Líneas de referencia para terminales
    fig.add_hline(y=0, line=dict(dash='dash', color='gray', width=1))
    fig.add_hline(y=longitud_ruta_km, line=dict(dash='dash', color='gray', width=1))

    # Anotaciones para terminales
    fig.add_annotation(
        xref='paper', yref='y',
        x=0.01, y=0.0,
        text='<b>Terminal A (Inicio)</b>',
        showarrow=False,
        font=dict(color=color_terminal, size=12),
        align="left",
        yshift=10
    )
    fig.add_annotation(
        xref='paper', yref='y',
        x=0.01, y=longitud_ruta_km,
        text='<b>Terminal B (Final)</b>',
        showarrow=False,
        font=dict(color=color_terminal, size=12),
        align="left",
        yshift=-10
    )

    # Elementos para leyenda
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines',
                             line=dict(color=color_ida, width=2), name='Trayecto de Ida'))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines',
                             line=dict(color=color_retorno, width=2), name='Trayecto de Retorno'))

    # Configuración visual
    fig.update_layout(
        title='<b>Recorrido de Vehículos: Ida y Retorno</b>',
        xaxis_title='<b>Tiempo (minutos)</b>',
        yaxis_title='<b>Distancia recorrida (km)</b>',
        xaxis=dict(tickmode='linear', dtick=intervalo, tickangle=0, tickfont=dict(size=10)),
        legend=dict(x=0.85, y=1, font=dict(size=11)),
        plot_bgcolor='white',
        hovermode='closest',
        width=1100,
        height=550,
        margin=dict(l=60, r=60, t=60, b=60)
    )

    fig.update_xaxes(
        showgrid=True, gridcolor='lightgray', gridwidth=0.5,
        zeroline=True, zerolinewidth=0.5, zerolinecolor='gray'
    )
    fig.update_yaxes(
        showgrid=True, gridcolor='rgb(217,217,217)', gridwidth=0.5,
        zeroline=True, zerolinewidth=0.5, zerolinecolor='rgb(217,217,217)'
    )

    # fig.show() se usa solo en jupyter notebbok
    st.plotly_chart(fig, use_container_width=True, key=key)

# GRAFICA DE VOLUMENES
def graficar_oferta_acumulada(intervalo, capacidad_bus, porcentaje_utilizacion, demanda_horaria, key=None):
    """
    Genera una gráfica de la oferta acumulada de pasajeros en una hora, basada en despachos regulares.

    Parámetros:
    -----------
    intervalo : float
        Intervalo entre despachos en minutos (default = 7.5)
    capacidad_bus : int
        Capacidad total de cada bus (default = 70 pasajeros)
    porcentaje_utilizacion : float
        Porcentaje de ocupación efectiva (default = 0.7, es decir 70%)
    demanda_horaria : int
        Línea de referencia de la demanda esperada por hora (default = 375 pasajeros)
    """

    # Cálculos base
    capacidad_util = capacidad_bus * porcentaje_utilizacion
    tiempos_despacho = np.arange(0, 60 + 0.1, intervalo)
    oferta_acumulada = np.arange(1, len(tiempos_despacho) + 1) * capacidad_util

    # Crear figura
    fig = go.Figure()

    # Línea escalonada
    fig.add_trace(go.Scatter(
        x=tiempos_despacho,
        y=oferta_acumulada,
        mode='lines',
        line=dict(shape='hv', color='green', width=2),
        fill='tozeroy',
        fillcolor='rgba(0,128,0,0.15)',
        name='Oferta acumulada'
    ))

    # Marcadores de buses
    fig.add_trace(go.Scatter(
        x=tiempos_despacho,
        y=oferta_acumulada,
        mode='markers',
        marker=dict(color='black', size=6),
        name='Buses'
    ))

    # Etiquetas de texto
    for t, p in zip(tiempos_despacho, oferta_acumulada):
        fig.add_annotation(
            x=t + 1,
            y=p + 8,
            text=f'{int(p)}',
            showarrow=False,
            font=dict(size=10),
            align='center'
        )

    # Línea horizontal de demanda
    fig.add_shape(
        type='line',
        x0=0,
        y0=demanda_horaria,
        x1=60,
        y1=demanda_horaria,
        line=dict(color='red', width=2, dash='dash'),
    )
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='red', width=2, dash='dash'),
        name='Demanda horaria'
    ))

    # Etiqueta de la demanda
    fig.add_annotation(
        x=30, y=demanda_horaria,
        text=f'Demanda horaria ({demanda_horaria})',
        showarrow=False,
        font=dict(size=12, color='red'),
        yshift=-18,
        bgcolor='white'
    )

    # Layout
    fig.update_layout(
        title='<b>Oferta acumulada de pasajeros durante 1 hora</b>',
        xaxis_title='<b>Tiempo (min)</b>',
        yaxis_title='<b>Pasajeros acumulados</b>',
        xaxis=dict(
            tickmode='array',
            tickvals=np.arange(0, 65, intervalo),
            range=[0, 61]
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=np.arange(0, max(oferta_acumulada)+75, 50),
            range=[0, max(oferta_acumulada) + 50]
        ),
        legend=dict(x=0.75, y=0.1),
        width=900,
        height=500
    )

    # fig.show() se usa solo en jupyter notebbok
    
    st.plotly_chart(fig, use_container_width=True, key=key)

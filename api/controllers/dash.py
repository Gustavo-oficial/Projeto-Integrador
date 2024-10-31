import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from config.db import *

query = 'SELECT * FROM tb_registro' 

# Carregar os dados do MySQL
df = conexao(query)

# Botão para atualização dos dados
if st.button('Atualizar dados'):
    df = conexao(query)
    
# Menu lateral
st.sidebar.header('Selecione a informação para gerar o gráfico')

# Seleção de colunas X
# Select box -> cria uma caixa de seleção na barra lateral
colunaX = st.sidebar.selectbox(
    'Eixo X',
    options=['umidade','temperatura', 'pressao', 'altitude', 'co2', 'poeira'],
    index=0
)

colunaY = st.sidebar.selectbox(
    'Eixo Y',
    options=['umidade','temperatura', 'pressao', 'altitude', 'co2', 'poeira'],
    index=1
)

# Verificar quais os atributos do filtro
def filtros(atributo):
    return atributo in [colunaX, colunaY]

# Filtro de range -> SLIDER
st.sidebar.header('Selecione o Filtro')

# Temperatura
if filtros('temperatura'):
    temperatura_range = st.sidebar.slider(
        'Temperatura (°c)',
        min_value=float(df['temperatura'].min()),
        # Valor mínimo
        max_value=float(df['temperatura'].max()),
        # Valor máximo 
        value=(float(df['temperatura'].min()), float(df['temperatura'].max())),
        # Faixa de valores slecionado
        step=0.1
        # Incremento para cada movimento do slider
    )
    
# Pressão
if filtros('pressao'):
    pressao_range = st.sidebar.slider(
        'Pressão',
        min_value=float(df['pressao'].min()),
        # Valor mínimo
        max_value=float(df['pressao'].max()),
        # Valor máximo 
        value=(float(df['pressao'].min()), float(df['pressao'].max())),
        # Faixa de valores slecionado
        step=0.1
        # Incremento para cada movimento do slider
    )
    
# Umidade
if filtros('umidade'):
    umidade_range = st.sidebar.slider(
        'Umidade %',
        min_value=float(df['umidade'].min()),
        # Valor mínimo
        max_value=float(df['umidade'].max()),
        # Valor máximo 
        value=(float(df['umidade'].min()), float(df['umidade'].max())),
        # Faixa de valores slecionado
        step=0.1
        # Incremento para cada movimento do slider
    )
    
# Altitude
if filtros('altitude'):
    altitude_range = st.sidebar.slider(
        'Altitude',
        min_value=float(df['altitude'].min()),
        # Valor mínimo
        max_value=float(df['altitude'].max()),
        # Valor máximo 
        value=(float(df['altitude'].min()), float(df['altitude'].max())),
        # Faixa de valores slecionado
        step=0.1
        # Incremento para cada movimento do slider
    )
    
# CO2
if filtros('co2'):
    co2_range = st.sidebar.slider(
        'CO2 pmm',
        min_value=float(df['co2'].min()),
        # Valor mínimo
        max_value=float(df['co2'].max()),
        # Valor máximo 
        value=(float(df['co2'].min()), float(df['co2'].max())),
        # Faixa de valores slecionado
        step=0.1
        # Incremento para cada movimento do slider
    )
    
# Poeira
if filtros('poeira'):
    poeira_range = st.sidebar.slider(
        'Poeira',
        min_value=float(df['poeira'].min()),
        # Valor mínimo
        max_value=float(df['poeira'].max()),
        # Valor máximo 
        value=(float(df['poeira'].min()), float(df['poeira'].max())),
        # Faixa de valores slecionado
        step=0.1
        # Incremento para cada movimento do slider
    )
    
df_selecionado = df.copy()

if filtros('temperatura'):
    df_selecionado = df_selecionado[
        (df_selecionado['temperatura'] >= temperatura_range[0]) &
        (df_selecionado['temperatura'] <= temperatura_range[1]) 
    ]
    
if filtros('pressao'):
    df_selecionado = df_selecionado[
        (df_selecionado['pressao'] >= pressao_range[0]) &
        (df_selecionado['pressao'] <= pressao_range[1]) 
    ]
if filtros('umidade'):
    df_selecionado = df_selecionado[
        (df_selecionado['umidade'] >= umidade_range[0]) &
        (df_selecionado['umidade'] <= umidade_range[1]) 
    ]
if filtros('altitude'):
    df_selecionado = df_selecionado[
        (df_selecionado['altitude'] >= altitude_range[0]) &
        (df_selecionado['altitude'] <= altitude_range[1]) 
    ]
if filtros('co2'):
    df_selecionado = df_selecionado[
        (df_selecionado['co2'] >= co2_range[0]) &
        (df_selecionado['co2'] <= co2_range[1]) 
    ]
if filtros('poeira'):
    df_selecionado = df_selecionado[
        (df_selecionado['poeira'] >= poeira_range[0]) &
        (df_selecionado['poeira'] <= poeira_range[1]) 
    ]
    
# Graficos
def Dash():
    with st.expander('Tabela'):
        mostrar_dados = st.multiselect(
            'Filtro: ',
            df_selecionado.columns,
            default=[],
            key='showData_home'
        )

        if mostrar_dados:
            st.write(df_selecionado[mostrar_dados])
    
    # Calculos estatisticos
    if not df_selecionado.empty:
        media_umidade = df_selecionado['umidade'].mean()
        media_temperatura = df_selecionado['temperatura'].mean()
        media_co2 = df_selecionado['co2'].mean()
        
        media1, media2, media3 = st.columns(3, gap='large')
        
        with media1:
            st.info('Média de Registros de Umidade', icon='📌')
            st.metric(label='Média', value=f'{media_umidade:.2f}')
            
        with media2:
            st.info('Média de Registros de Temperatura', icon='📌')
            st.metric(label='Média', value=f'{media_temperatura:.2f}')
            
        with media3:
            st.info('Média de Registros de CO2', icon='📌')
            st.metric(label='Média', value=f'{media_co2:.2f}')
            
        st.markdown(''''---------''')

def graficos():
    st.title("Dashboard Monitoramento")

    # Tabs for each simplified plot
    aba1, aba2, aba3, aba4 = st.tabs([
        "Gráfico de Barra", "Gráfico de Dispersão", "Histograma de Umidade", "Linha de Temperatura"
    ])

    # Bar Plot
    with aba1:
        if df_selecionado.empty:
            st.write("Nenhum dado está disponível para gerar o gráfico")
            return
        
        if colunaX == colunaY:
            st.warning("Selecione uma opção diferente para os eixos X e Y")
            return

        try:
            fig_valores = px.bar(
                df_selecionado,
                x=colunaX,
                title=f"Contagem de Registros por {colunaX.capitalize()}",
                labels={colunaX: colunaX.capitalize()},
                template="simple_white",
                color_discrete_sequence=["#0083b8"]
            )
            st.plotly_chart(fig_valores, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao criar o gráfico: {e}")

    # Scatter Plot
    with aba2:
        if df_selecionado.empty:
            st.write("Nenhum dado está disponível para gerar o gráfico de dispersão")
        elif colunaX == colunaY:
            st.warning("Selecione uma opção diferente para os eixos X e Y")
        else:
            fig_scatter = px.scatter(
                df_selecionado,
                x=colunaX,
                y=colunaY,
                title=f"Gráfico de Dispersão entre {colunaX.capitalize()} e {colunaY.capitalize()}",
                labels={colunaX: colunaX.capitalize(), colunaY: colunaY.capitalize()},
                template="simple_white",
                color_discrete_sequence=["#ff7675"]
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

    # Humidity Histogram
    with aba3:
        if "umidade" in df_selecionado.columns:
            fig_hist = px.histogram(
                df_selecionado,
                x="umidade",
                title="Distribuição de Umidade",
                labels={"umidade": "Umidade (%)"},
                nbins=30,
                color_discrete_sequence=["#00b894"],
                template="simple_white"
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.write("Dados de umidade não disponíveis para gerar o histograma.")

    # Temperature Line Plot
    with aba4:
        if "temperatura" in df_selecionado.columns:
            print("dsad", df_selecionado)
            fig_line = px.line(
                df_selecionado,
                x="tempo_registro",
                y="temperatura",
                title="Variação de Temperatura",
                labels={"index": "Data Registro (D:H)", "temperatura": "Temperatura (°C)"},
                template="simple_white",
                color_discrete_sequence=["#0984e3"]
            )
            
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.write("Dados de temperatura não estão disponíveis para gerar o gráfico de linha.")

         
Dash()
graficos()
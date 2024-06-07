import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Estatísticas Premier League 23/24",
                   page_icon="🏴󠁧󠁢󠁥󠁮󠁧󠁿",
                   layout="wide")

# Adicionando título na parte de cima com tamanho maior
st.markdown(
    "<h1 style='text-align: center; font-size: 3em;'>Estatísticas Premier League 23/24</h1>",
    unsafe_allow_html=True
)

# Carregar o arquivo Excel
df = pd.read_excel('statsPL 23_24.xlsx')

# Seção de filtragem no sidebar
st.sidebar.header("Filtre aqui:")
time = st.sidebar.multiselect(
    "Selecione o(s) time(s):",
    options=df['time'].unique(),
    default=df['time'].unique()[:1]
)

# Exibir a quantidade de times selecionados, centralizado
time_text = "Time" if len(time) == 1 else "Times"
st.markdown(
    f"<h2 style='text-align: center;'>Quantidade de Times selecionados:</h2>",
    unsafe_allow_html=True
)
st.markdown(
    f"<h2 style='text-align: center;'>{len(time)} {time_text}</h2>",
    unsafe_allow_html=True
)

# Seção de seleção de tipo de jogo
tipo_jogo = st.sidebar.radio(
    "Selecione o tipo de jogo:",
    options=['Casa', 'Fora', 'Geral']
)

# Filtragem das colunas com base no tipo de jogo
if tipo_jogo == 'Casa':
    cols_filtradas = [col for col in df.columns if col.endswith('_casa')]
elif tipo_jogo == 'Fora':
    cols_filtradas = [col for col in df.columns if col.endswith('_fora')]
else:
    cols_filtradas = [col for col in df.columns if '_geral' in col]

# Filtragem do DataFrame com base nos times selecionados
cols_selecionadas = ['time'] + cols_filtradas
df_filtrado = df[df['time'].isin(time)][cols_selecionadas]

# Cálculo de Derrotas, Empates e Vitórias
df_filtrado['Derrotas'] = df_filtrado.filter(like='Derrotas').sum(axis=1)
df_filtrado['Empates'] = df_filtrado.filter(like='Empates').sum(axis=1)
df_filtrado['Vitorias'] = df_filtrado.filter(like='Vitorias').sum(axis=1)

# Preparação dos dados para o gráfico de barras de resultados
df_grafico = df_filtrado.melt(id_vars=['time'], value_vars=['Derrotas', 'Empates', 'Vitorias'], 
                              var_name='Resultado', value_name='Quantidade')
cores = {'Derrotas': 'red', 'Empates': 'yellow', 'Vitorias': 'blue'}
fig1 = px.bar(df_grafico, x='time', y='Quantidade', color='Resultado', barmode='stack',
              title='Resultados: Vitória/Empate/Derrota', labels={'time': 'Time', 'Quantidade': 'Jogos', 'Resultado': 'Resultado'},
              color_discrete_map=cores)

st.plotly_chart(fig1)

# Cálculo de Pontos
df_filtrado['Pontos'] = df_filtrado.filter(like='Pontos').sum(axis=1)

# Preparação dos dados para o gráfico de pizza de aproveitamento
pizza_data = df_filtrado[['time', 'Pontos']]
fig2 = px.pie(pizza_data, names='time', values='Pontos',
              title='Aproveitamento (Em comparação com outros times)',
              color_discrete_sequence=px.colors.qualitative.Set3)

st.plotly_chart(fig2)

# Cálculo de Gols Feitos e Gols Levados
df_filtrado['Gols Feitos'] = df_filtrado.filter(like='GolsFeitos').sum(axis=1)
df_filtrado['Gols Levados'] = df_filtrado.filter(like='GolsLevados').sum(axis=1)

# Preparação dos dados para o gráfico de barras de gols feitos/levados
df_grafico = df_filtrado.melt(id_vars=['time'], value_vars=['Gols Feitos', 'Gols Levados'], 
                              var_name='Resultado', value_name='Quantidade')
cores = {'Gols Levados': 'red', 'Gols Feitos': 'blue'}
fig3 = px.bar(df_grafico, x='time', y='Quantidade', color='Resultado', barmode='stack',
              title='Gols Feitos / Gols Levados', labels={'time': 'Time', 'Quantidade': 'Gols Feitos/Levados', 'Resultado': 'Resultado'},
              color_discrete_map=cores)

st.plotly_chart(fig3)

# Cálculo de Gols Feitos Esperados
df_filtrado['Gols Feitos Esperados'] = df_filtrado.filter(like='ptsmaisEsperados').sum(axis=1)
df_grafico = df_filtrado.melt(id_vars=['time'], value_vars=['Gols Feitos Esperados'], 
                              var_name='Resultado', value_name='Quantidade')
cores = {'Gols Feitos Esperados': 'blue'}
fig4 = px.bar(df_grafico, x='Quantidade', y='time', color='Resultado', barmode='stack',
              title='Gols Feitos Esperados', labels={'time': 'Time', 'Quantidade': 'Gols Feitos Esperados', 'Resultado': 'Resultado'},
              color_discrete_map=cores)

# Cálculo de Gols Levados Esperados
df_filtrado['Gols Levados Esperados'] = df_filtrado.filter(like='ptsmenosEsperados').sum(axis=1)
df_grafico = df_filtrado.melt(id_vars=['time'], value_vars=['Gols Levados Esperados'], 
                              var_name='Resultado', value_name='Quantidade')
cores = {'Gols Levados Esperados': 'red'}
fig5 = px.bar(df_grafico, x='Quantidade', y='time', color='Resultado', barmode='stack',
              title='Gols Levados Esperados', labels={'time': 'Time', 'Quantidade': 'Gols Levados Esperados', 'Resultado': 'Resultado'},
              color_discrete_map=cores)

# Exibir gráficos lado a lado
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig4)
with col2:
    st.plotly_chart(fig5)

# Cálculo do Saldo de Gols
df_filtrado['Saldo'] = df_filtrado.filter(like='SaldoDeGols').sum(axis=1)
df_grafico_saldo = df_filtrado[['time', 'Saldo']]
df_grafico_saldo['Positivo'] = df_grafico_saldo['Saldo'].apply(lambda x: 'Saldo Positivo' if x > 0 else 'Saldo Negativo')

fig_saldo = px.bar(df_grafico_saldo, x='time', y='Saldo', color='Positivo',
                   title='Saldo de Gols', labels={'time': 'Time', 'Saldo': 'Saldo de Gols', 'Positivo': 'Positivo/Negativo'},
                   color_discrete_map={'Saldo Positivo': 'blue', 'Saldo Negativo': 'red'})

st.plotly_chart(fig_saldo)

# Ordenar o DataFrame em ordem decrescente com base na coluna 'Pontos'
df_filtrado = df_filtrado.sort_values(by='Pontos', ascending=False)

# Criar o gráfico de barras para a tabela de pontos
fig_bar = px.bar(df_filtrado, x='time', y='Pontos',
                 title='Tabela de pontos:',
                 labels={'time': 'Time', 'Pontos': 'Pontos'},
                 color='time',
                 hover_data=['Pontos'])

# Mostrar o gráfico com Streamlit
st.plotly_chart(fig_bar)
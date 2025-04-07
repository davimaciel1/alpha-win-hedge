
import streamlit as st
from utils import recomendar_estrategia

st.set_page_config(page_title="Painel Alpha WIN – Estratégia Inteligente Davi Maciel", layout="wide")

st.title("🚀 Painel Alpha WIN – Estratégia Inteligente Davi Maciel")
st.markdown("🧠 Hedge nas quedas • 🎯 Lucro nas altas • 🎛️ Controle total")

cenario = st.selectbox("Cenário atual do índice:", ["Baixa", "Alta"])
valor_carteira = st.number_input("Valor da carteira (R$)", value=100000)
percentual_protecao = st.slider("Quanto da carteira deseja proteger (%)", 10, 100, 100)
saldo_disponivel = st.number_input("Saldo disponível para operar (R$)", value=3000)
preco_atual = st.number_input("Preço atual do IBOV11", value=131000)
preco_simulado = st.number_input("Preço simulado do IBOV11 após movimento", value=127000)
usar_stop = st.checkbox("Usar Stop Loss nas opções?", value=False)
percentual_stop = st.slider("Stop % sobre prêmio da opção", 10, 100, 50) if usar_stop else 100

if st.button("Calcular Estratégia"):
    resultado = recomendar_estrategia(
        cenario, valor_carteira, percentual_protecao,
        saldo_disponivel, preco_atual, preco_simulado,
        usar_stop, percentual_stop
    )
    st.write("### 💡 Estratégia Recomendada:")
    st.dataframe(resultado)

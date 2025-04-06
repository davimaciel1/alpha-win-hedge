
import streamlit as st
from utils import recomendar_estrategia

st.set_page_config(page_title="Painel Alpha WIN – Estratégia Inteligente Davi Maciel", layout="wide")

st.title("🚀 Painel Alpha WIN – Estratégia Inteligente Davi Maciel")
st.markdown("🧠 Hedge automatizado nas quedas • 🎯 Lucro cirúrgico nas altas")

cenario = st.selectbox("Cenário atual do índice:", ["Baixa", "Alta"])
valor_carteira = st.number_input("Valor da carteira (R$)", value=100000)
preco_atual = st.number_input("Preço atual do WIN", value=131000)
preco_simulado = st.number_input("Preço simulado do WIN após movimento", value=127000)
usar_stop = st.checkbox("Usar Stop Loss nas opções?", value=False)
percentual_stop = st.slider("Stop % sobre prêmio da opção", 10, 100, 50) if usar_stop else 100

if st.button("Calcular Estratégia"):
    resultado = recomendar_estrategia(cenario, valor_carteira, preco_atual, preco_simulado, usar_stop, percentual_stop)
    st.write("### 💡 Estratégia Recomendada:")
    st.dataframe(resultado)

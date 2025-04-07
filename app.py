
import streamlit as st
from utils import (
    recomendar_estrategia,
    gerar_grafico_payoff,
    mostrar_curva_risco,
    atualizar_dados_mercado,
    listar_pozinhos_baratos
)

st.set_page_config(page_title="Alpha WIN v4.4 – Painel Inteligente", layout="wide")
st.title("📊 Painel Alpha WIN – Estratégia Inteligente")
st.caption("🔧 Versão: Alpha WIN v4.4 – Atualizado em 07/04/2025")

with st.sidebar:
    st.header("⚙️ Configurações")
    cenario = st.selectbox("Cenário atual:", ["Baixa", "Alta"])
    carteira = st.number_input("Valor da carteira (R$)", value=100000)
    protecao_pct = st.slider("Proteção desejada (%)", 10, 100, 100)
    saldo = st.number_input("Saldo disponível (R$)", value=3000)
    preco_atual = st.number_input("IBOV11 agora:", value=131000)
    preco_simulado = st.number_input("IBOV11 após queda", value=127000)
    usar_stop = st.checkbox("Usar Stop Loss nas PUTs?", value=False)
    stop_pct = st.slider("Stop %", 10, 100, 50) if usar_stop else 100
    usar_pozinho = st.checkbox("🧨 Usar Estratégia do Pózinho?", value=True)
    valor_pozinho = st.slider("Quanto investir no pózinho (R$)", 50, 1000, 200) if usar_pozinho else 0

    if st.button("🔄 Atualizar dados do mercado"):
        atualizar_dados_mercado()
        st.success("✅ Dados atualizados (válido por 10 min)")

if st.button("🚀 Calcular Estratégia"):
    resultado, explicacao = recomendar_estrategia(
        cenario, carteira, protecao_pct, saldo,
        preco_atual, preco_simulado, usar_stop,
        stop_pct, usar_pozinho, valor_pozinho
    )
    st.write("### 💡 Estratégia Recomendada:")
    st.dataframe(resultado)
    st.info(explicacao)

    if "Nenhuma opção de pózinho" in explicacao:
        st.warning("Nenhum pózinho viável encontrado. Veja os 5 mais baratos com liquidez:")
        st.dataframe(listar_pozinhos_baratos())

    st.write("### 📈 Gráfico de Payoff")
    fig = gerar_grafico_payoff(preco_atual, preco_simulado)
    st.pyplot(fig)

    st.write("### 📉 Curva de Risco")
    mostrar_curva_risco(carteira, protecao_pct, saldo)

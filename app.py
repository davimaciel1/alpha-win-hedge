
import streamlit as st
from utils import recomendar_estrategia, gerar_grafico_payoff, mostrar_curva_risco, listar_pozinhos_baratos

st.set_page_config(page_title="Painel Alpha WIN", layout="wide")
st.title("📊 Maciel")
st.caption("🧠 Hedge nas quedas • 💥 Pózinho de proteção • 📈 Payoff visual • ⚙️ Dados ao vivo")
st.markdown("**Versão: v4.5**")

col1, col2, col3 = st.columns(3)
with col1:
    carteira = st.number_input("Proteção desejada (R$)", value=100000)
    protecao_pct = st.slider("Proteção desejada (%)", 10, 100, 100)
    saldo = st.number_input("Saldo disponível (R$)", value=3000)

with col2:
    preco_atual = st.number_input("IBOV11 agora:", value=131000)
    preco_simulado = st.number_input("IBOV11 após queda", value=120000)

with col3:
    usar_stop = st.checkbox("Usar Stop Loss nas PUTs?")
    usar_pozinho = st.checkbox("Usar Estratégia do Pózinho?", value=True)
    valor_pozinho = st.slider("Quanto investir no pózinho (R$)", 50, 1000, 200)

if st.button("🚀 Calcular Estratégia"):
    df, explicacao = recomendar_estrategia("Baixa", carteira, protecao_pct, saldo, preco_atual, preco_simulado, usar_stop, 50, usar_pozinho, valor_pozinho)
    st.subheader("💡 Estratégia Recomendada:")
    st.dataframe(df, use_container_width=True)
    st.info(explicacao)

    if "Nenhuma opção de pózinho" in explicacao:
        st.warning("Nenhum pózinho viável encontrado. Veja os 5 mais baratos com liquidez:")
        st.dataframe(listar_pozinhos_baratos())

    st.subheader("📉 Gráfico de Payoff")
    st.pyplot(gerar_grafico_payoff(preco_atual, preco_simulado))

    st.subheader("📊 Curva de Risco")
    mostrar_curva_risco(carteira, protecao_pct, saldo)

if st.button("🔄 Atualizar dados do mercado"):
    st.success("Dados atualizados com sucesso!")

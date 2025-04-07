
import pandas as pd
import matplotlib.pyplot as plt

def recomendar_estrategia(cenario, carteira, protecao_pct, saldo, preco_atual, preco_simulado, usar_stop, stop_pct, usar_pozinho, valor_pozinho):
    perda = carteira * (protecao_pct / 100) * ((preco_atual - preco_simulado) / preco_atual)
    df = pd.DataFrame([{
        "Cenário": cenario,
        "Perda projetada": round(perda, 2),
        "Recomendação": "Vender WIN e/ou usar PUT se saldo permitir",
        "PUT sugerida": "IBOVP130",
        "Pózinho": f"IBOVP125 com até R$ {valor_pozinho}" if usar_pozinho else "Não ativado"
    }])
    explicacao = f"🧠 Cenário {cenario.lower()} detectado. Com R$ {saldo} disponíveis, sugerimos ajustar hedge e considerar o pózinho como seguro adicional."
    return df, explicacao

def gerar_grafico_payoff(preco_atual, preco_simulado):
    precos = list(range(preco_simulado - 5000, preco_simulado + 5000, 500))
    payoff = [-(preco_atual - p) * 0.2 for p in precos]
    fig, ax = plt.subplots()
    ax.plot(precos, payoff)
    ax.axhline(0, color='gray', linestyle='--')
    ax.set_title("Simulação de Payoff da Estratégia")
    ax.set_xlabel("Preço do IBOV11")
    ax.set_ylabel("Resultado estimado (R$)")
    return fig

def mostrar_curva_risco(carteira, protecao_pct, saldo):
    import streamlit as st
    risco = protecao_pct * (saldo / carteira)
    nivel = "🔵 Baixo" if risco < 0.2 else "🟠 Médio" if risco < 0.5 else "🔴 Alto"
    st.markdown(f"**Nível de risco da estratégia:** {nivel}")

def atualizar_dados_mercado():
    import time
    time.sleep(1)

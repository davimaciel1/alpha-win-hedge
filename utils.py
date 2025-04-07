
import pandas as pd
import matplotlib.pyplot as plt

def obter_preco_pozinho_real():
    return 1.23  # Simulação

def listar_pozinhos_baratos():
    # Simulação de tabela com opções
    dados = {
        "Ticker": ["IBOVP122", "IBOVP123", "IBOVP124", "IBOVP125", "IBOVP126"],
        "Preço": [0.25, 0.32, 0.38, 0.41, 0.45],
        "Strike": [122000, 123000, 124000, 125000, 126000],
        "Volume": [4500, 3800, 2700, 2200, 1900]
    }
    return pd.DataFrame(dados)

def recomendar_estrategia(cenario, carteira, protecao_pct, saldo, preco_atual, preco_simulado, usar_stop, stop_pct, usar_pozinho, valor_pozinho):
    perda_proj = carteira * (protecao_pct / 100) * ((preco_atual - preco_simulado) / preco_atual)

    resultado = {
        "Cenário": cenario,
        "Perda projetada": round(perda_proj, 2),
    }

    explicacao = ""

    if cenario == "Baixa":
        preco_put = 3630
        lucro_put = (130000 - preco_simulado) - (preco_put * (stop_pct / 100)) if usar_stop else (130000 - preco_simulado) - preco_put
        qtd_puts = int(min(saldo // preco_put, perda_proj // lucro_put)) if lucro_put > 0 else 0
        custo_total_put = qtd_puts * preco_put
        cobertura_put = qtd_puts * lucro_put

        pontos_necessarios = perda_proj - cobertura_put
        contratos_win = int(pontos_necessarios // ((preco_atual - preco_simulado) * 0.2)) if pontos_necessarios > 0 else 0

        resultado.update({
            "PUT sugerida": f"{qtd_puts}x IBOVP130",
            "Custo total PUT": f"R$ {custo_total_put:.2f}",
            "Venda WIN": f"{contratos_win} contrato(s)",
            "Cobertura com PUT": f"R$ {cobertura_put:.2f}",
        })

        explicacao += f"🛡️ Compre {qtd_puts} PUTs IBOVP130 a R$ {preco_put:.2f} → total R$ {custo_total_put:.2f}\n"
        if contratos_win > 0:
            explicacao += f"📉 Venda {contratos_win} contrato(s) de WIN usando ações como garantia.\n"

        if usar_pozinho:
            preco_pozinho_real = obter_preco_pozinho_real()
            if preco_pozinho_real > 0.10:
                resultado["Pózinho"] = "Nenhum viável (acima de R$ 0,10)"
                explicacao += "❌ Nenhuma opção de pózinho com preço até R$ 0,10 e liquidez disponível.\n"
            else:
                qtd_pozinho = int((valor_pozinho * 100) // (preco_pozinho_real * 100))
                lucro_pozinho = max(0, 125000 - preco_simulado)
                retorno_potencial = qtd_pozinho * lucro_pozinho

                resultado.update({
                    "Pózinho": f"{qtd_pozinho}x IBOVP125 a R$ {preco_pozinho_real:.2f}",
                    "Retorno potencial": f"R$ {retorno_potencial:.2f} (se cair até 125.000)"
                })
                explicacao += f"💣 Pózinho: {qtd_pozinho}x IBOVP125 a R$ {preco_pozinho_real:.2f}. Se índice cair até 125k, pode virar R$ {retorno_potencial:.2f}\n"
    else:
        resultado.update({
            "CALL sugerida": "IBOVC134",
            "Venda PUT (prêmio)": "IBOVP125"
        })
        explicacao = "🚀 Alta detectada: compre CALLs para lucro ou venda PUTs para gerar prêmio extra."

    return pd.DataFrame([resultado]), explicacao

def gerar_grafico_payoff(preco_atual, preco_simulado):
    precos = list(range(preco_simulado - 4000, preco_simulado + 4000, 500))
    payoff = [-(preco_atual - p) * 0.2 for p in precos]
    fig, ax = plt.subplots()
    ax.plot(precos, payoff, marker='o')
    ax.axhline(0, color='gray', linestyle='--')
    ax.set_xlabel("Preço do IBOV11")
    ax.set_ylabel("Resultado estimado (R$)")
    ax.set_title("Gráfico de Payoff (venda WIN)")
    return fig

def mostrar_curva_risco(carteira, protecao_pct, saldo):
    import streamlit as st
    risco = (protecao_pct / 100) * (saldo / carteira)
    if risco < 0.2:
        nivel = "🔵 Baixo"
    elif risco < 0.5:
        nivel = "🟠 Médio"
    else:
        nivel = "🔴 Alto"
    st.markdown(f"**Nível de risco:** {nivel}")

def atualizar_dados_mercado():
    import time
    time.sleep(1)

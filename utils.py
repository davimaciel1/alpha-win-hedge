
import pandas as pd

def recomendar_estrategia(cenario, carteira, protecao_pct, saldo, preco_atual, preco_simulado, usar_stop, stop_pct):
    protecao_desejada = carteira * (protecao_pct / 100)
    perda = protecao_desejada * ((preco_atual - preco_simulado) / preco_atual)

    resultado = {
        'Cenário': cenario,
        'Proteção desejada (R$)': round(protecao_desejada, 2),
        'Perda projetada': round(perda, 2),
        'Saldo disponível': saldo
    }

    if cenario == "Baixa":
        strike = 130000
        premio = 3630
        lucro_put_bruto = max(0, strike - preco_simulado)
        lucro_put = lucro_put_bruto - (premio * (stop_pct / 100)) if usar_stop else lucro_put_bruto - premio

        if lucro_put <= 0:
            qtd_puts = 0
        else:
            qtd_puts = int(min(saldo // premio, perda // lucro_put))

        custo_total = qtd_puts * premio
        cobertura = qtd_puts * lucro_put

        resultado.update({
            'PUT sugerida': "IBOVP130",
            'Strike': strike,
            'Prêmio': premio,
            'Lucro por opção': round(lucro_put, 2),
            'Qtd opções': qtd_puts,
            'Custo total': round(custo_total, 2),
            'Cobertura estimada': round(cobertura, 2)
        })

        pontos_necessarios = perda - cobertura
        pontos_por_contrato = (preco_atual - preco_simulado) * 0.2
        contratos_win = int(pontos_necessarios // pontos_por_contrato) if pontos_necessarios > 0 else 0

        resultado['Contratos WIN (venda)'] = contratos_win

    else:
        resultado.update({
            'CALL sugerida': "IBOVC134",
            'PUT a vender': "IBOVP125",
            'Estratégia': "Compra de CALL para ganho ou venda de PUT para prêmio"
        })

    return pd.DataFrame([resultado])

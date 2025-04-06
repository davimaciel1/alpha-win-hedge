
import pandas as pd

def recomendar_estrategia(cenario, carteira, preco_atual, preco_simulado, usar_stop, stop_pct):
    # Simulação fictícia para exibir lógica
    perda = carteira * ((preco_atual - preco_simulado) / preco_atual)
    contratos_win = round(perda / ((preco_atual - preco_simulado) * 0.2))
    opcao_put = {
        'Código': 'WINP130',
        'Strike': 130000,
        'Prêmio': 390,
        'Lucro PUT (sem stop)': max(0, 130000 - preco_simulado) - 390,
        'Lucro PUT (com stop)': max(0, (130000 - preco_simulado) - (390 * stop_pct / 100))
    }
    df = pd.DataFrame([{
        'Cenário': cenario,
        'Perda Projetada': round(perda, 2),
        'Contratos WIN (hedge)': contratos_win if cenario == 'Baixa' else 0,
        'CALL sugerida': 'WINC134' if cenario == 'Alta' else '-',
        'PUT sugerida': opcao_put['Código'] if cenario == 'Baixa' else '-',
        'Lucro PUT': opcao_put['Lucro PUT (com stop)' if usar_stop else 'Lucro PUT (sem stop)']
    }])
    return df

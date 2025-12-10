"""
Módulo de Formatação de Cardápios
Exibe cardápios no estilo profissional de nutricionista
"""

from datetime import datetime
from typing import Dict, List, Tuple
from data.regras_culinarias import normalizar_texto


def exibir_cardapio_nutricionista(cardapio, metas: Dict, config_refeicoes: List[Tuple]):
    """
    Exibe o cardápio em formato profissional estilo nutricionista.
    
    Args:
        cardapio: Objeto CardapioCompleto
        metas: Dicionário com metas nutricionais
        config_refeicoes: Lista de tuplas (nome_refeicao, porcentagem)
    """
    
    # Cabeçalho
    print("\n" + "═" * 80)
    print(" " * 20 + "🍽️  PLANO ALIMENTAR PERSONALIZADO")
    print("═" * 80)
    print(f"Elaborado por: Sistema IA Nutricional")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y')}")
    print(f"Meta Diária: {metas['meta_calorias']:.0f} kcal | " 
          f"Macros: {metas['pct_carbo']:.0f}C/{metas['pct_prot']:.0f}P/{metas['pct_gord']:.0f}G | "
          f"Orçamento: R$ {metas['orcamento']:.2f}")
    print("═" * 80 + "\n")
    
    # Exibe cada refeição
    for nome_refeicao, pct_calorias in config_refeicoes:
        if nome_refeicao in cardapio.refeicoes:
            alimentos_refeicao = cardapio.refeicoes[nome_refeicao]
            
            # Calcula totais da refeição
            calorias_ref = sum(a['calorias'] for a in alimentos_refeicao)
            proteinas_ref = sum(a['proteinas'] for a in alimentos_refeicao)
            carbos_ref = sum(a['carboidratos'] for a in alimentos_refeicao)
            gorduras_ref = sum(a['gorduras'] for a in alimentos_refeicao)
            fibras_ref = sum(a['fibras'] for a in alimentos_refeicao)
            custo_ref = sum(a['custo'] for a in alimentos_refeicao)
            
            # Emoji baseado no tipo de refeição
            emoji = _get_emoji_refeicao(nome_refeicao)
            
            # Box da refeição
            print("┌" + "─" * 78 + "┐")
            print(f"│ {emoji}  {nome_refeicao.upper():<50} {calorias_ref:>6.0f} kcal │")
            print(f"│ ({pct_calorias:.0f}% das calorias diárias)" + " " * (78 - len(f"({pct_calorias:.0f}% das calorias diárias)") - 1) + "│")
            print("├" + "─" * 78 + "┤")
            
            # Lista de alimentos
            for alimento in alimentos_refeicao:
                nome = alimento['nome']
                gramas = alimento['gramas']
                kcal = alimento['calorias']
                
                # Formata a linha
                if gramas >= 1000:  # Se for >= 1L ou 1kg
                    medida = f"{gramas/1000:.1f}L" if 'Leite' in nome or 'Água' in nome else f"{gramas/1000:.1f}kg"
                elif gramas == 1:  # Unidade
                    medida = "1 unid"
                else:
                    medida = f"{gramas:.0f}g"
                
                linha = f"│  • {medida:>8} de {nome:<42} {kcal:>6.0f} kcal │"
                print(linha)
            
            print("│" + " " * 78 + "│")
            
            # Macros da refeição
            print(f"│  📊 Macros: {proteinas_ref:>4.0f}g Prot | "
                  f"{carbos_ref:>4.0f}g Carbo | "
                  f"{gorduras_ref:>4.0f}g Gord | "
                  f"{fibras_ref:>4.0f}g Fib" + " " * (78 - len(f"  📊 Macros: {proteinas_ref:>4.0f}g Prot | {carbos_ref:>4.0f}g Carbo | {gorduras_ref:>4.0f}g Gord | {fibras_ref:>4.0f}g Fib") - 1) + "│")
            print(f"│  💰 Custo: R$ {custo_ref:>5.2f}" + " " * (78 - len(f"  💰 Custo: R$ {custo_ref:>5.2f}") - 1) + "│")
            print("└" + "─" * 78 + "┘")
            print()
    
    # Resumo do dia
    totais = cardapio.calcular_totais()
    
    print("═" * 80)
    print("📊 RESUMO NUTRICIONAL DO DIA")
    print("═" * 80)
    
    # Calorias
    pct_cal = (totais['calorias'] / metas['meta_calorias']) * 100
    status_cal = "✅" if 95 <= pct_cal <= 105 else "⚠️"
    print(f"Calorias: {totais['calorias']:.0f} kcal (Meta: {metas['meta_calorias']:.0f}) {status_cal} {pct_cal:.1f}%")
    
    # Proteínas
    pct_prot = (totais['proteinas'] / metas['gramas_prot']) * 100
    status_prot = "✅" if 90 <= pct_prot <= 110 else "⚠️"
    print(f"Proteínas: {totais['proteinas']:.0f}g (Meta: {metas['gramas_prot']:.0f}g) {status_prot} {pct_prot:.1f}%")
    
    # Carboidratos
    pct_carbo = (totais['carboidratos'] / metas['gramas_carbo']) * 100
    status_carbo = "✅" if 90 <= pct_carbo <= 110 else "⚠️"
    print(f"Carboidratos: {totais['carboidratos']:.0f}g (Meta: {metas['gramas_carbo']:.0f}g) {status_carbo} {pct_carbo:.1f}%")
    
    # Gorduras
    pct_gord = (totais['gorduras'] / metas['gramas_gord']) * 100
    status_gord = "✅" if 90 <= pct_gord <= 110 else "⚠️"
    print(f"Gorduras: {totais['gorduras']:.0f}g (Meta: {metas['gramas_gord']:.0f}g) {status_gord} {pct_gord:.1f}%")
    
    print()
    
    # Custo
    status_custo = "✅" if totais['custo'] <= metas['orcamento'] else "❌"
    print(f"Custo Total: R$ {totais['custo']:.2f} (Orçamento: R$ {metas['orcamento']:.2f}) {status_custo}")
    
    # Qualidade
    print(f"Saúde Média: {totais['saude_media']:.1f}/10 {'✅' if totais['saude_media'] >= 7 else '⚠️'}")
    print(f"Preferência: {totais['preferencia_media']:.1f}/10 {'✅' if totais['preferencia_media'] >= 7 else '⚠️'}")
    
    print("═" * 80 + "\n")


def _get_emoji_refeicao(nome: str) -> str:
    """Retorna emoji apropriado para cada refeição (normalizado, sem acentos)."""
    nome_norm = normalizar_texto(nome)
    
    if 'cafe' in nome_norm or ('manha' in nome_norm and 'lanche' not in nome_norm):
        return "☀️"
    elif 'lanche' in nome_norm and 'manha' in nome_norm:
        return "🍎"
    elif 'almoco' in nome_norm or 'almo' in nome_norm:
        return "🍽️"
    elif 'lanche' in nome_norm and 'tarde' in nome_norm:
        return "🥤"
    elif 'jantar' in nome_norm:
        return "🌙"
    elif 'ceia' in nome_norm:
        return "🌃"
    else:
        return "🍴"
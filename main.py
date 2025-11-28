"""
Sistema de Recomendação de Cardápio Saudável V2
Com Refeições Compostas e Controle de Macros

Autores: Cristian, Marco, Pedro e William
Professor: Marcos Sulzbach Morgenstern
"""

from datetime import datetime

from data.dados_alimentos import criar_base_dados
from algoritmos.fuzzy_saudavel import aplicar_logica_fuzzy
from algoritmos.rna_preferencias import SistemaPreferenciasRNA
from algoritmos.busca_a_star import BuscaAEstrela
from algoritmos.algoritmo_genetico import otimizar_cardapio_v2
from utils.formatacao import exibir_cardapio_nutricionista
from utils.validacao_input import validar_porcentagens, validar_numero


def exibir_cabecalho():
    """Exibe o cabeçalho bonito do sistema."""
    print("\n" + "=" * 80)
    print(" " * 15 + "🍽️  SISTEMA DE RECOMENDAÇÃO DE CARDÁPIO SAUDÁVEL")
    print("=" * 80)
    print("Trabalho Prático Final - Inteligência Artificial")
    print("Grupo: Cristian, Marco, Pedro e William")
    print("Professor: Marcos Sulzbach Morgenstern")
    print("=" * 80 + "\n")


def coletar_configuracao_refeicoes():
    """
    Coleta quantas refeições o usuário quer e seus nomes/distribuição.
    """
    print("=" * 80)
    print("🍴 CONFIGURAÇÃO DAS REFEIÇÕES")
    print("=" * 80 + "\n")
    
    # Número de refeições
    while True:
        num_refeicoes = validar_numero(
            "Quantas refeições você faz por dia? (3-8): ",
            3, 8, int
        )
        if num_refeicoes:
            break
    
    print(f"\n✅ Você fará {num_refeicoes} refeições por dia.\n")
    
    # Coleta nomes e porcentagens
    refeicoes = []
    porcentagens = []
    
    print("Agora vamos definir cada refeição:")
    print("(Ex: Café da Manhã, Lanche da Manhã, Almoço, Lanche da Tarde, Jantar, Ceia)\n")
    
    num_refeicoes = int(num_refeicoes)
    for i in range(num_refeicoes):
        nome = input(f"Nome da refeição {i+1}: ").strip()
        if not nome:
            nome = f"Refeição {i+1}"
        refeicoes.append(nome)
    
    print("\n" + "-" * 80)
    print("📊 DISTRIBUIÇÃO DE CALORIAS POR REFEIÇÃO")
    print("-" * 80)
    print("Defina qual porcentagem das calorias diárias cada refeição terá.")
    print("(A soma DEVE ser exatamente 100%)\n")
    
    while True:
        porcentagens = []
        for nome in refeicoes:
            pct = validar_numero(
                f"  {nome}: ",
                1, 100, float
            )
            porcentagens.append(pct)
        
        total = sum(porcentagens)
        if abs(total - 100) < 0.01:  # Tolerância para erros de float
            print(f"\n✅ Total: {total:.1f}% - Perfeito!\n")
            break
        else:
            print(f"\n⚠️  Total: {total:.1f}% - Deve ser 100%! Tente novamente.\n")
    
    return list(zip(refeicoes, porcentagens))


def coletar_metas_nutricionais():
    """
    Coleta meta de calorias, macros e orçamento.
    """
    print("=" * 80)
    print("🎯 METAS NUTRICIONAIS")
    print("=" * 80 + "\n")
    
    # Meta de calorias
    print("📊 META DE CALORIAS DIÁRIAS")
    print("   (1500-1800: perda de peso | 2000-2200: manutenção | 2500+: ganho de massa)\n")
    
    meta_calorias = validar_numero(
        "Digite sua meta de calorias diárias: ",
        1000, 5000, float
    )
    
    # Macros
    print("\n" + "-" * 80)
    print("🥗 DISTRIBUIÇÃO DE MACRONUTRIENTES")
    print("-" * 80)
    print("Defina a porcentagem de cada macronutriente nas calorias diárias.")
    print("(A soma DEVE ser 100%)\n")
    print("Exemplos comuns:")
    print("  • Balanceado: 50% Carbo / 30% Prot / 20% Gord")
    print("  • Low-carb: 30% Carbo / 40% Prot / 30% Gord")
    print("  • High-carb: 60% Carbo / 20% Prot / 20% Gord\n")
    
    while True:
        pct_carbo = validar_numero("  % Carboidratos: ", 10, 80, float)
        pct_prot = validar_numero("  % Proteínas: ", 10, 60, float)
        pct_gord = validar_numero("  % Gorduras: ", 10, 60, float)
        
        total = pct_carbo + pct_prot + pct_gord
        if abs(total - 100) < 0.01:
            print(f"\n✅ Total: {total:.1f}% - Perfeito!\n")
            break
        else:
            print(f"\n⚠️  Total: {total:.1f}% - Deve ser 100%! Tente novamente.\n")
    
    # Calcula gramas de cada macro
    # 1g Carbo = 4 kcal, 1g Prot = 4 kcal, 1g Gord = 9 kcal
    gramas_carbo = (meta_calorias * (pct_carbo / 100)) / 4
    gramas_prot = (meta_calorias * (pct_prot / 100)) / 4
    gramas_gord = (meta_calorias * (pct_gord / 100)) / 9
    
    print("📋 Resumo dos Macros:")
    print(f"   • Carboidratos: {gramas_carbo:.0f}g ({pct_carbo:.0f}%)")
    print(f"   • Proteínas: {gramas_prot:.0f}g ({pct_prot:.0f}%)")
    print(f"   • Gorduras: {gramas_gord:.0f}g ({pct_gord:.0f}%)\n")
    
    # Orçamento
    print("-" * 80)
    print("💰 ORÇAMENTO MÁXIMO DIÁRIO")
    print("   (Média brasileira: R$ 30-60 por dia)\n")
    
    orcamento = validar_numero(
        "Digite seu orçamento máximo diário: R$ ",
        10, 200, float
    )
    
    print("\n✅ Metas definidas com sucesso!\n")
    
    return {
        'meta_calorias': meta_calorias,
        'pct_carbo': pct_carbo,
        'pct_prot': pct_prot,
        'pct_gord': pct_gord,
        'gramas_carbo': gramas_carbo,
        'gramas_prot': gramas_prot,
        'gramas_gord': gramas_gord,
        'orcamento': orcamento
    }


def coletar_preferencias_vegetais():
    """
    Coleta preferências sobre vegetais/frutas.
    """
    print("=" * 80)
    print("🥬 PREFERÊNCIAS DE VEGETAIS E FRUTAS")
    print("=" * 80 + "\n")
    
    print("Vegetais e frutas são importantes para uma alimentação saudável!")
    print("Como você prefere incluí-los?\n")
    print("1 - Sempre incluir (obrigatório em todas as refeições)")
    print("2 - Incluir quando possível (preferencial, mas não obrigatório)")
    print("3 - Incluir minimamente (apenas se não atrapalhar os macros)")
    print("4 - Não incluir\n")
    
    opcao = validar_numero("Sua escolha (1-4): ", 1, 4, int)
    
    max_vegetais_por_refeicao = 0
    obrigatorio = False
    
    if opcao == 1:
        obrigatorio = True
        max_vegetais_por_refeicao = 2
        print("\n✅ Vegetais/frutas serão incluídos em todas as refeições!\n")
    elif opcao == 2:
        max_vegetais_por_refeicao = 2
        print("\n✅ Vegetais/frutas serão incluídos quando possível!\n")
    elif opcao == 3:
        max_vegetais_por_refeicao = 1
        print("\n✅ Vegetais/frutas serão incluídos minimamente.\n")
    else:
        max_vegetais_por_refeicao = 0
        print("\n✅ Vegetais/frutas não serão incluídos.\n")
    
    return {
        'max_vegetais': max_vegetais_por_refeicao,
        'obrigatorio': obrigatorio
    }


def main():
    """
    Função principal - Pipeline completo V2
    """
    
    exibir_cabecalho()
    
    print("🚀 Iniciando Sistema de Recomendação de Cardápio V2...\n")
    
    # ========================================================================
    # ETAPA 1: CARREGAMENTO DOS DADOS
    # ========================================================================
    print("=" * 80)
    print("📊 ETAPA 1/6: CARREGANDO BASE DE DADOS")
    print("=" * 80 + "\n")
    
    df_alimentos = criar_base_dados()
    print(f"✅ {len(df_alimentos)} alimentos carregados\n")
    
    # ========================================================================
    # ETAPA 2: LÓGICA FUZZY
    # ========================================================================
    print("=" * 80)
    print("🧠 ETAPA 2/6: APLICANDO LÓGICA FUZZY")
    print("=" * 80 + "\n")
    
    df_alimentos = aplicar_logica_fuzzy(df_alimentos)
    print("✅ Lógica Fuzzy aplicada!\n")
    
    # ========================================================================
    # ETAPA 3: CONFIGURAÇÃO DO USUÁRIO
    # ========================================================================
    print("=" * 80)
    print("⚙️  ETAPA 3/6: CONFIGURAÇÃO PERSONALIZADA")
    print("=" * 80 + "\n")
    
    # 3.1 - Refeições
    config_refeicoes = coletar_configuracao_refeicoes()
    
    # 3.2 - Metas nutricionais
    metas = coletar_metas_nutricionais()
    
    # 3.3 - Preferências vegetais
    pref_vegetais = coletar_preferencias_vegetais()
    
    # ========================================================================
    # ETAPA 4: RNA - PREFERÊNCIAS
    # ========================================================================
    print("=" * 80)
    print("🤖 ETAPA 4/6: REDE NEURAL ARTIFICIAL")
    print("=" * 80 + "\n")
    
    sistema_rna = SistemaPreferenciasRNA()
    preferencias_usuario = sistema_rna.coletar_preferencias_usuario()
    sistema_rna.treinar(df_alimentos, preferencias_usuario)
    df_alimentos = sistema_rna.adicionar_notas_preferencia_df(
        df_alimentos, preferencias_usuario
    )
    
    print("✅ RNA treinada!\n")
    
    # ========================================================================
    # ETAPA 5: A* - PRÉ-SELEÇÃO
    # ========================================================================
    print("=" * 80)
    print("🔍 ETAPA 5/6: ALGORITMO A*")
    print("=" * 80 + "\n")
    
    busca_astar = BuscaAEstrela(
        df_alimentos,
        meta_calorias=metas['meta_calorias'],
        orcamento_maximo=metas['orcamento']
    )
    
    melhores_alimentos = busca_astar.preselecionar_alimentos_todas_refeicoes(
        top_n_por_tipo=20
    )
    
    print("✅ A* concluído!\n")
    
    # ========================================================================
    # ETAPA 6: ALGORITMO GENÉTICO V2
    # ========================================================================
    print("=" * 80)
    print("🧬 ETAPA 6/6: ALGORITMO GENÉTICO")
    print("=" * 80 + "\n")
    
    print("Configurações do AG:")
    print("  • População: 150 indivíduos")
    print("  • Gerações: 100")
    print("  • Otimização: Macros + Calorias + Saúde + Custo\n")
    
    input("Pressione ENTER para iniciar a otimização...")
    print()
    
    melhor_cardapio = otimizar_cardapio_v2(
        df_alimentos=df_alimentos,
        alimentos_preselecionados=melhores_alimentos,
        config_refeicoes=config_refeicoes,
        metas=metas,
        pref_vegetais=pref_vegetais,
        tamanho_populacao=150,
        num_geracoes=100
    )
    
    # ========================================================================
    # FINALIZAÇÃO: EXIBIÇÃO E EXPORTAÇÃO
    # ========================================================================
    print("\n" + "=" * 80)
    print("💾 EXPORTANDO RESULTADOS")
    print("=" * 80 + "\n")
    
    # Exibe cardápio formatado
    exibir_cardapio_nutricionista(melhor_cardapio, metas, config_refeicoes)
    
    # Salva em arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"cardapio_personalizado_{timestamp}.txt"
    
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        # Redireciona print para arquivo
        import sys
        old_stdout = sys.stdout
        sys.stdout = f
        exibir_cardapio_nutricionista(melhor_cardapio, metas, config_refeicoes)
        sys.stdout = old_stdout
    
    print(f"✅ Cardápio salvo em: {nome_arquivo}")
    
    # Salva CSV detalhado
    df_cardapio = melhor_cardapio.exportar_para_dataframe()
    csv_filename = f"cardapio_detalhado_{timestamp}.csv"
    df_cardapio.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    print(f"✅ Detalhes salvos em: {csv_filename}")
    
    print("\n" + "=" * 80)
    print("🎉 SISTEMA CONCLUÍDO COM SUCESSO!")
    print("=" * 80)
    print("\nSeu cardápio personalizado está pronto! 🍽️")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Execução interrompida pelo usuário.")
    except Exception as e:
        print(f"\n\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
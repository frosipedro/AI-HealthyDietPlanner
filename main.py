"""
Sistema de Recomendação de Cardápio Saudável
Com Refeições Compostas e Controle de Macros
VERSÃO OTIMIZADA - Parâmetros ajustados e melhor integração entre técnicas

Autores: Cristian, Marco, Pedro e William
Professor: Marcos Sulzbach Morgenstern
"""

from datetime import datetime
from data.dados_alimentos import criar_base_dados
from algoritmos.fuzzy_saudavel import aplicar_logica_fuzzy
from algoritmos.rna_preferencias import SistemaPreferenciasRNA
from algoritmos.busca_a_star import BuscaAEstrela
from algoritmos.algoritmo_genetico import otimizar_cardapio
from utils.formatacao import exibir_cardapio_nutricionista
from utils.validacao_input import validar_numero
from utils.tmb_calculator import calcular_tmb


def exibir_cabecalho():
    """Exibe o cabeçalho do sistema."""
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
    print("-" * 80)
    print("🍴 CONFIGURAÇÃO DAS REFEIÇÕES")
    print("-" * 80)

    while True:
        num_refeicoes = validar_numero(
            "Quantas refeições você faz por dia? (3-8): ",
            3, 8, int
        )
        if num_refeicoes:
            break
    
    print(f"\n✅ Você fará {num_refeicoes} refeições por dia.\n")
    
    refeicoes = []
    porcentagens = []
    
    print("Agora vamos definir cada refeição:")
    print("Tipos: Café da Manhã, Lanche da Manhã, Almoço, Lanche da Tarde, Jantar, Ceia\n")
    
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
        if abs(total - 100) < 0.01:
            print(f"\n✅ Total: {total:.1f}% - Perfeito!\n")
            break
        else:
            print(f"\n⚠️  Total: {total:.1f}% - Deve ser 100%! Tente novamente.\n")
    
    return list(zip(refeicoes, porcentagens))


def coletar_metas_nutricionais():
    """
    Coleta meta de calorias, macros e orçamento.
    """
    print("-" * 80)
    print("🎯 CÁLCULO DA TAXA METABÓLICA BASAL (TMB)")
    print("-" * 80)
    print("Vamos coletar informações como peso, idade, para calcularmos suas necessidades nutricionais.\n")

    calculo_basal = []

    calculo_basal.append(validar_numero(
        "Qual é o seu peso atual? (kg): ",
        0, 500, float
        )
    )
    calculo_basal.append(validar_numero(
        "Qual é a sua altura? (cm): ",
        0, 250, float
        )
    )
    calculo_basal.append(validar_numero(
        "Qual é a sua idade? (anos): ",
        0, 120, int
        )
    )
    calculo_basal.append(validar_numero(
        "Qual é o seu sexo? (1 para masculino, 2 para feminino): ",
        1, 2, int
        )
    )
    calculo_basal.append(validar_numero(
        "Dentro das seguintes opções:\n\n" \
        "1- Sedentário (pouco ou nenhum exercício);\n" \
        "2- Levemente ativo (exercício leve 1-3 dias/semana);\n" \
        "3- Moderadamente ativo (exercício moderado 3-5 dias/semana);\n" \
        "4- Muito ativo (exercício pesado 6-7 dias/semana);\n"\
        "5- Extremamente ativo (trabalho físico pesado ou treino 2x dia);\n\n" \
        "Qual é o seu nível de atividade física? (1-5): ",
        1, 5, int
        )
    )

    calculo_basal = calcular_tmb(calculo_basal)

    # Meta de calorias
    print("\n" + "-" * 80)
    print("📊 META DE CALORIAS DIÁRIAS")
    print("-" * 80)
    print("Com base no seu TMB e nível de atividade, temos as seguintes recomendações:")
    print(f"{calculo_basal[1]-500:.0f}-{calculo_basal[1]-200:.0f}: perda de peso | {calculo_basal[1]:.0f}: manutenção | {calculo_basal[1]+200:.0f}+: ganho de massa\n")
    
    meta_calorias = validar_numero(
        "Digite sua meta de calorias diárias: ",
        1000, 8000, float
    )
    
    # Macros
    print("\n" + "-" * 80)
    print("🥗 DISTRIBUIÇÃO DE MACRONUTRIENTES")
    print("-" * 80)
    print("Vamos definir a porcentagem de cada macronutriente nas calorias diárias.")
    print("Temos algumas opções de estilos de dieta:\n")

    print("--- Estilos de Vida Comuns ---")
    print("  1. Equilibrada (Padrão OMS):      50% Carbo / 25% Prot / 25% Gord")
    print("  2. High-carb (Ganho/Energia):     60% Carbo / 20% Prot / 20% Gord")
    print("  3. Low-carb (Secar leve):         30% Carbo / 40% Prot / 30% Gord")

    print("\n--- Focados em Estética/Treino ---")
    print("  4. Cetogênica (Keto/Gordura):      10% Carbo / 30% Prot / 60% Gord")
    print("  5. High-Protein (Definição máx):  25% Carbo / 45% Prot / 30% Gord")
    print("  6. Zona (Controle Hormonal):      40% Carbo / 30% Prot / 30% Gord\n")
    
    opcoes_dieta = {
    1: {"nome": "Equilibrada",   "c": 50, "p": 25, "g": 25},
    2: {"nome": "High-carb",     "c": 60, "p": 20, "g": 20},
    3: {"nome": "Low-carb",      "c": 30, "p": 40, "g": 30},
    4: {"nome": "Cetogênica",    "c": 10,  "p": 30, "g": 60},
    5: {"nome": "High-Protein",  "c": 25, "p": 45, "g": 30},
    6: {"nome": "Zona",          "c": 40, "p": 30, "g": 30},
    }

    escolha_dieta = int(input("Escolha o número do seu estilo de dieta (1-6): "))
    macros = opcoes_dieta[escolha_dieta]

    print(f"\nVocê escolheu: {macros['nome']}")
    print(f"Carbos: {macros['c']}%, Proteínas: {macros['p']}%, Gorduras: {macros['g']}%")
    
    # Calcula gramas de cada macro
    gramas_carbo = (meta_calorias * (macros['c'] / 100)) / 4
    gramas_prot = (meta_calorias * (macros['p'] / 100)) / 4
    gramas_gord = (meta_calorias * (macros['g'] / 100)) / 9
    
    print("\n📋 Resumo dos Macros:")
    print(f"   • Carboidratos: {gramas_carbo:.0f}g ({macros['c']:.0f}%)")
    print(f"   • Proteínas: {gramas_prot:.0f}g ({macros['p']:.0f}%)")
    print(f"   • Gorduras: {gramas_gord:.0f}g ({macros['g']:.0f}%)\n")
    
    # Orçamento
    print("-" * 80)
    print("💰 ORÇAMENTO MÁXIMO DIÁRIO")
    print("-" * 80)
    print("Defina seu orçamento máximo diário para alimentação.")
    print("(Média brasileira: R$ 30-60 por dia)\n")
    
    orcamento = validar_numero(
        "Digite seu orçamento máximo diário: R$ ",
        10, 200, float
    )
    
    print("\n✅ Metas definidas com sucesso!\n")
    
    return {
        'meta_calorias': meta_calorias,
        'pct_carbo': macros['c'],
        'pct_prot': macros['p'],
        'pct_gord': macros['g'],
        'gramas_carbo': gramas_carbo,
        'gramas_prot': gramas_prot,
        'gramas_gord': gramas_gord,
        'orcamento': orcamento
    }


def coletar_preferencias_vegetais():
    """
    Coleta preferências sobre vegetais/frutas.
    """
    print("-" * 80)
    print("🥬 PREFERÊNCIAS DE VEGETAIS E FRUTAS")
    print("-" * 80 + "\n")
    
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
    Função principal - Pipeline completo
    VERSÃO OTIMIZADA - Parâmetros ajustados
    """
    
    exibir_cabecalho()
    
    print("🚀 Iniciando Sistema de Recomendação de Cardápio...\n")
    
    # ========================================================================
    # ETAPA 1: CARREGAMENTO DOS DADOS
    # ========================================================================
    print("=" * 80)
    print("📊 ETAPA 1/6: CARREGANDO BASE DE DADOS")
    print("=" * 80 + "\n")
    
    df_alimentos = criar_base_dados()
    print(f"✅ {len(df_alimentos)} alimentos carregados\n")
    
    # ========================================================================
    # ETAPA 2: LÓGICA FUZZY (Avaliação de Saudabilidade)
    # ========================================================================
    print("=" * 80)
    print("🧠 ETAPA 2/6: APLICANDO LÓGICA FUZZY")
    print("=" * 80 + "\n")
    print("A Lógica Fuzzy avalia a saudabilidade de cada alimento baseada em:")
    print("  • Proteínas, carboidratos, fibras")
    print("  • Sódio e gorduras (saturadas vs insaturadas)")
    print("  • Tipo de alimento (natural vs industrializado)\n")
    
    df_alimentos = aplicar_logica_fuzzy(df_alimentos)
    
    # Mostra alguns exemplos
    print("Exemplos de avaliação Fuzzy:")
    top_5 = df_alimentos.nlargest(5, 'nota_saudavel_fuzzy')[['nome', 'nota_saudavel_fuzzy']]
    print(top_5.to_string(index=False))
    print("\n✅ Lógica Fuzzy aplicada! Todos os alimentos avaliados.\n")
    
    # ========================================================================
    # ETAPA 3: CONFIGURAÇÃO DO USUÁRIO
    # ========================================================================
    print("=" * 80)
    print("⚙️  ETAPA 3/6: CONFIGURAÇÃO PERSONALIZADA")
    print("=" * 80 + "\n")
    
    config_refeicoes = coletar_configuracao_refeicoes()
    metas = coletar_metas_nutricionais()
    pref_vegetais = coletar_preferencias_vegetais()
    
    # ========================================================================
    # ETAPA 4: RNA - PREFERÊNCIAS (Aprendizado de Preferências)
    # ========================================================================
    print("=" * 80)
    print("🤖 ETAPA 4/6: REDE NEURAL ARTIFICIAL")
    print("=" * 80 + "\n")
    print("A RNA aprende suas preferências alimentares e prevê sua satisfação")
    print("com cada alimento, considerando fatores como:")
    print("  • Preferências por tipos de proteína (frango, carne, peixe)")
    print("  • Preferências por carboidratos (arroz, massa, pães)")
    print("  • Tolerância a industrializados e sódio")
    print("  • Preferências de custo\n")
    
    sistema_rna = SistemaPreferenciasRNA()
    preferencias_usuario = sistema_rna.coletar_preferencias_usuario()
    sistema_rna.treinar(df_alimentos, preferencias_usuario)
    df_alimentos = sistema_rna.adicionar_notas_preferencia_df(
        df_alimentos, preferencias_usuario
    )
    
    # Mostra alguns exemplos
    print("Alimentos mais alinhados com suas preferências:")
    top_5_pref = df_alimentos.nlargest(5, 'nota_preferencia_rna')[['nome', 'nota_preferencia_rna']]
    print(top_5_pref.to_string(index=False))
    print("\n✅ RNA treinada! Preferências personalizadas aplicadas.\n")
    
    # ========================================================================
    # ETAPA 5: A* - PRÉ-SELEÇÃO (Busca Inteligente)
    # ========================================================================
    print("=" * 80)
    print("🔍 ETAPA 5/6: ALGORITMO A*")
    print("=" * 80 + "\n")
    print("O algoritmo A* realiza uma busca inteligente para pré-selecionar")
    print("os melhores alimentos de cada tipo, considerando:")
    print("  • Notas de saudabilidade (Fuzzy)")
    print("  • Notas de preferência (RNA)")
    print("  • Custo-benefício")
    print("  • Adequação culinária para cada tipo de refeição\n")
    
    busca_astar = BuscaAEstrela(
        df_alimentos,
        meta_calorias=metas['meta_calorias'],
        orcamento_maximo=metas['orcamento']
    )
    
    # PARÂMETRO OTIMIZADO: top_n aumentado para 20
    melhores_alimentos = busca_astar.preselecionar_alimentos_todas_refeicoes(
        top_n_por_tipo=20
    )
    
    print("✅ A* concluído! Alimentos pré-selecionados com base em qualidade e adequação.\n")
    
    # ========================================================================
    # ETAPA 6: ALGORITMO GENÉTICO (Otimização Final)
    # ========================================================================
    print("=" * 80)
    print("🧬 ETAPA 6/6: ALGORITMO GENÉTICO")
    print("=" * 80 + "\n")
    print("O Algoritmo Genético otimiza o cardápio completo, considerando:")
    print("  • Metas calóricas e de macronutrientes")
    print("  • Distribuição proporcional entre refeições")
    print("  • Regras culinárias do mundo real")
    print("  • Saúde, preferência e custo")
    print("\nConfigurações do AG:")
    print("  • População: 200 indivíduos")  # OTIMIZADO
    print("  • Gerações: 150")  # OTIMIZADO
    print("  • Validação culinária: 22% do fitness")  # OTIMIZADO
    print("  • Peso para combinações obrigatórias (ex: Aveia + Leite)\n")
    
    input("Pressione ENTER para iniciar a otimização...")
    print()
    
    # PARÂMETROS OTIMIZADOS
    melhor_cardapio = otimizar_cardapio(
        df_alimentos=df_alimentos,
        alimentos_preselecionados=melhores_alimentos,
        config_refeicoes=config_refeicoes,
        metas=metas,
        pref_vegetais=pref_vegetais,
        tamanho_populacao=200,  # Aumentado de 150
        num_geracoes=150  # Aumentado de 100
    )
    
    # ========================================================================
    # FINALIZAÇÃO: EXIBIÇÃO E EXPORTAÇÃO
    # ========================================================================
    print("\n" + "=" * 80)
    print("💾 EXPORTANDO RESULTADOS")
    print("=" * 80 + "\n")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"cardapio_personalizado_{timestamp}.txt"
    
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        import sys
        old_stdout = sys.stdout
        sys.stdout = f
        exibir_cardapio_nutricionista(melhor_cardapio, metas, config_refeicoes)
        sys.stdout = old_stdout
    
    print(f"✅ Cardápio salvo em: {nome_arquivo}")
    
    print("\n" + "=" * 80)
    print("🎉 SISTEMA CONCLUÍDO COM SUCESSO!")
    print("=" * 80)
    print("\nSeu cardápio personalizado está pronto! 🍽️")
    print("\nResumo das técnicas de IA utilizadas:")
    print("  1. Lógica Fuzzy: Avaliou saudabilidade de todos os alimentos")
    print("  2. RNA: Aprendeu suas preferências pessoais")
    print("  3. A*: Pré-selecionou os melhores alimentos por tipo")
    print("  4. Algoritmo Genético: Otimizou o cardápio final")
    print("\nCada técnica contribuiu para um resultado mais preciso e personalizado!")
    print("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Execução interrompida pelo usuário.")
    except Exception as e:
        print(f"\n\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
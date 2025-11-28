import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def aplicar_logica_fuzzy(df_alimentos):
    # --- Configuração das Variáveis Fuzzy (Antecedentes e Consequente) ---

    # --- ANTECEDENTES (Entradas) ---
    proteina    = ctrl.Antecedent(np.arange(0, 41, 1), 'proteina')
    carboidrato = ctrl.Antecedent(np.arange(0, 101, 1), 'carboidrato')
    fibra       = ctrl.Antecedent(np.arange(0, 16, 1), 'fibra')
    sodio       = ctrl.Antecedent(np.arange(0, 2501, 1), 'sodio')
    gord_sat    = ctrl.Antecedent(np.arange(0, 61, 1), 'gord_sat')
    gord_insat  = ctrl.Antecedent(np.arange(0, 101, 1), 'gord_insat')

    # --- CONSEQUENTE (Saída) ---
    saudavel = ctrl.Consequent(np.arange(0, 11, 1), 'saudavel')

    # --- DEFINIÇÃO DAS FUNÇÕES DE PERTINÊNCIA (Mapeamento) ---
    proteina['baixa'] = fuzz.trimf(proteina.universe, [0, 0, 10])
    proteina['media'] = fuzz.trimf(proteina.universe, [5, 15, 25])
    proteina['alta']  = fuzz.trapmf(proteina.universe, [20, 30, 40, 40])

    sodio['baixo'] = fuzz.trimf(sodio.universe, [0, 0, 150])
    sodio['medio'] = fuzz.trimf(sodio.universe, [100, 300, 550]) 
    sodio['alto']  = fuzz.trapmf(sodio.universe, [400, 700, 2500, 2500]) 

    gord_sat['baixa'] = fuzz.trimf(gord_sat.universe, [0, 0, 3])
    gord_sat['media'] = fuzz.trimf(gord_sat.universe, [2, 6, 10])
    gord_sat['alta']  = fuzz.trapmf(gord_sat.universe, [8, 15, 60, 60])

    carboidrato['baixo'] = fuzz.trimf(carboidrato.universe, [0, 0, 20])
    carboidrato['medio'] = fuzz.trimf(carboidrato.universe, [10, 40, 70])
    carboidrato['alto']  = fuzz.trapmf(carboidrato.universe, [50, 80, 100, 100])

    fibra['baixa'] = fuzz.trimf(fibra.universe, [0, 0, 3])
    fibra['alta']  = fuzz.trapmf(fibra.universe, [2, 5, 15, 15])

    gord_insat['baixa'] = fuzz.trimf(gord_insat.universe, [0, 0, 5])
    gord_insat['alta']  = fuzz.trapmf(gord_insat.universe, [5, 10, 100, 100]) 

    # Saída
    saudavel['ruim']  = fuzz.trimf(saudavel.universe, [0, 0, 4])
    saudavel['medio'] = fuzz.trimf(saudavel.universe, [3, 5, 7])
    saudavel['bom']   = fuzz.trimf(saudavel.universe, [6, 10, 10])

    # --- REGRAS (O Cérebro do Sistema) ---

    # R1: O Ideal (Muita Proteína, pouco sódio, pouca gordura saturada) 
    r1 = ctrl.Rule(proteina['alta'] & sodio['baixo'] & gord_sat['baixa'], saudavel['bom'])

    # R2: O Vilão (Sódio alto e Saturada alta) 
    r2 = ctrl.Rule(sodio['alto'] & gord_sat['alta'], saudavel['ruim'])

    # R3: Penalidade Industrial (Carbo alto + Sódio alto) 
    r3 = ctrl.Rule(carboidrato['alto'] & sodio['alto'], saudavel['ruim'])

    # R4: Carbo Complexo (Carbo alto + Fibra alta)
    r4 = ctrl.Rule(carboidrato['alto'] & fibra['alta'] & sodio['baixo'], saudavel['bom'])

    # R5: Carbo Vazio (Anti-Farinha/Açúcar)
    r5 = ctrl.Rule(carboidrato['alto'] & fibra['baixa'] & proteina['baixa'], saudavel['medio'])

    # R6: Gordura Boa (Azeite, Salmão, Nozes, Abacate)
    r6 = ctrl.Rule(gord_insat['alta'] & ~gord_sat['alta'], saudavel['bom'])

    # R7: Equilíbrio
    r7 = ctrl.Rule(proteina['media'] & gord_sat['media'], saudavel['medio'])

    # R8: O Salvador do Feijão (Proteína Média + Fibra Alta)
    r8 = ctrl.Rule(proteina['media'] & fibra['alta'], saudavel['bom'])

    # R9: O Salvador do Ovo (Proteína Média + Baixo Carbo + Baixo Sódio)
    r9 = ctrl.Rule(proteina['media'] & carboidrato['baixo'] & sodio['baixo'], saudavel['bom'])

    # Sistema atualizado com as 9 regras
    sistema_saudavel = ctrl.ControlSystem([r1, r2, r3, r4, r5, r6, r7, r8, r9])
    simulador = ctrl.ControlSystemSimulation(sistema_saudavel)


    # --- FUNÇÃO PRINCIPAL ---
    def calcular_fuzzy(row):
        # --- 1. INPUTS ---
        simulador.input['proteina']    = row['proteinas']
        simulador.input['carboidrato'] = row['carboidratos']
        simulador.input['fibra']       = row['fibras']
        simulador.input['sodio']       = row['sodio']

        # Lógica de Gordura Saturada em Refeições
        if row['tipo'] == 'refeicao' and row['sodio'] < 400:
            simulador.input['gord_sat'] = row['gordura_saturada'] * 0.6
        else:
            simulador.input['gord_sat'] = row['gordura_saturada']

        simulador.input['gord_insat']  = row['gorduras_insaturadas']

        # --- 2. CÁLCULO BASE ---
        try:
            simulador.compute()
            score = simulador.output['saudavel']
        except (ValueError, KeyError):
            score = 5.0

        # --- 3. PÓS-PROCESSAMENTO ---

        # A) Penalidade Industrializados
        if row['tipo'] == 'industrializado':
            score -= 2.5

        # B) Lógica de Refeições
        elif row['tipo'] == 'refeicao':
            bonus = 1.5
            # Frango à Milanesa perde o bônus aqui (sodio >= 500 ou gordura >= 10)
            if row['sodio'] >= 500 or row['gorduras'] >= 10:
                bonus = 0.0
                score -= 1.0 # Penalidade leve por ser fritura

            score += bonus
            if row['proteinas'] > 15 and bonus > 0: score += 0.5

        # C) Bônus Vegetais/Frutas
        elif row['tipo'] in ['vegetal', 'fruta']:
            score += 1.5 + (row['fibras'] * 0.25)

        # D) Energia Limpa
        # Se é carboidrato/tubérculo, tem BAIXA gordura (<2g) e BAIXO sódio (<150mg),
        # ele é uma fonte de energia limpa e saudável.
        elif row['tipo'] in ['carboidrato', 'tuberculo']:
            if row['gorduras'] < 2.5 and row['sodio'] < 150:
                score += 1.5 # Arroz Branco sobe de 5.0 para 6.5 (Nota Azul!)

            # E se ainda por cima tiver fibra (Integral/Aveia), ganha mais um pouco
            if row['fibras'] > 2.5:
                score += 0.5

        # --- 4. TRAVAS DE SEGURANÇA ---

        # Trava de Sódio
        if row['sodio'] > 800: score = min(score, 4.0)
        elif row['sodio'] > 600: score = min(score, 5.0)

        # Trava de Gordura Saturada em Carnes
        if row['tipo'] == 'proteina' and row['gordura_saturada'] > 6:
            score -= 2.0

        # Trava de Farinha/Açúcar (Carbo alto, fibra quase zero e não é tubérculo natural)
        # Exceção para tapioca/mandioca que são naturais
        if row['carboidratos'] > 75 and row['fibras'] < 1 and row['tipo'] == 'carboidrato':
            score = min(score, 5.0)

        # Trava de Gordura Pura
        if row['gorduras'] > 80 and score > 8.5:
            score = 7.5

        return max(0, min(10, score))

    # --- Aplicando a Função Fuzzy ao DataFrame ---
    df_alimentos['nota_saudavel_fuzzy'] = df_alimentos.apply(calcular_fuzzy, axis=1).round(2)

    # --- Arredondar a nota final para 2 casas decimais ---
    df_alimentos['nota_saudavel_fuzzy'] = df_alimentos['nota_saudavel_fuzzy'].round(2)

    # --- Exibindo os Top 15 Mais Saudáveis e Top 15 Menos Saudáveis ---
    ## print("=== TOP 15 ALIMENTOS MAIS SAUDÁVEIS (FUZY) ===")
    ## print(df_alimentos.sort_values(by='nota_saudavel_fuzzy', ascending=False)[['nome', 'tipo', 'nota_saudavel_fuzzy']].head(15))

    ## print("\n=== TOP 15 ALIMENTOS MENOS SAUDÁVEIS ===")
    ## print(df_alimentos.sort_values(by='nota_saudavel_fuzzy', ascending=True)[['nome', 'tipo', 'nota_saudavel_fuzzy']].head(15))

    return df_alimentos
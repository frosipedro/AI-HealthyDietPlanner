"""Sistema Fuzzy para Avaliação de Salubridade de Alimentos"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd
import unicodedata


# ============================================================================
# CONSTANTES GLOBAIS
# ============================================================================

# Alimentos ultraprocessados/industrializados que recebem penalidade
ALIMENTOS_ULTRAPROCESSADOS = {
    'mortadela', 'presunto', 'salsicha', 'nuggets', 'nugget',
    'pao de queijo', 'coxinha', 'pastel', 'batata frita',
    'macarrao instantaneo', 'miojo'
}


def normalizar_nome(nome: str) -> str:
    """Remove acentos e converte para minúsculas."""
    nome_sem_acento = ''.join(
        c for c in unicodedata.normalize('NFD', nome)
        if unicodedata.category(c) != 'Mn'
    )
    return nome_sem_acento.lower().strip()


def aplicar_logica_fuzzy(df_alimentos: pd.DataFrame) -> pd.DataFrame:
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


    # --- FUNÇÃO PRINCIPAL DE CÁLCULO ---
    def calcular_fuzzy(row: pd.Series) -> float:
        """Calcula o score de salubridade usando lógica fuzzy e regras heurísticas."""
        
        # --- 1. INPUTS FUZZY ---
        simulador.input['proteina']    = row['proteinas']
        simulador.input['carboidrato'] = row['carboidratos']
        simulador.input['fibra']       = row['fibras']
        simulador.input['sodio']       = row['sodio']

        # Atenua gordura saturada em refeições caseiras com baixo sódio
        if row['tipo'] == 'refeicao' and row['sodio'] < 400:
            simulador.input['gord_sat'] = row['gordura_saturada'] * 0.6
        else:
            simulador.input['gord_sat'] = row['gordura_saturada']

        simulador.input['gord_insat']  = row['gorduras_insaturadas']

        # --- 2. CÁLCULO BASE FUZZY ---
        try:
            simulador.compute()
            score = simulador.output['saudavel']
        except (ValueError, KeyError):
            score = 5.0  # Valor neutro em caso de erro

        # --- 3. AJUSTES HEUÍSTICOS (aplicados em ordem de prioridade) ---
        
        nome_normalizado = normalizar_nome(row['nome'])
        tipo_alimento = row['tipo']
        
        # A) PENALIDADE ULTRAPROCESSADOS (maior prioridade)
        # Verifica se é exatamente um nome ultraprocessado (não substring)
        eh_ultraprocessado = nome_normalizado in ALIMENTOS_ULTRAPROCESSADOS
        if eh_ultraprocessado:
            score -= 2.0  # Penalidade pesada mas não exagerada
        
        # B) BÔNUS REFEIÇÕES CASEIRAS
        elif tipo_alimento == 'refeicao':
            # Refeições caseiras ganham bônus base
            bonus = 1.5
            
            # Perde bônus se for frita/muito gordurosa
            if row['sodio'] >= 500 or row['gorduras'] >= 10:
                bonus = 0.0
                score -= 1.0  # Penalidade por fritura
            
            score += bonus
            
            # Bônus extra para refeições proteicas saudáveis
            if row['proteinas'] > 15 and bonus > 0:
                score += 0.5
        
        # C) BÔNUS VEGETAIS/FRUTAS
        elif tipo_alimento in ['vegetal', 'fruta']:
            # Vegetais e frutas são sempre bem-vindos
            score += 1.5 + (row['fibras'] * 0.25)
        
        # D) BÔNUS ENERGIA LIMPA (carboidratos naturais)
        elif tipo_alimento in ['carboidrato', 'tuberculo']:
            # Fonte de energia limpa: baixa gordura E baixo sódio
            if row['gorduras'] < 2.5 and row['sodio'] < 150:
                score += 1.5  # Arroz branco, batata, mandioca
                
                # Bônus adicional para integrais (alto teor de fibra)
                if row['fibras'] > 2.5:
                    score += 0.5

        # --- 4. TRAVAS DE SEGURANÇA (aplicadas após todos os bônus) ---
        
        # Trava de Sódio (limite máximo progressivo)
        if row['sodio'] > 800:
            score = min(score, 4.0)  # Máximo 4.0 para sódio muito alto
        elif row['sodio'] > 600:
            score = min(score, 5.5)  # Máximo 5.5 para sódio alto

        # Trava de Gordura Saturada em Proteínas
        if tipo_alimento == 'proteina' and row['gordura_saturada'] > 6:
            score -= 2.0  # Carne muito gorda

        # Trava de Carboidrato Refinado (farinha branca, açúcar)
        if (row['carboidratos'] > 75 and row['fibras'] < 1 and 
            tipo_alimento == 'carboidrato'):
            score = min(score, 5.0)  # Carboidrato vazio

        # Trava de Gordura Pura (óleos, manteiga em excesso)
        if row['gorduras'] > 80:
            score = min(score, 7.5)  # Mesmo sendo gordura boa, não pode ser 10
        
        # --- 5. GARANTIR LIMITES [0, 10] ---
        return max(0.0, min(10.0, score))

    # --- Aplicando a Função Fuzzy ao DataFrame ---
    df_alimentos['nota_saudavel_fuzzy'] = (
        df_alimentos.apply(calcular_fuzzy, axis=1).round(2)
    )

    return df_alimentos
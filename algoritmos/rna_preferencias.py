"""Sistema de Preferências usando Rede Neural Artificial"""

import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple
from utils.validacao_input import validar_numero


# ============================================================================
# MAPEAMENTO DE CATEGORIAS DE ALIMENTOS (para detecção eficiente)
# ============================================================================

CATEGORIAS_ALIMENTOS = {
    'frango': ['frango'],
    'carne_vermelha': ['bife', 'picanha', 'alcatra', 'carne', 'coxão', 'patinho', 'acém'],
    'carne_porco': ['porco', 'lombo', 'pernil'],
    'peixe': ['salmão', 'tilápia', 'sardinha', 'atum', 'peixe', 'camarão', 'bacalhau'],
    'ovos': ['ovo'],
    'laticinio': ['queijo', 'leite', 'iogurte', 'requeijão'],
    'embutidos': ['linguiça', 'bacon', 'carne seca'],
    'industrializados': ['mortadela', 'presunto', 'salsicha', 'nugget'],
    'arroz': ['arroz'],
    'massa': ['macarrão', 'massa'],
    'pao': ['pão'],
    'batata': ['batata', 'mandioca', 'inhame', 'cará'],
    'leguminosas': ['feijão', 'lentilha', 'grão-de-bico', 'ervilha', 'soja'],
    'integral': ['integral', 'aveia', 'centeio'],
    'vegetais_verdes': ['brócolis', 'couve', 'alface', 'repolho', 'vagem'],
    'vegetais_raiz': ['cenoura', 'beterraba', 'abobrinha'],
    'frutas_doces': ['banana', 'mamão', 'uva', 'melancia', 'abacaxi'],
    'frutas_citricas': ['laranja', 'tangerina', 'limão'],
    'abacate': ['abacate'],
    'oleaginosas': ['amendoim', 'castanha', 'nozes', 'amêndoas'],
    'azeite': ['azeite']
}


def categorizar_alimento(nome: str) -> Dict[str, bool]:
    """Retorna dict com flags booleanas indicando categorias do alimento."""
    nome_lower = nome.lower()
    categorias = {}
    
    for categoria, palavras_chave in CATEGORIAS_ALIMENTOS.items():
        categorias[categoria] = any(palavra in nome_lower for palavra in palavras_chave)
    
    return categorias

# ============================================================================
# 1. REDE NEURAL ARTIFICIAL - SISTEMA DE PREFERÊNCIAS
# ============================================================================

class SistemaPreferenciasRNA:
    """
    RNA que aprende e prevê as preferências do usuário para cada alimento.
    """

    def __init__(self):
        self.modelo = MLPRegressor(
            hidden_layer_sizes=(64, 32, 16),
            activation='relu',
            max_iter=500,
            random_state=42,
            early_stopping=True
        )
        self.scaler = StandardScaler()
        self.treinado = False

    def coletar_preferencias_usuario(self) -> Dict:
        """
        Coleta as preferências do usuário sobre ALIMENTOS ESPECÍFICOS.
        Isso permite que o AG escolha entre alimentos nutricionalmente equivalentes.
        """
        print("-" * 80)
        print("🍽️  QUESTIONÁRIO DE PREFERÊNCIAS ALIMENTARES")
        print("-" * 80)
        print("Responda de 0 a 10 (0 = detesto, 10 = amo)")
        print("Isso ajudará a escolher entre alimentos nutricionalmente similares.\n")

        preferencias = {}

        # === PROTEÍNAS ===
        print("-" * 80)
        print("🍗 PROTEÍNAS ANIMAIS")
        print("-" * 80)
        preferencias['pref_frango'] = validar_numero("Quanto você gosta de FRANGO? ", 0, 10) / 10
        preferencias['pref_carne_vermelha'] = validar_numero("Quanto você gosta de CARNE VERMELHA (boi, porco)? ", 0, 10) / 10
        preferencias['pref_peixe'] = validar_numero("Quanto você gosta de PEIXE? ", 0, 10) / 10
        preferencias['pref_ovos'] = validar_numero("Quanto você gosta de OVOS? ", 0, 10) / 10
        preferencias['pref_laticinio'] = validar_numero("Quanto você gosta de LATICÍNIOS (queijo, iogurte, leite)? ", 0, 10) / 10

        # === CARBOIDRATOS ===
        print("\n" + "-" * 80)
        print("🍚 CARBOIDRATOS")
        print("-" * 80)
        preferencias['pref_arroz'] = validar_numero("Quanto você gosta de ARROZ? ", 0, 10) / 10
        preferencias['pref_massa'] = validar_numero("Quanto você gosta de MASSAS (macarrão)? ", 0, 10) / 10
        preferencias['pref_paes'] = validar_numero("Quanto você gosta de PÃES? ", 0, 10) / 10
        preferencias['pref_batata'] = validar_numero("Quanto você gosta de BATATA/TUBÉRCULOS? ", 0, 10) / 10
        preferencias['pref_leguminosas'] = validar_numero("Quanto você gosta de FEIJÃO/LENTILHA/GRÃO-DE-BICO? ", 0, 10) / 10
        preferencias['pref_integral'] = validar_numero("Prefere versões INTEGRAIS (arroz integral, pão integral)? ", 0, 10) / 10

        # === VEGETAIS E FRUTAS ===
        print("\n" + "-" * 80)
        print("🥬 VEGETAIS E FRUTAS")
        print("-" * 80)
        preferencias['pref_vegetais_verdes'] = validar_numero("Quanto você gosta de VEGETAIS VERDES (brócolis, couve)? ", 0, 10) / 10
        preferencias['pref_vegetais_raiz'] = validar_numero("Quanto você gosta de VEGETAIS DE RAIZ (cenoura, beterraba)? ", 0, 10) / 10
        preferencias['pref_frutas_doces'] = validar_numero("Quanto você gosta de FRUTAS DOCES (banana, mamão, uva)? ", 0, 10) / 10
        preferencias['pref_frutas_citricas'] = validar_numero("Quanto você gosta de FRUTAS CÍTRICAS (laranja, tangerina)? ", 0, 10) / 10

        # === GORDURAS E OLEAGINOSAS ===
        print("\n" + "-" * 80)
        print("🥑 GORDURAS SAUDÁVEIS")
        print("-" * 80)
        preferencias['pref_abacate'] = validar_numero("Quanto você gosta de ABACATE? ", 0, 10) / 10
        preferencias['pref_oleaginosas'] = validar_numero("Quanto você gosta de CASTANHAS/NOZES/AMENDOIM? ", 0, 10) / 10
        preferencias['pref_azeite'] = validar_numero("Prefere AZEITE DE OLIVA a outros óleos? ", 0, 10) / 10

        # === INDUSTRIALIZADOS ===
        print("\n" + "-" * 80)
        print("🍕 ALIMENTOS INDUSTRIALIZADOS/PRÁTICOS")
        print("-" * 80)
        preferencias['aceita_industrializados'] = validar_numero("Você aceita INDUSTRIALIZADOS (mortadela, presunto, nuggets)? ", 0, 10) / 10
        preferencias['aceita_embutidos'] = validar_numero("Você aceita EMBUTIDOS (linguiça, salsicha)? ", 0, 10) / 10

        # === RESTRIÇÕES GERAIS ===
        print("\n" + "-" * 80)
        print("⚙️  PREFERÊNCIAS GERAIS")
        print("-" * 80)
        preferencias['evita_sodio'] = validar_numero("Você EVITA alimentos com alto SÓDIO? ", 0, 10) / 10
        preferencias['pref_custo_baixo'] = validar_numero("Prefere alimentos mais ECONÔMICOS? ", 0, 10) / 10

        print("\n✅ Preferências coletadas com sucesso!\n")
        return preferencias

    def gerar_dados_treino_sinteticos(self, df_alimentos: pd.DataFrame, preferencias: Dict, n_samples: int = 500):
        """
        Gera dados sintéticos de treinamento baseado nas preferências do usuário.
        Versão OTIMIZADA usando operações vetorizadas.
        """
        n_alimentos = len(df_alimentos)
        n_total = n_samples * n_alimentos
        
        # Pré-aloca arrays para melhor performance
        # Features: 8 nutricionais + nome do alimento (one-hot seria ideal, mas simplificamos)
        n_features = 8 + len(preferencias)
        X_treino = np.zeros((n_total, n_features), dtype=np.float32)
        y_treino = np.zeros(n_total, dtype=np.float32)
        
        # Extrai features dos alimentos (vetorizado)
        features_alimentos = df_alimentos[['proteinas', 'carboidratos', 'gorduras', 
                                           'fibras', 'calorias', 'sodio', 'custo', 
                                           'nota_saudavel_fuzzy']].values
        
        # Normaliza features dos alimentos
        features_norm = features_alimentos / np.array([50, 100, 50, 20, 500, 2000, 30, 100])
        
        # Converte preferências para array
        pref_array = np.array(list(preferencias.values()), dtype=np.float32)
        
        # Gera variações de preferências (n_samples x n_prefs)
        ruido_pref = np.random.normal(0, 0.15, (n_samples, len(preferencias)))
        pref_variadas = np.clip(pref_array + ruido_pref, 0, 1)
        
        # Para cada amostra de preferências
        idx_base = 0
        for i in range(n_samples):
            idx_fim = idx_base + n_alimentos
            
            # Copia features normalizadas dos alimentos
            X_treino[idx_base:idx_fim, :8] = features_norm
            
            # Adiciona preferências variadas (broadcasting)
            X_treino[idx_base:idx_fim, 8:] = pref_variadas[i]
            
            # Calcula notas de preferência (vetorizado)
            y_treino[idx_base:idx_fim] = self._calcular_notas_vetorizado(
                df_alimentos, features_alimentos, pref_variadas[i], preferencias
            )
            
            idx_base = idx_fim
        
        return X_treino, y_treino

    def _calcular_notas_vetorizado(self, df_alimentos: pd.DataFrame,
                                   features_alimentos: np.ndarray, 
                                   pref: np.ndarray, pref_dict: Dict) -> np.ndarray:
        """
        Versão REALMENTE VETORIZADA do cálculo de notas de preferência.
        Usa operações vetorizadas do NumPy/Pandas para máxima performance.
        """
        n_alimentos = len(features_alimentos)
        notas = np.full(n_alimentos, 0.5, dtype=np.float32)  # baseline
        
        # Extrai colunas nutricionais (vetorizado)
        sodio = features_alimentos[:, 5]
        custo = features_alimentos[:, 6]
        saude = features_alimentos[:, 7]
        
        # Extrai preferências do array
        pref_keys = list(pref_dict.keys())
        prefs = {key: pref[pref_keys.index(key)] for key in pref_keys}
        
        # === CATEGORIZAÇÃO DE ALIMENTOS (UMA VEZ SÓ) ===
        # Cria array de categorias para cada alimento
        categorias_array = df_alimentos['nome'].apply(categorizar_alimento)
        
        # Converte para arrays booleanos (vetorizado)
        mask_frango = np.array([cat['frango'] for cat in categorias_array])
        mask_carne_vermelha = np.array([cat['carne_vermelha'] for cat in categorias_array])
        mask_carne_porco = np.array([cat['carne_porco'] for cat in categorias_array])
        mask_peixe = np.array([cat['peixe'] for cat in categorias_array])
        mask_ovos = np.array([cat['ovos'] for cat in categorias_array])
        mask_laticinio = np.array([cat['laticinio'] for cat in categorias_array])
        mask_embutidos = np.array([cat['embutidos'] for cat in categorias_array])
        mask_industrializados = np.array([cat['industrializados'] for cat in categorias_array])
        mask_arroz = np.array([cat['arroz'] for cat in categorias_array])
        mask_massa = np.array([cat['massa'] for cat in categorias_array])
        mask_pao = np.array([cat['pao'] for cat in categorias_array])
        mask_batata = np.array([cat['batata'] for cat in categorias_array])
        mask_leguminosas = np.array([cat['leguminosas'] for cat in categorias_array])
        mask_integral = np.array([cat['integral'] for cat in categorias_array])
        mask_vegetais_verdes = np.array([cat['vegetais_verdes'] for cat in categorias_array])
        mask_vegetais_raiz = np.array([cat['vegetais_raiz'] for cat in categorias_array])
        mask_frutas_doces = np.array([cat['frutas_doces'] for cat in categorias_array])
        mask_frutas_citricas = np.array([cat['frutas_citricas'] for cat in categorias_array])
        mask_abacate = np.array([cat['abacate'] for cat in categorias_array])
        mask_oleaginosas = np.array([cat['oleaginosas'] for cat in categorias_array])
        mask_azeite = np.array([cat['azeite'] for cat in categorias_array])
        
        # === APLICAÇÃO DE BÔNUS/PENALIDADES (VETORIZADO) ===
        
        # Proteínas animais
        notas += np.where(mask_frango, prefs['pref_frango'] * 0.4, 0.0)
        notas += np.where(mask_carne_vermelha, prefs['pref_carne_vermelha'] * 0.4, 0.0)
        notas += np.where(mask_carne_porco, prefs['pref_carne_vermelha'] * 0.35, 0.0)
        notas += np.where(mask_peixe, prefs['pref_peixe'] * 0.4, 0.0)
        notas += np.where(mask_ovos, prefs['pref_ovos'] * 0.4, 0.0)
        notas += np.where(mask_laticinio, prefs['pref_laticinio'] * 0.4, 0.0)
        
        # Embutidos e industrializados (penaliza se não aceita)
        aceita_emb = prefs['aceita_embutidos']
        aceita_ind = prefs['aceita_industrializados']
        notas += np.where(mask_embutidos, aceita_emb * 0.3 - (1 - aceita_emb) * 0.3, 0.0)
        notas += np.where(mask_industrializados, aceita_ind * 0.3 - (1 - aceita_ind) * 0.3, 0.0)
        
        # Carboidratos (com lógica de integral)
        pref_int = prefs['pref_integral']
        notas += np.where(mask_arroz & mask_integral, (prefs['pref_arroz'] * 0.4 + pref_int * 0.2) / 2, 0.0)
        notas += np.where(mask_arroz & ~mask_integral, prefs['pref_arroz'] * 0.4 - pref_int * 0.1, 0.0)
        notas += np.where(mask_massa, prefs['pref_massa'] * 0.4, 0.0)
        notas += np.where(mask_pao & mask_integral, (prefs['pref_paes'] * 0.4 + pref_int * 0.2) / 2, 0.0)
        notas += np.where(mask_pao & ~mask_integral, prefs['pref_paes'] * 0.4 - pref_int * 0.1, 0.0)
        notas += np.where(mask_batata, prefs['pref_batata'] * 0.4, 0.0)
        notas += np.where(mask_leguminosas, prefs['pref_leguminosas'] * 0.4, 0.0)
        notas += np.where(mask_integral & ~mask_arroz & ~mask_pao, pref_int * 0.3, 0.0)
        
        # Vegetais
        notas += np.where(mask_vegetais_verdes, prefs['pref_vegetais_verdes'] * 0.35, 0.0)
        notas += np.where(mask_vegetais_raiz, prefs['pref_vegetais_raiz'] * 0.35, 0.0)
        
        # Frutas
        notas += np.where(mask_frutas_doces, prefs['pref_frutas_doces'] * 0.35, 0.0)
        notas += np.where(mask_frutas_citricas, prefs['pref_frutas_citricas'] * 0.35, 0.0)
        notas += np.where(mask_abacate, prefs['pref_abacate'] * 0.4, 0.0)
        
        # Oleaginosas e gorduras
        notas += np.where(mask_oleaginosas, prefs['pref_oleaginosas'] * 0.4, 0.0)
        notas += np.where(mask_azeite, prefs['pref_azeite'] * 0.3, 0.0)
        
        # Penalização por sódio alto (vetorizado)
        notas -= np.where(sodio > 500, prefs['evita_sodio'] * 0.2, 0.0)
        
        # Bonificação/penalização por custo (vetorizado)
        pref_custo = prefs['pref_custo_baixo']
        notas += np.where(custo < 5, pref_custo * 0.15, 0.0)
        notas -= np.where(custo > 10, pref_custo * 0.1, 0.0)
        
        # Usa nota de saúde fuzzy (peso menor)
        notas += (saude / 100) * 0.1
        
        # Adiciona ruído para variabilidade
        notas += np.random.normal(0, 0.05, n_alimentos).astype(np.float32)
        
        return np.clip(notas, 0, 1)

    def treinar(self, df_alimentos: pd.DataFrame, preferencias: Dict):
        """
        Treina a RNA com dados sintéticos baseados nas preferências.
        """
        print("🧠 Treinando Rede Neural Artificial...")

        X_treino, y_treino = self.gerar_dados_treino_sinteticos(
            df_alimentos, preferencias, n_samples=500
        )

        # Normaliza os dados
        X_treino_scaled = self.scaler.fit_transform(X_treino)

        # Treina o modelo
        self.modelo.fit(X_treino_scaled, y_treino)
        self.treinado = True

        print(f"✅ RNA treinada! Score: {self.modelo.score(X_treino_scaled, y_treino):.3f}\n")

    def prever_preferencia_alimento(self, alimento: pd.Series, preferencias: Dict) -> float:
        """
        Prevê a nota de preferência do usuário para um alimento específico.
        """
        if not self.treinado:
            raise Exception("Modelo não treinado! Execute treinar() primeiro.")

        # Prepara features
        features = [
            alimento['proteinas'] / 50,
            alimento['carboidratos'] / 100,
            alimento['gorduras'] / 50,
            alimento['fibras'] / 20,
            alimento['calorias'] / 500,
            alimento['sodio'] / 2000,
            alimento['custo'] / 30,
            alimento['nota_saudavel_fuzzy'] / 100
        ]
        features_completas = features + list(preferencias.values())

        # Normaliza e prevê
        X = self.scaler.transform([features_completas])
        nota = self.modelo.predict(X)[0]

        return np.clip(nota, 0, 1)

    def adicionar_notas_preferencia_df(self, df_alimentos: pd.DataFrame, preferencias: Dict) -> pd.DataFrame:
        """
        Adiciona coluna 'nota_preferencia_rna' no dataframe.
        """
        df = df_alimentos.copy()
        df['nota_preferencia_rna'] = df.apply(
            lambda row: self.prever_preferencia_alimento(row, preferencias),
            axis=1
        )
        return df
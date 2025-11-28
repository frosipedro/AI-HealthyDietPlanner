import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from typing import Dict
from utils.validacao_input import validar_numero

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
        Coleta as preferências do usuário através de perguntas.
        Retorna um dicionário com as preferências.
        """
        print("=" * 60)
        print("🍽️  QUESTIONÁRIO DE PREFERÊNCIAS ALIMENTARES")
        print("=" * 60)
        print("Responda de 0 a 10 (0 = não gosto, 10 = amo)\n")

        preferencias = {}

        # Preferências por macronutrientes
        preferencias['pref_proteina'] = validar_numero("Quanto você gosta de alimentos ricos em PROTEÍNA (carnes, ovos)? ", 0, 10) / 10
        preferencias['pref_carboidrato'] = validar_numero("Quanto você gosta de CARBOIDRATOS (massas, pães, arroz)? ", 0, 10) / 10
        preferencias['pref_gordura'] = validar_numero("Quanto você gosta de alimentos com GORDURA (abacate, castanhas)? ", 0, 10) / 10
        preferencias['pref_fibras'] = validar_numero("Quanto você gosta de FIBRAS (vegetais, grãos integrais)? ", 0, 10) / 10

        # Preferências por tipo
        print("\n" + "-" * 60)
        preferencias['pref_baixa_caloria'] = validar_numero("Prefere alimentos de BAIXA CALORIA? ", 0, 10) / 10
        preferencias['evita_sodio'] = validar_numero("Você EVITA alimentos com alto SÓDIO? ", 0, 10) / 10
        preferencias['pref_custo_baixo'] = validar_numero("Prefere alimentos mais BARATOS? ", 0, 10) / 10

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
        n_features = 8 + len(preferencias)  # 8 features do alimento + preferências
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
                features_alimentos, pref_variadas[i], preferencias
            )
            
            idx_base = idx_fim
        
        return X_treino, y_treino

    def _calcular_notas_vetorizado(self, features_alimentos: np.ndarray, 
                                   pref: np.ndarray, pref_dict: Dict) -> np.ndarray:
        """
        Versão VETORIZADA do cálculo de notas de preferência.
        Processa todos os alimentos de uma vez.
        """
        n_alimentos = len(features_alimentos)
        notas = np.full(n_alimentos, 0.5, dtype=np.float32)  # baseline
        
        # Extrai colunas (evita múltiplos acessos)
        proteinas = features_alimentos[:, 0]
        carboidratos = features_alimentos[:, 1]
        gorduras = features_alimentos[:, 2]
        fibras = features_alimentos[:, 3]
        calorias = features_alimentos[:, 4]
        sodio = features_alimentos[:, 5]
        custo = features_alimentos[:, 6]
        saude = features_alimentos[:, 7]
        
        # Mapeia preferências
        pref_proteina = pref[0]
        pref_carboidrato = pref[1]
        pref_gordura = pref[2]
        pref_fibras = pref[3]
        pref_baixa_cal = pref[4]
        evita_sodio = pref[5]
        pref_custo = pref[6]
        
        # Pontuação por macronutrientes (vetorizado)
        notas += np.where(proteinas > 15, pref_proteina * 0.2, 0)
        notas += np.where(carboidratos > 30, pref_carboidrato * 0.2, 0)
        notas += np.where(gorduras > 10, pref_gordura * 0.15, 0)
        notas += np.where(fibras > 5, pref_fibras * 0.15, 0)
        
        # Bonificação/penalização por calorias
        notas += np.where(calorias < 200, pref_baixa_cal * 0.1, 0)
        notas -= np.where(calorias > 400, pref_baixa_cal * 0.1, 0)
        
        # Penalização por sódio alto
        notas -= np.where(sodio > 500, evita_sodio * 0.15, 0)
        
        # Bonificação por custo baixo
        notas += np.where(custo < 5, pref_custo * 0.1, 0)
        
        # Usa nota de saúde fuzzy
        notas += (saude / 100) * 0.2
        
        # Adiciona ruído
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
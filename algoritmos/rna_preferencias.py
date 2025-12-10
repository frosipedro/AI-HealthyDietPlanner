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
        Versão VETORIZADA do cálculo de notas de preferência.
        Usa CATEGORIAS ESPECÍFICAS de alimentos ao invés de macronutrientes genéricos.
        """
        n_alimentos = len(features_alimentos)
        notas = np.full(n_alimentos, 0.5, dtype=np.float32)  # baseline
        
        # Extrai colunas nutricionais
        sodio = features_alimentos[:, 5]
        custo = features_alimentos[:, 6]
        saude = features_alimentos[:, 7]
        
        # Mapeia as novas preferências
        pref_keys = list(pref_dict.keys())
        pref_frango = pref[pref_keys.index('pref_frango')]
        pref_carne_vermelha = pref[pref_keys.index('pref_carne_vermelha')]
        pref_peixe = pref[pref_keys.index('pref_peixe')]
        pref_ovos = pref[pref_keys.index('pref_ovos')]
        pref_laticinio = pref[pref_keys.index('pref_laticinio')]
        pref_arroz = pref[pref_keys.index('pref_arroz')]
        pref_massa = pref[pref_keys.index('pref_massa')]
        pref_paes = pref[pref_keys.index('pref_paes')]
        pref_batata = pref[pref_keys.index('pref_batata')]
        pref_leguminosas = pref[pref_keys.index('pref_leguminosas')]
        pref_integral = pref[pref_keys.index('pref_integral')]
        pref_vegetais_verdes = pref[pref_keys.index('pref_vegetais_verdes')]
        pref_vegetais_raiz = pref[pref_keys.index('pref_vegetais_raiz')]
        pref_frutas_doces = pref[pref_keys.index('pref_frutas_doces')]
        pref_frutas_citricas = pref[pref_keys.index('pref_frutas_citricas')]
        pref_abacate = pref[pref_keys.index('pref_abacate')]
        pref_oleaginosas = pref[pref_keys.index('pref_oleaginosas')]
        pref_azeite = pref[pref_keys.index('pref_azeite')]
        aceita_industrializados = pref[pref_keys.index('aceita_industrializados')]
        aceita_embutidos = pref[pref_keys.index('aceita_embutidos')]
        evita_sodio = pref[pref_keys.index('evita_sodio')]
        pref_custo_baixo = pref[pref_keys.index('pref_custo_baixo')]
        
        # Itera sobre alimentos e aplica preferências específicas
        for i, row in df_alimentos.iterrows():
            nome = row['nome'].lower()
            bonus = 0.0
            
            # === PROTEÍNAS ANIMAIS ===
            if 'frango' in nome:
                bonus += pref_frango * 0.4
            elif any(x in nome for x in ['bife', 'picanha', 'alcatra', 'carne', 'coxão', 'patinho', 'acém']):
                bonus += pref_carne_vermelha * 0.4
            elif 'porco' in nome or 'lombo' in nome or 'pernil' in nome:
                bonus += pref_carne_vermelha * 0.35  # Um pouco menos que boi
            elif any(x in nome for x in ['salmão', 'tilápia', 'sardinha', 'atum', 'peixe']):
                bonus += pref_peixe * 0.4
            elif 'ovo' in nome:
                bonus += pref_ovos * 0.4
            elif any(x in nome for x in ['queijo', 'leite', 'iogurte', 'requeijão']):
                bonus += pref_laticinio * 0.4
            
            # === EMBUTIDOS (penalização se não aceita) ===
            if any(x in nome for x in ['linguiça', 'bacon', 'carne seca']):
                bonus += aceita_embutidos * 0.3 - (1 - aceita_embutidos) * 0.3
            if any(x in nome for x in ['mortadela', 'presunto', 'salsicha']):
                bonus += aceita_industrializados * 0.3 - (1 - aceita_industrializados) * 0.3
            
            # === CARBOIDRATOS ===
            if 'arroz' in nome:
                if 'integral' in nome:
                    bonus += (pref_arroz * 0.4 + pref_integral * 0.2) / 2
                else:
                    bonus += pref_arroz * 0.4 - pref_integral * 0.1  # Penaliza se prefere integral
            elif any(x in nome for x in ['macarrão', 'massa']):
                bonus += pref_massa * 0.4
            elif 'pão' in nome:
                if 'integral' in nome or 'centeio' in nome:
                    bonus += (pref_paes * 0.4 + pref_integral * 0.2) / 2
                else:
                    bonus += pref_paes * 0.4 - pref_integral * 0.1
            elif any(x in nome for x in ['batata', 'mandioca', 'inhame', 'cará']):
                bonus += pref_batata * 0.4
            elif any(x in nome for x in ['feijão', 'lentilha', 'grão-de-bico', 'ervilha', 'soja']):
                bonus += pref_leguminosas * 0.4
            elif 'aveia' in nome or 'integral' in nome:
                bonus += pref_integral * 0.3
            
            # === VEGETAIS ===
            if any(x in nome for x in ['brócolis', 'couve', 'alface', 'repolho', 'vagem']):
                bonus += pref_vegetais_verdes * 0.35
            elif any(x in nome for x in ['cenoura', 'beterraba', 'abobrinha']):
                bonus += pref_vegetais_raiz * 0.35
            
            # === FRUTAS ===
            if any(x in nome for x in ['banana', 'mamão', 'uva', 'melancia', 'abacaxi']):
                bonus += pref_frutas_doces * 0.35
            elif any(x in nome for x in ['laranja', 'tangerina', 'limão']):
                bonus += pref_frutas_citricas * 0.35
            elif 'abacate' in nome:
                bonus += pref_abacate * 0.4
            
            # === OLEAGINOSAS E GORDURAS ===
            if any(x in nome for x in ['amendoim', 'castanha', 'nozes', 'amêndoas']):
                bonus += pref_oleaginosas * 0.4
            elif 'azeite' in nome:
                bonus += pref_azeite * 0.3
            
            # === INDUSTRIALIZADOS GERAIS ===
            if row['tipo'] == 'industrializado':
                bonus += aceita_industrializados * 0.2 - (1 - aceita_industrializados) * 0.2
            
            notas[i] += bonus
        
        # Penalização por sódio alto (vetorizado)
        notas -= np.where(sodio > 500, evita_sodio * 0.2, 0)
        
        # Bonificação por custo baixo (vetorizado)
        notas += np.where(custo < 5, pref_custo_baixo * 0.15, 0)
        notas -= np.where(custo > 10, pref_custo_baixo * 0.1, 0)
        
        # Usa nota de saúde fuzzy (peso menor agora)
        notas += (saude / 100) * 0.1
        
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
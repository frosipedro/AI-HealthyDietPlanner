import pandas as pd
import heapq
from typing import List, Dict, Tuple, Set, Optional, cast
from dataclasses import dataclass, field
from data.regras_culinarias import obter_categoria_culinaria, alimento_permitido_na_refeicao

# ============================================================================
# 2. ALGORITMO A* - PRÉ-SELEÇÃO INTELIGENTE DE ALIMENTOS
# VERSÃO MELHORADA - Considera contexto culinário
# ============================================================================

@dataclass(order=True)
class No:
    """
    Representa um nó na árvore de busca do A*.
    """
    f: float
    g: float = field(compare=False)
    h: float = field(compare=False)
    alimentos: Tuple[int, ...] = field(compare=False)
    proximo_indice: int = field(compare=False)

    def __hash__(self):
        return hash(self.alimentos)


class BuscaAEstrela:
    """
    Implementa A* verdadeiro para pré-selecionar os melhores alimentos por tipo de refeição.
    VERSÃO MELHORADA - Filtra por categorias culinárias apropriadas.
    """

    def __init__(self, df_alimentos: pd.DataFrame, meta_calorias: float,
                 orcamento_maximo: float, pesos: Optional[Dict[str, float]] = None):
        self.df: pd.DataFrame = df_alimentos
        self.meta_calorias = meta_calorias
        self.orcamento = orcamento_maximo

        # Pesos otimizados (mais peso para saúde e preferência)
        self.pesos = pesos or {
            'saude': 0.40,
            'preferencia': 0.35,
            'custo': 0.15,
            'calorias': 0.10
        }
        
        self._cache_metricas = {}

    def _get_metricas_alimento(self, idx: int) -> Tuple[float, float, float, float]:
        """Retorna métricas do alimento com cache."""
        if idx not in self._cache_metricas:
            row = self.df.iloc[idx]
            self._cache_metricas[idx] = (
                row['calorias'],
                row['custo'],
                row['nota_saudavel_fuzzy'],
                row['nota_preferencia_rna']
            )
        return self._cache_metricas[idx]

    def _calcular_metricas_selecao(self, indices: Tuple[int, ...]) -> Tuple[float, float, float, float]:
        """Calcula métricas agregadas para uma seleção de alimentos."""
        if not indices:
            return 0.0, 0.0, 0.0, 0.0
        
        total_calorias = 0.0
        total_custo = 0.0
        soma_saude = 0.0
        soma_pref = 0.0
        
        for idx in indices:
            cal, custo, saude, pref = self._get_metricas_alimento(idx)
            total_calorias += cal
            total_custo += custo
            soma_saude += saude
            soma_pref += pref
        
        n = len(indices)
        return total_calorias, total_custo, soma_saude / n, soma_pref / n

    def calcular_custo_g(self, indices: Tuple[int, ...]) -> float:
        """
        Custo real g(n): mede a "penalidade" da seleção atual.
        """
        if not indices:
            return 0.0

        calorias, custo, saude_media, pref_media = self._calcular_metricas_selecao(indices)
        
        if custo > self.orcamento:
            return float('inf')
        
        qualidade_saude = saude_media / 100.0
        qualidade_pref = pref_media
        
        penalidade_custo = custo / self.orcamento if self.orcamento > 0 else 0
        
        g = (
            self.pesos['saude'] * (1 - qualidade_saude) +
            self.pesos['preferencia'] * (1 - qualidade_pref) +
            self.pesos['custo'] * penalidade_custo
        )
        
        return g

    def calcular_heuristica(self, indices: Tuple[int, ...], 
                           indices_disponiveis: List[int],
                           proximo_idx: int,
                           max_alimentos: int) -> float:
        """
        Heurística admissível h(n): estima o custo mínimo para completar a seleção.
        """
        alimentos_restantes = max_alimentos - len(indices)
        
        if alimentos_restantes <= 0:
            calorias, custo, saude, pref = self._calcular_metricas_selecao(indices)
            
            if self.meta_calorias > 0:
                desvio_calorico = abs(calorias - self.meta_calorias) / self.meta_calorias
            else:
                desvio_calorico = 0
            
            return self.pesos['calorias'] * desvio_calorico
        
        if proximo_idx >= len(indices_disponiveis):
            return 0.0
        
        melhores_disponiveis = []
        for i in range(proximo_idx, min(proximo_idx + alimentos_restantes, len(indices_disponiveis))):
            idx = indices_disponiveis[i]
            _, custo, saude, pref = self._get_metricas_alimento(idx)
            score = (saude / 100.0 + pref) / 2
            melhores_disponiveis.append(score)
        
        if not melhores_disponiveis:
            return 0.0
        
        melhor_score_possivel = max(melhores_disponiveis) if melhores_disponiveis else 1.0
        h = (1 - melhor_score_possivel) * 0.1
        
        return h

    def buscar_melhores_alimentos_por_tipo(self, tipo_refeicao: str,
                                           top_n: int = 15,
                                           max_alimentos_selecao: int = 5,
                                           max_iteracoes: int = 10000) -> List[int]:
        """
        Usa A* para encontrar a melhor combinação de alimentos.
        VERSÃO MELHORADA - Filtra por categorias culinárias apropriadas.
        """
        print(f"🔍 A* buscando melhores alimentos para: {tipo_refeicao}")

        df_tipo = cast(pd.DataFrame, self.df[self.df['tipo'] == tipo_refeicao].copy())

        if len(df_tipo) == 0:
            print(f"⚠️  Nenhum alimento encontrado do tipo '{tipo_refeicao}'")
            return []

        # NOVO: Filtra por categorias culinárias apropriadas
        # Determina qual tipo de refeição este tipo nutricional pode servir
        # Ex: proteína -> almoço/jantar, carboidrato -> todas, fruta -> lanches
        refeicoes_alvo = self._determinar_refeicoes_alvo(tipo_refeicao)
        
        # Filtra alimentos que são apropriados para PELO MENOS UMA refeição alvo
        df_tipo_filtrado = df_tipo[
            df_tipo.apply(
                lambda row: any(
                    alimento_permitido_na_refeicao(row['nome'], ref) 
                    for ref in refeicoes_alvo
                ),
                axis=1
            )
        ].copy()  # .copy() evita o warning
        
        if len(df_tipo_filtrado) == 0:
            print(f"⚠️  Nenhum alimento apropriado encontrado para {tipo_refeicao}")
            return []
        
        # Score inicial com pesos otimizados
        df_tipo_filtrado['_score_inicial'] = (
            (df_tipo_filtrado['nota_saudavel_fuzzy'] / 100) * self.pesos['saude'] +
            df_tipo_filtrado['nota_preferencia_rna'] * self.pesos['preferencia'] -
            (df_tipo_filtrado['custo'] / max(df_tipo_filtrado['custo'].max(), 1)) * self.pesos['custo']
        )
        df_tipo_sorted = df_tipo_filtrado.sort_values(by='_score_inicial', ascending=False)
        indices_disponiveis = df_tipo_sorted.index.tolist()
        
        max_candidatos = min(len(indices_disponiveis), top_n * 3)
        indices_disponiveis = indices_disponiveis[:max_candidatos]

        # Inicialização do A*
        estado_inicial = tuple()
        g_inicial = 0.0
        h_inicial = self.calcular_heuristica(estado_inicial, indices_disponiveis, 0, max_alimentos_selecao)
        
        no_inicial = No(
            f=g_inicial + h_inicial,
            g=g_inicial,
            h=h_inicial,
            alimentos=estado_inicial,
            proximo_indice=0
        )

        fronteira: List[No] = []
        heapq.heappush(fronteira, no_inicial)
        
        visitados: Set[Tuple[int, ...]] = set()
        
        melhor_solucao: Optional[Tuple[int, ...]] = None
        melhor_custo = float('inf')
        
        todas_solucoes: List[Tuple[float, Tuple[int, ...]]] = []
        
        iteracoes = 0
        nos_expandidos = 0
        
        while fronteira and iteracoes < max_iteracoes:
            iteracoes += 1
            
            no_atual = heapq.heappop(fronteira)
            
            if no_atual.alimentos in visitados:
                continue
            
            visitados.add(no_atual.alimentos)
            nos_expandidos += 1
            
            if len(no_atual.alimentos) > 0:
                calorias, custo, _, _ = self._calcular_metricas_selecao(no_atual.alimentos)
                
                if custo <= self.orcamento:
                    todas_solucoes.append((no_atual.g, no_atual.alimentos))
                    
                    if no_atual.g < melhor_custo:
                        melhor_custo = no_atual.g
                        melhor_solucao = no_atual.alimentos
            
            if len(no_atual.alimentos) >= max_alimentos_selecao:
                continue
            
            if no_atual.proximo_indice >= len(indices_disponiveis):
                continue
            
            for i in range(no_atual.proximo_indice, len(indices_disponiveis)):
                novo_alimento = indices_disponiveis[i]
                
                novos_alimentos = no_atual.alimentos + (novo_alimento,)
                
                if novos_alimentos in visitados:
                    continue
                
                novo_g = self.calcular_custo_g(novos_alimentos)
                
                if novo_g == float('inf'):
                    continue
                
                novo_h = self.calcular_heuristica(
                    novos_alimentos, 
                    indices_disponiveis, 
                    i + 1,
                    max_alimentos_selecao
                )
                
                novo_no = No(
                    f=novo_g + novo_h,
                    g=novo_g,
                    h=novo_h,
                    alimentos=novos_alimentos,
                    proximo_indice=i + 1
                )
                
                heapq.heappush(fronteira, novo_no)

        todas_solucoes.sort(key=lambda x: x[0])
        
        alimentos_selecionados = []
        alimentos_vistos = set()
        
        for _, solucao in todas_solucoes:
            for idx in solucao:
                if idx not in alimentos_vistos:
                    alimentos_vistos.add(idx)
                    alimentos_selecionados.append(idx)
                    if len(alimentos_selecionados) >= top_n:
                        break
            if len(alimentos_selecionados) >= top_n:
                break
        
        if len(alimentos_selecionados) < top_n:
            for idx in indices_disponiveis:
                if idx not in alimentos_vistos:
                    alimentos_selecionados.append(idx)
                    if len(alimentos_selecionados) >= top_n:
                        break

        print(f"   📊 Iterações: {iteracoes}, Nós expandidos: {nos_expandidos}")
        print(f"   📊 Soluções encontradas: {len(todas_solucoes)}")
        print(f"✅ {len(alimentos_selecionados)} alimentos pré-selecionados!\n")

        return alimentos_selecionados
    
    def _determinar_refeicoes_alvo(self, tipo_nutricional: str) -> List[str]:
        """
        NOVO: Determina quais refeições são apropriadas para cada tipo nutricional.
        """
        mapeamento = {
            'proteina': ['Café da Manhã', 'Almoço', 'Lanche da Tarde', 'Jantar'],
            'carboidrato': ['Café da Manhã', 'Almoço', 'Lanche da Manhã', 'Lanche da Tarde', 'Jantar'],
            'vegetal': ['Almoço', 'Jantar'],
            'fruta': ['Café da Manhã', 'Lanche da Manhã', 'Lanche da Tarde', 'Ceia'],
            'gordura': ['Café da Manhã', 'Almoço', 'Lanche da Tarde', 'Jantar'],
            'industrializado': ['Lanche da Manhã', 'Lanche da Tarde'],
        }
        
        return mapeamento.get(tipo_nutricional, ['Almoço', 'Jantar', 'Café da Manhã'])

    def preselecionar_alimentos_todas_refeicoes(self, top_n_por_tipo: int = 20) -> Dict[str, List[int]]:
        """
        Executa A* para cada tipo de refeição e retorna dicionário com os melhores.
        VERSÃO MELHORADA - top_n aumentado de 15 para 20.
        """
        tipos_refeicao = self.df['tipo'].unique()

        print("-" * 60)
        print("🎯 EXECUTANDO ALGORITMO A* - PRÉ-SELEÇÃO INTELIGENTE")
        print("-" * 60 + "\n")

        self._cache_metricas.clear()

        melhores_por_tipo = {}

        for tipo in tipos_refeicao:
            melhores = self.buscar_melhores_alimentos_por_tipo(tipo, top_n_por_tipo)
            melhores_por_tipo[tipo] = melhores

        print("-" * 60)
        print("Alimentos pré-selecionados por tipo de refeição.")
        print("-" * 60 + "\n")
        
        return melhores_por_tipo
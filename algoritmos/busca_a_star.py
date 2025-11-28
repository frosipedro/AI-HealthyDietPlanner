import pandas as pd
import heapq
from typing import List, Dict, Tuple, Set, Optional
from dataclasses import dataclass, field

# ============================================================================
# 2. ALGORITMO A* - PRÉ-SELEÇÃO INTELIGENTE DE ALIMENTOS
# ============================================================================

@dataclass(order=True)
class No:
    """
    Representa um nó na árvore de busca do A*.
    Usa dataclass com order=True para comparação automática pelo primeiro campo (f).
    """
    f: float  # f(n) = g(n) + h(n) - deve ser primeiro para ordenação
    g: float = field(compare=False)  # custo real acumulado
    h: float = field(compare=False)  # heurística
    alimentos: Tuple[int, ...] = field(compare=False)  # tupla para ser hashável
    proximo_indice: int = field(compare=False)  # próximo alimento a considerar

    def __hash__(self):
        return hash(self.alimentos)


class BuscaAEstrela:
    """
    Implementa A* verdadeiro para pré-selecionar os melhores alimentos por tipo de refeição.
    
    O algoritmo busca a melhor combinação de alimentos que:
    - Maximiza saúde e preferência
    - Minimiza custo
    - Respeita restrições de orçamento e calorias
    """

    def __init__(self, df_alimentos: pd.DataFrame, meta_calorias: float,
                 orcamento_maximo: float, pesos: Optional[Dict[str, float]] = None):
        self.df = df_alimentos
        self.meta_calorias = meta_calorias
        self.orcamento = orcamento_maximo

        # Pesos para a função objetivo (podem ser ajustados)
        self.pesos = pesos or {
            'saude': 0.35,
            'preferencia': 0.35,
            'custo': 0.15,
            'calorias': 0.15
        }
        
        # Cache para métricas dos alimentos
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
        
        Quanto melhor a seleção (alta saúde, alta preferência, baixo custo),
        menor será g(n).
        """
        if not indices:
            return 0.0

        calorias, custo, saude_media, pref_media = self._calcular_metricas_selecao(indices)
        
        # Penalidade por exceder orçamento (custo proibitivo)
        if custo > self.orcamento:
            return float('inf')
        
        # Custo baseado no inverso da qualidade
        # Normaliza saúde (0-100) e preferência (0-1) para mesma escala
        qualidade_saude = saude_media / 100.0
        qualidade_pref = pref_media
        
        # Penalidade por custo (normalizado pelo orçamento)
        penalidade_custo = custo / self.orcamento if self.orcamento > 0 else 0
        
        # g(n) = custo acumulado (menor = melhor)
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
        
        A heurística é ADMISSÍVEL (nunca superestima) pois assume que podemos
        adicionar os melhores alimentos restantes.
        """
        alimentos_restantes = max_alimentos - len(indices)
        
        if alimentos_restantes <= 0:
            # Já temos o máximo de alimentos - avalia qualidade final
            calorias, custo, saude, pref = self._calcular_metricas_selecao(indices)
            
            # Penalidade por desvio calórico
            if self.meta_calorias > 0:
                desvio_calorico = abs(calorias - self.meta_calorias) / self.meta_calorias
            else:
                desvio_calorico = 0
            
            return self.pesos['calorias'] * desvio_calorico
        
        # Estima melhoria possível com alimentos restantes
        # Assume otimisticamente que podemos adicionar alimentos perfeitos
        # (saúde=100, pref=1, custo=0) - isso garante admissibilidade
        
        # A heurística retorna 0 como limite inferior otimista
        # Isso é admissível mas não muito informativo
        # Podemos melhorar calculando baseado nos melhores alimentos disponíveis
        
        if proximo_idx >= len(indices_disponiveis):
            return 0.0
        
        # Calcula a melhor melhoria possível com alimentos restantes
        melhores_disponiveis = []
        for i in range(proximo_idx, min(proximo_idx + alimentos_restantes, len(indices_disponiveis))):
            idx = indices_disponiveis[i]
            _, custo, saude, pref = self._get_metricas_alimento(idx)
            score = (saude / 100.0 + pref) / 2  # score médio
            melhores_disponiveis.append(score)
        
        if not melhores_disponiveis:
            return 0.0
        
        # Heurística otimista: assume que conseguiremos o melhor score possível
        melhor_score_possivel = max(melhores_disponiveis) if melhores_disponiveis else 1.0
        h = (1 - melhor_score_possivel) * 0.1  # fator pequeno para manter admissibilidade
        
        return h

    def buscar_melhores_alimentos_por_tipo(self, tipo_refeicao: str,
                                           top_n: int = 15,
                                           max_alimentos_selecao: int = 5,
                                           max_iteracoes: int = 10000) -> List[int]:
        """
        Usa A* verdadeiro para encontrar a melhor combinação de alimentos.
        
        Args:
            tipo_refeicao: tipo de refeição a buscar
            top_n: número máximo de alimentos a retornar
            max_alimentos_selecao: máximo de alimentos em uma combinação
            max_iteracoes: limite de iterações para evitar loops infinitos
        
        Returns:
            Lista de índices dos melhores alimentos encontrados
        """
        print(f"🔍 A* buscando melhores alimentos para: {tipo_refeicao}")

        # Filtra alimentos do tipo específico
        df_tipo = self.df[self.df['tipo'] == tipo_refeicao].copy()

        if len(df_tipo) == 0:
            print(f"⚠️  Nenhum alimento encontrado do tipo '{tipo_refeicao}'")
            return []

        # Índices disponíveis (ordenados por score inicial para melhor performance)
        df_tipo['_score_inicial'] = (
            (df_tipo['nota_saudavel_fuzzy'] / 100) * self.pesos['saude'] +
            df_tipo['nota_preferencia_rna'] * self.pesos['preferencia'] -
            (df_tipo['custo'] / max(df_tipo['custo'].max(), 1)) * self.pesos['custo']
        )
        df_tipo_sorted = df_tipo.sort_values('_score_inicial', ascending=False)
        indices_disponiveis = df_tipo_sorted.index.tolist()
        
        # Limita candidatos para melhor performance
        max_candidatos = min(len(indices_disponiveis), top_n * 3)
        indices_disponiveis = indices_disponiveis[:max_candidatos]

        # Inicialização do A*
        # Estado inicial: nenhum alimento selecionado
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

        # Fila de prioridade (min-heap)
        fronteira: List[No] = []
        heapq.heappush(fronteira, no_inicial)
        
        # Conjunto de estados visitados
        visitados: Set[Tuple[int, ...]] = set()
        
        # Melhor solução encontrada
        melhor_solucao: Optional[Tuple[int, ...]] = None
        melhor_custo = float('inf')
        
        # Coleta todas as boas soluções para retornar top_n
        todas_solucoes: List[Tuple[float, Tuple[int, ...]]] = []
        
        iteracoes = 0
        nos_expandidos = 0
        
        while fronteira and iteracoes < max_iteracoes:
            iteracoes += 1
            
            # Remove nó com menor f(n)
            no_atual = heapq.heappop(fronteira)
            
            # Pula se já visitado
            if no_atual.alimentos in visitados:
                continue
            
            visitados.add(no_atual.alimentos)
            nos_expandidos += 1
            
            # Verifica se é uma solução válida
            if len(no_atual.alimentos) > 0:
                calorias, custo, _, _ = self._calcular_metricas_selecao(no_atual.alimentos)
                
                # Solução válida se não excede orçamento
                if custo <= self.orcamento:
                    todas_solucoes.append((no_atual.g, no_atual.alimentos))
                    
                    if no_atual.g < melhor_custo:
                        melhor_custo = no_atual.g
                        melhor_solucao = no_atual.alimentos
            
            # Se já temos alimentos suficientes ou não há mais candidatos, não expande
            if len(no_atual.alimentos) >= max_alimentos_selecao:
                continue
            
            if no_atual.proximo_indice >= len(indices_disponiveis):
                continue
            
            # Expande: gera sucessores adicionando cada alimento disponível
            for i in range(no_atual.proximo_indice, len(indices_disponiveis)):
                novo_alimento = indices_disponiveis[i]
                
                # Cria novo estado
                novos_alimentos = no_atual.alimentos + (novo_alimento,)
                
                # Pula se já visitado
                if novos_alimentos in visitados:
                    continue
                
                # Calcula custo g do novo estado
                novo_g = self.calcular_custo_g(novos_alimentos)
                
                # Poda: ignora estados inválidos
                if novo_g == float('inf'):
                    continue
                
                # Calcula heurística
                novo_h = self.calcular_heuristica(
                    novos_alimentos, 
                    indices_disponiveis, 
                    i + 1,
                    max_alimentos_selecao
                )
                
                # Cria novo nó
                novo_no = No(
                    f=novo_g + novo_h,
                    g=novo_g,
                    h=novo_h,
                    alimentos=novos_alimentos,
                    proximo_indice=i + 1
                )
                
                heapq.heappush(fronteira, novo_no)

        # Ordena soluções por custo e extrai os melhores alimentos únicos
        todas_solucoes.sort(key=lambda x: x[0])
        
        # Coleta alimentos únicos das melhores soluções
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
        
        # Se não encontrou suficientes, completa com os melhores por score
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

    def preselecionar_alimentos_todas_refeicoes(self, top_n_por_tipo: int = 15) -> Dict[str, List[int]]:
        """
        Executa A* para cada tipo de refeição e retorna dicionário com os melhores.
        """
        tipos_refeicao = self.df['tipo'].unique()

        print("=" * 60)
        print("🎯 EXECUTANDO ALGORITMO A* - PRÉ-SELEÇÃO INTELIGENTE")
        print("=" * 60 + "\n")

        # Limpa cache entre execuções
        self._cache_metricas.clear()

        melhores_por_tipo = {}

        for tipo in tipos_refeicao:
            melhores = self.buscar_melhores_alimentos_por_tipo(tipo, top_n_por_tipo)
            melhores_por_tipo[tipo] = melhores

        print("=" * 60)
        print("✅ A* concluído! Alimentos pré-selecionados por tipo de refeição.")
        print("=" * 60 + "\n")
        
        return melhores_por_tipo
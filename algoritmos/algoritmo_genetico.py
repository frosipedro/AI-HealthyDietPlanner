"""
Algoritmo Genético V2 - Refeições Compostas com Controle de Macros
"""

import numpy as np
import pandas as pd
import random
from typing import List, Dict, Tuple


# ============================================================================
# CONFIGURAÇÕES DE GRAMATURA POR TIPO DE ALIMENTO (BASE)
# Estes valores são para uma refeição de ~600 kcal (referência)
# Serão escalados dinamicamente conforme as calorias-alvo
# ============================================================================

LIMITES_BASE_GRAMATURA = {
    'proteina': {'min': 80, 'max': 200, 'ideal': 120},
    'carboidrato': {'min': 50, 'max': 200, 'ideal': 100},
    'gordura': {'min': 5, 'max': 30, 'ideal': 10},
    'vegetal': {'min': 50, 'max': 150, 'ideal': 100},
    'fruta': {'min': 80, 'max': 200, 'ideal': 120},
    'industrializado': {'min': 30, 'max': 100, 'ideal': 50},
    'refeicao': {'min': 100, 'max': 400, 'ideal': 200}
}

# Calorias de referência para escalonamento
CALORIAS_REFERENCIA_REFEICAO = 600  # Refeição média


def calcular_limites_dinamicos(tipo_alimento: str, calorias_alvo_refeicao: float) -> Dict[str, float]:
    """
    Calcula limites de gramatura dinamicamente baseado nas calorias-alvo.
    
    Args:
        tipo_alimento: Tipo do alimento
        calorias_alvo_refeicao: Calorias-alvo da refeição
    
    Returns:
        Dict com limites ajustados {'min': x, 'max': y, 'ideal': z}
    """
    limites_base = LIMITES_BASE_GRAMATURA.get(tipo_alimento, {'min': 30, 'max': 300, 'ideal': 100})
    
    # Vegetais e frutas NÃO escalam (sempre porção padrão)
    if tipo_alimento in ['vegetal', 'fruta']:
        return limites_base.copy()
    
    # Calcula fator de escala baseado nas calorias
    fator_escala = calorias_alvo_refeicao / CALORIAS_REFERENCIA_REFEICAO
    
    # Limita o escalonamento para evitar valores absurdos
    # Máximo 3x e mínimo 0.5x dos valores base
    fator_escala = max(0.5, min(3.0, fator_escala))
    
    # Aplica escala aos limites
    limites_ajustados = {
        'min': limites_base['min'] * fator_escala,
        'max': limites_base['max'] * fator_escala,
        'ideal': limites_base['ideal'] * fator_escala
    }
    
    # Garante que min não seja menor que 30g
    limites_ajustados['min'] = max(30, limites_ajustados['min'])
    
    # Para gorduras, mantém um limite máximo absoluto
    if tipo_alimento == 'gordura':
        limites_ajustados['max'] = min(50, limites_ajustados['max'])
    
    return limites_ajustados


class CardapioCompleto:
    """
    Representa um cardápio completo do dia com refeições compostas.
    """
    def __init__(self, refeicoes: Dict[str, List[Dict]]):
        """
        Args:
            refeicoes: Dict com {nome_refeicao: [{alimento: idx, gramas: g}, ...]}
        """
        self.refeicoes = refeicoes
        self.fitness = 0.0
        self.metricas = {}
    
    def calcular_totais(self) -> Dict:
        """Calcula totais nutricionais do dia."""
        totais = {
            'calorias': 0,
            'proteinas': 0,
            'carboidratos': 0,
            'gorduras': 0,
            'fibras': 0,
            'sodio': 0,
            'custo': 0,
            'saude_media': 0,
            'preferencia_media': 0
        }
        
        total_alimentos = 0
        soma_saude = 0
        soma_pref = 0
        
        for alimentos_ref in self.refeicoes.values():
            for alimento in alimentos_ref:
                totais['calorias'] += alimento['calorias']
                totais['proteinas'] += alimento['proteinas']
                totais['carboidratos'] += alimento['carboidratos']
                totais['gorduras'] += alimento['gorduras']
                totais['fibras'] += alimento['fibras']
                totais['sodio'] += alimento['sodio']
                totais['custo'] += alimento['custo']
                soma_saude += alimento['nota_saudavel_fuzzy']
                soma_pref += alimento['nota_preferencia_rna']
                total_alimentos += 1
        
        if total_alimentos > 0:
            totais['saude_media'] = soma_saude / total_alimentos
            totais['preferencia_media'] = soma_pref / total_alimentos
        
        return totais
    
    def exportar_para_dataframe(self) -> pd.DataFrame:
        """Exporta cardápio para DataFrame."""
        linhas = []
        
        for nome_ref, alimentos in self.refeicoes.items():
            for alimento in alimentos:
                linha = alimento.copy()
                linha['refeicao'] = nome_ref
                linhas.append(linha)
        
        return pd.DataFrame(linhas)


class AlgoritmoGeneticoV2:
    """
    Algoritmo Genético para otimizar cardápios com refeições compostas.
    """
    
    def __init__(self, df_alimentos: pd.DataFrame,
                 alimentos_preselecionados: Dict[str, List[int]],
                 config_refeicoes: List[Tuple[str, float]],
                 metas: Dict,
                 pref_vegetais: Dict):
        """
        Args:
            df_alimentos: DataFrame com alimentos
            alimentos_preselecionados: Dict do A* {tipo: [indices]}
            config_refeicoes: [(nome, pct_calorias), ...]
            metas: Metas nutricionais
            pref_vegetais: Preferências de vegetais
        """
        self.df = df_alimentos
        self.alimentos_pre = alimentos_preselecionados
        self.config_refeicoes = config_refeicoes
        self.metas = metas
        self.pref_veg = pref_vegetais
        
        # Histórico
        self.historico_fitness = []
        self.historico_melhor = []
        self.melhor_cardapio = None
    
    def criar_cardapio_aleatorio(self) -> CardapioCompleto:
        """Cria um cardápio aleatório."""
        refeicoes = {}
        
        for nome_ref, pct_cal in self.config_refeicoes:
            calorias_alvo = (self.metas['meta_calorias'] * pct_cal) / 100
            alimentos_ref = self._gerar_refeicao_aleatoria(calorias_alvo, nome_ref)
            refeicoes[nome_ref] = alimentos_ref
        
        return CardapioCompleto(refeicoes)
    
    def _gerar_refeicao_aleatoria(self, calorias_alvo: float, nome_ref: str) -> List[Dict]:
        """
        Gera uma refeição aleatória tentando atingir as calorias.
        MELHORADO: Agora usa limites dinâmicos que escalam com as calorias.
        """
        alimentos_ref = []
        calorias_atual = 0
        
        # Separa tipos disponíveis
        tipos_disponiveis = list(self.alimentos_pre.keys())
        tipos_principais = [t for t in tipos_disponiveis if t in ['proteina', 'carboidrato']]
        tipos_complementares = [t for t in tipos_disponiveis if t in ['vegetal', 'fruta']]
        
        # Sempre inclui proteína e carboidrato em refeições principais
        if 'lanche' not in nome_ref.lower():
            # REFEIÇÃO PRINCIPAL (Almoço/Jantar)
            
            # 1. PROTEÍNA (contribui ~40-50% das calorias)
            if 'proteina' in self.alimentos_pre and self.alimentos_pre['proteina']:
                idx = random.choice(self.alimentos_pre['proteina'])
                
                # Calcula limites dinâmicos
                limites = calcular_limites_dinamicos('proteina', calorias_alvo)
                gramas = random.randint(int(limites['min']), int(limites['max']))
                
                alimentos_ref.append(self._escalar_alimento(self.df.loc[idx], gramas, calorias_alvo))
                calorias_atual += alimentos_ref[-1]['calorias']
            
            # 2. CARBOIDRATO (contribui ~30-40% das calorias)
            if 'carboidrato' in self.alimentos_pre and self.alimentos_pre['carboidrato']:
                idx = random.choice(self.alimentos_pre['carboidrato'])
                calorias_restantes = calorias_alvo - calorias_atual
                alimento_base = self.df.loc[idx]
                
                # Calcula limites dinâmicos
                limites = calcular_limites_dinamicos('carboidrato', calorias_alvo)
                
                if alimento_base['calorias'] > 0:
                    gramas_calculada = (calorias_restantes * 0.6 / alimento_base['calorias']) * 100
                    gramas = max(limites['min'], min(limites['max'], gramas_calculada))
                else:
                    gramas = limites['ideal']
                
                alimentos_ref.append(self._escalar_alimento(alimento_base, gramas, calorias_alvo))
                calorias_atual += alimentos_ref[-1]['calorias']
            
            # 3. VEGETAL (sempre porção padrão - não escala)
            if self.pref_veg['max_vegetais'] > 0 and tipos_complementares:
                tipo_escolhido = random.choice(tipos_complementares)
                if tipo_escolhido in self.alimentos_pre and self.alimentos_pre[tipo_escolhido]:
                    idx = random.choice(self.alimentos_pre[tipo_escolhido])
                    limites = calcular_limites_dinamicos(tipo_escolhido, calorias_alvo)
                    gramas = limites['ideal']
                    alimentos_ref.append(self._escalar_alimento(self.df.loc[idx], gramas, calorias_alvo))
            
            # 4. Segundo vegetal/fruta se configurado
            if self.pref_veg['max_vegetais'] > 1 and random.random() < 0.5:
                if tipos_complementares:
                    tipo_escolhido = random.choice(tipos_complementares)
                    if tipo_escolhido in self.alimentos_pre and self.alimentos_pre[tipo_escolhido]:
                        idx = random.choice(self.alimentos_pre[tipo_escolhido])
                        limites = calcular_limites_dinamicos(tipo_escolhido, calorias_alvo)
                        gramas = limites['ideal']
                        alimentos_ref.append(self._escalar_alimento(self.df.loc[idx], gramas, calorias_alvo))
        
        else:
            # LANCHE (mais simples, 1-2 itens)
            num_itens = random.randint(1, 2)
            cal_por_item = calorias_alvo / num_itens
            
            tipos_possiveis = tipos_principais.copy()
            if self.pref_veg['max_vegetais'] > 0:
                tipos_possiveis.extend(tipos_complementares)
            
            for _ in range(num_itens):
                if not tipos_possiveis:
                    break
                
                tipo = random.choice(tipos_possiveis)
                if tipo not in self.alimentos_pre or not self.alimentos_pre[tipo]:
                    continue
                
                idx = random.choice(self.alimentos_pre[tipo])
                alimento_base = self.df.loc[idx]
                
                # Calcula limites dinâmicos para lanches também
                limites = calcular_limites_dinamicos(tipo, calorias_alvo)
                
                if tipo in ['vegetal', 'fruta']:
                    gramas = limites['ideal']
                else:
                    if alimento_base['calorias'] > 0:
                        gramas_calculada = (cal_por_item / alimento_base['calorias']) * 100
                        gramas = max(limites['min'], min(limites['max'], gramas_calculada))
                    else:
                        gramas = limites['ideal']
                
                alimentos_ref.append(self._escalar_alimento(alimento_base, gramas, calorias_alvo))
        
        return alimentos_ref
    
    def _escalar_alimento(self, alimento: pd.Series, gramas: float, calorias_alvo_refeicao: float = 600) -> Dict:
        """
        Escala nutrientes proporcionalmente.
        MELHORADO: Usa limites dinâmicos baseados nas calorias-alvo.
        
        Args:
            alimento: Série do alimento
            gramas: Gramatura desejada
            calorias_alvo_refeicao: Calorias-alvo da refeição (para calcular limites)
        """
        tipo_alimento = alimento['tipo']
        
        # Calcula limites dinâmicos
        limites = calcular_limites_dinamicos(tipo_alimento, calorias_alvo_refeicao)
        
        # Valida gramatura nos limites calculados
        gramas = max(limites['min'], min(limites['max'], gramas))
        
        fator = gramas / 100  # Valores são por 100g
        
        return {
            'idx': alimento.name,
            'nome': alimento['nome'],
            'gramas': round(gramas, 1),
            'calorias': alimento['calorias'] * fator,
            'proteinas': alimento['proteinas'] * fator,
            'carboidratos': alimento['carboidratos'] * fator,
            'gorduras': alimento['gorduras'] * fator,
            'fibras': alimento['fibras'] * fator,
            'sodio': alimento['sodio'] * fator,
            'custo': alimento['custo'] * fator,
            'nota_saudavel_fuzzy': alimento['nota_saudavel_fuzzy'],
            'nota_preferencia_rna': alimento['nota_preferencia_rna']
        }
    
    def calcular_fitness(self, cardapio: CardapioCompleto) -> float:
        """
        Calcula fitness multi-objetivo.
        """
        totais = cardapio.calcular_totais()
        
        # 1. Calorias (20%)
        desvio_cal = abs(totais['calorias'] - self.metas['meta_calorias'])
        fitness_cal = max(0, 1 - (desvio_cal / self.metas['meta_calorias']))
        
        # 2. Proteínas (20%)
        desvio_prot = abs(totais['proteinas'] - self.metas['gramas_prot'])
        fitness_prot = max(0, 1 - (desvio_prot / self.metas['gramas_prot']))
        
        # 3. Carboidratos (20%)
        desvio_carbo = abs(totais['carboidratos'] - self.metas['gramas_carbo'])
        fitness_carbo = max(0, 1 - (desvio_carbo / self.metas['gramas_carbo']))
        
        # 4. Gorduras (15%)
        desvio_gord = abs(totais['gorduras'] - self.metas['gramas_gord'])
        fitness_gord = max(0, 1 - (desvio_gord / self.metas['gramas_gord']))
        
        # 5. Saúde (10%)
        fitness_saude = totais['saude_media'] / 10
        
        # 6. Preferência (10%)
        fitness_pref = totais['preferencia_media']
        
        # 7. Custo (5%)
        if totais['custo'] <= self.metas['orcamento']:
            fitness_custo = 1.0 - (totais['custo'] / self.metas['orcamento']) * 0.3
        else:
            fitness_custo = -0.5
        
        # Fitness total
        fitness = (
            0.20 * fitness_cal +
            0.20 * fitness_prot +
            0.20 * fitness_carbo +
            0.15 * fitness_gord +
            0.10 * fitness_saude +
            0.10 * fitness_pref +
            0.05 * fitness_custo
        )
        
        cardapio.fitness = fitness
        cardapio.metricas = {
            'fitness_cal': fitness_cal,
            'fitness_prot': fitness_prot,
            'fitness_carbo': fitness_carbo,
            'fitness_gord': fitness_gord,
            'fitness_saude': fitness_saude,
            'fitness_pref': fitness_pref,
            'fitness_custo': fitness_custo,
            **totais
        }
        
        return fitness
    
    def crossover(self, pai1: CardapioCompleto, pai2: CardapioCompleto) -> Tuple[CardapioCompleto, CardapioCompleto]:
        """Crossover: troca refeições entre pais."""
        ponto = random.randint(1, len(self.config_refeicoes) - 1)
        
        refeicoes_filho1 = {}
        refeicoes_filho2 = {}
        
        for i, (nome_ref, _) in enumerate(self.config_refeicoes):
            if i < ponto:
                refeicoes_filho1[nome_ref] = pai1.refeicoes[nome_ref].copy()
                refeicoes_filho2[nome_ref] = pai2.refeicoes[nome_ref].copy()
            else:
                refeicoes_filho1[nome_ref] = pai2.refeicoes[nome_ref].copy()
                refeicoes_filho2[nome_ref] = pai1.refeicoes[nome_ref].copy()
        
        return CardapioCompleto(refeicoes_filho1), CardapioCompleto(refeicoes_filho2)
    
    def mutacao(self, cardapio: CardapioCompleto, taxa: float = 0.2):
        """
        Mutação: altera alimentos ou quantidades.
        MELHORADO: Usa limites dinâmicos por refeição.
        """
        for nome_ref in cardapio.refeicoes:
            if random.random() < taxa:
                # Calcula calorias-alvo desta refeição
                pct_refeicao = next((pct for nome, pct in self.config_refeicoes if nome == nome_ref), 20)
                calorias_alvo_ref = (self.metas['meta_calorias'] * pct_refeicao) / 100
                
                # Escolhe tipo de mutação
                if random.random() < 0.5:
                    # Troca um alimento
                    if cardapio.refeicoes[nome_ref]:
                        idx_mut = random.randrange(len(cardapio.refeicoes[nome_ref]))
                        alimento_atual = cardapio.refeicoes[nome_ref][idx_mut]
                        
                        tipo_alimento = self.df.loc[alimento_atual['idx']]['tipo']
                        if tipo_alimento in self.alimentos_pre and self.alimentos_pre[tipo_alimento]:
                            novo_idx = random.choice(self.alimentos_pre[tipo_alimento])
                            novo_alimento = self.df.loc[novo_idx]
                            gramas = alimento_atual['gramas']
                            
                            cardapio.refeicoes[nome_ref][idx_mut] = self._escalar_alimento(
                                novo_alimento, gramas, calorias_alvo_ref
                            )
                else:
                    # Ajusta gramatura RESPEITANDO LIMITES DINÂMICOS
                    if cardapio.refeicoes[nome_ref]:
                        idx_mut = random.randrange(len(cardapio.refeicoes[nome_ref]))
                        alimento = cardapio.refeicoes[nome_ref][idx_mut]
                        
                        tipo_alimento = self.df.loc[alimento['idx']]['tipo']
                        limites = calcular_limites_dinamicos(tipo_alimento, calorias_alvo_ref)
                        
                        # Varia ±20% mantendo nos limites
                        fator = random.uniform(0.8, 1.2)
                        nova_gramas = alimento['gramas'] * fator
                        nova_gramas = max(limites['min'], min(limites['max'], nova_gramas))
                        
                        alimento_base = self.df.loc[alimento['idx']]
                        cardapio.refeicoes[nome_ref][idx_mut] = self._escalar_alimento(
                            alimento_base, nova_gramas, calorias_alvo_ref
                        )
    
    def evoluir(self, tamanho_pop: int = 150, num_ger: int = 100) -> CardapioCompleto:
        """Executa o AG."""
        print("🧬 Inicializando Algoritmo Genético...\n")
        
        # População inicial
        populacao = [self.criar_cardapio_aleatorio() for _ in range(tamanho_pop)]
        
        for ind in populacao:
            self.calcular_fitness(ind)
        
        # Evolução
        for gen in range(num_ger):
            populacao.sort(key=lambda x: x.fitness, reverse=True)
            
            melhor = populacao[0]
            media = np.mean([ind.fitness for ind in populacao])
            
            self.historico_melhor.append(melhor.fitness)
            self.historico_fitness.append(media)
            
            if gen % 20 == 0 or gen == num_ger - 1:
                print(f"Geração {gen:3d} | Fitness: {melhor.fitness:.4f} | "
                      f"Calorias: {melhor.metricas['calorias']:.0f} | "
                      f"Custo: R$ {melhor.metricas['custo']:.2f}")
            
            # Nova geração
            nova_pop = populacao[:10]  # Elitismo
            
            while len(nova_pop) < tamanho_pop:
                # Torneio
                pai1 = max(random.sample(populacao[:50], 3), key=lambda x: x.fitness)
                pai2 = max(random.sample(populacao[:50], 3), key=lambda x: x.fitness)
                
                # Crossover
                if random.random() < 0.8:
                    filho1, filho2 = self.crossover(pai1, pai2)
                else:
                    filho1 = CardapioCompleto({k: v.copy() for k, v in pai1.refeicoes.items()})
                    filho2 = CardapioCompleto({k: v.copy() for k, v in pai2.refeicoes.items()})
                
                # Mutação
                self.mutacao(filho1, 0.2)
                self.mutacao(filho2, 0.2)
                
                self.calcular_fitness(filho1)
                self.calcular_fitness(filho2)
                
                nova_pop.extend([filho1, filho2])
            
            populacao = nova_pop[:tamanho_pop]
        
        populacao.sort(key=lambda x: x.fitness, reverse=True)
        self.melhor_cardapio = populacao[0]
        
        print(f"\n✅ Evolução concluída! Melhor Fitness: {self.melhor_cardapio.fitness:.4f}\n")
        
        return self.melhor_cardapio


def otimizar_cardapio_v2(df_alimentos: pd.DataFrame,
                         alimentos_preselecionados: Dict[str, List[int]],
                         config_refeicoes: List[Tuple[str, float]],
                         metas: Dict,
                         pref_vegetais: Dict,
                         tamanho_populacao: int = 150,
                         num_geracoes: int = 100) -> CardapioCompleto:
    """
    Função principal do AG V2.
    """
    ag = AlgoritmoGeneticoV2(
        df_alimentos,
        alimentos_preselecionados,
        config_refeicoes,
        metas,
        pref_vegetais
    )
    
    return ag.evoluir(tamanho_populacao, num_geracoes)
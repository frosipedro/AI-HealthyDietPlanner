"""
Algoritmo Genético - Refeições Compostas com Controle de Macros e Regras Culinárias do Mundo Real
"""

import numpy as np 
import pandas as pd 
import random
from typing import List, Dict, Tuple
from data.regras_culinarias import (
    obter_categoria_culinaria,
    obter_regras_refeicao,
    obter_limites_gramatura,
    alimento_permitido_na_refeicao,
    validar_composicao_refeicao,
    GRAMATURA_REALISTA
)


# ============================================================================
# CLASSES PRINCIPAIS
# ============================================================================
class CardapioCompleto:
    """Representa um cardápio completo com várias refeições."""
        
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
        totais: Dict = {
            'calorias': 0.0,
            'proteinas': 0.0,
            'carboidratos': 0.0,
            'gorduras': 0.0,
            'fibras': 0.0,
            'sodio': 0.0,
            'custo': 0.0,
            'saude_media': 0.0,
            'preferencia_media': 0.0
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


class AlgoritmoGenetico:
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
        Gera uma refeição aleatória seguindo REGRAS CULINÁRIAS DO MUNDO REAL.
        
        Args:
            calorias_alvo: Meta de calorias para esta refeição
            nome_ref: Nome da refeição (ex: "Café da Manhã", "Almoço")
        
        Returns:
            Lista de alimentos escalados
        """
        alimentos_ref = []
        calorias_atual = 0
        
        # Obtém as regras para esta refeição
        regras = obter_regras_refeicao(nome_ref)
        estrutura = regras.get('estrutura', {})
        
        # Se tem estrutura complexa (ex: almoço com refeição_completa ou refeicao_pronta)
        if 'refeicao_completa' in estrutura:
            # 80% das vezes faz refeição completa, 20% prato pronto
            if random.random() < 0.8:
                est = estrutura['refeicao_completa']
            else:
                est = estrutura.get('refeicao_pronta', estrutura['refeicao_completa'])
        else:
            est = estrutura
        
        # Coleta alimentos OBRIGATÓRIOS
        categorias_obrigatorias = est.get('obrigatorio', [])
        categorias_opcionais = est.get('opcional', [])
        
        # NOVO: Aumenta número de opcionais se há poucas refeições no dia
        num_total_refeicoes = len(self.config_refeicoes)
        if num_total_refeicoes <= 4:
            # Com poucas refeições, precisa de mais componentes
            num_opcionais = random.randint(1, min(4, len(categorias_opcionais)))
        else:
            # Padrão: 0-2 opcionais
            num_opcionais = random.randint(0, min(2, len(categorias_opcionais)))
        
        # Distribui calorias entre componentes
        num_obrigatorios = len(categorias_obrigatorias)
        total_componentes = num_obrigatorios + num_opcionais
        
        if total_componentes == 0:
            # Fallback: cria refeição genérica
            return self._gerar_refeicao_generica(calorias_alvo, nome_ref, regras)
        
        # Distribui calorias de forma inteligente
        calorias_por_componente = calorias_alvo / total_componentes
        
        # Adiciona componentes OBRIGATÓRIOS
        for categoria in categorias_obrigatorias:
            alimento = self._escolher_alimento_por_categoria(
                categoria, 
                calorias_por_componente, 
                nome_ref
            )
            if alimento:
                alimentos_ref.append(alimento)
                calorias_atual += alimento['calorias']
        
        # Adiciona componentes OPCIONAIS
        categorias_op_escolhidas = random.sample(categorias_opcionais, num_opcionais)
        for categoria in categorias_op_escolhidas:
            alimento = self._escolher_alimento_por_categoria(
                categoria,
                calorias_por_componente,
                nome_ref
            )
            if alimento:
                alimentos_ref.append(alimento)
                calorias_atual += alimento['calorias']
        
        # Ajuste fino: se faltam calorias, aumenta porções proporcionalmente
        if calorias_atual > 0 and abs(calorias_atual - calorias_alvo) > 50:
            fator_ajuste = calorias_alvo / calorias_atual
            
            # NOVO: Permite ajuste maior se há poucas refeições
            num_total_refeicoes = len(self.config_refeicoes)
            if num_total_refeicoes <= 4:
                fator_ajuste = max(0.5, min(2.0, fator_ajuste))  # Ajuste mais agressivo
            else:
                fator_ajuste = max(0.7, min(1.3, fator_ajuste))  # Ajuste padrão
            
            for i, alimento in enumerate(alimentos_ref):
                alimento_base = self.df.loc[alimento['idx']]
                nova_gramas = alimento['gramas'] * fator_ajuste
                
                # Respeita limites culinários (mas aumentados se necessário)
                limites = obter_limites_gramatura(alimento['nome'])
                
                # NOVO: Aumenta limite máximo se refeição é grande
                calorias_refeicao_media = self.metas['meta_calorias'] / num_total_refeicoes
                if calorias_refeicao_media > 800:
                    limites_max_ajustado = int(limites['max'] * 1.5)
                else:
                    limites_max_ajustado = limites['max']
                
                nova_gramas = max(limites['min'], min(limites_max_ajustado, nova_gramas))
                
                alimentos_ref[i] = self._escalar_alimento(alimento_base, nova_gramas, calorias_alvo)
        
        return alimentos_ref
    
    def _escolher_alimento_por_categoria(self, categoria_culinaria: str, 
                                         calorias_alvo: float, 
                                         nome_ref: str) -> Dict | None:
        """
        Escolhe um alimento que pertença à categoria culinária especificada.
        
        Args:
            categoria_culinaria: Ex: 'prato_principal', 'acompanhamento_base', 'lanche_leve'
            calorias_alvo: Calorias que este alimento deve contribuir
            nome_ref: Nome da refeição
        
        Returns:
            Alimento escalado ou None se não encontrar
        """
        # Filtra alimentos por categoria culinária
        candidatos = []
        
        for tipo_nutri, indices in self.alimentos_pre.items():
            for idx in indices:
                alimento_nome = str(self.df.loc[idx, 'nome'])
                cat_culinaria = obter_categoria_culinaria(alimento_nome)
                
                if cat_culinaria == categoria_culinaria:
                    # Verifica se é permitido nesta refeição
                    if alimento_permitido_na_refeicao(alimento_nome, nome_ref):
                        candidatos.append(idx)
        
        if not candidatos:
            return None
        
        # Escolhe aleatoriamente
        idx_escolhido = random.choice(candidatos)
        alimento_base = self.df.loc[idx_escolhido]
        
        # Calcula gramatura baseada nas calorias-alvo e limites culinários
        limites = obter_limites_gramatura(str(alimento_base['nome']))
        
            try:
                calorias_value = float(alimento_base['calorias'])  # type: ignore
            except (ValueError, TypeError):
                calorias_value = 0.0
            
            if calorias_value > 0:
                # Calcula gramas necessárias para atingir calorias
                gramas_calculada = (calorias_alvo / calorias_value) * 100
                
                # NOVO: Aumenta limite se há poucas refeições
                num_total_refeicoes = len(self.config_refeicoes)
                if num_total_refeicoes <= 4:
                    limites_max_ajustado = int(limites['max'] * 1.5)
                else:
                    limites_max_ajustado = limites['max']
                
                gramas = max(limites['min'], min(limites_max_ajustado, gramas_calculada))
            else:
                gramas = limites['ideal']
            
            return self._escalar_alimento(alimento_base, gramas, calorias_alvo)  # type: ignore    def _gerar_refeicao_generica(self, calorias_alvo: float, nome_ref: str, regras: dict) -> List[Dict]:
        """Fallback: gera refeição genérica quando não há estrutura definida."""
        alimentos_ref = []
        
        # Pega tipos permitidos
        tipos_permitidos = []
        for tipo in self.alimentos_pre.keys():
            # Verifica se algum alimento deste tipo é permitido
            for idx in self.alimentos_pre[tipo]:
                if alimento_permitido_na_refeicao(str(self.df.loc[idx, 'nome']), nome_ref):
                    tipos_permitidos.append(tipo)
                    break
        
        if not tipos_permitidos:
            tipos_permitidos = list(self.alimentos_pre.keys())
        
        # NOVO: Ajusta número de itens baseado no total de refeições
        num_total_refeicoes = len(self.config_refeicoes)
        if num_total_refeicoes <= 4:
            num_itens = random.randint(2, 4)  # Mais itens com poucas refeições
        else:
            num_itens = random.randint(1, 3)  # Padrão
        
        cal_por_item = calorias_alvo / num_itens
        
        for _ in range(num_itens):
            if not tipos_permitidos:
                break
            
            tipo = random.choice(tipos_permitidos)
            if tipo not in self.alimentos_pre or not self.alimentos_pre[tipo]:
                continue
            
            # Filtra por regras da refeição
            candidatos = [
                idx for idx in self.alimentos_pre[tipo]
                if alimento_permitido_na_refeicao(str(self.df.loc[idx, 'nome']), nome_ref)
            ]
            
            if not candidatos:
                continue
            
            idx = random.choice(candidatos)
            alimento_base = self.df.loc[idx]
            
            # Usa limites culinários
            limites = obter_limites_gramatura(str(alimento_base['nome']))
            
            try:
                calorias_value = float(alimento_base['calorias'])  # type: ignore
            except (ValueError, TypeError):
                calorias_value = 0.0
            
            if calorias_value > 0:
                gramas_calculada = (cal_por_item / calorias_value) * 100
                
                # NOVO: Aumenta limite se há poucas refeições
                num_total_refeicoes = len(self.config_refeicoes)
                if num_total_refeicoes <= 4:
                    limites_max_ajustado = int(limites['max'] * 1.5)
                else:
                    limites_max_ajustado = limites['max']
                
                gramas = max(limites['min'], min(limites_max_ajustado, gramas_calculada))
            else:
                gramas = limites['ideal']
            
            alimentos_ref.append(self._escalar_alimento(alimento_base, gramas, calorias_alvo))  # type: ignore
        
        return alimentos_ref
    
    def _escalar_alimento(self, alimento: pd.Series, gramas: float, calorias_alvo_refeicao: float = 600) -> Dict:
        """
        Escala nutrientes proporcionalmente.
        VERSÃO 3: Usa limites culinários realistas do mundo real.
        
        Args:
            alimento: Série do alimento
            gramas: Gramatura desejada
            calorias_alvo_refeicao: Calorias-alvo da refeição (informativo)
        """
        # Usa limites culinários (não mais nutricionais)
        limites = obter_limites_gramatura(alimento['nome'])
        
        # Valida gramatura nos limites culinários
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
        NOVO: Inclui penalização por refeições que não fazem sentido culinariamente.
        NOVO: Inclui distribuição proporcional de macros por refeição.
        """
        totais = cardapio.calcular_totais()
        
        # 1. Calorias (18%)
        desvio_cal = abs(totais['calorias'] - self.metas['meta_calorias'])
        fitness_cal = max(0, 1 - (desvio_cal / self.metas['meta_calorias']))
        
        # 2. Proteínas (18%)
        desvio_prot = abs(totais['proteinas'] - self.metas['gramas_prot'])
        fitness_prot = max(0, 1 - (desvio_prot / self.metas['gramas_prot']))
        
        # 3. Carboidratos (18%)
        desvio_carbo = abs(totais['carboidratos'] - self.metas['gramas_carbo'])
        fitness_carbo = max(0, 1 - (desvio_carbo / self.metas['gramas_carbo']))
        
        # 4. Gorduras (13%)
        desvio_gord = abs(totais['gorduras'] - self.metas['gramas_gord'])
        fitness_gord = max(0, 1 - (desvio_gord / self.metas['gramas_gord']))
        
        # 5. Saúde (8%)
        fitness_saude = totais['saude_media'] / 10
        
        # 6. Preferência (8%)
        fitness_pref = totais['preferencia_media']
        
        # 7. Custo (5%)
        if totais['custo'] <= self.metas['orcamento']:
            fitness_custo = 1.0 - (totais['custo'] / self.metas['orcamento']) * 0.3
        else:
            fitness_custo = -0.5
        
        # 8. VALIDAÇÃO CULINÁRIA (12% do fitness)
        # Este é o componente que vai ensinar o algoritmo a "pensar como humano"
        fitness_culinario = 0.0
        num_refeicoes = len(cardapio.refeicoes)
        
        for nome_ref, alimentos_ref in cardapio.refeicoes.items():
            # Prepara dados para validação
            alimentos_info = [
                {'nome': alimento['nome'], 'gramas': alimento['gramas']}
                for alimento in alimentos_ref
            ]
            
            # Valida composição
            validacao = validar_composicao_refeicao(alimentos_info, nome_ref)
            fitness_culinario += validacao['score']
        
        fitness_culinario /= num_refeicoes  # Média entre refeições
        
        # 9. NOVO: DISTRIBUIÇÃO PROPORCIONAL DE MACROS POR REFEIÇÃO (15% do fitness)
        # Garante que cada refeição tenha macros proporcionais à sua % de calorias
        fitness_distribuicao = 0.0
        
        for nome_ref, alimentos_ref in cardapio.refeicoes.items():
            # Encontra a porcentagem de calorias desta refeição
            pct_refeicao = None
            for nome_config, pct in self.config_refeicoes:
                if nome_config == nome_ref:
                    pct_refeicao = pct / 100.0
                    break
            
            if pct_refeicao is None:
                continue
            
            # Calcula macros esperados para esta refeição (proporcionalmente)
            prot_esperado = self.metas['gramas_prot'] * pct_refeicao
            carbo_esperado = self.metas['gramas_carbo'] * pct_refeicao
            gord_esperado = self.metas['gramas_gord'] * pct_refeicao
            
            # Calcula macros reais desta refeição
            prot_real = sum(a['proteinas'] for a in alimentos_ref)
            carbo_real = sum(a['carboidratos'] for a in alimentos_ref)
            gord_real = sum(a['gorduras'] for a in alimentos_ref)
            
            # Calcula desvios (com tolerância de 30% para flexibilidade)
            desvio_prot_ref = abs(prot_real - prot_esperado) / max(prot_esperado, 1)
            desvio_carbo_ref = abs(carbo_real - carbo_esperado) / max(carbo_esperado, 1)
            desvio_gord_ref = abs(gord_real - gord_esperado) / max(gord_esperado, 1)
            
            # Fitness desta refeição (penaliza desvios grandes)
            fitness_ref = (
                max(0, 1 - desvio_prot_ref) +
                max(0, 1 - desvio_carbo_ref) +
                max(0, 1 - desvio_gord_ref)
            ) / 3.0
            
            fitness_distribuicao += fitness_ref
        
        fitness_distribuicao /= num_refeicoes  # Média entre refeições
        
        # Fitness total
        fitness = (
            0.14 * fitness_cal +         # Reduzido de 0.16
            0.14 * fitness_prot +        # Reduzido de 0.16
            0.14 * fitness_carbo +       # Reduzido de 0.16
            0.10 * fitness_gord +        # Reduzido de 0.12
            0.08 * fitness_saude +
            0.08 * fitness_pref +
            0.04 * fitness_custo +
            0.13 * fitness_culinario +   # Reduzido de 0.20
            0.15 * fitness_distribuicao  # NOVO: garante distribuição proporcional
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
            'fitness_culinario': fitness_culinario,
            'fitness_distribuicao': fitness_distribuicao,  # NOVO!
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
        VERSÃO 3: Usa limites culinários realistas.
        """
        for nome_ref in cardapio.refeicoes:
            if random.random() < taxa:
                # Calcula calorias-alvo desta refeição
                pct_refeicao = next((pct for nome, pct in self.config_refeicoes if nome == nome_ref), 20)
                calorias_alvo_ref = (self.metas['meta_calorias'] * pct_refeicao) / 100
                
                # Escolhe tipo de mutação
                if random.random() < 0.5:
                    # Troca um alimento MANTENDO A CATEGORIA CULINÁRIA
                    if cardapio.refeicoes[nome_ref]:
                        idx_mut = random.randrange(len(cardapio.refeicoes[nome_ref]))
                        alimento_atual = cardapio.refeicoes[nome_ref][idx_mut]
                        
                        # Obtém categoria culinária do alimento atual
                        nome_atual = alimento_atual['nome']
                        cat_culinaria = obter_categoria_culinaria(nome_atual)
                        
                        # Busca substituto da mesma categoria
                        candidatos = []
                        for tipo_nutri, indices in self.alimentos_pre.items():
                            for idx in indices:
                                alimento_nome = str(self.df.loc[idx, 'nome'])
                                if obter_categoria_culinaria(alimento_nome) == cat_culinaria:
                                    if alimento_permitido_na_refeicao(alimento_nome, nome_ref):
                                        candidatos.append(idx)
                        
                        if candidatos:
                            novo_idx = random.choice(candidatos)
                            novo_alimento = self.df.loc[novo_idx]
                            gramas = alimento_atual['gramas']
                            
                            cardapio.refeicoes[nome_ref][idx_mut] = self._escalar_alimento(
                                novo_alimento, gramas, calorias_alvo_ref
                            )
                else:
                    # Ajusta gramatura RESPEITANDO LIMITES CULINÁRIOS
                    if cardapio.refeicoes[nome_ref]:
                        idx_mut = random.randrange(len(cardapio.refeicoes[nome_ref]))
                        alimento = cardapio.refeicoes[nome_ref][idx_mut]
                        
                        # Usa limites culinários
                        limites = obter_limites_gramatura(str(alimento['nome']))
                        
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
                      f"Culinário: {melhor.metricas['fitness_culinario']:.2f} | "
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


def otimizar_cardapio(df_alimentos: pd.DataFrame,
                         alimentos_preselecionados: Dict[str, List[int]],
                         config_refeicoes: List[Tuple[str, float]],
                         metas: Dict,
                         pref_vegetais: Dict,
                         tamanho_populacao: int = 150,
                         num_geracoes: int = 100) -> CardapioCompleto:
    """
    Função principal.
    """
    ag = AlgoritmoGenetico(
        df_alimentos,
        alimentos_preselecionados,
        config_refeicoes,
        metas,
        pref_vegetais
    )
    
    return ag.evoluir(tamanho_populacao, num_geracoes)
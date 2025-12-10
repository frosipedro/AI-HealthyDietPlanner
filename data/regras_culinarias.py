"""
Regras Culinárias - Contexto do Mundo Real para Composição de Refeições

Este módulo define:
1. Categorias culinárias dos alimentos
2. Regras de combinação por tipo de refeição
3. Restrições de gramatura realistas
"""

import unicodedata


def normalizar_texto(texto: str) -> str:
    """
    Normaliza texto removendo acentos e convertendo para minúsculas.
    Ex: "Café da Manhã" -> "cafe da manha"
    """
    # Remove acentos
    texto_sem_acento = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    # Converte para minúsculas e remove espaços extras
    return texto_sem_acento.lower().strip()

# ============================================================================
# CATEGORIAS CULINÁRIAS (além das categorias nutricionais)
# ============================================================================

CATEGORIAS_CULINARIAS = {
    # PROTEÍNAS
    'Peito de Frango': 'prato_principal',
    'Coxa de Frango': 'prato_principal',
    'Asa de Frango': 'prato_principal',
    'Carne Moída Patinho': 'prato_principal',
    'Carne Moída Acém': 'prato_principal',
    'Bife de Patinho': 'prato_principal',
    'Picanha': 'prato_principal',
    'Alcatra': 'prato_principal',
    'Coxão Duro': 'prato_principal',
    'Carne Seca': 'prato_principal',
    'Linguiça Toscana': 'prato_principal',
    'Linguiça de Frango': 'prato_principal',
    'Lombo Suíno': 'prato_principal',
    'Pernil Suíno': 'prato_principal',
    'Bacon': 'frios',  # Geralmente acompanha, não é prato principal
    'Salmão': 'prato_principal',
    'Tilápia': 'prato_principal',
    'Sardinha': 'prato_principal',
    'Atum': 'prato_principal',
    
    # OVOS E LATICÍNIOS
    'Ovo': 'proteina_cafe',
    'Ovo Mexido': 'proteina_cafe',
    'Queijo Minas': 'frios',
    'Queijo Mussarela': 'frios',
    'Queijo Parmesão': 'tempero',
    'Requeijão': 'frios',
    'Leite Integral': 'bebida',
    'Leite Desnatado': 'bebida',
    'Iogurte Natural': 'iogurte',
    'Iogurte Grego': 'iogurte',
    'Manteiga': 'tempero',
    
    # CARBOIDRATOS BASE (acompanhamentos)
    'Arroz Branco': 'acompanhamento_base',
    'Arroz Integral': 'acompanhamento_base',
    'Macarrão': 'acompanhamento_base',
    'Macarrão Instantâneo': 'refeicao_rapida',  # Prato único, não acompanhamento
    'Aveia': 'cafe_da_manha_liquido',  # PRECISA de leite/iogurte!
    'Mingau de Aveia': 'mingau', # Já preparado
    'Farinha de Mandioca': 'ingrediente',  # Não se come puro - precisa virar farofa!
    'Farinha de Trigo': 'ingrediente',  # Não se come puro
    'Cuscuz de Milho': 'cafe_da_manha',
    'Pão Francês': 'cafe_da_manha',
    'Pão Integral': 'cafe_da_manha',
    'Tapioca': 'cafe_da_manha',
    'Pão de Forma': 'cafe_da_manha',
    'Pão de Centeio': 'cafe_da_manha',
    
    # LEGUMINOSAS
    'Feijão Preto': 'leguminosa',
    'Feijão Carioca': 'leguminosa',
    'Lentilha': 'leguminosa',  # Não se come 140g puro!
    'Grão-de-bico': 'leguminosa',
    'Ervilha': 'leguminosa',
    'Soja': 'leguminosa',
    
    # TUBÉRCULOS (podem ser acompanhamento ou prato)
    'Batata Inglesa': 'tuberculo',
    'Batata Doce': 'tuberculo',
    'Mandioca': 'tuberculo',
    'Inhame': 'tuberculo',
    'Cará': 'tuberculo',
    
    # VEGETAIS (sempre guarnição/salada)
    'Brócolis': 'guarnição',
    'Couve Flor': 'guarnição',
    'Cenoura': 'guarnição',
    'Beterraba': 'guarnição',
    'Abobrinha': 'guarnição',
    'Alface': 'salada',
    'Tomate': 'salada',
    'Pepino': 'salada',
    'Repolho': 'salada',
    'Vagem': 'guarnição',
    'Milho Verde': 'guarnição',
    
    # FRUTAS (lanches ou sobremesas)
    'Banana Prata': 'fruta',
    'Banana Nanica': 'fruta',
    'Maçã': 'fruta',
    'Pera': 'fruta',
    'Melancia': 'fruta',
    'Mamão': 'fruta',
    'Laranja': 'fruta',
    'Tangerina': 'fruta',
    'Morango': 'fruta',
    'Abacate': 'fruta',
    'Abacaxi': 'fruta',
    'Uva': 'fruta',
    
    # OLEAGINOSAS (sempre pequenas quantidades)
    'Amendoim': 'oleaginosa',
    'Castanha de Caju': 'oleaginosa',
    'Castanha do Pará': 'oleaginosa',
    'Nozes': 'oleaginosa',
    'Amêndoas': 'oleaginosa',
    
    # GORDURAS (tempero, não prato)
    'Óleo de Soja': 'tempero',
    'Óleo de Canola': 'tempero',
    'Azeite de Oliva': 'tempero',
    'Margarina': 'tempero',
    
    # INDUSTRIALIZADOS E PREPARAÇÕES
    'Arroz Carreteiro': 'refeicao_pronta',
    'Feijoada': 'refeicao_pronta',
    'Pão de Queijo': 'lanche_leve',
    'Coxinha': 'lanche_leve',
    'Pastel de Carne': 'lanche_leve',
    'Mortadela': 'frios',
    'Presunto': 'frios',
    'Peito de Peru': 'frios',
    'Arroz + Feijão': 'refeicao_pronta',
    'Omelete': 'proteina_cafe',
    'Purê de Batata': 'tuberculo',
    'Salada Mista': 'salada',
    'Strogonoff de Frango': 'refeicao_pronta',
    'Frango à Milanesa': 'refeicao_pronta',
}


# ============================================================================
# REGRAS DE COMPOSIÇÃO POR TIPO DE REFEIÇÃO
# ============================================================================

REGRAS_COMPOSICAO = {
    'Café da Manhã': {
        'permitidos': [
            'cafe_da_manha',           # Pães, tapioca, cuscuz, mingau
            'cafe_da_manha_liquido',   # Aveia (PRECISA de líquido)
            'mingau',                  # Mingau pronto
            'fruta',                   # Frutas
            'oleaginosa',              # Castanhas
            'iogurte',                 # Iogurtes
            'frios',                   # Queijos, presunto
            'bebida',                  # Leite
            'tempero',                 # Manteiga
            'proteina_cafe',           # Ovos
        ],
        'proibidos': [
            'acompanhamento_base',     # Sem arroz/feijão/lentilha
            'leguminosa',              # Sem feijão
            'tuberculo',               # Sem batata
            'prato_principal',         # Sem bife/frango
            'refeicao_pronta',         # Sem feijoada/strogonoff
            'ingrediente',             # Sem farinha pura!
            'guarnição',
            'salada',
        ],
        'estrutura': {
            'obrigatorio_um_de': ['cafe_da_manha', 'fruta', 'cafe_da_manha_liquido', 'proteina_cafe', 'iogurte', 'mingau'],
            'opcional': ['frios', 'bebida', 'tempero', 'oleaginosa'],
            'min_itens': 1,
            'max_itens': 4,
        },
        'combinacoes_obrigatorias': {
            # Se tem aveia, DEVE ter leite ou iogurte
            'cafe_da_manha_liquido': ['bebida', 'iogurte'],
            # Se tem pão, DEVE ter algo para passar/rechear (frios, tempero, ovo)
            'cafe_da_manha': ['frios', 'tempero', 'proteina_cafe', 'bebida'],
        }
    },
    
    'Lanche da Manhã': {
        'permitidos': [
            'fruta',
            'oleaginosa',
            'iogurte',
            'lanche_leve',
            'cafe_da_manha',
            'mingau',
            'frios',
            'bebida',
        ],
        'proibidos': [
            'prato_principal',
            'acompanhamento_base',
            'leguminosa',
            'tuberculo',
            'refeicao_pronta',
            'proteina_cafe',
        ],
        'estrutura': {
            'obrigatorio_um_de': ['fruta', 'iogurte', 'oleaginosa', 'lanche_leve', 'cafe_da_manha', 'mingau'],
            'opcional': ['frios', 'bebida'],
            'min_itens': 1,
            'max_itens': 3,
        }
    },
    
    'Almoço': {
        'permitidos': [
            'prato_principal',
            'acompanhamento_base', # Arroz, Macarrão
            'leguminosa',          # Feijão
            'tuberculo',           # Batata
            'frios',               # Queijo (para macarrão)
            'guarnição',
            'salada',
            'refeicao_pronta',
            'tempero',
        ],
        'proibidos': [
            'cafe_da_manha',      # Sem pão/aveia no almoço
            'cafe_da_manha_liquido',
            'fruta',              # Fruta geralmente é sobremesa, mas vamos focar no prato principal
            'oleaginosa',
            'iogurte',
            'proteina_cafe',
            'ingrediente',
        ],
        'estrutura': {
            # Opção 1: Refeição completa tradicional
            'refeicao_completa': {
                'obrigatorio': ['prato_principal'],
                'opcional': ['acompanhamento_base', 'leguminosa', 'tuberculo', 'guarnição', 'salada', 'frios'],
                'min_itens': 2,
                'max_itens': 5,
            },
            # Opção 2: Prato único pronto
            'refeicao_pronta': {
                'obrigatorio': ['refeicao_pronta'],
                'opcional': ['guarnição', 'salada'],
                'min_itens': 1,
                'max_itens': 3,
            }
        }
    },
    
    'Lanche da Tarde': {
        'permitidos': [
            'fruta',
            'oleaginosa',
            'iogurte',
            'lanche_leve',
            'cafe_da_manha',
            'mingau',
            'frios',
            'bebida',
            'proteina_cafe', # Ovos a tarde pode
        ],
        'proibidos': [
            'prato_principal',
            'acompanhamento_base',
            'leguminosa',
            'tuberculo',
            'refeicao_pronta',
        ],
        'estrutura': {
            'obrigatorio_um_de': ['fruta', 'iogurte', 'oleaginosa', 'lanche_leve', 'cafe_da_manha', 'proteina_cafe', 'mingau'],
            'opcional': ['frios', 'bebida'],
            'min_itens': 1,
            'max_itens': 3,
        }
    },
    
    'Jantar': {
        # Mesmas regras do almoço
        'permitidos': [
            'prato_principal',
            'acompanhamento_base',
            'leguminosa',
            'tuberculo',
            'frios',
            'guarnição',
            'salada',
            'refeicao_pronta',
            'tempero',
            'proteina_cafe', # Omelete no jantar é comum
        ],
        'proibidos': [
            'cafe_da_manha',
            'cafe_da_manha_liquido',
            'fruta',
            'oleaginosa',
            'iogurte',
            'ingrediente',
            'mingau',
        ],
        'estrutura': {
            'refeicao_completa': {
                'obrigatorio_um_de': ['prato_principal', 'proteina_cafe'],
                'opcional': ['acompanhamento_base', 'leguminosa', 'tuberculo', 'guarnição', 'salada', 'frios'],
                'min_itens': 2,
                'max_itens': 5,
            },
            'refeicao_pronta': {
                'obrigatorio': ['refeicao_pronta'],
                'opcional': ['guarnição', 'salada'],
                'min_itens': 1,
                'max_itens': 3,
            }
        }
    },
    
    'Ceia': {
        'permitidos': [
            'fruta',
            'oleaginosa',
            'iogurte',
            'lanche_leve',
            'bebida',
            'mingau',
        ],
        'proibidos': [
            'prato_principal',
            'acompanhamento_base',
            'leguminosa',
            'tuberculo',
            'refeicao_pronta',
            'cafe_da_manha',
            'frios',
            'proteina_cafe',
        ],
        'estrutura': {
            'obrigatorio_um_de': ['fruta', 'iogurte', 'bebida', 'lanche_leve', 'mingau'],
            'opcional': ['oleaginosa'],
            'min_itens': 1,
            'max_itens': 2,
        }
    },
}

# Regra padrão para refeições não mapeadas
REGRA_PADRAO = {
    'permitidos': ['lanche_leve', 'prato_principal', 'acompanhamento_base'],
    'proibidos': ['tempero', 'ingrediente'],
    'estrutura': {
        'obrigatorio': [],
        'opcional': ['lanche_leve', 'prato_principal'],
        'min_itens': 1,
        'max_itens': 3,
    }
}


# ============================================================================
# GRAMATURA REALISTA POR CATEGORIA CULINÁRIA
# ============================================================================

GRAMATURA_REALISTA = {
    'prato_principal': {
        'min': 100,
        'max': 200,
        'ideal': 150,
        'descricao': 'Porção proteica principal'
    },
    'proteina_cafe': {
        'min': 50,
        'max': 150,
        'ideal': 100,
        'descricao': 'Ovos ou omelete'
    },
    'acompanhamento_base': {
        'min': 80,
        'max': 150,
        'ideal': 100,
        'descricao': 'Arroz, macarrão'
    },
    'leguminosa': {
        'min': 70,
        'max': 140,
        'ideal': 100,
        'descricao': 'Feijão, lentilha'
    },
    'tuberculo': {
        'min': 80,
        'max': 150,
        'ideal': 100,
        'descricao': 'Batatas, mandioca'
    },
    'acompanhamento': {
        'min': 50,
        'max': 150,
        'ideal': 80,
        'descricao': 'Farofa, complementos'
    },
    'frios': {
        'min': 30,
        'max': 60,
        'ideal': 40,
        'descricao': 'Queijos, presunto'
    },
    'guarnição': {
        'min': 50,
        'max': 120,
        'ideal': 80,
        'descricao': 'Legumes cozidos'
    },
    'salada': {
        'min': 30,
        'max': 100,
        'ideal': 60,
        'descricao': 'Vegetais crus'
    },
    'fruta': {
        'min': 80,
        'max': 200,
        'ideal': 120,
        'descricao': 'Frutas in natura'
    },
    'oleaginosa': {
        'min': 15,
        'max': 40,
        'ideal': 30,
        'descricao': 'Castanhas, nozes'
    },
    'iogurte': {
        'min': 100,
        'max': 200,
        'ideal': 170,
        'descricao': 'Iogurtes'
    },
    'lanche_leve': {
        'min': 30,
        'max': 150,
        'ideal': 80,
        'descricao': 'Pão de queijo, snacks'
    },
    'cafe_da_manha': {
        'min': 40,
        'max': 100,
        'ideal': 60,
        'descricao': 'Pães, tapioca, cuscuz'
    },
    'cafe_da_manha_liquido': {
        'min': 30,
        'max': 80,
        'ideal': 50,
        'descricao': 'Aveia (precisa de leite/iogurte)'
    },
    'mingau': {
        'min': 150,
        'max': 300,
        'ideal': 200,
        'descricao': 'Mingau de aveia ou similar'
    },
    'refeicao_pronta': {
        'min': 150,
        'max': 350,
        'ideal': 250,
        'descricao': 'Pratos prontos completos'
    },
    'refeicao_rapida': {
        'min': 60,
        'max': 100,
        'ideal': 75,
        'descricao': 'Miojo, sopas instantâneas'
    },
    'bebida': {
        'min': 200,
        'max': 300,
        'ideal': 250,
        'descricao': 'Leite, sucos (ml = g)'
    },
    'tempero': {
        'min': 5,
        'max': 20,
        'ideal': 10,
        'descricao': 'Manteiga, óleo, queijo ralado'
    },
    'ingrediente': {
        'min': 0,
        'max': 0,
        'ideal': 0,
        'descricao': 'Não deve ser usado isoladamente'
    },
}


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def obter_categoria_culinaria(nome_alimento: str) -> str:
    """Retorna a categoria culinária do alimento."""
    return CATEGORIAS_CULINARIAS.get(nome_alimento, 'lanche_leve')


def obter_regras_refeicao(nome_refeicao: str) -> dict:
    """
    Retorna as regras de composição para uma refeição.
    Busca por nome exato ou por palavras-chave (normalizado, sem acentos).
    """
    # Busca exata (case-sensitive, com acentos)
    if nome_refeicao in REGRAS_COMPOSICAO:
        return REGRAS_COMPOSICAO[nome_refeicao]
    
    # Normaliza o nome para busca case-insensitive e sem acentos
    nome_norm = normalizar_texto(nome_refeicao)
    
    # Busca por palavras-chave (agora normalizado)
    if 'cafe' in nome_norm or 'breakfast' in nome_norm:
        return REGRAS_COMPOSICAO['Café da Manhã']
    elif 'almoco' in nome_norm or 'lunch' in nome_norm:
        return REGRAS_COMPOSICAO['Almoço']
    elif 'jantar' in nome_norm or 'janta' in nome_norm or 'dinner' in nome_norm:
        return REGRAS_COMPOSICAO['Jantar']
    elif 'lanche' in nome_norm or 'snack' in nome_norm:
        if 'manha' in nome_norm or 'morning' in nome_norm:
            return REGRAS_COMPOSICAO['Lanche da Manhã']
        else:
            return REGRAS_COMPOSICAO['Lanche da Tarde']
    elif 'ceia' in nome_norm or 'supper' in nome_norm:
        return REGRAS_COMPOSICAO['Ceia']
    
    # Padrão
    return REGRA_PADRAO


def obter_limites_gramatura(nome_alimento: str) -> dict:
    """Retorna os limites de gramatura realistas para o alimento."""
    categoria = obter_categoria_culinaria(nome_alimento)
    return GRAMATURA_REALISTA.get(categoria, GRAMATURA_REALISTA['lanche_leve'])


def alimento_permitido_na_refeicao(nome_alimento: str, nome_refeicao: str) -> bool:
    """Verifica se um alimento é permitido em determinada refeição."""
    categoria = obter_categoria_culinaria(nome_alimento)
    regras = obter_regras_refeicao(nome_refeicao)
    
    # Verifica proibições
    if categoria in regras.get('proibidos', []):
        return False
    
    # Verifica permissões
    if categoria in regras.get('permitidos', []):
        return True
    
    # Se não está nem permitido nem proibido, depende da regra
    # Por padrão, bloqueia se houver lista de permitidos
    if regras.get('permitidos'):
        return False
    
    return True


def validar_composicao_refeicao(alimentos: list, nome_refeicao: str) -> dict:
    """
    Valida se uma composição de refeição faz sentido culinariamente.
    
    Args:
        alimentos: Lista de dicts com {'nome': str, 'gramas': float}
        nome_refeicao: Nome da refeição
    
    Returns:
        {
            'valida': bool,
            'problemas': [str],  # Lista de problemas encontrados
            'score': float  # 0-1, quanto mais próximo de 1, melhor
        }
    """
    regras = obter_regras_refeicao(nome_refeicao)
    problemas = []
    score = 1.0
    
    # Obtém categorias dos alimentos
    categorias_presentes = [obter_categoria_culinaria(a['nome']) for a in alimentos]
    nomes_presentes = [a['nome'] for a in alimentos]
    
    # Verifica estrutura
    estrutura = regras.get('estrutura', {})
    
    # Se tem múltiplas estruturas possíveis (ex: almoço)
    if 'refeicao_completa' in estrutura:
        # Tenta validar contra cada estrutura possível
        estruturas_possiveis = [
            estrutura['refeicao_completa'],
            estrutura.get('refeicao_pronta', {})
        ]
        
        melhor_score = 0
        melhores_problemas = []
        
        for est in estruturas_possiveis:
            temp_problemas = []
            temp_score = 1.0
            
            # Verifica obrigatórios
            for obrig in est.get('obrigatorio', []):
                if obrig not in categorias_presentes:
                    temp_problemas.append(f"Falta {obrig} na {nome_refeicao}")
                    temp_score -= 0.3

            # Verifica obrigatorio_um_de (PELO MENOS UM deve estar presente)
            obrigatorio_um_de = est.get('obrigatorio_um_de', [])
            if obrigatorio_um_de:
                tem_pelo_menos_um = any(cat in categorias_presentes for cat in obrigatorio_um_de)
                if not tem_pelo_menos_um:
                    temp_problemas.append(f"Precisa ter pelo menos um de: {', '.join(obrigatorio_um_de)}")
                    temp_score -= 0.5
            
            # Verifica quantidade de itens
            num_itens = len(alimentos)
            if num_itens < est.get('min_itens', 1):
                temp_problemas.append(f"Poucos itens ({num_itens}), mínimo {est['min_itens']}")
                temp_score -= 0.2
            elif num_itens > est.get('max_itens', 10):
                temp_problemas.append(f"Muitos itens ({num_itens}), máximo {est['max_itens']}")
                temp_score -= 0.1
            
            if temp_score > melhor_score:
                melhor_score = temp_score
                melhores_problemas = temp_problemas
        
        score = melhor_score
        problemas = melhores_problemas
    else:
        # Estrutura simples
        # Verifica obrigatórios (TODOS devem estar presentes)
        for obrig in estrutura.get('obrigatorio', []):
            if obrig not in categorias_presentes:
                problemas.append(f"Falta {obrig} na {nome_refeicao}")
                score -= 0.3
        
        # Verifica obrigatorio_um_de (PELO MENOS UM deve estar presente)
        obrigatorio_um_de = estrutura.get('obrigatorio_um_de', [])
        if obrigatorio_um_de:
            tem_pelo_menos_um = any(cat in categorias_presentes for cat in obrigatorio_um_de)
            if not tem_pelo_menos_um:
                problemas.append(f"Precisa ter pelo menos um de: {', '.join(obrigatorio_um_de)}")
                score -= 0.5
        
        num_itens = len(alimentos)
        if num_itens < estrutura.get('min_itens', 1):
            problemas.append(f"Poucos itens ({num_itens})")
            score -= 0.2
        elif num_itens > estrutura.get('max_itens', 10):
            problemas.append(f"Muitos itens ({num_itens})")
            score -= 0.1
    
    # Verifica alimentos proibidos
    for alimento in alimentos:
        if not alimento_permitido_na_refeicao(alimento['nome'], nome_refeicao):
            categoria = obter_categoria_culinaria(alimento['nome'])
            problemas.append(f"{alimento['nome']} ({categoria}) não é apropriado para {nome_refeicao}")
            score -= 0.4
    
    # NOVO: Verifica combinações obrigatórias (ex: aveia precisa de leite)
    combinacoes_obrigatorias = regras.get('combinacoes_obrigatorias', {})
    for categoria_que_exige, categorias_necessarias in combinacoes_obrigatorias.items():
        # Se tem a categoria que exige, verifica se tem pelo menos uma das necessárias
        if categoria_que_exige in categorias_presentes:
            tem_necessaria = any(cat in categorias_presentes for cat in categorias_necessarias)
            if not tem_necessaria:
                # Identifica qual alimento está sem a combinação
                alimento_problema = next((a['nome'] for a in alimentos 
                                        if obter_categoria_culinaria(a['nome']) == categoria_que_exige), None)
                problemas.append(f"{alimento_problema} precisa de {' ou '.join(categorias_necessarias)}")
                score -= 0.7  # Penalidade MUITO PESADA - combinação inválida!
    
    # NOVO: Lógica Arroz + Feijão
    # Se tem Arroz (acompanhamento_base), recomenda fortemente Feijão (leguminosa)
    # Mas se for Macarrão (também acompanhamento_base), não precisa.
    tem_arroz = any('Arroz' in nome for nome in nomes_presentes)
    tem_leguminosa = 'leguminosa' in categorias_presentes
    
    if tem_arroz and not tem_leguminosa:
        problemas.append("Arroz sem feijão/leguminosa")
        score -= 0.3
    
    # Verifica duplicação de categorias de carboidratos (REGRA CRÍTICA)
    # Não pode ter 'acompanhamento_base' + 'tuberculo' (Arroz + Batata)
    # Não pode ter múltiplos 'acompanhamento_base' (Arroz + Macarrão)
    count_base = categorias_presentes.count('acompanhamento_base')
    count_tuberculo = categorias_presentes.count('tuberculo')
    
    if count_base > 1:
        problemas.append(f"Múltiplos carboidratos base ({count_base})")
        score -= 0.6
        
    if count_base > 0 and count_tuberculo > 0:
        # Exceção: Se for uma refeição pronta que já inclui tudo, ok? Mas aqui estamos validando componentes.
        problemas.append("Mistura de carboidratos (Base + Tubérculo)")
        score -= 0.5
    
    # Verifica gramaturas absurdas
    for alimento in alimentos:
        limites = obter_limites_gramatura(alimento['nome'])
        gramas = alimento['gramas']
        
        if gramas < limites['min'] or gramas > limites['max']:
            problemas.append(
                f"{alimento['nome']}: {gramas:.0f}g (ideal: {limites['min']}-{limites['max']}g)"
            )
            score -= 0.2
    
    return {
        'valida': score >= 0.5,  # Considera válida se score >= 0.5
        'problemas': problemas,
        'score': max(0, score)
    }

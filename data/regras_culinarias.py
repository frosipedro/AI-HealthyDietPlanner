"""
Regras Culinárias - Contexto do Mundo Real para Composição de Refeições
VERSÃO MELHORADA - Validações mais rígidas e categorias refinadas
"""

import unicodedata


def normalizar_texto(texto: str) -> str:
    """
    Normaliza texto removendo acentos e convertendo para minúsculas.
    """
    texto_sem_acento = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
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
    'Bacon': 'frios',
    'Salmão': 'prato_principal',
    'Tilápia': 'prato_principal',
    'Sardinha': 'prato_principal',
    'Atum': 'prato_principal',
    'Camarão': 'prato_principal',
    'Bacalhau': 'prato_principal',
    
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
    
    # CARBOIDRATOS BASE
    'Arroz Branco': 'acompanhamento_base',
    'Arroz Integral': 'acompanhamento_base',
    'Macarrão': 'acompanhamento_base',
    'Macarrão Instantâneo': 'refeicao_rapida',
    'Aveia': 'cafe_da_manha_liquido',  # PRECISA de leite/iogurte!
    'Mingau de Aveia': 'mingau',
    'Farinha de Mandioca': 'ingrediente',  # NUNCA ISOLADO
    'Farinha de Trigo': 'ingrediente',  # NUNCA ISOLADO
    'Cuscuz de Milho': 'cafe_da_manha',
    'Pão Francês': 'cafe_da_manha',
    'Pão Integral': 'cafe_da_manha',
    'Tapioca': 'cafe_da_manha',
    'Pão de Forma': 'cafe_da_manha',
    'Pão de Centeio': 'cafe_da_manha',
    'Granola': 'cafe_da_manha_liquido',  # PRECISA de leite/iogurte!
    
    # LEGUMINOSAS
    'Feijão Preto': 'leguminosa',
    'Feijão Carioca': 'leguminosa',
    'Lentilha': 'leguminosa',
    'Grão-de-bico': 'leguminosa',
    'Ervilha': 'leguminosa',
    'Soja': 'leguminosa',
    
    # TUBÉRCULOS
    'Batata Inglesa': 'tuberculo',
    'Batata Doce': 'tuberculo',
    'Mandioca': 'tuberculo',
    'Inhame': 'tuberculo',
    'Cará': 'tuberculo',
    
    # VEGETAIS
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
    
    # FRUTAS
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
    
    # OLEAGINOSAS
    'Amendoim': 'oleaginosa',
    'Castanha de Caju': 'oleaginosa',
    'Castanha do Pará': 'oleaginosa',
    'Nozes': 'oleaginosa',
    'Amêndoas': 'oleaginosa',
    
    # GORDURAS
    'Óleo de Soja': 'tempero',
    'Óleo de Canola': 'tempero',
    'Azeite de Oliva': 'tempero',
    'Margarina': 'tempero',
    
    # INDUSTRIALIZADOS
    'Pão de Queijo': 'lanche_leve',
    'Coxinha': 'lanche_leve',
    'Pastel de Carne': 'lanche_leve',
    'Mortadela': 'frios',
    'Presunto': 'frios',
    'Peito de Peru': 'frios',
    'Salsicha': 'frios',
    'Nuggets de Frango': 'lanche_leve',
    'Batata Frita Congelada': 'lanche_leve',
}


# ============================================================================
# REGRAS DE COMPOSIÇÃO POR TIPO DE REFEIÇÃO
# ============================================================================

REGRAS_COMPOSICAO = {
    'Café da Manhã': {
        'permitidos': [
            'cafe_da_manha',
            'cafe_da_manha_liquido',
            'mingau',
            'fruta',
            'oleaginosa',
            'iogurte',
            'frios',
            'bebida',
            'tempero',
            'proteina_cafe',
        ],
        'proibidos': [
            'acompanhamento_base',
            'leguminosa',
            'tuberculo',
            'prato_principal',
            'refeicao_pronta',
            'ingrediente',  # CRÍTICO: Farinha nunca sozinha
            'guarnição',
            'salada',
            'refeicao_rapida',
        ],
        'estrutura': {
            'obrigatorio_um_de': ['cafe_da_manha', 'fruta', 'cafe_da_manha_liquido', 'proteina_cafe', 'iogurte', 'mingau'],
            'opcional': ['frios', 'bebida', 'tempero', 'oleaginosa'],
            'min_itens': 1,
            'max_itens': 4,
        },
        'combinacoes_obrigatorias': {
            # Se tem aveia/granola, DEVE ter leite ou iogurte
            'cafe_da_manha_liquido': ['bebida', 'iogurte'],
            # Se tem pão, DEVE ter algo para passar/rechear
            'cafe_da_manha': ['frios', 'tempero', 'proteina_cafe'],
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
            'ingrediente',
            'cafe_da_manha_liquido',  # Aveia precisa de preparo completo
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
            'acompanhamento_base',
            'leguminosa',
            'tuberculo',
            'frios',
            'guarnição',
            'salada',
            'refeicao_pronta',
            'tempero',
        ],
        'proibidos': [
            'cafe_da_manha',
            'cafe_da_manha_liquido',
            'fruta',
            'oleaginosa',
            'iogurte',
            'proteina_cafe',
            'ingrediente',
            'mingau',
            'lanche_leve',
        ],
        'estrutura': {
            'refeicao_completa': {
                'obrigatorio': ['prato_principal'],
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
            'proteina_cafe',
        ],
        'proibidos': [
            'prato_principal',
            'acompanhamento_base',
            'leguminosa',
            'tuberculo',
            'refeicao_pronta',
            'ingrediente',
            'cafe_da_manha_liquido',
        ],
        'estrutura': {
            'obrigatorio_um_de': ['fruta', 'iogurte', 'oleaginosa', 'lanche_leve', 'cafe_da_manha', 'proteina_cafe', 'mingau'],
            'opcional': ['frios', 'bebida'],
            'min_itens': 1,
            'max_itens': 3,
        },
        'combinacoes_obrigatorias': {
            'cafe_da_manha': ['frios', 'tempero', 'proteina_cafe'],
        }
    },
    
    'Jantar': {
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
            'proteina_cafe',
        ],
        'proibidos': [
            'cafe_da_manha',
            'cafe_da_manha_liquido',
            'fruta',
            'oleaginosa',
            'iogurte',
            'ingrediente',
            'mingau',
            'lanche_leve',
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
            'cafe_da_manha_liquido',
            'frios',
            'proteina_cafe',
            'ingrediente',
        ],
        'estrutura': {
            'obrigatorio_um_de': ['fruta', 'iogurte', 'bebida', 'lanche_leve', 'mingau'],
            'opcional': ['oleaginosa'],
            'min_itens': 1,
            'max_itens': 2,
        }
    },
}

REGRA_PADRAO = {
    'permitidos': ['lanche_leve', 'prato_principal', 'acompanhamento_base', 'fruta', 'iogurte'],
    'proibidos': ['tempero', 'ingrediente'],
    'estrutura': {
        'obrigatorio_um_de': ['lanche_leve', 'prato_principal', 'fruta'],
        'opcional': ['acompanhamento_base'],
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
        'descricao': 'Aveia, granola (precisa de leite/iogurte)'
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
        'descricao': 'NUNCA deve ser usado isoladamente'
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
    """
    if nome_refeicao in REGRAS_COMPOSICAO:
        return REGRAS_COMPOSICAO[nome_refeicao]
    
    nome_norm = normalizar_texto(nome_refeicao)
    
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
    
    return REGRA_PADRAO


def obter_limites_gramatura(nome_alimento: str) -> dict:
    """Retorna os limites de gramatura realistas para o alimento."""
    categoria = obter_categoria_culinaria(nome_alimento)
    return GRAMATURA_REALISTA.get(categoria, GRAMATURA_REALISTA['lanche_leve'])


def alimento_permitido_na_refeicao(nome_alimento: str, nome_refeicao: str) -> bool:
    """
    Verifica se um alimento é permitido em determinada refeição.
    VERSÃO MELHORADA - Bloqueia ingredientes SEMPRE.
    """
    categoria = obter_categoria_culinaria(nome_alimento)
    
    # REGRA CRÍTICA: Ingredientes NUNCA são permitidos isoladamente
    if categoria == 'ingrediente':
        return False
    
    regras = obter_regras_refeicao(nome_refeicao)
    
    # Verifica proibições
    if categoria in regras.get('proibidos', []):
        return False
    
    # Verifica permissões
    if categoria in regras.get('permitidos', []):
        return True
    
    if regras.get('permitidos'):
        return False
    
    return True


def validar_composicao_refeicao(alimentos: list, nome_refeicao: str) -> dict:
    """
    Valida se uma composição de refeição faz sentido culinariamente.
    VERSÃO MELHORADA - Penalizações mais pesadas.
    """
    regras = obter_regras_refeicao(nome_refeicao)
    problemas = []
    score = 1.0
    
    categorias_presentes = [obter_categoria_culinaria(a['nome']) for a in alimentos]
    nomes_presentes = [a['nome'] for a in alimentos]
    
    # PENALIDADE CRÍTICA: Se tem ingrediente puro
    if 'ingrediente' in categorias_presentes:
        problemas.append("CRÍTICO: Farinha/Ingrediente não pode ser servido puro!")
        score -= 0.9  # Quase zera o score
    
    estrutura = regras.get('estrutura', {})
    
    if 'refeicao_completa' in estrutura:
        estruturas_possiveis = [
            estrutura['refeicao_completa'],
            estrutura.get('refeicao_pronta', {})
        ]
        
        melhor_score = 0
        melhores_problemas = []
        
        for est in estruturas_possiveis:
            temp_problemas = []
            temp_score = 1.0
            
            for obrig in est.get('obrigatorio', []):
                if obrig not in categorias_presentes:
                    temp_problemas.append(f"Falta {obrig}")
                    temp_score -= 0.4  # Penalidade aumentada
            
            obrigatorio_um_de = est.get('obrigatorio_um_de', [])
            if obrigatorio_um_de:
                tem_pelo_menos_um = any(cat in categorias_presentes for cat in obrigatorio_um_de)
                if not tem_pelo_menos_um:
                    temp_problemas.append(f"Precisa ter: {', '.join(obrigatorio_um_de)}")
                    temp_score -= 0.6  # Penalidade aumentada
            
            num_itens = len(alimentos)
            if num_itens < est.get('min_itens', 1):
                temp_problemas.append(f"Poucos itens ({num_itens})")
                temp_score -= 0.3
            elif num_itens > est.get('max_itens', 10):
                temp_problemas.append(f"Muitos itens ({num_itens})")
                temp_score -= 0.2
            
            if temp_score > melhor_score:
                melhor_score = temp_score
                melhores_problemas = temp_problemas
        
        score = min(score, melhor_score)
        problemas = melhores_problemas
    else:
        for obrig in estrutura.get('obrigatorio', []):
            if obrig not in categorias_presentes:
                problemas.append(f"Falta {obrig}")
                score -= 0.4
        
        obrigatorio_um_de = estrutura.get('obrigatorio_um_de', [])
        if obrigatorio_um_de:
            tem_pelo_menos_um = any(cat in categorias_presentes for cat in obrigatorio_um_de)
            if not tem_pelo_menos_um:
                problemas.append(f"Precisa ter: {', '.join(obrigatorio_um_de)}")
                score -= 0.6
        
        num_itens = len(alimentos)
        if num_itens < estrutura.get('min_itens', 1):
            problemas.append(f"Poucos itens ({num_itens})")
            score -= 0.3
        elif num_itens > estrutura.get('max_itens', 10):
            problemas.append(f"Muitos itens ({num_itens})")
            score -= 0.2
    
    # Verifica alimentos proibidos
    for alimento in alimentos:
        if not alimento_permitido_na_refeicao(alimento['nome'], nome_refeicao):
            categoria = obter_categoria_culinaria(alimento['nome'])
            problemas.append(f"{alimento['nome']} ({categoria}) inadequado")
            score -= 0.5  # Penalidade aumentada
    
    # COMBINAÇÕES OBRIGATÓRIAS (penalidade MUITO PESADA)
    combinacoes_obrigatorias = regras.get('combinacoes_obrigatorias', {})
    for categoria_que_exige, categorias_necessarias in combinacoes_obrigatorias.items():
        if categoria_que_exige in categorias_presentes:
            tem_necessaria = any(cat in categorias_presentes for cat in categorias_necessarias)
            if not tem_necessaria:
                alimento_problema = next((a['nome'] for a in alimentos 
                                        if obter_categoria_culinaria(a['nome']) == categoria_que_exige), None)
                problemas.append(f"CRÍTICO: {alimento_problema} precisa de {' ou '.join(categorias_necessarias)}")
                score -= 0.8  # Penalidade aumentada
    
    # Lógica Arroz + Feijão
    tem_arroz = any('Arroz' in nome for nome in nomes_presentes)
    tem_leguminosa = 'leguminosa' in categorias_presentes
    
    if tem_arroz and not tem_leguminosa:
        problemas.append("Arroz sem feijão")
        score -= 0.4  # Penalidade aumentada
    
    # Duplicação de carboidratos (CRÍTICO)
    count_base = categorias_presentes.count('acompanhamento_base')
    count_tuberculo = categorias_presentes.count('tuberculo')
    
    if count_base > 1:
        problemas.append(f"CRÍTICO: Múltiplos carboidratos base ({count_base})")
        score -= 0.7  # Penalidade aumentada
        
    if count_base > 0 and count_tuberculo > 0:
        problemas.append("CRÍTICO: Carboidrato base + Tubérculo")
        score -= 0.6  # Penalidade aumentada
    
    # Gramaturas absurdas
    for alimento in alimentos:
        limites = obter_limites_gramatura(alimento['nome'])
        gramas = alimento['gramas']
        
        if gramas < limites['min'] or gramas > limites['max']:
            problemas.append(
                f"{alimento['nome']}: {gramas:.0f}g fora do limite ({limites['min']}-{limites['max']}g)"
            )
            score -= 0.25
    
    return {
        'valida': score >= 0.4,  # Threshold mais rigoroso
        'problemas': problemas,
        'score': max(0, score)
    }
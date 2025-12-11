"""
Regras Culinárias - Contexto do Mundo Real para Composição de Refeições
Compatibilidade entre alimentos e validações rigorosas

Inclui:
- Categorias culinárias detalhadas
- Regras de composição por refeição
- NOVO: Sistema de compatibilidade entre proteínas e acompanhamentos
- NOVO: Regras específicas do usuário para combinações tradicionais brasileiras
"""

import unicodedata
from typing import List, Tuple, Dict


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
# SISTEMA DE COMPATIBILIDADE ENTRE ALIMENTOS
# Define quais proteínas combinam com quais acompanhamentos
# ============================================================================

# Classificação de proteínas por tipo
PROTEINAS_CARNE_VERMELHA = {
    'Carne Moída Patinho', 'Carne Moída Acém', 'Bife de Patinho', 
    'Picanha', 'Alcatra', 'Coxão Duro', 'Carne Seca',
    'Lombo Suíno', 'Pernil Suíno', 'Linguiça Toscana', 'Bacon'
}

PROTEINAS_FRANGO = {
    'Peito de Frango', 'Coxa de Frango', 'Asa de Frango', 
    'Linguiça de Frango', 'Nuggets de Frango'
}

PROTEINAS_PEIXE = {
    'Salmão', 'Tilápia', 'Sardinha', 'Atum', 'Bacalhau', 'Camarão'
}

PROTEINAS_OVOS = {
    'Ovo', 'Ovo Mexido'
}

PROTEINAS_EMBUTIDOS = {
    'Mortadela', 'Presunto', 'Peito de Peru', 'Salsicha'
}

# Classificação de acompanhamentos
ACOMPANHAMENTOS_ARROZ = {'Arroz Branco', 'Arroz Integral'}
ACOMPANHAMENTOS_MASSA = {'Macarrão', 'Macarrão Instantâneo'}
ACOMPANHAMENTOS_PAO = {'Pão Francês', 'Pão Integral', 'Pão de Forma', 'Pão de Centeio', 'Tapioca'}
ACOMPANHAMENTOS_BATATA = {'Batata Inglesa', 'Batata Doce'}
ACOMPANHAMENTOS_TUBERCULOS = {'Mandioca', 'Inhame', 'Cará'}
ACOMPANHAMENTOS_LEGUMINOSAS = {'Feijão Preto', 'Feijão Carioca', 'Lentilha', 'Grão-de-bico', 'Ervilha', 'Soja'}

# ============================================================================
# REGRAS DE COMPATIBILIDADE (Baseadas nas preferências do usuário)
# ============================================================================

# Formato: proteína -> set de acompanhamentos PERMITIDOS
COMPATIBILIDADE_PROTEINA_ACOMPANHAMENTO = {
    # CARNE VERMELHA
    'carne_vermelha': {
        'arroz': True,
        'massa': True,
        'pao': True,
        'batata': True,
        'tuberculos': True,
        'leguminosas': True, 
    },
    
    # FRANGO
    'frango': {
        'arroz': True,
        'massa': True,
        'pao': True,
        'batata': True,
        'tuberculos': True,
        'leguminosas': True,  
    },
    
    # PEIXE
    'peixe': {
        'arroz': True,
        'massa': True,      
        'pao': True,        
        'batata': True,     
        'tuberculos': False,  
        'leguminosas': False,  
    },
    
    # OVOS
    'ovos': {
        'arroz': True,
        'massa': True,
        'pao': True,
        'batata': True,
        'tuberculos': True,
        'leguminosas': True,  
    },
    
    # EMBUTIDOS
    'embutidos': {
        'arroz': True,
        'massa': True,
        'pao': True,
        'batata': True,
        'tuberculos': True,
        'leguminosas': True,
    },
}

def obter_tipo_proteina(nome_alimento: str) -> str | None:
    """Retorna o tipo de proteína (carne_vermelha, frango, peixe, ovos, embutidos) ou None."""
    if nome_alimento in PROTEINAS_CARNE_VERMELHA:
        return 'carne_vermelha'
    elif nome_alimento in PROTEINAS_FRANGO:
        return 'frango'
    elif nome_alimento in PROTEINAS_PEIXE:
        return 'peixe'
    elif nome_alimento in PROTEINAS_OVOS:
        return 'ovos'
    elif nome_alimento in PROTEINAS_EMBUTIDOS:
        return 'embutidos'
    return None


def obter_tipo_acompanhamento(nome_alimento: str) -> str | None:
    """Retorna o tipo de acompanhamento ou None."""
    if nome_alimento in ACOMPANHAMENTOS_ARROZ:
        return 'arroz'
    elif nome_alimento in ACOMPANHAMENTOS_MASSA:
        return 'massa'
    elif nome_alimento in ACOMPANHAMENTOS_PAO:
        return 'pao'
    elif nome_alimento in ACOMPANHAMENTOS_BATATA:
        return 'batata'
    elif nome_alimento in ACOMPANHAMENTOS_TUBERCULOS:
        return 'tuberculos'
    elif nome_alimento in ACOMPANHAMENTOS_LEGUMINOSAS:
        return 'leguminosas'
    return None


def verificar_compatibilidade_proteina_acompanhamento(
    nome_proteina: str, 
    nome_acompanhamento: str
) -> Tuple[bool, str]:
    """
    Verifica se uma proteína combina com um acompanhamento.
    
    Returns:
        Tuple[bool, str]: (é_compatível, mensagem_erro)
    """
    tipo_proteina = obter_tipo_proteina(nome_proteina)
    tipo_acompanhamento = obter_tipo_acompanhamento(nome_acompanhamento)
    
    # Se não conseguiu classificar, assume compatível
    if tipo_proteina is None or tipo_acompanhamento is None:
        return True, ""
    
    # Busca regras de compatibilidade
    regras = COMPATIBILIDADE_PROTEINA_ACOMPANHAMENTO.get(tipo_proteina, {})
    compativel = regras.get(tipo_acompanhamento, True)  # Default: compatível
    
    if not compativel:
        return False, f"{nome_proteina} não combina com {nome_acompanhamento}"
    
    return True, ""


def verificar_compatibilidade_leguminosa(
    nome_leguminosa: str,
    outros_alimentos: List[str]
) -> Tuple[bool, List[str]]:
    """
    Verifica se uma leguminosa (feijão, lentilha) está em combinação válida.
    
    Regras:
    - Leguminosa PRECISA de arroz ou massa
    - Leguminosa NÃO pode estar com peixe
    
    Returns:
        Tuple[bool, List[str]]: (é_válida, lista_de_problemas)
    """
    problemas = []
    
    # Verifica se tem arroz ou massa junto
    tem_acompanhamento_valido = False
    for alimento in outros_alimentos:
        tipo_acomp = obter_tipo_acompanhamento(alimento)
        if tipo_acomp in ['arroz', 'massa']:
            tem_acompanhamento_valido = True
            break
    
    if not tem_acompanhamento_valido:
        problemas.append(f"{nome_leguminosa} precisa de arroz ou massa como acompanhamento")
    
    # Verifica se tem peixe junto (PROIBIDO)
    for alimento in outros_alimentos:
        if alimento in PROTEINAS_PEIXE:
            problemas.append(f"{nome_leguminosa} não combina com {alimento} (peixe)")
    
    return len(problemas) == 0, problemas


def validar_diversidade_cardapio(cardapio_completo: Dict[str, List[dict]]) -> Tuple[float, List[str]]:
    """
    Valida a diversidade de alimentos no cardápio do dia inteiro.
    Penaliza alimentos que aparecem mais de uma vez em diferentes refeições.
    
    Args:
        cardapio_completo: Dict com {nome_refeicao: [{'nome': str, 'gramas': float}, ...]}
    
    Returns:
        Tuple[float, List[str]]: (score de 0 a 1, lista de problemas)
    """
    from collections import Counter
    
    problemas = []
    penalidade_total = 0.0
    
    # Coleta todos os alimentos do dia
    todos_alimentos = []
    for nome_refeicao, alimentos in cardapio_completo.items():
        for alimento in alimentos:
            todos_alimentos.append((alimento['nome'], nome_refeicao))
    
    # Conta quantas vezes cada alimento aparece
    contador = Counter([alimento[0] for alimento in todos_alimentos])
    
    # Penaliza repetições
    for alimento, quantidade in contador.items():
        if quantidade > 1:
            # Encontra em quais refeições aparece
            refeicoes_com_alimento = [ref for nome, ref in todos_alimentos if nome == alimento]
            
            problemas.append(
                f"REPETIÇÃO: {alimento} aparece {quantidade}x no dia ({', '.join(set(refeicoes_com_alimento))})"
            )
            
            # Penalidade progressiva: quanto mais repete, pior
            # 2x = -0.3, 3x = -0.5, 4x+ = -0.8
            if quantidade == 2:
                penalidade_total += 0.3
            elif quantidade == 3:
                penalidade_total += 0.5
            else:
                penalidade_total += 0.8
    
    score = max(0.0, 1.0 - penalidade_total)
    return score, problemas


def validar_compatibilidade_refeicao(alimentos: List[dict]) -> Tuple[float, List[str]]:
    """
    Valida a compatibilidade entre todos os alimentos de uma refeição.
    
    Args:
        alimentos: Lista de dicts com {'nome': str, 'gramas': float, ...}
    
    Returns:
        Tuple[float, List[str]]: (score de 0 a 1, lista de problemas)
    """
    nomes = [a['nome'] for a in alimentos]
    problemas = []
    penalidade_total = 0.0
    
    # Identifica proteínas e acompanhamentos na refeição
    proteinas_na_refeicao = [n for n in nomes if obter_tipo_proteina(n) is not None]
    leguminosas_na_refeicao = [n for n in nomes if n in ACOMPANHAMENTOS_LEGUMINOSAS]
    
    # 1. Verifica compatibilidade proteína-acompanhamento
    for proteina in proteinas_na_refeicao:
        for acompanhamento in nomes:
            if acompanhamento == proteina:
                continue
            compativel, msg = verificar_compatibilidade_proteina_acompanhamento(proteina, acompanhamento)
            if not compativel:
                problemas.append(f"INCOMPATÍVEL: {msg}")
                penalidade_total += 0.4  # Penalidade pesada
    
    # 2. Verifica regras específicas de leguminosas
    for leguminosa in leguminosas_na_refeicao:
        outros = [n for n in nomes if n != leguminosa]
        valida, probs = verificar_compatibilidade_leguminosa(leguminosa, outros)
        if not valida:
            for p in probs:
                problemas.append(f"INCOMPATÍVEL: {p}")
                penalidade_total += 0.5  # Penalidade muito pesada
    
    # 3. Verifica múltiplas proteínas conflitantes
    tem_peixe = any(p in PROTEINAS_PEIXE for p in proteinas_na_refeicao)
    
    # Peixe não combina com outras carnes
    if tem_peixe:
        outras_carnes = [p for p in proteinas_na_refeicao 
                        if p in PROTEINAS_CARNE_VERMELHA or p in PROTEINAS_FRANGO]
        if outras_carnes:
            problemas.append("INCOMPATÍVEL: Peixe não deve ser misturado com outras carnes")
            penalidade_total += 0.3
    
    # Múltiplas proteínas principais na mesma refeição (exceto embutidos que são complementos)
    proteinas_principais = [p for p in proteinas_na_refeicao if p not in PROTEINAS_EMBUTIDOS]
    if len(proteinas_principais) > 1:
        # Só penaliza se forem tipos diferentes
        tipos_proteinas = set(obter_tipo_proteina(p) for p in proteinas_principais)
        if len(tipos_proteinas) > 1:
            problemas.append(f"INCOMPATÍVEL: Múltiplas proteínas principais na mesma refeição ({', '.join(proteinas_principais)})")
            penalidade_total += 0.4
    
    # 4. Múltiplos acompanhamentos base (arroz + macarrão = ESTRANHO)
    acompanhamentos_base = [a['nome'] for a in alimentos if a['nome'] in ACOMPANHAMENTOS_ARROZ or a['nome'] in ACOMPANHAMENTOS_MASSA]
    if len(acompanhamentos_base) > 1:
        problemas.append(f"INCOMPATÍVEL: Múltiplos acompanhamentos base na mesma refeição ({', '.join(acompanhamentos_base)})")
        penalidade_total += 0.5  # Penalidade pesada - isso é muito estranho!
    
    # 5. Múltiplas leguminosas (feijão + lentilha = ESTRANHO)
    if len(leguminosas_na_refeicao) > 1:
        problemas.append(f"INCOMPATÍVEL: Múltiplas leguminosas na mesma refeição ({', '.join(leguminosas_na_refeicao)})")
        penalidade_total += 0.5  # Penalidade pesada - brasileiro não mistura feijões!
    
    score = max(0.0, 1.0 - penalidade_total)
    return score, problemas

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
    'Aveia': 'cafe_da_manha_liquido', 
    'Mingau de Aveia': 'mingau',
    'Farinha de Mandioca': 'ingrediente',  
    'Farinha de Trigo': 'ingrediente',  
    'Cuscuz de Milho': 'cafe_da_manha',
    'Pão Francês': 'cafe_da_manha',
    'Pão Integral': 'cafe_da_manha',
    'Tapioca': 'cafe_da_manha',
    'Pão de Forma': 'cafe_da_manha',
    'Pão de Centeio': 'cafe_da_manha',
    'Granola': 'cafe_da_manha_liquido', 
    
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
            'ingrediente',  
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
            'cafe_da_manha_liquido': ['bebida', 'iogurte'],
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
            'cafe_da_manha_liquido',
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
    VERSÃO 2.0 - Inclui validação de compatibilidade entre alimentos.
    """
    regras = obter_regras_refeicao(nome_refeicao)
    problemas = []
    score = 1.0
    
    categorias_presentes = [obter_categoria_culinaria(a['nome']) for a in alimentos]
    
    # =========================================================================
    # Compatibilidade entre alimentos (peixe/feijão, etc.)
    # =========================================================================
    score_compat, problemas_compat = validar_compatibilidade_refeicao(alimentos)
    if problemas_compat:
        problemas.extend(problemas_compat)
        score -= (1.0 - score_compat)  # Aplica penalidade proporcional
    
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
        problemas.extend(melhores_problemas)
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
    
    # Duplicação de carboidratos (CRÍTICO)
    count_base = categorias_presentes.count('acompanhamento_base')
    count_tuberculo = categorias_presentes.count('tuberculo')
    
    if count_base > 1:
        problemas.append(f"CRÍTICO: Múltiplos carboidratos base ({count_base})")
        score -= 0.7  # Penalidade aumentada
        
    if count_base > 0 and count_tuberculo > 0:
        problemas.append("CRÍTICO: Carboidrato base + Tubérculo na mesma refeição")
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
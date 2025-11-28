import pandas as pd

dados_alimentos_completo = {
    'nome': [
        # PROTEÍNAS ANIMAIS
        'Peito de Frango', 'Coxa de Frango', 'Asa de Frango', 'Carne Moída Patinho',
        'Carne Moída Acém', 'Bife de Patinho', 'Picanha', 'Alcatra',
        'Coxão Duro', 'Carne Seca', 'Linguiça Toscana', 'Linguiça de Frango',
        'Lombo Suíno', 'Pernil Suíno', 'Bacon', 'Salmão', 'Tilápia', 'Sardinha',
        'Atum',
        # OVOS E LATICÍNIOS
        'Ovo', 'Ovo Mexido', 'Queijo Minas', 'Queijo Mussarela', 'Queijo Parmesão',
        'Requeijão', 'Leite Integral', 'Leite Desnatado', 'Iogurte Natural',
        'Iogurte Grego', 'Manteiga',
        # CARBOIDRATOS / CEREAIS
        'Arroz Branco', 'Arroz Integral', 'Macarrão', 'Macarrão Instantâneo',
        'Aveia', 'Farinha de Mandioca', 'Farinha de Trigo', 'Cuscuz de Milho',
        'Pão Francês', 'Pão Integral', 'Tapioca', 'Pão de Forma', 'Pão de Centeio',
        # LEGUMINOSAS
        'Feijão Preto', 'Feijão Carioca', 'Lentilha', 'Grão-de-bico', 'Ervilha',
        'Soja',
        # TUBÉRCULOS
        'Batata Inglesa', 'Batata Doce', 'Mandioca', 'Inhame', 'Cará',
        # VEGETAIS
        'Brócolis', 'Couve Flor', 'Cenoura', 'Beterraba', 'Abobrinha',
        'Alface', 'Tomate', 'Pepino', 'Repolho', 'Vagem', 'Milho Verde',
        # FRUTAS
        'Banana Prata', 'Banana Nanica', 'Maçã', 'Pera', 'Melancia', 'Mamão',
        'Laranja', 'Tangerina', 'Morango', 'Abacate', 'Abacaxi', 'Uva',
        # OLEAGINOSAS
        'Amendoim', 'Castanha de Caju', 'Castanha do Pará', 'Nozes', 'Amêndoas',
        # GORDURAS
        'Óleo de Soja', 'Óleo de Canola', 'Azeite de Oliva', 'Margarina',
        # INDUSTRIALIZADOS
        'Arroz Carreteiro', 'Feijoada', 'Pão de Queijo', 'Coxinha', 'Pastel de Carne',
        'Mortadela', 'Presunto', 'Peito de Peru',
        # PREPARAÇÕES CASEIRAS
        'Arroz + Feijão', 'Omelete', 'Purê de Batata', 'Salada Mista',
        'Strogonoff de Frango', 'Frango à Milanesa'
    ],
    'calorias': [
        165, 215, 290, 212, 250, 180, 289, 220, 215, 239, 330, 260, 210, 240, 540, 208, 128, 185, 130, # Prots
        155, 160, 280, 300, 392, 257, 61, 42, 60, 115, 720, # Ovos/Lat
        130, 124, 157, 440, 394, 361, 360, 112, 270, 265, 150, 260, 240, # Carbos
        77, 85, 116, 164, 84, 172, # Legum
        86, 86, 125, 97, 78, # Tuber
        55, 30, 35, 49, 15, 15, 18, 12, 23, 31, 98, # Veg
        89, 92, 52, 57, 30, 45, 46, 50, 32, 160, 50, 67, # Frut
        567, 553, 659, 588, 576, # Oleo
        884, 884, 884, 720, # Gord
        180, 150, 360, 280, 300, 280, 110, 110, # Ind
        138, 160, 110, 30, 180, 250 # Caseiros
    ],
    'proteinas': [
        31, 28, 24, 27, 26, 29, 22, 29, 28, 24, 16, 18, 29, 27, 37, 20, 26, 25, 29,
        13, 12, 17, 22, 35, 7.5, 3.2, 3.4, 4, 7, 0.5,
        2.7, 2.6, 5.8, 9, 17, 1.6, 10, 2.5, 8, 9, 0.2, 8, 9,
        5.1, 5.6, 9, 9, 5, 16,
        1.7, 1.6, 1.5, 1.7, 1.8,
        3.7, 2.2, 0.8, 1.8, 1.1, 1.2, 0.9, 0.7, 1.2, 1.8, 3.4,
        1.1, 1.2, 0.3, 0.4, 0.6, 0.5, 0.9, 0.8, 0.8, 2, 0.5, 0.7,
        26, 18, 14, 15, 21,
        0, 0, 0, 0,
        12, 8, 5, 10, 12, 13, 18, 17,
        5, 12, 2, 1.2, 18, 22
    ],
    'gorduras': [
        3.6, 10, 21, 11, 17, 6, 23, 10, 9, 12, 28, 19, 9, 13, 42, 13, 2, 9, 0.6,
        11, 12, 22, 22, 26, 23, 3.4, 0.2, 3, 5, 81,
        0.3, 1, 0.9, 19, 7, 0.3, 1.4, 0.3, 1.5, 3.2, 0.1, 4.0, 2.5,
        0.5, 0.5, 0.4, 2.6, 0.4, 9,
        0.1, 0.1, 0.3, 0.2, 0.1,
        0.6, 0.3, 0.2, 0.1, 0.3, 0.2, 0.2, 0.1, 0.1, 0.2, 1.7,
        0.3, 0.3, 0.2, 0.1, 0.2, 0.2, 0.1, 0.3, 0.3, 14, 0.1, 0.4,
        49, 44, 67, 59, 49,
        100, 100, 100, 80,
        6, 7, 20, 15, 18, 23, 4, 2,
        1, 12, 4, 0.3, 10, 10
    ],
    'gordura_saturada': [
        1.0, 2.5, 6.0, 4.0, 6.5, 2.5, 10.0, 4.0, 3.5, 5.0, 10.0, 6.0, 3.0, 4.5, 14.0, 3.0, 0.9, 2.5, 0.2,
        3.0, 3.5, 14.0, 14.0, 17.0, 14.0, 2.1, 0.1, 1.9, 3.0, 51.0,
        0.1, 0.2, 0.2, 8.0, 1.2, 0.1, 0.3, 0.1, 0.5, 0.6, 0.0, 1.0, 0.5,
        0.1, 0.1, 0.1, 0.3, 0.1, 1.3,
        0.0, 0.0, 0.1, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2,
        0.1, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.1, 0.0, 0.1,
        6.8, 7.8, 15.0, 6.1, 3.7,
        15.0, 7.0, 14.0, 20.0,
        2.0, 3.0, 10.0, 6.0, 7.0, 8.0, 1.5, 0.5,
        0.3, 4.0, 2.0, 0.1, 5.0, 4.0
    ],
    'carboidratos': [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1.4, 0, 0, 0, 0,
        1.1, 2, 1.3, 2.3, 1.8, 3, 5, 5, 6, 9, 0,
        28, 25.8, 30, 56, 66, 87, 75, 25, 58, 49, 36, 48, 45,
        14, 14, 20, 27, 15, 7,
        20, 20, 30, 23, 19,
        11, 5.2, 8, 11, 2.9, 2.9, 3.9, 2.2, 5.2, 7, 17,
        23, 23, 14, 15, 7.6, 12, 12, 13, 7.7, 8.5, 13, 17,
        16, 30, 11, 18, 22,
        0, 0, 0, 0,
        18, 12, 38, 25, 24, 2, 1, 2,
        26, 2, 17, 5, 5, 18
    ],
    'fibras': [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0.3, 2.7, 1.8, 2.3, 10, 4.0, 2.4, 2, 2.1, 6.5, 0, 1.5, 5.0,
        8.4, 8, 8, 7.6, 5, 6,
        1.4, 3, 1.7, 1.5, 1.3,
        3.3, 2.3, 3, 3.4, 1.2, 1.3, 1.2, 0.8, 2.9, 3.2, 2.4,
        2.6, 2.6, 2.4, 3.1, 0.3, 1.4, 2.4, 1.8, 2, 6.7, 1.4, 0.9,
        8.5, 3.3, 7.5, 6.7, 12.5,
        0, 0, 0, 0,
        2, 4, 1, 2, 1, 0, 0, 0,
        4, 0, 1, 2, 0, 1
    ],
    'sodio': [
        60, 75, 80, 60, 65, 60, 60, 60, 60, 2500, 1100, 900, 55, 65, 1200, 50, 40, 300, 40,
        130, 150, 200, 400, 1200, 500, 50, 50, 45, 40, 10,
        1, 1, 1, 1800, 0, 0, 2, 5, 550, 400, 2, 450, 400,
        1, 1, 2, 5, 1, 2,
        5, 5, 4, 3, 4,
        30, 25, 35, 60, 2, 5, 5, 2, 10, 5, 2,
        1, 1, 1, 1, 1, 3, 0, 1, 1, 2, 1, 1,
        5, 10, 2, 2, 1,
        0, 0, 0, 700,
        900, 1200, 600, 500, 600, 1200, 1100, 950,
        300, 400, 250, 100, 600, 500
    ],
    'custo': [
        1.8,1.6,1.8,3.5,2.6,4.2,8.0,6.0,3.5,5.0,3.0,2.5,3.0,2.6,5.0,10.0,4.0,2.0,4.5,
        0.8,0.8,3.5,3.6,5.0,2.0,0.4,0.4,1.2,1.8,5.0,
        0.4,0.45,0.5,1.2,0.7,0.3,0.25,0.2,0.5,0.8,0.5, 0.6, 0.9,
        0.5,0.5,0.6,0.8,0.7,0.9,
        0.3,0.6,0.4,0.4,0.4,
        1.2,1.0,0.6,0.5,0.7,0.2,0.4,0.4,0.6,0.6,0.7,
        0.4,0.4,0.5,0.6,0.2,0.4,0.3,0.3,1.0,1.2,0.4,0.8,
        2.5,4.0,4.5,6.0,6.0,
        0.7,1.2,4.0,1.0,
        2.0,3.0,1.5,2.0,3.0,2.0,2.0,3.0,
        0.45,1.0,0.4,0.4,3.0,3.0
    ],
    'tipo': [
        'proteina','proteina','proteina','proteina','proteina','proteina','proteina','proteina',
        'proteina','proteina','proteina','proteina','proteina','proteina','gordura','proteina',
        'proteina','proteina','proteina',
        'proteina','proteina','proteina','proteina','proteina','gordura','proteina',
        'proteina','proteina','proteina','gordura',
        'carboidrato','carboidrato','carboidrato','carboidrato','carboidrato',
        'carboidrato','carboidrato','carboidrato','carboidrato','carboidrato', 'carboidrato',
        'carboidrato', 'carboidrato',
        'carboidrato','carboidrato','carboidrato','carboidrato','carboidrato','carboidrato',
        'carboidrato','carboidrato','carboidrato','carboidrato','carboidrato',
        'vegetal','vegetal','vegetal','vegetal','vegetal','vegetal','vegetal',
        'vegetal','vegetal','vegetal','vegetal',
        'fruta','fruta','fruta','fruta','fruta','fruta','fruta','fruta','fruta',
        'fruta','fruta','fruta',
        'gordura','gordura','gordura','gordura','gordura',
        'gordura','gordura','gordura','gordura',
        'industrializado','industrializado','industrializado','industrializado',
        'industrializado','industrializado','industrializado','industrializado',
        'refeicao','refeicao','refeicao','refeicao','refeicao','refeicao'
    ]
}

df_alimentos = pd.DataFrame(dados_alimentos_completo)

# --- CRIAÇÃO DA GORDURA INSATURADA ---
# "O que não é saturada, consideramos 'boa' (mono+poli)"
df_alimentos['gorduras_insaturadas'] = df_alimentos['gorduras'] - df_alimentos['gordura_saturada']

# Garante que não fique negativo (caso haja erro de input)
df_alimentos['gorduras_insaturadas'] = df_alimentos['gorduras_insaturadas'].clip(lower=0)

def criar_base_dados():
    """ Cria e retorna a base de dados de alimentos como um DataFrame do Pandas. """
    return df_alimentos.copy()
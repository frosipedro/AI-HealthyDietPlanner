"""Base de Dados de Alimentos

Contém informações nutricionais completas para 100+ alimentos brasileiros.

Campos por alimento (valores por 100g):
- nome: Nome do alimento
- calorias: Energia em kcal
- proteinas: Proteínas em gramas
- gorduras: Gorduras totais em gramas
- gordura_saturada: Gordura saturada em gramas
- carboidratos: Carboidratos em gramas
- fibras: Fibras em gramas
- sodio: Sódio em miligramas
- custo: Custo estimado em R$ por 100g
- tipo: Categoria nutricional (proteina, carboidrato, vegetal, fruta, gordura)
"""

import pandas as pd

# Lista de alimentos com todas as informações nutricionais
alimentos = [
    # PROTEÍNAS ANIMAIS
    {"nome": "Alcatra", "calorias": 153, "proteinas": 20.6, "gorduras": 7.8, "gordura_saturada": 3.0, "carboidratos": 0.0, "fibras": 0.0, "sodio": 53, "custo": 6.0, "tipo": "proteina"},
    {"nome": "Asa de Frango", "calorias": 288, "proteinas": 26.6, "gorduras": 19.3, "gordura_saturada": 5.4, "carboidratos": 0.0, "fibras": 0.0, "sodio": 400, "custo": 1.8, "tipo": "proteina"},
    {"nome": "Atum", "calorias": 108, "proteinas": 23.3, "gorduras": 0.9, "gordura_saturada": 0.2, "carboidratos": 0.0, "fibras": 0.0, "sodio": 40, "custo": 4.5, "tipo": "proteina"},
    {"nome": "Bacalhau", "calorias": 122, "proteinas": 20.9, "gorduras": 3.6, "gordura_saturada": 0.6, "carboidratos": 0.4, "fibras": 0.0, "sodio": 200, "custo": 12.0, "tipo": "proteina"},
    {"nome": "Bacon", "calorias": 540, "proteinas": 37.0, "gorduras": 42.0, "gordura_saturada": 14.0, "carboidratos": 1.4, "fibras": 0.0, "sodio": 2300, "custo": 5.0, "tipo": "proteina"},
    {"nome": "Bife de Patinho", "calorias": 195, "proteinas": 33.0, "gorduras": 6.3, "gordura_saturada": 1.7, "carboidratos": 0.0, "fibras": 0.0, "sodio": 60, "custo": 4.2, "tipo": "proteina"},
    {"nome": "Camarão", "calorias": 154, "proteinas": 24.4, "gorduras": 5.0, "gordura_saturada": 0.9, "carboidratos": 1.2, "fibras": 0.0, "sodio": 400, "custo": 15.0, "tipo": "proteina"},
    {"nome": "Carne Moída Acém", "calorias": 212, "proteinas": 26.7, "gorduras": 10.9, "gordura_saturada": 7.5, "carboidratos": 0.0, "fibras": 0.0, "sodio": 65, "custo": 2.6, "tipo": "proteina"},
    {"nome": "Carne Moída Patinho", "calorias": 150, "proteinas": 30.0, "gorduras": 2.5, "gordura_saturada": 1.0, "carboidratos": 0.0, "fibras": 0.0, "sodio": 60, "custo": 3.5, "tipo": "proteina"},
    {"nome": "Carne Seca", "calorias": 146, "proteinas": 21.0, "gorduras": 7.0, "gordura_saturada": 2.9, "carboidratos": 0.0, "fibras": 0.0, "sodio": 837, "custo": 5.0, "tipo": "proteina"},
    {"nome": "Coxa de Frango", "calorias": 171, "proteinas": 28.0, "gorduras": 5.6, "gordura_saturada": 1.4, "carboidratos": 0.0, "fibras": 0.0, "sodio": 250, "custo": 1.6, "tipo": "proteina"},
    {"nome": "Coxão Duro", "calorias": 169, "proteinas": 21.2, "gorduras": 5.6, "gordura_saturada": 2.5, "carboidratos": 0.0, "fibras": 0.0, "sodio": 71, "custo": 3.5, "tipo": "proteina"},
    {"nome": "Linguiça de Frango", "calorias": 237, "proteinas": 14.0, "gorduras": 17.0, "gordura_saturada": 4.8, "carboidratos": 5.0, "fibras": 0.0, "sodio": 1200, "custo": 2.5, "tipo": "proteina"},
    {"nome": "Linguiça Toscana", "calorias": 222, "proteinas": 14.0, "gorduras": 18.0, "gordura_saturada": 6.8, "carboidratos": 1.0, "fibras": 0.0, "sodio": 900, "custo": 3.0, "tipo": "proteina"},
    {"nome": "Lombo Suíno", "calorias": 136, "proteinas": 20.5, "gorduras": 5.4, "gordura_saturada": 1.8, "carboidratos": 0.0, "fibras": 0.0, "sodio": 55, "custo": 3.0, "tipo": "proteina"},
    {"nome": "Peito de Frango", "calorias": 195, "proteinas": 29.5, "gorduras": 7.6, "gordura_saturada": 2.1, "carboidratos": 0.0, "fibras": 0.0, "sodio": 134, "custo": 1.8, "tipo": "proteina"},
    {"nome": "Pernil Suíno", "calorias": 170, "proteinas": 23.0, "gorduras": 8.8, "gordura_saturada": 3.3, "carboidratos": 0.0, "fibras": 0.0, "sodio": 65, "custo": 2.6, "tipo": "proteina"},
    {"nome": "Picanha", "calorias": 238, "proteinas": 31.9, "gorduras": 11.3, "gordura_saturada": 4.5, "carboidratos": 0.0, "fibras": 0.0, "sodio": 106, "custo": 8.0, "tipo": "proteina"},
    {"nome": "Salmão", "calorias": 171, "proteinas": 24.0, "gorduras": 7.5, "gordura_saturada": 2.0, "carboidratos": 0.0, "fibras": 0.0, "sodio": 323, "custo": 10.0, "tipo": "proteina"},
    {"nome": "Sardinha", "calorias": 208, "proteinas": 24.6, "gorduras": 11.5, "gordura_saturada": 1.5, "carboidratos": 0.0, "fibras": 0.0, "sodio": 505, "custo": 2.0, "tipo": "proteina"},
    {"nome": "Tilápia", "calorias": 131, "proteinas": 25.5, "gorduras": 3.1, "gordura_saturada": 1.2, "carboidratos": 0.0, "fibras": 0.0, "sodio": 99, "custo": 4.0, "tipo": "proteina"},
    
    # OVOS E LATICÍNIOS
    {"nome": "Iogurte Grego", "calorias": 124, "proteinas": 5.0, "gorduras": 4.8, "gordura_saturada": 2.6, "carboidratos": 15.0, "fibras": 0.0, "sodio": 94, "custo": 1.8, "tipo": "proteina"},
    {"nome": "Iogurte Natural", "calorias": 63, "proteinas": 5.2, "gorduras": 1.55, "gordura_saturada": 1.0, "carboidratos": 7.0, "fibras": 0.0, "sodio": 70, "custo": 1.2, "tipo": "proteina"},
    {"nome": "Leite Desnatado", "calorias": 35, "proteinas": 3.4, "gorduras": 0.5, "gordura_saturada": 0.0, "carboidratos": 5.0, "fibras": 0.0, "sodio": 65, "custo": 0.4, "tipo": "proteina"},
    {"nome": "Leite Integral", "calorias": 59, "proteinas": 3.1, "gorduras": 3.0, "gordura_saturada": 2.1, "carboidratos": 4.8, "fibras": 0.0, "sodio": 55, "custo": 0.4, "tipo": "proteina"},
    {"nome": "Manteiga", "calorias": 740, "proteinas": 1.0, "gorduras": 81.0, "gordura_saturada": 51.0, "carboidratos": 1.0, "fibras": 0.0, "sodio": 680, "custo": 5.0, "tipo": "gordura"},
    {"nome": "Ovo", "calorias": 155, "proteinas": 13.0, "gorduras": 11.0, "gordura_saturada": 3.0, "carboidratos": 1.1, "fibras": 0.0, "sodio": 198, "custo": 0.8, "tipo": "proteina"},
    {"nome": "Ovo Mexido", "calorias": 199, "proteinas": 13.0, "gorduras": 15.2, "gordura_saturada": 5.5, "carboidratos": 2.0, "fibras": 0.0, "sodio": 211, "custo": 0.8, "tipo": "proteina"},
    {"nome": "Queijo Minas", "calorias": 336, "proteinas": 18.9, "gorduras": 26.0, "gordura_saturada": 15.6, "carboidratos": 6.9, "fibras": 0.0, "sodio": 1298, "custo": 3.5, "tipo": "proteina"},
    {"nome": "Queijo Mussarela", "calorias": 300, "proteinas": 23.0, "gorduras": 22.0, "gordura_saturada": 12.0, "carboidratos": 2.0, "fibras": 0.0, "sodio": 598, "custo": 3.6, "tipo": "proteina"},
    {"nome": "Queijo Parmesão", "calorias": 430, "proteinas": 33.0, "gorduras": 33.0, "gordura_saturada": 22.0, "carboidratos": 1.8, "fibras": 0.0, "sodio": 800, "custo": 5.0, "tipo": "proteina"},
    {"nome": "Requeijão", "calorias": 349, "proteinas": 7.5, "gorduras": 34.0, "gordura_saturada": 21.0, "carboidratos": 2.6, "fibras": 0.0, "sodio": 296, "custo": 2.0, "tipo": "proteina"},
    
    # CARBOIDRATOS / CEREAIS
    {"nome": "Arroz Branco", "calorias": 130, "proteinas": 2.7, "gorduras": 0.3, "gordura_saturada": 0.1, "carboidratos": 28.0, "fibras": 0.3, "sodio": 1, "custo": 0.4, "tipo": "carboidrato"},
    {"nome": "Arroz Integral", "calorias": 124, "proteinas": 2.6, "gorduras": 1.0, "gordura_saturada": 0.2, "carboidratos": 25.8, "fibras": 2.7, "sodio": 1, "custo": 0.45, "tipo": "carboidrato"},
    {"nome": "Aveia", "calorias": 394, "proteinas": 17.0, "gorduras": 7.0, "gordura_saturada": 1.2, "carboidratos": 66.0, "fibras": 10.0, "sodio": 0, "custo": 0.7, "tipo": "carboidrato"},
    {"nome": "Cuscuz de Milho", "calorias": 112, "proteinas": 2.5, "gorduras": 0.3, "gordura_saturada": 0.1, "carboidratos": 25.0, "fibras": 2.0, "sodio": 5, "custo": 0.2, "tipo": "carboidrato"},
    {"nome": "Farinha de Mandioca", "calorias": 361, "proteinas": 1.6, "gorduras": 0.3, "gordura_saturada": 0.1, "carboidratos": 87.0, "fibras": 4.0, "sodio": 0, "custo": 0.3, "tipo": "carboidrato"},
    {"nome": "Farinha de Trigo", "calorias": 360, "proteinas": 10.0, "gorduras": 1.4, "gordura_saturada": 0.3, "carboidratos": 75.0, "fibras": 2.4, "sodio": 2, "custo": 0.25, "tipo": "carboidrato"},
    {"nome": "Granola", "calorias": 471, "proteinas": 10.0, "gorduras": 20.0, "gordura_saturada": 3.5, "carboidratos": 64.0, "fibras": 8.0, "sodio": 10, "custo": 1.5, "tipo": "carboidrato"},
    {"nome": "Macarrão", "calorias": 157, "proteinas": 5.8, "gorduras": 0.9, "gordura_saturada": 0.2, "carboidratos": 30.0, "fibras": 1.8, "sodio": 1, "custo": 0.5, "tipo": "carboidrato"},
    {"nome": "Macarrão Instantâneo", "calorias": 440, "proteinas": 9.0, "gorduras": 19.0, "gordura_saturada": 8.0, "carboidratos": 56.0, "fibras": 2.3, "sodio": 1800, "custo": 1.2, "tipo": "carboidrato"},
    {"nome": "Mingau de Aveia", "calorias": 150, "proteinas": 5.0, "gorduras": 3.0, "gordura_saturada": 0.5, "carboidratos": 27.0, "fibras": 4.0, "sodio": 50, "custo": 0.7, "tipo": "carboidrato"},
    {"nome": "Pão de Centeio", "calorias": 240, "proteinas": 9.0, "gorduras": 2.5, "gordura_saturada": 0.5, "carboidratos": 45.0, "fibras": 5.0, "sodio": 400, "custo": 0.9, "tipo": "carboidrato"},
    {"nome": "Pão de Forma", "calorias": 260, "proteinas": 8.0, "gorduras": 4.0, "gordura_saturada": 1.0, "carboidratos": 48.0, "fibras": 1.5, "sodio": 450, "custo": 0.6, "tipo": "carboidrato"},
    {"nome": "Pão Francês", "calorias": 270, "proteinas": 8.0, "gorduras": 1.5, "gordura_saturada": 0.5, "carboidratos": 58.0, "fibras": 2.1, "sodio": 550, "custo": 0.5, "tipo": "carboidrato"},
    {"nome": "Pão Integral", "calorias": 265, "proteinas": 9.0, "gorduras": 3.2, "gordura_saturada": 0.6, "carboidratos": 49.0, "fibras": 6.5, "sodio": 400, "custo": 0.8, "tipo": "carboidrato"},
    {"nome": "Tapioca", "calorias": 150, "proteinas": 0.2, "gorduras": 0.1, "gordura_saturada": 0.0, "carboidratos": 36.0, "fibras": 0.0, "sodio": 2, "custo": 0.5, "tipo": "carboidrato"},
    
    # LEGUMINOSAS
    {"nome": "Ervilha", "calorias": 84, "proteinas": 5.0, "gorduras": 0.4, "gordura_saturada": 0.1, "carboidratos": 15.0, "fibras": 5.0, "sodio": 1, "custo": 0.7, "tipo": "carboidrato"},
    {"nome": "Feijão Preto", "calorias": 77, "proteinas": 5.1, "gorduras": 0.5, "gordura_saturada": 0.1, "carboidratos": 14.0, "fibras": 8.4, "sodio": 1, "custo": 0.5, "tipo": "carboidrato"},
    {"nome": "Feijão Carioca", "calorias": 76, "proteinas": 4.8, "gorduras": 0.5, "gordura_saturada": 0.1, "carboidratos": 14.0, "fibras": 8.0, "sodio": 2, "custo": 0.5, "tipo": "carboidrato"},
    {"nome": "Grão-de-bico", "calorias": 164, "proteinas": 9.0, "gorduras": 2.6, "gordura_saturada": 0.3, "carboidratos": 27.0, "fibras": 7.6, "sodio": 5, "custo": 0.8, "tipo": "carboidrato"},
    {"nome": "Lentilha", "calorias": 116, "proteinas": 9.0, "gorduras": 0.4, "gordura_saturada": 0.1, "carboidratos": 20.0, "fibras": 8.0, "sodio": 2, "custo": 0.6, "tipo": "carboidrato"},
    {"nome": "Soja", "calorias": 172, "proteinas": 16.0, "gorduras": 9.0, "gordura_saturada": 1.3, "carboidratos": 7.0, "fibras": 6.0, "sodio": 2, "custo": 0.9, "tipo": "carboidrato"},
    
    # TUBÉRCULOS
    {"nome": "Batata Inglesa", "calorias": 86, "proteinas": 1.7, "gorduras": 0.1, "gordura_saturada": 0.0, "carboidratos": 20.0, "fibras": 1.4, "sodio": 5, "custo": 0.3, "tipo": "carboidrato"},
    {"nome": "Batata Doce", "calorias": 86, "proteinas": 1.6, "gorduras": 0.1, "gordura_saturada": 0.0, "carboidratos": 20.0, "fibras": 3.0, "sodio": 5, "custo": 0.6, "tipo": "carboidrato"},
    {"nome": "Cará", "calorias": 78, "proteinas": 1.8, "gorduras": 0.1, "gordura_saturada": 0.0, "carboidratos": 19.0, "fibras": 1.3, "sodio": 4, "custo": 0.4, "tipo": "carboidrato"},
    {"nome": "Inhame", "calorias": 97, "proteinas": 1.7, "gorduras": 0.2, "gordura_saturada": 0.0, "carboidratos": 23.0, "fibras": 1.5, "sodio": 3, "custo": 0.4, "tipo": "carboidrato"},
    {"nome": "Mandioca", "calorias": 125, "proteinas": 1.5, "gorduras": 0.3, "gordura_saturada": 0.1, "carboidratos": 30.0, "fibras": 1.7, "sodio": 4, "custo": 0.4, "tipo": "carboidrato"},
    
    # VEGETAIS
    {"nome": "Abobrinha", "calorias": 15, "proteinas": 1.1, "gorduras": 0.3, "gordura_saturada": 0.0, "carboidratos": 2.9, "fibras": 1.2, "sodio": 2, "custo": 0.7, "tipo": "vegetal"},
    {"nome": "Alface", "calorias": 15, "proteinas": 1.2, "gorduras": 0.2, "gordura_saturada": 0.0, "carboidratos": 2.9, "fibras": 1.3, "sodio": 5, "custo": 0.2, "tipo": "vegetal"},
    {"nome": "Beterraba", "calorias": 49, "proteinas": 1.8, "gorduras": 0.1, "gordura_saturada": 0.0, "carboidratos": 11.0, "fibras": 3.4, "sodio": 60, "custo": 0.5, "tipo": "vegetal"},
    {"nome": "Brócolis", "calorias": 55, "proteinas": 3.7, "gorduras": 0.6, "gordura_saturada": 0.0, "carboidratos": 11.0, "fibras": 3.3, "sodio": 30, "custo": 1.2, "tipo": "vegetal"},
    {"nome": "Cenoura", "calorias": 35, "proteinas": 0.8, "gorduras": 0.2, "gordura_saturada": 0.0, "carboidratos": 8.0, "fibras": 3.0, "sodio": 35, "custo": 0.6, "tipo": "vegetal"},
    {"nome": "Couve Flor", "calorias": 30, "proteinas": 2.2, "gorduras": 0.3, "gordura_saturada": 0.0, "carboidratos": 5.2, "fibras": 2.3, "sodio": 25, "custo": 1.0, "tipo": "vegetal"},
    {"nome": "Milho Verde", "calorias": 98, "proteinas": 3.4, "gorduras": 1.7, "gordura_saturada": 0.2, "carboidratos": 17.0, "fibras": 2.4, "sodio": 2, "custo": 0.7, "tipo": "vegetal"},
    {"nome": "Pepino", "calorias": 12, "proteinas": 0.7, "gorduras": 0.1, "gordura_saturada": 0.0, "carboidratos": 2.2, "fibras": 0.8, "sodio": 2, "custo": 0.4, "tipo": "vegetal"},
    {"nome": "Repolho", "calorias": 23, "proteinas": 1.2, "gorduras": 0.1, "gordura_saturada": 0.0, "carboidratos": 5.2, "fibras": 2.9, "sodio": 10, "custo": 0.6, "tipo": "vegetal"},
    {"nome": "Tomate", "calorias": 18, "proteinas": 0.9, "gorduras": 0.2, "gordura_saturada": 0.0, "carboidratos": 3.9, "fibras": 1.2, "sodio": 5, "custo": 0.4, "tipo": "vegetal"},
    {"nome": "Vagem", "calorias": 31, "proteinas": 1.8, "gorduras": 0.2, "gordura_saturada": 0.0, "carboidratos": 7.0, "fibras": 3.2, "sodio": 5, "custo": 0.6, "tipo": "vegetal"},
    
    # FRUTAS
    {"nome": "Abacate", "calorias": 160, "proteinas": 2.0, "gorduras": 14.0, "gordura_saturada": 2.1, "carboidratos": 8.5, "fibras": 6.7, "sodio": 2, "custo": 1.2, "tipo": "fruta"},
    {"nome": "Abacaxi", "calorias": 50, "proteinas": 0.5, "gorduras": 0.1, "gordura_saturada": 0.0, "carboidratos": 13.0, "fibras": 1.4, "sodio": 1, "custo": 0.4, "tipo": "fruta"},
    {"nome": "Banana Prata", "calorias": 89, "proteinas": 1.1, "gorduras": 0.3, "gordura_saturada": 0.1, "carboidratos": 23.0, "fibras": 2.6, "sodio": 1, "custo": 0.4, "tipo": "fruta"},
    {"nome": "Laranja", "calorias": 46, "proteinas": 0.9, "gorduras": 0.1, "gordura_saturada": 0.0, "carboidratos": 12.0, "fibras": 2.4, "sodio": 0, "custo": 0.3, "tipo": "fruta"},
    {"nome": "Maçã", "calorias": 52, "proteinas": 0.3, "gorduras": 0.2, "gordura_saturada": 0.0, "carboidratos": 14.0, "fibras": 2.4, "sodio": 1, "custo": 0.5, "tipo": "fruta"},
    {"nome": "Mamão", "calorias": 45, "proteinas": 0.5, "gorduras": 0.2, "gordura_saturada": 0.0, "carboidratos": 12.0, "fibras": 1.4, "sodio": 3, "custo": 0.4, "tipo": "fruta"},
    {"nome": "Melancia", "calorias": 30, "proteinas": 0.6, "gorduras": 0.2, "gordura_saturada": 0.0, "carboidratos": 7.6, "fibras": 0.3, "sodio": 1, "custo": 0.2, "tipo": "fruta"},
    {"nome": "Morango", "calorias": 32, "proteinas": 0.8, "gorduras": 0.3, "gordura_saturada": 0.0, "carboidratos": 7.7, "fibras": 2.0, "sodio": 1, "custo": 1.0, "tipo": "fruta"},
    {"nome": "Pera", "calorias": 57, "proteinas": 0.4, "gorduras": 0.1, "gordura_saturada": 0.0, "carboidratos": 15.0, "fibras": 3.1, "sodio": 1, "custo": 0.6, "tipo": "fruta"},
    {"nome": "Tangerina", "calorias": 50, "proteinas": 0.8, "gorduras": 0.3, "gordura_saturada": 0.0, "carboidratos": 13.0, "fibras": 1.8, "sodio": 1, "custo": 0.3, "tipo": "fruta"},
    {"nome": "Uva", "calorias": 67, "proteinas": 0.7, "gorduras": 0.4, "gordura_saturada": 0.1, "carboidratos": 17.0, "fibras": 0.9, "sodio": 1, "custo": 0.8, "tipo": "fruta"},

    # OLEAGINOSAS
    {"nome": "Amendoim", "calorias": 567, "proteinas": 26.0, "gorduras": 49.0, "gordura_saturada": 6.8, "carboidratos": 16.0, "fibras": 8.5, "sodio": 5, "custo": 2.5, "tipo": "gordura"},
    {"nome": "Amêndoas", "calorias": 576, "proteinas": 21.0, "gorduras": 49.0, "gordura_saturada": 3.7, "carboidratos": 22.0, "fibras": 12.5, "sodio": 1, "custo": 6.0, "tipo": "gordura"},
    {"nome": "Castanha de Caju", "calorias": 553, "proteinas": 18.0, "gorduras": 44.0, "gordura_saturada": 7.8, "carboidratos": 30.0, "fibras": 3.3, "sodio": 10, "custo": 4.0, "tipo": "gordura"},
    {"nome": "Castanha do Pará", "calorias": 659, "proteinas": 14.0, "gorduras": 67.0, "gordura_saturada": 15.0, "carboidratos": 11.0, "fibras": 7.5, "sodio": 2, "custo": 4.5, "tipo": "gordura"},
    {"nome": "Nozes", "calorias": 588, "proteinas": 15.0, "gorduras": 59.0, "gordura_saturada": 6.1, "carboidratos": 18.0, "fibras": 6.7, "sodio": 2, "custo": 6.0, "tipo": "gordura"},
    
    # GORDURAS
    {"nome": "Azeite de Oliva", "calorias": 884, "proteinas": 0.0, "gorduras": 100.0, "gordura_saturada": 14.0, "carboidratos": 0.0, "fibras": 0.0, "sodio": 0, "custo": 4.0, "tipo": "gordura"},
    {"nome": "Margarina", "calorias": 720, "proteinas": 0.0, "gorduras": 80.0, "gordura_saturada": 20.0, "carboidratos": 0.0, "fibras": 0.0, "sodio": 700, "custo": 1.0, "tipo": "gordura"},
    {"nome": "Óleo de Soja", "calorias": 884, "proteinas": 0.0, "gorduras": 100.0, "gordura_saturada": 15.0, "carboidratos": 0.0, "fibras": 0.0, "sodio": 0, "custo": 0.7, "tipo": "gordura"},
    {"nome": "Óleo de Canola", "calorias": 884, "proteinas": 0.0, "gorduras": 100.0, "gordura_saturada": 7.0, "carboidratos": 0.0, "fibras": 0.0, "sodio": 0, "custo": 1.2, "tipo": "gordura"},
    
    # INDUSTRIALIZADOS / LANCHES
    {"nome": "Batata Frita Congelada", "calorias": 312, "proteinas": 3.4, "gorduras": 15.0, "gordura_saturada": 2.0, "carboidratos": 41.0, "fibras": 3.5, "sodio": 600, "custo": 1.5, "tipo": "carboidrato"},
    {"nome": "Mortadela", "calorias": 280, "proteinas": 13.0, "gorduras": 23.0, "gordura_saturada": 8.0, "carboidratos": 2.0, "fibras": 0.0, "sodio": 1200, "custo": 2.0, "tipo": "proteina"},
    {"nome": "Nuggets de Frango", "calorias": 290, "proteinas": 15.0, "gorduras": 20.0, "gordura_saturada": 4.0, "carboidratos": 15.0, "fibras": 1.0, "sodio": 800, "custo": 2.5, "tipo": "proteina"},
    {"nome": "Peito de Peru", "calorias": 110, "proteinas": 17.0, "gorduras": 2.0, "gordura_saturada": 0.5, "carboidratos": 2.0, "fibras": 0.0, "sodio": 950, "custo": 3.0, "tipo": "proteina"},
    {"nome": "Pão de Queijo", "calorias": 360, "proteinas": 5.0, "gorduras": 20.0, "gordura_saturada": 10.0, "carboidratos": 38.0, "fibras": 1.0, "sodio": 600, "custo": 1.5, "tipo": "carboidrato"},
    {"nome": "Presunto", "calorias": 110, "proteinas": 18.0, "gorduras": 4.0, "gordura_saturada": 1.5, "carboidratos": 1.0, "fibras": 0.0, "sodio": 1100, "custo": 2.0, "tipo": "proteina"},
    {"nome": "Salsicha", "calorias": 290, "proteinas": 12.0, "gorduras": 25.0, "gordura_saturada": 9.0, "carboidratos": 2.0, "fibras": 0.0, "sodio": 1200, "custo": 1.5, "tipo": "proteina"}
]


# GRUPOS DE EXCLUSÃO MÚTUA
# Alimentos similares que não devem aparecer juntos no mesmo dia
grupos_exclusao_mutua = {
    'feijao': ['Feijão Preto', 'Feijão Carioca'],
    'linguica': ['Linguiça de Frango', 'Linguiça Toscana'],
    'batata': ['Batata Inglesa', 'Batata Doce'],
    'arroz': ['Arroz Branco', 'Arroz Integral'],
    'pao': ['Pão Francês', 'Pão de Forma', 'Pão Integral', 'Pão de Centeio'],
    'leite': ['Leite Integral', 'Leite Desnatado'],
    'iogurte': ['Iogurte Natural', 'Iogurte Grego'],
    'queijo': ['Queijo Minas', 'Queijo Mussarela', 'Queijo Parmesão'],
    'carne_bovina': ['Alcatra', 'Picanha', 'Bife de Patinho', 'Coxão Duro'],
    'carne_moida': ['Carne Moída Acém', 'Carne Moída Patinho'],
    'frango': ['Peito de Frango', 'Coxa de Frango', 'Asa de Frango'],
    'peixe': ['Salmão', 'Tilápia', 'Atum', 'Bacalhau', 'Sardinha'],
    'oleo': ['Óleo de Soja', 'Óleo de Canola', 'Azeite de Oliva']
}


def obter_grupo_exclusao(nome_alimento: str) -> str | None:
    """
    Retorna o grupo de exclusão mútua ao qual o alimento pertence.
    
    Args:
        nome_alimento: Nome do alimento
        
    Returns:
        Nome do grupo ou None se não pertencer a nenhum grupo
    """
    for grupo, alimentos in grupos_exclusao_mutua.items():
        if nome_alimento in alimentos:
            return grupo
    return None


def verificar_conflito_exclusao(alimentos_dia: list[str]) -> bool:
    """
    Verifica se há alimentos conflitantes (do mesmo grupo) no dia.
    
    Args:
        alimentos_dia: Lista com nomes dos alimentos do dia
        
    Returns:
        True se há conflito, False caso contrário
    """
    grupos_usados = {}
    
    for alimento in alimentos_dia:
        grupo = obter_grupo_exclusao(alimento)
        if grupo:
            if grupo in grupos_usados:
                # Conflito detectado!
                return True
            grupos_usados[grupo] = alimento
    
    return False


def criar_base_dados() -> pd.DataFrame:
    """
    Cria e retorna a base de dados de alimentos como DataFrame do Pandas.
    
    Realiza processamento automático:
    - Converte lista de dicts para DataFrame
    - Calcula gorduras insaturadas (gordura total - saturada)
    - Valida consistência dos dados
    - Garante tipos corretos das colunas
    
    Returns:
        DataFrame com todos os alimentos e suas informações nutricionais
    """
    # Converte para DataFrame
    df = pd.DataFrame(alimentos)
    
    # Calcula gorduras insaturadas (mono + poli = total - saturada)
    df['gorduras_insaturadas'] = df['gorduras'] - df['gordura_saturada']
    
    # Garante que não fique negativo (proteção contra erros de input)
    df['gorduras_insaturadas'] = df['gorduras_insaturadas'].clip(lower=0)
    
    # Validações básicas
    assert len(df) > 0, "Base de dados vazia!"
    assert df['calorias'].min() >= 0, "Calorias não podem ser negativas!"
    assert df['custo'].min() >= 0, "Custo não pode ser negativo!"
    
    return df.copy()
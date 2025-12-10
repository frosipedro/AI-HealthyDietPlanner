import pandas as pd

# Lista de alimentos com todas as informações nutricionais
alimentos = [
    # PROTEÍNAS ANIMAIS
    {"nome": "Peito de Frango", "calorias": 165, "proteinas": 31.0, "gorduras": 3.6, "gordura_saturada": 1.0, "carboidratos": 0.0, "fibras": 0.0, "sodio": 60, "custo": 1.8, "tipo": "proteina"},
    {"nome": "Coxa de Frango", "calorias": 215, "proteinas": 28.0, "gorduras": 10.0, "gordura_saturada": 2.5, "carboidratos": 0.0, "fibras": 0.0, "sodio": 75, "custo": 1.6, "tipo": "proteina"},
    {"nome": "Asa de Frango", "calorias": 290, "proteinas": 24.0, "gorduras": 21.0, "gordura_saturada": 6.0, "carboidratos": 0.0, "fibras": 0.0, "sodio": 80, "custo": 1.8, "tipo": "proteina"},
    {"nome": "Carne Moída Patinho", "calorias": 212, "proteinas": 27.0, "gorduras": 11.0, "gordura_saturada": 4.0, "carboidratos": 0.0, "fibras": 0.0, "sodio": 60, "custo": 3.5, "tipo": "proteina"},
    {"nome": "Carne Moída Acém", "calorias": 250, "proteinas": 26.0, "gorduras": 17.0, "gordura_saturada": 6.5, "carboidratos": 0.0, "fibras": 0.0, "sodio": 65, "custo": 2.6, "tipo": "proteina"},
    {"nome": "Bife de Patinho", "calorias": 180, "proteinas": 29.0, "gorduras": 6.0, "gordura_saturada": 2.5, "carboidratos": 0.0, "fibras": 0.0, "sodio": 60, "custo": 4.2, "tipo": "proteina"},
    {"nome": "Picanha", "calorias": 289, "proteinas": 22.0, "gorduras": 23.0, "gordura_saturada": 10.0, "carboidratos": 0.0, "fibras": 0.0, "sodio": 60, "custo": 8.0, "tipo": "proteina"},
    {"nome": "Alcatra", "calorias": 220, "proteinas": 29.0, "gorduras": 10.0, "gordura_saturada": 4.0, "carboidratos": 0.0, "fibras": 0.0, "sodio": 60, "custo": 6.0, "tipo": "proteina"},
    {"nome": "Coxão Duro", "calorias": 215, "proteinas": 28.0, "gorduras": 9.0, "gordura_saturada": 3.5, "carboidratos": 0.0, "fibras": 0.0, "sodio": 60, "custo": 3.5, "tipo": "proteina"},
    {"nome": "Carne Seca", "calorias": 239, "proteinas": 24.0, "gorduras": 12.0, "gordura_saturada": 5.0, "carboidratos": 0.0, "fibras": 0.0, "sodio": 2500, "custo": 5.0, "tipo": "proteina"},
    {"nome": "Linguiça Toscana", "calorias": 330, "proteinas": 16.0, "gorduras": 28.0, "gordura_saturada": 10.0, "carboidratos": 1.0, "fibras": 0.0, "sodio": 1100, "custo": 3.0, "tipo": "proteina"},
    {"nome": "Linguiça de Frango", "calorias": 260, "proteinas": 18.0, "gorduras": 19.0, "gordura_saturada": 6.0, "carboidratos": 1.0, "fibras": 0.0, "sodio": 900, "custo": 2.5, "tipo": "proteina"},
    {"nome": "Lombo Suíno", "calorias": 210, "proteinas": 29.0, "gorduras": 9.0, "gordura_saturada": 3.0, "carboidratos": 0.0, "fibras": 0.0, "sodio": 55, "custo": 3.0, "tipo": "proteina"},
    {"nome": "Pernil Suíno", "calorias": 240, "proteinas": 27.0, "gorduras": 13.0, "gordura_saturada": 4.5, "carboidratos": 0.0, "fibras": 0.0, "sodio": 65, "custo": 2.6, "tipo": "proteina"},
    {"nome": "Bacon", "calorias": 540, "proteinas": 37.0, "gorduras": 42.0, "gordura_saturada": 14.0, "carboidratos": 1.4, "fibras": 0.0, "sodio": 1200, "custo": 5.0, "tipo": "gordura"},
    {"nome": "Salmão", "calorias": 208, "proteinas": 20.0, "gorduras": 13.0, "gordura_saturada": 3.0, "carboidratos": 0.0, "fibras": 0.0, "sodio": 50, "custo": 10.0, "tipo": "proteina"},
    {"nome": "Tilápia", "calorias": 128, "proteinas": 26.0, "gorduras": 2.0, "gordura_saturada": 0.9, "carboidratos": 0.0, "fibras": 0.0, "sodio": 40, "custo": 4.0, "tipo": "proteina"},
    {"nome": "Sardinha", "calorias": 185, "proteinas": 25.0, "gorduras": 9.0, "gordura_saturada": 2.5, "carboidratos": 0.0, "fibras": 0.0, "sodio": 300, "custo": 2.0, "tipo": "proteina"},
    {"nome": "Atum", "calorias": 130, "proteinas": 29.0, "gorduras": 0.6, "gordura_saturada": 0.2, "carboidratos": 0.0, "fibras": 0.0, "sodio": 40, "custo": 4.5, "tipo": "proteina"},
    {"nome": "Camarão", "calorias": 99, "proteinas": 24.0, "gorduras": 0.3, "gordura_saturada": 0.1, "carboidratos": 0.2, "fibras": 0.0, "sodio": 148, "custo": 15.0, "tipo": "proteina"},
    {"nome": "Bacalhau", "calorias": 105, "proteinas": 23.0, "gorduras": 0.9, "gordura_saturada": 0.2, "carboidratos": 0.0, "fibras": 0.0, "sodio": 70, "custo": 12.0, "tipo": "proteina"},
    
    # OVOS E LATICÍNIOS
    {"nome": "Ovo", "calorias": 155, "proteinas": 13.0, "gorduras": 11.0, "gordura_saturada": 3.0, "carboidratos": 1.1, "fibras": 0.0, "sodio": 130, "custo": 0.8, "tipo": "proteina"},
    {"nome": "Ovo Mexido", "calorias": 160, "proteinas": 12.0, "gorduras": 12.0, "gordura_saturada": 3.5, "carboidratos": 2.0, "fibras": 0.0, "sodio": 150, "custo": 0.8, "tipo": "proteina"},
    {"nome": "Queijo Minas", "calorias": 280, "proteinas": 17.0, "gorduras": 22.0, "gordura_saturada": 14.0, "carboidratos": 1.3, "fibras": 0.0, "sodio": 200, "custo": 3.5, "tipo": "proteina"},
    {"nome": "Queijo Mussarela", "calorias": 300, "proteinas": 22.0, "gorduras": 22.0, "gordura_saturada": 14.0, "carboidratos": 2.3, "fibras": 0.0, "sodio": 400, "custo": 3.6, "tipo": "proteina"},
    {"nome": "Queijo Parmesão", "calorias": 392, "proteinas": 35.0, "gorduras": 26.0, "gordura_saturada": 17.0, "carboidratos": 1.8, "fibras": 0.0, "sodio": 1200, "custo": 5.0, "tipo": "proteina"},
    {"nome": "Requeijão", "calorias": 257, "proteinas": 7.5, "gorduras": 23.0, "gordura_saturada": 14.0, "carboidratos": 3.0, "fibras": 0.0, "sodio": 500, "custo": 2.0, "tipo": "gordura"},
    {"nome": "Leite Integral", "calorias": 61, "proteinas": 3.2, "gorduras": 3.4, "gordura_saturada": 2.1, "carboidratos": 5.0, "fibras": 0.0, "sodio": 50, "custo": 0.4, "tipo": "proteina"},
    {"nome": "Leite Desnatado", "calorias": 42, "proteinas": 3.4, "gorduras": 0.2, "gordura_saturada": 0.1, "carboidratos": 5.0, "fibras": 0.0, "sodio": 50, "custo": 0.4, "tipo": "proteina"},
    {"nome": "Iogurte Natural", "calorias": 60, "proteinas": 4.0, "gorduras": 3.0, "gordura_saturada": 1.9, "carboidratos": 6.0, "fibras": 0.0, "sodio": 45, "custo": 1.2, "tipo": "proteina"},
    {"nome": "Iogurte Grego", "calorias": 115, "proteinas": 7.0, "gorduras": 5.0, "gordura_saturada": 3.0, "carboidratos": 9.0, "fibras": 0.0, "sodio": 40, "custo": 1.8, "tipo": "proteina"},
    {"nome": "Manteiga", "calorias": 720, "proteinas": 0.5, "gorduras": 81.0, "gordura_saturada": 51.0, "carboidratos": 0.0, "fibras": 0.0, "sodio": 10, "custo": 5.0, "tipo": "gordura"},
    
    # CARBOIDRATOS / CEREAIS
    {"nome": "Arroz Branco", "calorias": 130, "proteinas": 2.7, "gorduras": 0.3, "gordura_saturada": 0.1, "carboidratos": 28.0, "fibras": 0.3, "sodio": 1, "custo": 0.4, "tipo": "carboidrato"},
    {"nome": "Arroz Integral", "calorias": 124, "proteinas": 2.6, "gorduras": 1.0, "gordura_saturada": 0.2, "carboidratos": 25.8, "fibras": 2.7, "sodio": 1, "custo": 0.45, "tipo": "carboidrato"},
    {"nome": "Macarrão", "calorias": 157, "proteinas": 5.8, "gorduras": 0.9, "gordura_saturada": 0.2, "carboidratos": 30.0, "fibras": 1.8, "sodio": 1, "custo": 0.5, "tipo": "carboidrato"},
    {"nome": "Macarrão Instantâneo", "calorias": 440, "proteinas": 9.0, "gorduras": 19.0, "gordura_saturada": 8.0, "carboidratos": 56.0, "fibras": 2.3, "sodio": 1800, "custo": 1.2, "tipo": "carboidrato"},
    {"nome": "Aveia", "calorias": 394, "proteinas": 17.0, "gorduras": 7.0, "gordura_saturada": 1.2, "carboidratos": 66.0, "fibras": 10.0, "sodio": 0, "custo": 0.7, "tipo": "carboidrato"},
    {"nome": "Farinha de Mandioca", "calorias": 361, "proteinas": 1.6, "gorduras": 0.3, "gordura_saturada": 0.1, "carboidratos": 87.0, "fibras": 4.0, "sodio": 0, "custo": 0.3, "tipo": "carboidrato"},
    {"nome": "Farinha de Trigo", "calorias": 360, "proteinas": 10.0, "gorduras": 1.4, "gordura_saturada": 0.3, "carboidratos": 75.0, "fibras": 2.4, "sodio": 2, "custo": 0.25, "tipo": "carboidrato"},
    {"nome": "Cuscuz de Milho", "calorias": 112, "proteinas": 2.5, "gorduras": 0.3, "gordura_saturada": 0.1, "carboidratos": 25.0, "fibras": 2.0, "sodio": 5, "custo": 0.2, "tipo": "carboidrato"},
    {"nome": "Pão Francês", "calorias": 270, "proteinas": 8.0, "gorduras": 1.5, "gordura_saturada": 0.5, "carboidratos": 58.0, "fibras": 2.1, "sodio": 550, "custo": 0.5, "tipo": "carboidrato"},
    {"nome": "Pão Integral", "calorias": 265, "proteinas": 9.0, "gorduras": 3.2, "gordura_saturada": 0.6, "carboidratos": 49.0, "fibras": 6.5, "sodio": 400, "custo": 0.8, "tipo": "carboidrato"},
    {"nome": "Tapioca", "calorias": 150, "proteinas": 0.2, "gorduras": 0.1, "gordura_saturada": 0.0, "carboidratos": 36.0, "fibras": 0.0, "sodio": 2, "custo": 0.5, "tipo": "carboidrato"},
    {"nome": "Pão de Forma", "calorias": 260, "proteinas": 8.0, "gorduras": 4.0, "gordura_saturada": 1.0, "carboidratos": 48.0, "fibras": 1.5, "sodio": 450, "custo": 0.6, "tipo": "carboidrato"},
    {"nome": "Pão de Centeio", "calorias": 240, "proteinas": 9.0, "gorduras": 2.5, "gordura_saturada": 0.5, "carboidratos": 45.0, "fibras": 5.0, "sodio": 400, "custo": 0.9, "tipo": "carboidrato"},
    {"nome": "Granola", "calorias": 471, "proteinas": 10.0, "gorduras": 20.0, "gordura_saturada": 3.5, "carboidratos": 64.0, "fibras": 8.0, "sodio": 10, "custo": 1.5, "tipo": "carboidrato"},
    {"nome": "Mingau de Aveia", "calorias": 150, "proteinas": 5.0, "gorduras": 3.0, "gordura_saturada": 0.5, "carboidratos": 27.0, "fibras": 4.0, "sodio": 50, "custo": 0.7, "tipo": "carboidrato"},
    
    # LEGUMINOSAS
    {"nome": "Feijão Preto", "calorias": 77, "proteinas": 5.1, "gorduras": 0.5, "gordura_saturada": 0.1, "carboidratos": 14.0, "fibras": 8.4, "sodio": 1, "custo": 0.5, "tipo": "carboidrato"},
    {"nome": "Feijão Carioca", "calorias": 85, "proteinas": 5.6, "gorduras": 0.5, "gordura_saturada": 0.1, "carboidratos": 14.0, "fibras": 8.0, "sodio": 1, "custo": 0.5, "tipo": "carboidrato"},
    {"nome": "Lentilha", "calorias": 116, "proteinas": 9.0, "gorduras": 0.4, "gordura_saturada": 0.1, "carboidratos": 20.0, "fibras": 8.0, "sodio": 2, "custo": 0.6, "tipo": "carboidrato"},
    {"nome": "Grão-de-bico", "calorias": 164, "proteinas": 9.0, "gorduras": 2.6, "gordura_saturada": 0.3, "carboidratos": 27.0, "fibras": 7.6, "sodio": 5, "custo": 0.8, "tipo": "carboidrato"},
    {"nome": "Ervilha", "calorias": 84, "proteinas": 5.0, "gorduras": 0.4, "gordura_saturada": 0.1, "carboidratos": 15.0, "fibras": 5.0, "sodio": 1, "custo": 0.7, "tipo": "carboidrato"},
    {"nome": "Soja", "calorias": 172, "proteinas": 16.0, "gorduras": 9.0, "gordura_saturada": 1.3, "carboidratos": 7.0, "fibras": 6.0, "sodio": 2, "custo": 0.9, "tipo": "carboidrato"},
    
    # TUBÉRCULOS
    {"nome": "Batata Inglesa", "calorias": 86, "proteinas": 1.7, "gorduras": 0.1, "gordura_saturada": 0.0, "carboidratos": 20.0, "fibras": 1.4, "sodio": 5, "custo": 0.3, "tipo": "carboidrato"},
    {"nome": "Batata Doce", "calorias": 86, "proteinas": 1.6, "gorduras": 0.1, "gordura_saturada": 0.0, "carboidratos": 20.0, "fibras": 3.0, "sodio": 5, "custo": 0.6, "tipo": "carboidrato"},
    {"nome": "Mandioca", "calorias": 125, "proteinas": 1.5, "gorduras": 0.3, "gordura_saturada": 0.1, "carboidratos": 30.0, "fibras": 1.7, "sodio": 4, "custo": 0.4, "tipo": "carboidrato"},
    {"nome": "Inhame", "calorias": 97, "proteinas": 1.7, "gorduras": 0.2, "gordura_saturada": 0.0, "carboidratos": 23.0, "fibras": 1.5, "sodio": 3, "custo": 0.4, "tipo": "carboidrato"},
    {"nome": "Cará", "calorias": 78, "proteinas": 1.8, "gorduras": 0.1, "gordura_saturada": 0.0, "carboidratos": 19.0, "fibras": 1.3, "sodio": 4, "custo": 0.4, "tipo": "carboidrato"},
    
    # VEGETAIS
    {"nome": "Brócolis", "calorias": 55, "proteinas": 3.7, "gorduras": 0.6, "gordura_saturada": 0.0, "carboidratos": 11.0, "fibras": 3.3, "sodio": 30, "custo": 1.2, "tipo": "vegetal"},
    {"nome": "Couve Flor", "calorias": 30, "proteinas": 2.2, "gorduras": 0.3, "gordura_saturada": 0.0, "carboidratos": 5.2, "fibras": 2.3, "sodio": 25, "custo": 1.0, "tipo": "vegetal"},
    {"nome": "Cenoura", "calorias": 35, "proteinas": 0.8, "gorduras": 0.2, "gordura_saturada": 0.0, "carboidratos": 8.0, "fibras": 3.0, "sodio": 35, "custo": 0.6, "tipo": "vegetal"},
    {"nome": "Beterraba", "calorias": 49, "proteinas": 1.8, "gorduras": 0.1, "gordura_saturada": 0.0, "carboidratos": 11.0, "fibras": 3.4, "sodio": 60, "custo": 0.5, "tipo": "vegetal"},
    {"nome": "Abobrinha", "calorias": 15, "proteinas": 1.1, "gorduras": 0.3, "gordura_saturada": 0.0, "carboidratos": 2.9, "fibras": 1.2, "sodio": 2, "custo": 0.7, "tipo": "vegetal"},
    {"nome": "Alface", "calorias": 15, "proteinas": 1.2, "gorduras": 0.2, "gordura_saturada": 0.0, "carboidratos": 2.9, "fibras": 1.3, "sodio": 5, "custo": 0.2, "tipo": "vegetal"},
    {"nome": "Tomate", "calorias": 18, "proteinas": 0.9, "gorduras": 0.2, "gordura_saturada": 0.0, "carboidratos": 3.9, "fibras": 1.2, "sodio": 5, "custo": 0.4, "tipo": "vegetal"},
    {"nome": "Pepino", "calorias": 12, "proteinas": 0.7, "gorduras": 0.1, "gordura_saturada": 0.0, "carboidratos": 2.2, "fibras": 0.8, "sodio": 2, "custo": 0.4, "tipo": "vegetal"},
    {"nome": "Repolho", "calorias": 23, "proteinas": 1.2, "gorduras": 0.1, "gordura_saturada": 0.0, "carboidratos": 5.2, "fibras": 2.9, "sodio": 10, "custo": 0.6, "tipo": "vegetal"},
    {"nome": "Vagem", "calorias": 31, "proteinas": 1.8, "gorduras": 0.2, "gordura_saturada": 0.0, "carboidratos": 7.0, "fibras": 3.2, "sodio": 5, "custo": 0.6, "tipo": "vegetal"},
    {"nome": "Milho Verde", "calorias": 98, "proteinas": 3.4, "gorduras": 1.7, "gordura_saturada": 0.2, "carboidratos": 17.0, "fibras": 2.4, "sodio": 2, "custo": 0.7, "tipo": "vegetal"},
    
    # FRUTAS
    {"nome": "Banana Prata", "calorias": 89, "proteinas": 1.1, "gorduras": 0.3, "gordura_saturada": 0.1, "carboidratos": 23.0, "fibras": 2.6, "sodio": 1, "custo": 0.4, "tipo": "fruta"},
    {"nome": "Banana Nanica", "calorias": 92, "proteinas": 1.2, "gorduras": 0.3, "gordura_saturada": 0.1, "carboidratos": 23.0, "fibras": 2.6, "sodio": 1, "custo": 0.4, "tipo": "fruta"},
    {"nome": "Maçã", "calorias": 52, "proteinas": 0.3, "gorduras": 0.2, "gordura_saturada": 0.0, "carboidratos": 14.0, "fibras": 2.4, "sodio": 1, "custo": 0.5, "tipo": "fruta"},
    {"nome": "Pera", "calorias": 57, "proteinas": 0.4, "gorduras": 0.1, "gordura_saturada": 0.0, "carboidratos": 15.0, "fibras": 3.1, "sodio": 1, "custo": 0.6, "tipo": "fruta"},
    {"nome": "Melancia", "calorias": 30, "proteinas": 0.6, "gorduras": 0.2, "gordura_saturada": 0.0, "carboidratos": 7.6, "fibras": 0.3, "sodio": 1, "custo": 0.2, "tipo": "fruta"},
    {"nome": "Mamão", "calorias": 45, "proteinas": 0.5, "gorduras": 0.2, "gordura_saturada": 0.0, "carboidratos": 12.0, "fibras": 1.4, "sodio": 3, "custo": 0.4, "tipo": "fruta"},
    {"nome": "Laranja", "calorias": 46, "proteinas": 0.9, "gorduras": 0.1, "gordura_saturada": 0.0, "carboidratos": 12.0, "fibras": 2.4, "sodio": 0, "custo": 0.3, "tipo": "fruta"},
    {"nome": "Tangerina", "calorias": 50, "proteinas": 0.8, "gorduras": 0.3, "gordura_saturada": 0.0, "carboidratos": 13.0, "fibras": 1.8, "sodio": 1, "custo": 0.3, "tipo": "fruta"},
    {"nome": "Morango", "calorias": 32, "proteinas": 0.8, "gorduras": 0.3, "gordura_saturada": 0.0, "carboidratos": 7.7, "fibras": 2.0, "sodio": 1, "custo": 1.0, "tipo": "fruta"},
    {"nome": "Abacate", "calorias": 160, "proteinas": 2.0, "gorduras": 14.0, "gordura_saturada": 2.1, "carboidratos": 8.5, "fibras": 6.7, "sodio": 2, "custo": 1.2, "tipo": "fruta"},
    {"nome": "Abacaxi", "calorias": 50, "proteinas": 0.5, "gorduras": 0.1, "gordura_saturada": 0.0, "carboidratos": 13.0, "fibras": 1.4, "sodio": 1, "custo": 0.4, "tipo": "fruta"},
    {"nome": "Uva", "calorias": 67, "proteinas": 0.7, "gorduras": 0.4, "gordura_saturada": 0.1, "carboidratos": 17.0, "fibras": 0.9, "sodio": 1, "custo": 0.8, "tipo": "fruta"},
    
    # OLEAGINOSAS
    {"nome": "Amendoim", "calorias": 567, "proteinas": 26.0, "gorduras": 49.0, "gordura_saturada": 6.8, "carboidratos": 16.0, "fibras": 8.5, "sodio": 5, "custo": 2.5, "tipo": "gordura"},
    {"nome": "Castanha de Caju", "calorias": 553, "proteinas": 18.0, "gorduras": 44.0, "gordura_saturada": 7.8, "carboidratos": 30.0, "fibras": 3.3, "sodio": 10, "custo": 4.0, "tipo": "gordura"},
    {"nome": "Castanha do Pará", "calorias": 659, "proteinas": 14.0, "gorduras": 67.0, "gordura_saturada": 15.0, "carboidratos": 11.0, "fibras": 7.5, "sodio": 2, "custo": 4.5, "tipo": "gordura"},
    {"nome": "Nozes", "calorias": 588, "proteinas": 15.0, "gorduras": 59.0, "gordura_saturada": 6.1, "carboidratos": 18.0, "fibras": 6.7, "sodio": 2, "custo": 6.0, "tipo": "gordura"},
    {"nome": "Amêndoas", "calorias": 576, "proteinas": 21.0, "gorduras": 49.0, "gordura_saturada": 3.7, "carboidratos": 22.0, "fibras": 12.5, "sodio": 1, "custo": 6.0, "tipo": "gordura"},
    
    # GORDURAS
    {"nome": "Óleo de Soja", "calorias": 884, "proteinas": 0.0, "gorduras": 100.0, "gordura_saturada": 15.0, "carboidratos": 0.0, "fibras": 0.0, "sodio": 0, "custo": 0.7, "tipo": "gordura"},
    {"nome": "Óleo de Canola", "calorias": 884, "proteinas": 0.0, "gorduras": 100.0, "gordura_saturada": 7.0, "carboidratos": 0.0, "fibras": 0.0, "sodio": 0, "custo": 1.2, "tipo": "gordura"},
    {"nome": "Azeite de Oliva", "calorias": 884, "proteinas": 0.0, "gorduras": 100.0, "gordura_saturada": 14.0, "carboidratos": 0.0, "fibras": 0.0, "sodio": 0, "custo": 4.0, "tipo": "gordura"},
    {"nome": "Margarina", "calorias": 720, "proteinas": 0.0, "gorduras": 80.0, "gordura_saturada": 20.0, "carboidratos": 0.0, "fibras": 0.0, "sodio": 700, "custo": 1.0, "tipo": "gordura"},
    
    # INDUSTRIALIZADOS
    {"nome": "Pão de Queijo", "calorias": 360, "proteinas": 5.0, "gorduras": 20.0, "gordura_saturada": 10.0, "carboidratos": 38.0, "fibras": 1.0, "sodio": 600, "custo": 1.5, "tipo": "industrializado"},
    {"nome": "Coxinha", "calorias": 280, "proteinas": 10.0, "gorduras": 15.0, "gordura_saturada": 6.0, "carboidratos": 25.0, "fibras": 2.0, "sodio": 500, "custo": 2.0, "tipo": "industrializado"},
    {"nome": "Pastel de Carne", "calorias": 300, "proteinas": 12.0, "gorduras": 18.0, "gordura_saturada": 7.0, "carboidratos": 24.0, "fibras": 1.0, "sodio": 600, "custo": 3.0, "tipo": "industrializado"},
    {"nome": "Mortadela", "calorias": 280, "proteinas": 13.0, "gorduras": 23.0, "gordura_saturada": 8.0, "carboidratos": 2.0, "fibras": 0.0, "sodio": 1200, "custo": 2.0, "tipo": "industrializado"},
    {"nome": "Presunto", "calorias": 110, "proteinas": 18.0, "gorduras": 4.0, "gordura_saturada": 1.5, "carboidratos": 1.0, "fibras": 0.0, "sodio": 1100, "custo": 2.0, "tipo": "industrializado"},
    {"nome": "Peito de Peru", "calorias": 110, "proteinas": 17.0, "gorduras": 2.0, "gordura_saturada": 0.5, "carboidratos": 2.0, "fibras": 0.0, "sodio": 950, "custo": 3.0, "tipo": "industrializado"},
    {"nome": "Salsicha", "calorias": 290, "proteinas": 12.0, "gorduras": 25.0, "gordura_saturada": 9.0, "carboidratos": 2.0, "fibras": 0.0, "sodio": 1200, "custo": 1.5, "tipo": "industrializado"},
    {"nome": "Nuggets de Frango", "calorias": 290, "proteinas": 15.0, "gorduras": 20.0, "gordura_saturada": 4.0, "carboidratos": 15.0, "fibras": 1.0, "sodio": 800, "custo": 2.5, "tipo": "industrializado"},
    {"nome": "Batata Frita Congelada", "calorias": 312, "proteinas": 3.4, "gorduras": 15.0, "gordura_saturada": 2.0, "carboidratos": 41.0, "fibras": 3.5, "sodio": 600, "custo": 1.5, "tipo": "industrializado"}
]

# Converte para DataFrame
df_alimentos = pd.DataFrame(alimentos)

# --- CRIAÇÃO DA GORDURA INSATURADA ---
# "O que não é saturada, consideramos 'boa' (mono+poli)"
df_alimentos['gorduras_insaturadas'] = df_alimentos['gorduras'] - df_alimentos['gordura_saturada']

# Garante que não fique negativo (caso haja erro de input)
df_alimentos['gorduras_insaturadas'] = df_alimentos['gorduras_insaturadas'].clip(lower=0)

def criar_base_dados():
    """ Cria e retorna a base de dados de alimentos como um DataFrame do Pandas. """
    return df_alimentos.copy()
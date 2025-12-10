def calcular_tmb(calculo_basal):
    "Calcula a Taxa Metabólica Basal (TMB) usando a fórmula de Mifflin-St Jeor."
    peso = calculo_basal[0]
    altura = calculo_basal[1]
    idade = calculo_basal[2]
    sexo = calculo_basal[3]
    nivel_atividade = calculo_basal[4]

    tmb = []

    if sexo == 1:
        tmb.append((10 * peso) + (6.25 * altura) - (5 * idade) + 5)
    else:
        tmb.append((10 * peso) + (6.25 * altura) - (5 * idade) - 161)
    
    # Ajusta TMB com base no nível de atividade
    fatores_atividade = {
        1: 1.2,    # Sedentário
        2: 1.375,  # Levemente ativo
        3: 1.55,   # Moderadamente ativo
        4: 1.725,  # Muito ativo
        5: 1.9     # Extremamente ativo
    }

    tmb.append(tmb[0] * fatores_atividade.get(nivel_atividade))
    
    return tmb
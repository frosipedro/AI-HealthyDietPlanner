"""
Módulo de Validação de Inputs do Usuário
"""

from typing import Union, Callable


def validar_numero(
    mensagem: str,
    minimo: Union[int, float],
    maximo: Union[int, float],
    tipo: Callable = float
) -> Union[int, float]:
    """
    Valida entrada numérica do usuário.
    
    Args:
        mensagem: Mensagem a exibir
        minimo: Valor mínimo aceito
        maximo: Valor máximo aceito
        tipo: Tipo de retorno (int ou float)
    
    Returns:
        Número validado
    """
    while True:
        try:
            valor = tipo(input(mensagem))
            if minimo <= valor <= maximo:
                return valor
            else:
                print(f"⚠️  Valor deve estar entre {minimo} e {maximo}.")
        except ValueError:
            print(f"⚠️  Por favor, insira um número válido.")


def validar_porcentagens(valores: list) -> bool:
    """
    Verifica se a soma de porcentagens é 100%.
    
    Args:
        valores: Lista de porcentagens
    
    Returns:
        True se soma == 100%
    """
    total = sum(valores)
    return abs(total - 100) < 0.01  # Tolerância para erros de float


def validar_sim_nao(mensagem: str) -> bool:
    """
    Valida resposta Sim/Não.
    
    Args:
        mensagem: Pergunta para o usuário
    
    Returns:
        True para Sim, False para Não
    """
    while True:
        resposta = input(mensagem + " (S/n): ").strip().lower()
        if resposta in ['s', 'sim', 'y', 'yes', '']:
            return True
        elif resposta in ['n', 'nao', 'não', 'no']:
            return False
        else:
            print("⚠️  Por favor, responda com S (Sim) ou N (Não).")
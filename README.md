# 🍽️ Sistema de Recomendação de Cardápio Saudável com IA

Este projeto implementa um sistema avançado para geração de cardápios alimentares personalizados utilizando técnicas de Inteligência Artificial. O sistema é capaz de criar planos alimentares que respeitam metas nutricionais (calorias, macronutrientes), preferências pessoais e restrições orçamentárias.

## 🧠 Tecnologias e Algoritmos

O sistema utiliza uma arquitetura híbrida composta por quatro módulos principais de IA:

1.  **Lógica Fuzzy (`skfuzzy`)**: Classifica o quão saudável é um alimento baseando-se em sua composição nutricional (proteínas, sódio, gorduras, fibras, etc.).
2.  **Redes Neurais Artificiais (`scikit-learn`)**: Um modelo `MLPRegressor` aprende as preferências do usuário através de um questionário inicial e prevê a nota de preferência para todos os alimentos da base.
3.  **Busca A\* (A-Star)**: Realiza uma pré-seleção inteligente dos melhores alimentos candidatos para cada tipo de refeição, otimizando o espaço de busca.
4.  **Algoritmo Genético**: Otimiza a combinação final das refeições do dia, evoluindo populações de cardápios para maximizar o fitness (adequação às calorias, macros, custo e preferências).

## 📋 Pré-requisitos

- **Python 3.8** ou superior
- `pip` (gerenciador de pacotes do Python)

## 🚀 Instalação e Execução (Linux/macOS)

Siga os passos abaixo para configurar o ambiente e executar o projeto.

### 1. Clone o repositório

```bash
git clone https://github.com/frosipedro/AI-HealthyDietPlanner.git
cd AI-HealthyDietPlanner
```

### 2. Crie um ambiente virtual (Recomendado)

Isso isola as dependências do projeto do seu sistema principal.

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

Instale as bibliotecas necessárias (`numpy`, `pandas`, `scikit-learn`, `scikit-fuzzy`).

```bash
pip install -r requirements.txt
# Caso não tenha o arquivo requirements.txt, execute:
# pip install numpy pandas scikit-learn scikit-fuzzy
```

### 4. Execute o sistema

```bash
python main.py
```

## ⚙️ Como Usar

Ao executar o programa, você será guiado por um assistente interativo no terminal:

1.  **Configuração de Refeições**: Defina quantas refeições faz por dia (ex: 3 a 8) e a distribuição calórica para cada uma.
2.  **Metas Nutricionais**: Insira sua meta de calorias, distribuição de macros (Carboidratos, Proteínas, Gorduras) e orçamento diário.
3.  **Preferências**: Responda ao questionário sobre seus gostos alimentares para treinar a Rede Neural.
4.  **Geração**: O sistema executará os algoritmos de otimização.
5.  **Resultado**: O cardápio será exibido no terminal e exportado para arquivos `.txt` e `.csv`.

## 📂 Estrutura do Projeto

```
AI-HealthyDietPlanner/
├── algoritmos/             # Módulos de IA (Genético, A*, Fuzzy, RNA)
├── data/                   # Base de dados de alimentos
├── utils/                  # Utilitários de formatação e validação
├── README.md               # Documentação do projeto
└── main.py                 # Arquivo principal de execução
```

## 👥 Autores

**Grupo:**

- Cristian dos Santos Siqueira — https://github.com/CristianSSiqueira
- Marco Antônio Hendges — https://github.com/Marco-Hendges
- Pedro Rockenbach Frosi — https://github.com/frosipedro
- William Rafael Fagundes — https://github.com/Williamrafaelfagundes

**Professor:** Marcos Sulzbach Morgenstern

_Desenvolvido para a disciplina de Inteligência Artificial._

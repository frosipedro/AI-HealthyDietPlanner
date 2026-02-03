# 🍽️ AI-HealthyDietPlanner

### Sistema Inteligente de Recomendação de Cardápios Personalizados

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Fuzzy Logic](https://img.shields.io/badge/AI-Fuzzy%20Logic-orange.svg)]()
[![Neural Network](https://img.shields.io/badge/AI-Neural%20Network-purple.svg)]()
[![Genetic Algorithm](https://img.shields.io/badge/AI-Genetic%20Algorithm-red.svg)]()
[![A* Search](https://img.shields.io/badge/AI-A*%20Search-yellow.svg)]()

## 📖 Sobre o Projeto

O **AI-HealthyDietPlanner** é um sistema avançado de geração automática de cardápios alimentares que combina **4 técnicas de Inteligência Artificial** para criar planos nutricionais personalizados, saudáveis e realistas, respeitando a culinária brasileira.

Desenvolvido como Trabalho Final da disciplina de **Inteligência Artificial** na **Unisinos**, o projeto vai além de simples calculadoras nutricionais: ele entende preferências pessoais, aplica regras culinárias do mundo real, e evolui cardápios otimizados usando algoritmos genéticos.

### 🎯 Motivação

**Por que criamos este projeto?**

1. **Nutrição é complexa**: Não basta somar calorias. É preciso considerar macronutrientes, micronutrientes, preferências pessoais, orçamento e compatibilidade entre alimentos.

2. **Cardápios realistas**: Muitos sistemas sugerem combinações absurdas (peixe com feijão, salsicha no mingau de aveia). Nosso sistema aplica **regras culinárias brasileiras** validadas.

3. **Personalização real**: Cada pessoa tem preferências únicas. Nosso sistema aprende com você usando **Redes Neurais** e gera cardápios que você realmente vai querer seguir.

4. **Aplicação prática de IA**: Demonstrar como técnicas clássicas de IA (Fuzzy, RNA, A\*, AG) podem resolver problemas reais do dia a dia de forma integrada.

5. **Saúde acessível**: Considera orçamento e custo dos alimentos, tornando alimentação saudável mais democrática.

## 🧠 Arquitetura e Técnicas de IA

O sistema utiliza **4 módulos de IA integrados** em um pipeline sequencial:

### 1️⃣ **Lógica Fuzzy** - Avaliação de Salubridade

```python
Biblioteca: scikit-fuzzy
Arquivo: algoritmos/fuzzy_saudavel.py
```

**Função**: Classifica cada alimento em uma escala de 0-10 de "quão saudável" ele é.

**Como funciona**:

- Define funções de pertinência fuzzy para nutrientes (proteínas: baixa/média/alta, sódio: baixo/médio/alto, etc.)
- Aplica **9 regras fuzzy**
- Considera contexto brasileiro (penaliza ultraprocessados, favorece feijão, ovo, peixe)

**Output**: Score de saúde (0-10) para cada alimento

### 2️⃣ **Rede Neural Artificial** - Aprendizado de Preferências

```python
Biblioteca: scikit-learn (MLPRegressor)
Arquivo: algoritmos/rna_preferencias.py
```

**Função**: Aprende suas preferências alimentares e prevê notas de satisfação.

**Como funciona**:

- Coleta preferências via questionário (gosta de frango? 0-10, peixe? 0-10, etc.)
- Gera **500 amostras sintéticas** de treinamento com ruído realista
- Treina rede neural **3 camadas** (64→32→16 neurônios)
- Prevê nota de preferência (0-1) para todos os alimentos

**Output**: Score de preferência personalizado para cada alimento

### 3️⃣ **Busca A\* (A-Star)** - Pré-Seleção Inteligente

```python
Algoritmo: A* Search com heurística admissível
Arquivo: algoritmos/busca_a_star.py
```

**Função**: Seleciona os melhores candidatos de alimentos ANTES do algoritmo genético.

**Como funciona**:

- **Heurística admissível**: Nunca superestima custo → garante otimalidade
- Custo g(n) = penalidade por baixa saúde/preferência + excesso de orçamento
- Filtra por regras culinárias (ex: proteínas só em almoço/jantar)
- Retorna **top 15-20 alimentos** de cada tipo nutricional

**Output**: Conjunto reduzido e otimizado de candidatos → acelera AG

### 4️⃣ **Algoritmo Genético** - Otimização de Cardápios

```python
Algoritmo: Genetic Algorithm multi-objetivo
Arquivo: algoritmos/algoritmo_genetico.py
```

**Função**: Evolui cardápios completos (todas refeições do dia) para maximizar fitness.

**Como funciona**:

- **População**: 150 cardápios aleatórios seguindo regras culinárias
- **Fitness multi-objetivo** (10 critérios):
  - Calorias (14%), Proteínas (14%), Carboidratos (11%), Gorduras (7%)
  - Saúde (8%), Preferência (10%), Custo (5%)
  - **Validação culinária** (16%), Diversidade (10%), **Exclusão mútua** (5%)
- **Seleção**: Torneio entre 5 indivíduos
- **Crossover**: Troca refeições entre cardápios (ponto de corte)
- **Mutação**: 20% chance de alterar alimento ou gramatura
- **Elitismo**: Mantém 10 melhores a cada geração

**Output**: Cardápio otimizado do dia inteiro

## 🌟 Funcionalidades Principais

### ✅ Regras Culinárias Brasileiras

- ❌ Peixe NÃO combina com feijão
- ✅ Feijão PRECISA de arroz ou massa
- ✅ Aveia PRECISA de leite/iogurte
- ✅ Café da manhã: pães, frutas, ovos, iogurte
- ✅ Almoço/Jantar: proteína + acompanhamento + guarnição

### ✅ Sistema de Exclusão Mútua

Evita alimentos similares no mesmo dia:

- **Feijão Preto** OU **Feijão Carioca** (não ambos)
- **Linguiça de Frango** OU **Linguiça Toscana**
- **Arroz Branco** OU **Arroz Integral**
- 13 grupos configurados (ver [EXCLUSAO_MUTUA.md](EXCLUSAO_MUTUA.md))

### ✅ Limites de Gramatura Realistas

```python
Manteiga: 5-20g (não sugere 100g!)
Arroz: 100-200g (5 colheres de sopa)
Frango: 100-250g (1 filé médio)
Castanhas: 15-40g (1 punhado)
```

### ✅ Cálculo Automático de TMB

- Fórmula Mifflin-St Jeor
- Ajuste por nível de atividade física
- Sugestões para perda/ganho/manutenção

### ✅ Estilos de Dieta Pré-Configurados

1. Equilibrada (50C/25P/25G)
2. High-Carb (60/20/20)
3. Low-Carb (30/40/30)
4. Cetogênica (10/30/60)
5. High-Protein (25/45/30)
6. Zona (40/30/30)

## 📊 Base de Dados

**96 alimentos brasileiros** com informações completas:

| Categoria        | Exemplos                             | Quantidade   |
| ---------------- | ------------------------------------ | ------------ |
| **Proteínas**    | Frango, Carne, Peixe, Ovos, Queijos  | 36 alimentos |
| **Carboidratos** | Arroz, Feijão, Pães, Massas, Batatas | 28 alimentos |
| **Vegetais**     | Brócolis, Cenoura, Tomate, Alface    | 11 alimentos |
| **Frutas**       | Banana, Maçã, Laranja, Mamão         | 11 alimentos |
| **Gorduras**     | Azeite, Oleaginosas, Manteiga        | 10 alimentos |

**Dados por 100g**: calorias, proteínas, carboidratos, gorduras (saturadas/insaturadas), fibras, sódio, custo estimado.

## 🚀 Instalação e Uso

### Pré-requisitos

- **Python 3.8+**
- `pip` (gerenciador de pacotes)

### 1. Clone o repositório

```bash
git clone https://github.com/frosipedro/AI-HealthyDietPlanner.git
cd AI-HealthyDietPlanner
```

### 2. Crie um ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

**Bibliotecas instaladas**:

- `numpy` (≥2.3.5)
- `pandas` (≥2.3.3)
- `scikit-fuzzy` (≥0.5.0)
- `scikit-learn` (≥1.7.2)
- `networkx` (≥3.6.1)

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

```bash
python main.py
```

### 5. Siga o assistente interativo

O sistema guiará você através de:

1. **Configuração de Refeições** (quantas? quais nomes? distribuição calórica)
2. **Cálculo de TMB** (peso, altura, idade, sexo, nível de atividade)
3. **Metas Nutricionais** (calorias, estilo de dieta)
4. **Preferências de Vegetais** (quais você gosta mais?)
5. **Questionário de Preferências** (RNA aprenderá suas preferências)
6. **Otimização** (A\* + Algoritmo Genético)
7. **Cardápio Final** (formatado estilo nutricionista)

### 6. Resultados

O sistema salvará automaticamente:

- **`cardapio_personalizado_YYYYMMDD_HHMMSS.txt`**: Cardápio formatado para impressão
- **`cardapio_dataframe_YYYYMMDD_HHMMSS.csv`**: Dados em formato tabular (Excel/análise)

## 📁 Estrutura do Projeto

```
AI-HealthyDietPlanner/
│
├── main.py                          # Ponto de entrada do sistema
│
├── algoritmos/                      # Módulos de IA
│   ├── fuzzy_saudavel.py           # Lógica Fuzzy (salubridade)
│   ├── rna_preferencias.py         # Rede Neural (preferências)
│   ├── busca_a_star.py             # A* (pré-seleção)
│   └── algoritmo_genetico.py       # AG (otimização final)
│
├── data/                            # Dados e regras
│   ├── dados_alimentos.py          # Base: 96 alimentos brasileiros
│   └── regras_culinarias.py        # Regras culinárias + compatibilidade
│
├── utils/                           # Utilitários
│   ├── formatacao.py               # Formatação de saída
│   ├── validacao_input.py          # Validação de entradas
│   └── tmb_calculator.py           # Cálculo de TMB
│
├── requirements.txt                 # Dependências Python
├── README.md                        # Este arquivo
└── LICENSE                          # Licença MIT
```

## 🎨 Exemplo de Saída

```
════════════════════════════════════════════════════════════════════════════════
                    🍽️  PLANO ALIMENTAR PERSONALIZADO
════════════════════════════════════════════════════════════════════════════════
Elaborado por: Sistema IA Nutricional
Data: 11/12/2025
Meta Diária: 2800 kcal | Macros: 50C/25P/25G | Orçamento: R$ 30.00
════════════════════════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────────────────────────────┐
│ ☀️  CAFÉ DA MANHÃ                                            560 kcal │
│ (20% das calorias diárias)                                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│  •      80g de Aveia                                         315 kcal │
│  •     200g de Leite Integral                                118 kcal │
│  •     120g de Banana Prata                                  107 kcal │
│  •      30g de Castanha de Caju                              166 kcal │
│                                                                              │
│  📊 Macros:   21g Prot |   82g Carbo |   20g Gord |   14g Fib                │
│  💰 Custo: R$  3.56                                                          │
└──────────────────────────────────────────────────────────────────────────────┘

[...]

════════════════════════════════════════════════════════════════════════════════
📊 RESUMO NUTRICIONAL DO DIA
════════════════════════════════════════════════════════════════════════════════
Calorias: 2795 kcal (Meta: 2800) ✅ 99.8%
Proteínas: 175g (Meta: 175g) ✅ 100.0%
Carboidratos: 348g (Meta: 350g) ✅ 99.4%
Gorduras: 77g (Meta: 78g) ✅ 98.7%

Custo Total: R$ 24.80 (Orçamento: R$ 30.00) ✅
Saúde Média: 7.8/10 ✅
Preferência: 8.5/10 ✅
════════════════════════════════════════════════════════════════════════════════
```

## 🏆 Autores

Desenvolvido como **Trabalho Final** da disciplina de Inteligência Artificial.

**Grupo:**

- **Cristian dos Santos Siqueira** — [@CristianSSiqueira](https://github.com/CristianSSiqueira)
- **Marco Antônio Hendges** — [@Marco-Hendges](https://github.com/Marco-Hendges)
- **Pedro Rockenbach Frosi** — [@frosipedro](https://github.com/frosipedro)
- **William Rafael Fagundes** — [@Williamrafaelfagundes](https://github.com/Williamrafaelfagundes)

**Orientador**: Prof. Marcos Sulzbach Morgenstern

**Instituição**: Universidade Regional do Noroeste do Estado do Rio Grande do Sul (UNIJUÍ)

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

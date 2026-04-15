backup_codigo.py

# Análise de Desvios Orçado vs Realizado

## Objetivo
Analisar as variações entre orçamento planejado e despesas realizadas, identificando principais desvios e seus drivers.

## Dor de Negócio
Empresas frequentemente enfrentam:
- Falta de controle sobre execução do orçamento
- Dificuldade em explicar desvios
- Baixa velocidade na tomada de decisão

## Cenário
A empresa possui:
- Orçamento mensal por categoria
- Despesas realizadas

O time de FP&A precisa:
- Identificar onde ocorreram os maiores desvios
- Entender quais categorias impactaram mais
- Apoiar ações corretivas

## Abordagem
- Comparar orçamento vs realizado
- Calcular variação absoluta e percentual
- Identificar top desvios
- Visualizar impacto por categoria

## Insights Esperados
- Categorias com maior estouro de orçamento
- Áreas com eficiência (abaixo do orçado)
- Priorização de ajustes

## Valor para o Negócio
- Maior controle financeiro
- Redução de desperdícios
- Melhor acuracidade de forecast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# Criando base simulada
n = 120

df = pd.DataFrame({
    'Mes': pd.date_range(start='2024-01-01', periods=n, freq='MS'),
    'Categoria': np.random.choice(['Aluguel', 'Energia', 'TI', 'Manutenção', 'Marketing'], n),
    'Orcado': np.random.randint(5000, 15000, n),
})

# Simulando realizado com variação (±30%)
df['Realizado'] = df['Orcado'] * np.random.uniform(0.7, 1.3, n)

# Cálculo dos desvios
df['Desvio_Abs'] = df['Realizado'] - df['Orcado']
df['Desvio_%'] = df['Desvio_Abs'] / df['Orcado']

# Visualização inicial
print("Amostra dos dados:")
print(df.head())

# Análise por categoria
resumo = df.groupby('Categoria')[['Orcado', 'Realizado', 'Desvio_Abs']].sum()
resumo['Desvio_%'] = resumo['Desvio_Abs'] / resumo['Orcado']

print("\nResumo por categoria:")
print(resumo.sort_values(by='Desvio_Abs', ascending=False))

# Gráfico: desvio por categoria
resumo['Desvio_Abs'].plot(kind='bar', title='Desvio Absoluto por Categoria')
plt.axhline(0)
plt.show()

# Evolução mensal
mensal = df.groupby('Mes')[['Orcado', 'Realizado']].sum()

mensal.plot(title='Orçado vs Realizado ao longo do tempo')
plt.show()

# Maiores desvios positivos
top_desvios = df.sort_values(by='Desvio_Abs', ascending=False).head(10)

print("\nTop 10 maiores desvios positivos:")
print(top_desvios[['Mes', 'Categoria', 'Orcado', 'Realizado', 'Desvio_Abs']])

# Maiores economias
economias = df.sort_values(by='Desvio_Abs').head(10)

print("\nTop 10 menores desvios (economia):")
print(economias[['Mes', 'Categoria', 'Orcado', 'Realizado', 'Desvio_Abs']])

# Distribuição dos desvios
df['Desvio_Abs'].hist(bins=20)
plt.title('Distribuição dos Desvios')
plt.show()

# Pareto dos desvios
pareto = resumo['Desvio_Abs'].abs().sort_values(ascending=False)
pareto_perc = pareto / pareto.sum()

pareto_perc.cumsum().plot(title='Pareto dos Desvios')
plt.show()
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import random
from datetime import datetime, timedelta

# Carregar os dados do arquivo CSV
df = pd.read_csv('vendas_acessorios_celular.csv')

# Agrupar os dados por produto e somar as quantidades vendidas
vendas_por_produto = df.groupby('produto')['quantidade'].sum()

# Identificar os 5 produtos mais vendidos
top_5_produtos = vendas_por_produto.nlargest(5)

# Calcular o valor faturado para cada linha
df['valor_faturado'] = df['quantidade'] * df['valor']

# Agrupar os dados por produto e somar os valores faturados
faturamento_por_produto = df.groupby('produto')['valor_faturado'].sum()

# Classificar os valores do maior para o menor
faturamento_por_produto = faturamento_por_produto.sort_values(ascending=False)

# Converter a coluna de data para o formato datetime
df['data'] = pd.to_datetime(df['data'])

# Agrupar os dados por data e somar os valores faturados
faturamento_por_dia = df.groupby('data')['valor_faturado'].sum()

# Identificar o dia com maior faturamento
dia_maior_faturamento = faturamento_por_dia.idxmax()
valor_maior_faturamento = faturamento_por_dia.max()

# Agrupar os dados por mês e somar os valores faturados
faturamento_por_mes = df.groupby(df['data'].dt.to_period('M'))['valor_faturado'].sum()

# Identificar o mês com maior faturamento
mes_maior_faturamento = faturamento_por_mes.idxmax()
valor_maior_faturamento = faturamento_por_mes.max()

# Identificar a linha com o maior valor faturado
maior_venda = df.loc[df['valor_faturado'].idxmax()]

# Quantidade Vendida por Produto
quantidade_por_produto = df.groupby('produto')['quantidade'].sum().sort_values(ascending=False)

# Faturamento Diário
faturamento_diario = df.groupby('data').apply(lambda x: (x['quantidade'] * x['valor']).sum())

# Faturamento Mensal
faturamento_mensal = df.groupby(df['data'].dt.to_period('M')).apply(lambda x: (x['quantidade'] * x['valor']).sum())

# Produto Mais Vendido
produto_mais_vendido = df.groupby('produto')['quantidade'].sum().idxmax()

# Função para salvar gráficos como imagens
def salvar_grafico(fig, nome_arquivo):
    fig.savefig(nome_arquivo, bbox_inches='tight')

# Gerar gráficos
fig1, ax1 = plt.subplots()
faturamento_mensal.plot(kind='line', ax=ax1)
ax1.set_title('Faturamento Mensal')
ax1.set_xlabel('Mês')
ax1.set_ylabel('Faturamento')
salvar_grafico(fig1, 'faturamento_mensal.png')

fig2, ax2 = plt.subplots()
df['valor'].plot(kind='hist', bins=20, ax=ax2)
ax2.set_title('Distribuição de Preços')
ax2.set_xlabel('Valor')
ax2.set_ylabel('Frequência')
salvar_grafico(fig2, 'distribuicao_precos.png')

# Criar PDF
pdf = FPDF()
pdf.add_page()

# Adicionar título
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, 'Relatório de Vendas', 0, 1, 'C')

# Adicionar texto
pdf.set_font('Arial', '', 12)
pdf.cell(0, 10, f'Os 5 produtos mais vendidos foram:', 0, 1)
for produto, quantidade in top_5_produtos.items():
    pdf.cell(0, 10, f'{produto}: {quantidade}', 0, 1)

pdf.cell(0, 10, 'Valor faturado por produto (classificado do maior para o menor):', 0, 1)
for produto, valor in faturamento_por_produto.items():
    pdf.cell(0, 10, f'{produto}: R$ {valor:.2f}', 0, 1)

pdf.cell(0, 10, f'O dia com maior faturamento foi: {dia_maior_faturamento} com um faturamento de R$ {valor_maior_faturamento:.2f}.', 0, 1)
pdf.cell(0, 10, f'O mês com maior faturamento foi: {mes_maior_faturamento} com um faturamento de R$ {valor_maior_faturamento:.2f}.', 0, 1)

pdf.cell(0, 10, 'A maior venda no período foi:', 0, 1)
for coluna, valor in maior_venda.items():
    pdf.cell(0, 10, f'{coluna}: {valor}', 0, 1)

pdf.cell(0, 10, 'Quantidade vendida por produto:', 0, 1)
for produto, quantidade in quantidade_por_produto.items():
    pdf.cell(0, 10, f'{produto}: {quantidade}', 0, 1)

pdf.cell(0, 10, f'O produto mais vendido é: {produto_mais_vendido}', 0, 1)

# Adicionar gráficos
pdf.image('faturamento_mensal.png', x=10, y=None, w=190)
pdf.image('distribuicao_precos.png', x=10, y=None, w=190)

# Salvar PDF
pdf.output('relatorio_vendas.pdf')

print("Relatório PDF gerado com sucesso!")

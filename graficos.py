import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

# Carregar o arquivo CSV
df = pd.read_csv('vendas_acessorios_celular.csv')

# Converter a coluna 'data' para o tipo datetime
df['data'] = pd.to_datetime(df['data'])

# Criar uma nova coluna 'faturamento' (quantidade * valor)
df['faturamento'] = df['quantidade'] * df['valor']

# Criar um arquivo PDF para salvar os gráficos
with PdfPages('relatorio_vendas.pdf') as pdf:
    # Visualização 1: Faturamento total por produto
    faturamento_por_produto = df.groupby('produto')['faturamento'].sum().sort_values(ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=faturamento_por_produto.values, y=faturamento_por_produto.index)
    plt.title('Faturamento Total por Produto')
    plt.xlabel('Faturamento (R$)')
    plt.ylabel('Produto')
    pdf.savefig()  # Salvar o gráfico no PDF
    plt.close()
    
    # Visualização 2: Faturamento total ao longo do tempo
    faturamento_por_data = df.groupby('data')['faturamento'].sum()
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=faturamento_por_data.index, y=faturamento_por_data.values, marker='o', color='blue')
    plt.title('Faturamento ao Longo do Tempo')
    plt.xlabel('Data')
    plt.ylabel('Faturamento Diário (R$)')
    plt.grid(True)
    pdf.savefig()  # Salvar o gráfico no PDF
    plt.close()
    
    # Visualização 3: Produtos mais vendidos (em quantidade)
    quantidade_por_produto = df.groupby('produto')['quantidade'].sum().sort_values(ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=quantidade_por_produto.values, y=quantidade_por_produto.index)
    plt.title('Produtos Mais Vendidos (Quantidade Total)')
    plt.xlabel('Quantidade Vendida')
    plt.ylabel('Produto')
    pdf.savefig()  # Salvar o gráfico no PDF
    plt.close()
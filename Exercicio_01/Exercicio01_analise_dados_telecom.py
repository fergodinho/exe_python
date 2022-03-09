#!/usr/bin/env python
# coding: utf-8

# # Análise de Dados com Python
# 
# ### Desafio:
# 
# Você trabalha em uma empresa de telecom e tem clientes de vários serviços diferentes, entre os principais: internet e telefone.
# 
# O problema é que, analisando o histórico dos clientes dos últimos anos, você percebeu que a empresa está com Churn de mais de 26% dos clientes.
# 
# Isso representa uma perda de milhões para a empresa.
# 
# O que a empresa precisa fazer para resolver isso?
# 
# Link Original do Kaggle: https://www.kaggle.com/radmirzosimov/telecom-users-dataset

# In[1]:


#importar biblioteca para análise de dados
import pandas as pd

# importar o arquivo para python

dados_telecom = pd.read_csv(r"telecom_users.csv") #r serve para dizer que é uma raw string

# visualizar base de dados
#formatar a base de dados
#axis = 0 -> linha
#axis = 1 -> coluna

dados_telecom = dados_telecom.drop(["Unnamed: 0"], axis=1) #deletar
display(dados_telecom)


# In[2]:


#analisar como as informações estão sendo lidas
# visualizar informações sobre os dados da base de dados
print(dados_telecom.info()) 


# In[3]:


# corrigir variáveis da base de dados que estão sendo lidas de forma incorreta

dados_telecom["TotalGasto"] = pd.to_numeric(dados_telecom["TotalGasto"], errors="coerce")

print(dados_telecom.info()) 


# In[4]:


# excluir colunas (axis=1) completamente (all) nulas com dropna

dados_telecom = dados_telecom.dropna(how="all", axis=1)

# excluir linhas (axis=0) que tem pelo menos uma (any) informação nula com dropna

dados_telecom = dados_telecom.dropna(how="any", axis=0)

print(dados_telecom.info()) 


# In[5]:


# analise inicial dos dados de cancelamento de assinatura que constam na base de dados

# calcular quantos clientes cancelaram e quantos nao cancelaram usando count

print(dados_telecom["Churn"].value_counts())

#calcular por porcentagem usando count
# .map("{:.2%}".format) coloca duas casas porcentuais

print(dados_telecom["Churn"].value_counts(normalize=True).map("{:.2%}".format))


# In[6]:


# construir e exibir gráfico para visualizar a quantidade de cancelamentos e permanências

get_ipython().system('pip install plotly')
import plotly.express as px #biblioteca pra criar gráficos

grafico_dados_telecom = px.histogram(dados_telecom["Churn"], x="Churn")

grafico_dados_telecom.show()


# In[7]:


# construir e exibir gráficos com índice de cancelamento para cada coluna da base de dados

for indicador in dados_telecom.columns:
    grafico = px.histogram(dados_telecom, x=indicador, color="Churn")
    grafico.show()


# ### Conclusões e Ações

# - Em algumas das categorias análisadas foi possível perceber uma disparidade entre a tava de cancelamentos, comparativamente. Estas foram:
# 
#     - A taxa de cancelamento é muito maior nos primeiros meses de contrato, podendo representar a conversão de usuários não qualificados;
#     - Há uma taxa de cancelamento muito maior entre os clientes que optam por pagamento via boleto bancário;
#     - Os clientes que recebem fatura digital também estão mais propensos ao cancelamento;
#     - Clientes com contrato mensal apresentam um índice elevado de cancelamento;
#     - Quando há outros serviços inclusos no plano, principalmente aqueles relativos a segurança e suporte (representados na base de dado pelos indicadores suporte técnico, proteção ao equipamento, serviço de backup online e serviço de segurança online), a taxa de cancelamento tende a ser reduzida;
#     - Usuários casados e com dependentes tendem menos ao cancelamento, o que pode indicar vantagem para operadora em oferecer descontos para planos familiares
# 
# 

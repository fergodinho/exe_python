#!/usr/bin/env python
# coding: utf-8

# # Automação Web e Busca de Informações com Python
# 
# #### Problema: 
# Necessidade de atualização constante das cotações do dolar, euro e ouro para atualizar uma base de dados que tem essas moedas como parâmetro para precificação dos seus produtos. Então é necessário buscar a cotação de cada uma das moedas, atualizar o valor do câmbio na base de dados e atualizar o valor de compra e venda dos produtos.
# 
# #### Solução: 
# Uma automação web com Selenium para buscar, de forma automática, a cotação desses 3 itens e atualizar o valor dos produtos na base de dados nativa.
# 

# In[32]:


# importar webdriver (para comandar navegador), keys (para usar teclas) e by (para localizar na tela)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#criar o navegador
navegador = webdriver.Chrome()

#entrar no google
navegador.get("https://www.google.com/")

#localizar a barra de pesquisa com o By a partir do XPATH ' ' e então usar o Keys para escrever a pesquisa e clicar enter
navegador.find_element(By.XPATH, 
                       '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação dólar", Keys.ENTER)

#como o google já disponibiliza o valor da cotação sem a necessidade de entrar em algum site, basta localizar o elemento onde é armazenada a cotação e atribuir a uma variável
cotacao_dolar = navegador.find_element(By.XPATH, 
                       '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')

# repetir o  mesmo passo a passo para a cotação do euro
navegador.get("https://www.google.com/")
navegador.find_element(By.XPATH, 
                       '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação euro", Keys.ENTER)

cotacao_euro = navegador.find_element(By.XPATH, 
                        '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')

# para cotação ouro vamos utilizar um site de cambio específico
navegador.get("https://www.melhorcambio.com/ouro-hoje")
cotacao_ouro = navegador.find_element(By.XPATH, '//*[@id="comercial"]').get_attribute('value')

# fechar navegador
navegador.quit()

print("Cotação do dólar: " + cotacao_dolar)
print("Cotação do euro: " + cotacao_euro )
print("Cotação do ouro com vírgula: " + cotacao_ouro + "\n")

# o python separa casas decimais por . então é necessário substituir o sinal gráfico da cotação do ouro, que foi importada com ,

cotacao_ouro = cotacao_ouro.replace(",", ".")

print("Cotação do ouro atualizada: " + cotacao_ouro)


# ### Atualização da base de preços com as novas cotações

# - Importando a base de dados

# In[33]:


# importar o pandas 
import pandas as pd

# importar e visualizar a base de dados
tabela_produtos = pd.read_excel("Produtos.xlsx")
print("\n Tabela original: ")
display(tabela_produtos)


# - Atualizando os preços e o cálculo do Preço Final

# In[34]:


# filtrar as linhas e colunas onde as devidas atualizações devem sem implementadas utilizando o .loc
# .loc[linha, coluna]

tabela_produtos.loc[tabela_produtos["Moeda"]=="Dólar", "Cotação"] = float(cotacao_dolar)
tabela_produtos.loc[tabela_produtos["Moeda"]=="Euro", "Cotação"] = float(cotacao_euro)
tabela_produtos.loc[tabela_produtos["Moeda"]=="Ouro", "Cotação"] = float(cotacao_ouro)

print("\n Tabela com cotação atualizada: \n")
display(tabela_produtos)

#atualizar preço de compra (compra = preço original * cotação)
tabela_produtos["Preço de Compra"]= tabela_produtos["Preço Original"] * tabela_produtos["Cotação"]

#atualizar preço de venda (venda = preço de compra * margem)
tabela_produtos["Preço de Venda"] = tabela_produtos["Preço de Compra"] * tabela_produtos["Margem"]

print("\nTabela com valores atualizados: \n")
display(tabela_produtos)


# ### Exportação da nova base de preços atualizada

# In[35]:


# substituir o arquivo original pela tabela atualizada exportando a tabela com o mesmo nome do arquivo original (escrevi um nome diferente para não perder a base antiga)

tabela_produtos.to_excel("Produtos_atualizados.xlsx", index=False)


# In[ ]:







# 🚀 Classificador de Exoplanetas com IA

 **Projeto desenvolvido para o [NASA Space Apps Challenge 2025](https://www.spaceappschallenge.org/).**

Este projeto é um protótipo funcional de uma aplicação web que utiliza Machine Learning para classificar candidatos a exoplanetas a partir do dataset da missão Kepler da NASA. A aplicação permite que um usuário insira as características de um "Objeto de Interesse Kepler" (KOI) e receba uma classificação instantânea, além de uma visualização 3D interativa do sistema planetário previsto.

## 🎯 Objetivo do Desafio

[cite\_start]O desafio proposto pela NASA foi criar um modelo de IA/ML treinado com dados de missões de exoplanetas para analisar novos dados e identificar planetas com precisão, tudo isso apresentado através de uma interface web interativa[cite: 1, 3, 11]. [cite\_start]Nossa solução ataca diretamente o problema da análise manual de dados, que é demorada, automatizando a classificação inicial para que os cientistas possam focar nos candidatos mais promissores[cite: 1].

## ✨ Features

  * [cite\_start]**Modelo de Machine Learning:** Utiliza um `RandomForestClassifier` treinado com o dataset do Kepler para classificar candidatos em `CONFIRMED`, `CANDIDATE` ou `FALSE POSITIVE`[cite: 11].
  * [cite\_start]**API Robusta:** Um backend construído com **FastAPI** que serve o modelo de IA e lida com as requisições de predição[cite: 7, 11].
  * [cite\_start]**Frontend Interativo:** Uma interface de usuário amigável construída com HTML, CSS e JavaScript puro[cite: 8].
  * **Visualização 3D Dinâmica:** Uma cena 3D construída com **Three.js** que renderiza o exoplaneta classificado, com cor e tamanho baseados no resultado da IA.

## 🛠️ Tecnologias Utilizadas

[cite\_start]Este projeto foi construído utilizando as seguintes tecnologias de código aberto, conforme sugerido pelo roteiro do desafio[cite: 4]:

  * **Backend & IA:**

      * 
      * 
      * 
      * 

  * **Frontend:**

      * 
      * 
      * 
      * 

## 📁 Estrutura do Projeto

O projeto está organizado da seguinte forma para uma clara separação de responsabilidades:

```
nasa_finale/
├── data/
│   └── kepler_data.csv       # Dataset de treinamento
├── saved_model/
│   └── model.joblib          # Modelo de IA treinado e salvo
├── website/
│   ├── index.html            # Estrutura da página
│   ├── style.css             # Estilização
│   └── script.js             # Lógica do frontend e da cena 3D
├── train_model.py            # Script para treinar e salvar o modelo
├── main.py                   # Script da API FastAPI (backend)
└── README.md                 # Este arquivo
```

## ⚙️ Como Executar o Projeto Localmente

Para executar esta aplicação em sua máquina, siga os passos abaixo.

### Pré-requisitos

  * **Anaconda ou Miniconda:** Recomendado para gerenciar o ambiente virtual. [Instale aqui](https://www.anaconda.com/products/distribution).
  * **Git:** Para clonar o repositório.

### Guia de Instalação

**1. Clone o Repositório:**
Abra seu terminal e clone este repositório para sua máquina local.

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

**2. Crie e Ative o Ambiente Virtual (Conda):**
É crucial criar um ambiente isolado para instalar as dependências do projeto.

```bash
# Cria um novo ambiente chamado 'nasa_api' com Python 3.9
conda create --name nasa_api python=3.9

# Ativa o ambiente
conda activate nasa_api
```

**3. Instale todas as Dependências:**
O arquivo `requirements.txt` (que você pode criar com `pip freeze > requirements.txt`) conteria todas as dependências. Para este guia, vamos instalar manualmente.

```bash
pip install pandas scikit-learn joblib fastapi "uvicorn[standard]"
```

**4. Treine o Modelo de IA:**
Antes de iniciar a API, você precisa treinar o modelo com os dados do Kepler.
*(Certifique-se de que seu arquivo `kepler_data.csv` está na pasta `data/`)*

```bash
python train_model.py
```

Este comando irá gerar o arquivo `saved_model/model.joblib`.

**5. Inicie a API (Backend):**
Com o modelo treinado, inicie o servidor FastAPI.

```bash
uvicorn main:app --reload
```

O terminal deve indicar que o servidor está rodando em `http://127.0.0.1:8000`.

**6. Abra a Aplicação Web (Frontend):**
Abra seu navegador de internet. **Não acesse o endereço da API diretamente.**

  * Vá até a pasta do projeto no seu explorador de arquivos (Finder no Mac, Explorer no Windows).
  * Entre na pasta `website`.
  * Dê um **clique duplo no arquivo `index.html`**.

A aplicação web será aberta no seu navegador e já estará pronta para se comunicar com a API que está rodando.

### Como Usar

1.  A página principal exibirá um formulário com campos para as principais características de um candidato a exoplaneta.
2.  Preencha os campos com os dados de um KOI. Você pode usar os valores padrão ou os [casos de teste sugeridos](https://www.google.com/search?q=link-para-os-casos-de-teste-se-tiver).
3.  Clique no botão **"Classificar"**.
4.  O resultado da classificação e uma visualização 3D interativa do sistema planetário aparecerão ao lado. Você pode girar a cena com o mouse e dar zoom com o scroll.

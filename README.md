# business_card_ocr

# Instalação
pip install -U -r requirements.txt

Se necessário instale o TensorFlow
python3 -m pip install tensorflow[and-cuda]
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
!pip install tensorflow-gpu==2.8.0

Atenção: Se estiver no Windows descomentar a linha do pywin32 e pywinpty

# Requisitos
- Python 3
- Jupyter Notebook

# Bibliotecas Python utilizadas no Módulo de Visão Computacional
- OpenCV
- Numpy
- Pytesseract

# Bibliotecas Python usadas no processamento de linguagem natural
- SpaCy
- Pandas
- Regular Expression
- String

O sistema segue as seguintes etapas utilizadas no projeto:

1. Preparação de dados
- Extraindo texto de imagens de cartão de visita
- Limpeza e rotulagem dos dados

2. Pré-processamento de dados
- Carregando e preparando os dados
- Convertendo dados em formato de treinamento Spacy
- Divisão Train-Test

3. Treinamento do Modelo NER com Spacy
- Arquitetura de Modelo e Processo de Treinamento
- Avaliação e Métricas de Desempenho

4. Testando o modelo treinado
- Preparação de dados em novas imagens
- Previsão e geração de caixa delimitadora
- Avaliação e Refinamento

5. Scanner de documentos
Detecção de bordas e transformações morfológicas
Transformação de perspectiva e recorte de imagem

6. Desenvolvimento de Web App em Flask
- Upload e digitalização de documentos
- Ajuste manual com JavaScript Canvas
- Extração de texto e previsão de entidade
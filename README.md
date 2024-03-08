# DevApps BCR (Business Card Reader)
O DevApps BCR é um pequeno sistema em Python projetado para extrair dados de cartões de visita usando OCR (Reconhecimento Óptico de Caracteres) e realizar processamento de linguagem natural com o SpaCy.

# Instalação
Antes de usar o DevApps BCR, é necessário instalar as dependências. Utilize o seguinte comando:

```
pip install -U -r requirements.txt
```
Certifique-se também de baixar o modelo de linguagem portuguesa para o SpaCy:
```
python -m spacy download pt_core_news_lg
```
Se necessário, instale o TensorFlow. Certifique-se de verificar a versão adequada para o seu sistema:
```
python3 -m pip install tensorflow[and-cuda]
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
!pip install tensorflow-gpu==2.8.0
```

Atenção: Se estiver no Windows, descomente a linha referente a **pywin32** e **pywinpty** no arquivo de requisitos (requirements.txt).

# Requisitos
- Python 3
- Jupyter Notebook (Treinamento do modelo)

# Bibliotecas Python utilizadas no Módulo de Visão Computacional
- OpenCV
- Numpy
- Pytesseract

# Bibliotecas Python usadas no processamento de linguagem natural
- SpaCy
- Pandas
- Regular Expression
- String

# Uso
Para iniciar a aplicação execute na raiz do projeto o comando:
```
python main.py
```
No navegador abra o link: [http://localhost:5000](http://localhost:5000)

O sistema visa facilitar a extração de dados de cartões de visita, proporcionando uma solução pronta para análise e organização das informações.

**Observação:** Certifique-se de seguir as boas práticas de segurança ao lidar com dados sensíveis extraídos dos cartões de visita.
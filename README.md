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

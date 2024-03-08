import os

# Diretório base do projeto (diretório de trabalho atual)
BASE_DIR = os.getcwd()

# Diretório onde os arquivos de mídia serão armazenados (estático)
MEDIA_DIR = 'static/media'

# Caminho completo para o diretório de salvamento de arquivos
SAVE_DIR = os.path.join(BASE_DIR, MEDIA_DIR)

def join_path(directory, filename):
    """
    Combina um diretório e um nome de arquivo para criar o caminho completo do arquivo.
    
    Parâmetros:
    - directory (str): Diretório onde o arquivo será armazenado.
    - filename (str): Nome do arquivo.
    
    Retorna:
    str: Caminho completo do arquivo combinando o diretório e o nome do arquivo.
    """
    filepath = os.path.join(directory, filename)
    return filepath
import os

# Diretório base do projeto (diretório de trabalho atual)
BASE_DIR = os.getcwd()

# Diretório onde os arquivos de mídia serão armazenados (estático)
MEDIA_DIR = 'static/media'

# Caminho completo para o diretório de salvamento de arquivos
SAVE_DIR = os.path.join(BASE_DIR, MEDIA_DIR)

def join_path(directory, filename):
    """
    Combina um diretório e um nome de arquivo para criar o caminho completo do arquivo.
    
    Parâmetros:
    - directory (str): Diretório onde o arquivo será armazenado.
    - filename (str): Nome do arquivo.
    
    Retorna:
    str: Caminho completo do arquivo combinando o diretório e o nome do arquivo.
    """
    filepath = os.path.join(directory, filename)
    return filepath

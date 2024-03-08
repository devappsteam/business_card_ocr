#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import cv2
import pytesseract
from glob import glob
import spacy
import re
import string
import warnings
warnings.filterwarnings('ignore')
import pt_core_news_lg

### Carrega o modelo NER
model_ner = spacy.load('./output/model-best/') # Modelo treinado
#model_ner = spacy.load('pt_core_news_lg') # modelo generico em PT

def cleanText(txt):
    """
    Limpa o texto removendo espaços em branco e pontuações.
    
    Parâmetros:
    - txt (str): O texto a ser limpo.
    
    Retorna:
    str: Texto limpo.
    """
    whitespace = string.whitespace
    punctuation = "!#$%&\'()*+:;<=>?[\\]^`{|}~"
    tableWhitespace = str.maketrans('', '', whitespace)
    tablePunctuation = str.maketrans('', '', punctuation)
    text = str(txt)
    removewhitespace = text.translate(tableWhitespace)
    removepunctuation = removewhitespace.translate(tablePunctuation)
    
    return str(removepunctuation)

# agrupa o rótulo
class groupgen():
    def __init__(self):
        self.id = 0
        self.text = ''
        
    def getgroup(self, text):
        """
        Atribui um grupo com base no texto. Se o texto for o mesmo que o texto anterior, o mesmo grupo é atribuído.
        Caso contrário, um novo grupo é criado.
        
        Parâmetros:
        - text (str): O texto para o qual o grupo está sendo atribuído.
        
        Retorna:
        int: ID do grupo atribuído.
        """
        if self.text == text:
            return self.id
        else:
            self.id += 1
            self.text = text
            return self.id

# Função para padronizar números de telefone para o formato +55 (xx) xxxx-xxxx
def format_phone(match):
    return f"({match.group(1)}) {match.group(2)}-{match.group(3)}"

def parser(text, label):
    """
    Realiza o pré-processamento do texto com base no rótulo (label) associado.
    
    Parâmetros:
    - text (str): O texto a ser processado.
    - label (str): O rótulo associado ao texto.
    
    Retorna:
    str: Texto processado.
    """
    if label == 'PHONE':
        text = text.lower()
        pattern = re.compile('/((\(?0\d{4}\)?\s?\d{3}\s?\d{3})|(\(?0\d{3}\)?\s?\d{3}\s?\d{4})|(\(?0\d{2}\)?\s?\d{4}\s?\d{4}))(\s?\#(\d{4}|\d{3}))?/;', re.VERBOSE)
        text = pattern.sub(format_phone, text)
        
    elif label == 'EMAIL':
        text = text.lower()
        text = re.sub('/(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))/;','',text)
        
    elif label == 'WEB':
        text = text.lower()
        text = re.sub('/[a-zA-Z0-9][a-zA-Z0-9-_]{0,61}[a-zA-Z0-9]{0,1}\.([a-zA-Z]{1,6}|[a-zA-Z0-9-]{1,30}\.[a-zA-Z]{2,3})/;','',text)
        
    elif label in ('NAME', 'DES'):
        text = text.lower()
        text = re.sub(r'[^a-z ]','',text)
        text = text.title()
        
    elif label == 'ORG':
        text = text.lower()
        text = re.sub(r'[^a-z0-9 ]','',text)
        text = text.title()
        
    return text

grp_gen = groupgen()

def getPredictions(image):
    """
    Extrai informações de texto da imagem usando Pytesseract, realiza o reconhecimento de entidades (NER) usando o modelo treinado,
    e retorna a imagem com caixas delimitadoras (Bounding Boxes) e as entidades extraídas.
    
    Parâmetros:
    - image: A imagem da qual as informações estão sendo extraídas.
    
    Retorna:
    - img_bb: Imagem com caixas delimitadoras desenhadas.
    - entities: Dicionário contendo entidades extraídas categorizadas.
    """
    # extrair dados usando Pytesseract
    tessData = pytesseract.image_to_data(image)
    # converter em dataframe
    tessList = list(map(lambda x:x.split('\t'), tessData.split('\n')))
    df = pd.DataFrame(tessList[1:],columns=tessList[0])
    df.dropna(inplace=True) # drop missing values
    df['text'] = df['text'].apply(cleanText)

    # converter dados em conteúdo
    df_clean = df.query('text != "" ')
    content = " ".join([w for w in df_clean['text']])
    
    print("///////////////////////////////")
    print("//// COUTEUDO EXTRAIDO    /////")
    print("///////////////////////////////")
    print('\n')
    print(content)
    print('\n\n\n')
    
    # obter previsão do modelo NER
    doc = model_ner(content)

    # convertendo documento em json
    docjson = doc.to_json()
    doc_text = docjson['text']

    # criando tokens
    datafram_tokens = pd.DataFrame(docjson['tokens'])
    datafram_tokens['token'] = datafram_tokens[['start','end']].apply(
        lambda x:doc_text[x[0]:x[1]] , axis = 1)

    right_table = pd.DataFrame(docjson['ents'])[['start','label']]
    datafram_tokens = pd.merge(datafram_tokens,right_table,how='left',on='start')
    datafram_tokens.fillna('O',inplace=True)

    # junta o rótulo do dataframe df_clean
    df_clean['end'] = df_clean['text'].apply(lambda x: len(x)+1).cumsum() - 1 
    df_clean['start'] = df_clean[['text','end']].apply(lambda x: x[1] - len(x[0]),axis=1)

    # junção interna com início
    dataframe_info = pd.merge(df_clean,datafram_tokens[['start','token','label']],how='inner',on='start')

    # Área delimitadora

    bb_df = dataframe_info.query("label != 'O' ")

    bb_df['label'] = bb_df['label'].apply(lambda x: x[2:])
    bb_df['group'] = bb_df['label'].apply(grp_gen.getgroup)

    # direita e inferior da área delimitadora
    bb_df[['left','top','width','height']] = bb_df[['left','top','width','height']].astype(int)
    bb_df['right'] = bb_df['left'] + bb_df['width']
    bb_df['bottom'] = bb_df['top'] + bb_df['height']

    # marcação: grupo por grupo
    col_group = ['left','top','right','bottom','label','token','group']
    group_tag_img = bb_df[col_group].groupby(by='group')
    img_tagging = group_tag_img.agg({

        'left':min,
        'right':max,
        'top':min,
        'bottom':max,
        'label':np.unique,
        'token':lambda x: " ".join(x)

    })

    img_bb = image.copy()
    for l,r,t,b,label,token in img_tagging.values:
        cv2.rectangle(img_bb,(l,t),(r,b),(0,255,0),2)

        cv2.putText(img_bb,label,(l,t),cv2.FONT_HERSHEY_PLAIN,1,(255,0,255),2)


    # Entidades

    info_array = dataframe_info[['token','label']].values
    entities = dict(NAME=[],ORG=[],DES=[],PHONE=[],EMAIL=[],WEB=[])
    previous = 'O'

    for token, label in info_array:
        bio_tag = label[0]
        label_tag = label[2:]
        text = parser(token,label_tag)

        if bio_tag in ('B','I'):

            if previous != label_tag:
                entities[label_tag].append(text)

            else:
                if bio_tag == "B":
                    entities[label_tag].append(text)

                else:
                    if label_tag in ("NAME",'ORG','DES'):
                        entities[label_tag][-1] = entities[label_tag][-1] + " " + text

                    else:
                        entities[label_tag][-1] = entities[label_tag][-1] + text


        previous = label_tag
        
    return img_bb, entities

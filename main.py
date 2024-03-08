from flask import Flask, request
from flask import render_template
import settings
import utils
import numpy as np
import cv2
import predictions as pred

app = Flask(__name__)
app.secret_key = 'business_card_ocr'

docscan = utils.DocumentScan()

@app.route('/', methods=['GET', 'POST'])
def scandoc():
    """
    Rota principal do aplicativo que lida com o upload e digitalização de documentos.

    Se o método for POST, realiza o upload da imagem, salva-a e tenta prever as coordenadas do documento.
    Em seguida, exibe as coordenadas ou uma mensagem de erro na página web.

    Se o método for GET, renderiza a página inicial do scanner.

    Retorna:
    render_template: Página HTML com as coordenadas ou mensagem de erro.
    """
    if request.method == 'POST':
        file = request.files['image_name']
        upload_image_path = utils.save_upload_image(file)
        print('Image saved in = ', upload_image_path)
        
        # Prever as coordenadas do documento
        four_points, size = docscan.document_scanner(upload_image_path)
        print(four_points, size)

        if four_points is None:
            message = 'INCAPAZ DE LOCALIZAR AS COORDENADAS DO DOCUMENTO: os pontos exibidos são aleatórios.'
            points = [
                {'x': 10, 'y': 10},
                {'x': 120, 'y': 10},
                {'x': 120, 'y': 120},
                {'x': 10, 'y': 120}
            ]
            return render_template('scanner.html', points=points, fileupload=True, message=message)

        else:
            points = utils.array_to_json_format(four_points)
            message = 'Localizou as coordenadas do documento usando OpenCV'
            return render_template('scanner.html', points=points, fileupload=True, message=message)

    return render_template('scanner.html')

@app.route('/transform', methods=['POST'])
def transform():
    """
    Rota para transformar a imagem escaneada para o tamanho original com base nas coordenadas fornecidas.

    Retorna:
    str: 'sucess' se bem-sucedido, 'fail' se houver falha.
    """
    try:
        points = request.json['data']
        array = np.array(points)
        magic_color = docscan.calibrate_to_original_size(array)

        # Salva a imagem transformada
        filename = 'magic_color.jpg'
        magic_image_path = settings.join_path(settings.MEDIA_DIR, filename)
        cv2.imwrite(magic_image_path, magic_color)

        return 'success'

    except:
        return 'fail'

@app.route('/prediction')
def prediction():
    """
    Rota para exibir as previsões do texto na imagem transformada.

    Retorna:
    render_template: Página HTML com as previsões.
    """
    # Carrega a imagem transformada
    wrap_image_filepath = settings.join_path(settings.MEDIA_DIR, 'magic_color.jpg')
    image = cv2.imread(wrap_image_filepath)
    image_bb, results = pred.getPredictions(image)

    # Salva a imagem com caixas delimitadoras
    bb_filename = settings.join_path(settings.MEDIA_DIR, 'bounding_box.jpg')
    cv2.imwrite(bb_filename, image_bb)

    return render_template('predictions.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)
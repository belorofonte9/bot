from imagekitio import ImageKit
from config import *
from base64 import b64encode
from pprint import pprint
import telebot


ik = ImageKit(public_key=IK_PUBLIC, private_key=IK_PRIVATE, url_endpoint=IK_URL)

def ik_subir_imagen(ruta_imagen, nombre_archivo):
    with open(ruta_imagen, "rb") as f:
        imagen = b64encode(f.read())
    print("♔ ♕ ♖ ♗ ♘ ♙ ♚ ♛ ♜ ♝ ♞ ♟ subiendo imagen a imagekit")
    try:
        res = ik.upload_file(file=imagen, file_name=nombre_archivo)
    except Exception as e:
        return f'ERROR: ✘ {e.message}'
    
    status_code = res.response_metadata.http_status_code
    
    if status_code == 200:
        return res.response_metadata.raw
    else:
        return f'ERROR: ✘ {status_code}'


def ik_eliminar_imagen(file_id):
    try:
        res = ik.delete_file(file_id=file_id)
    except Exception as e:
        return f'ERROR: ✘ {e.message}'
    status_code = res.response_metadata.http_status_code
    if status_code == 204:
        return "OK"
    else:
        return f'ERROR: ✘ {status_code}'



if __name__ == '__main__':
    #res = ik_subir_imagen("eav1.jpeg", "eav1.jpeg")
    #pprint(res, sort_dicts=False)        
    res = ik_eliminar_imagen("651e2cc888c257da33463588")  
    pprint(res) 
    
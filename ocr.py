from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import pytesseract
import os
import re
import shutil

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def procesar_imagen(image_path):
    
    img_original = Image.open(image_path)
  
    exif_orientation = img_original.getexif().get(274, 1)

    if exif_orientation == 3:
        img_original = img_original.rotate(180, expand=True)
    elif exif_orientation == 6:
        img_original = img_original.rotate(-90, expand=True)
    elif exif_orientation == 8:
        img_original = img_original.rotate(90, expand=True)

    # Aplicar mejoras en la imagen:
    enhancer_contrast = ImageEnhance.Contrast(img_original)
    img_contrast = enhancer_contrast.enhance(2.5)

    img_grayscale = ImageOps.grayscale(img_contrast)

    threshold = 0  # NOTA: Cambiar valor.
    img_binarized = img_grayscale.point(lambda p: p > threshold and 250)

    img_smoothed = img_binarized.filter(ImageFilter.SMOOTH)
    
    img_no_noise = img_smoothed.filter(ImageFilter.MedianFilter(size=5))
    
    enhancer_brightness = ImageEnhance.Brightness(img_no_noise)
    img_final = enhancer_brightness.enhance(2.0)

    new_size = (img_original.width // 2, img_original.height // 2)
    img_resized = img_final.resize(new_size, Image.LANCZOS)
    
    # Realizar el procesamiento OCR en img_resized:
    texto_extraido = pytesseract.image_to_string(img_resized)

    # Encontrar el número de remito en el texto extraído:
    inicio_remito = texto_extraido.find("REMITO")
    fin_remito = texto_extraido.find("\n", inicio_remito) if inicio_remito != -1 else len(texto_extraido)
    remito = texto_extraido[inicio_remito:fin_remito].strip()

    if not remito:
        inicio_ot = texto_extraido.find("OT")
        fin_ot = texto_extraido.find("\n", inicio_ot) if inicio_ot != -1 else len(texto_extraido)
        ot = texto_extraido[inicio_ot:fin_ot].strip()

        # Usar OT como identificador si se encuentra:
        if ot:
            remito = ot

    if not remito:
        remito = "DESCONOCIDO"

    return img_resized, remito

# Ruta del directorio que contiene las imagenes:
directorio_imagenes = ''

archivos = os.listdir(directorio_imagenes)

for archivo in archivos:
    
    if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        
        if re.match(r'(REMITO_|OT_)', archivo):
            print(f"El archivo {archivo} ya tiene el formato de remito deseado. No se realizarán cambios.")
            continue

        image_path = os.path.join(directorio_imagenes, archivo)

        img_resized, remito = procesar_imagen(image_path)

        print(f"Para la imagen {archivo}, el numero de remito es: {remito}")

        remito = ''.join(caracter if caracter.isalnum() or caracter in {'-', '_'} else '_' for caracter in remito)

        nuevo_nombre = remito

        nueva_ruta = os.path.join(directorio_imagenes, nuevo_nombre)

        try:
            contador = 1
            while os.path.exists(nueva_ruta):
                nuevo_nombre = remito + f"_{contador}" 
                nueva_ruta = os.path.join(directorio_imagenes, nuevo_nombre)
                contador += 1

            shutil.copy2(image_path, nueva_ruta)

            print(f"La imagen {archivo} ha sido reemplazada con el nombre: {nuevo_nombre}")

            os.remove(image_path)
        except Exception as e:
            print(f"Error al guardar la imagen {archivo}: {e}")

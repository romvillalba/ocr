# Tesseract OCR Image Processing

Este proyecto es un script de Python que utiliza el motor Tesseract OCR para procesar imágenes y extraer información de remitos o números de orden de trabajo (OT).

## Descripción

El script utiliza la biblioteca Pytesseract para realizar OCR en imágenes. Primero, aplica diversas mejoras a las imágenes para aumentar la calidad del texto extraído. Luego, busca y extrae el número de remito o, en su defecto, el número de OT del texto.

## Requisitos

Antes de utilizar este script, asegúrate de tener instalado Tesseract OCR en tu sistema y configura la ruta correcta en la variable `pytesseract.pytesseract.tesseract_cmd`. Además, necesitas tener las bibliotecas Pillow y OpenCV instaladas. Puedes instalar estas dependencias ejecutando:

```bash
pip install pytesseract pillow opencv-python

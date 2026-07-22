# IA-Document-Converter

Herramienta desarrollada en Python para convertir documentos e imágenes a formato Markdown optimizado para su uso con modelos de Inteligencia Artificial (LLMs), sistemas RAG (Retrieval-Augmented Generation) y bases de conocimiento.

---

# Objetivos

El proyecto busca automatizar la conversión de distintos formatos de documentos hacia Markdown, preservando en la mayor medida posible:

- estructura
- títulos
- tablas
- imágenes
- listas
- metadatos

El sistema será escalable para soportar múltiples tipos de documentos y diferentes motores de extracción.

---

# Tecnologías

- Python 3.11+
- Docling
- PyPDF
- Pillow
- pytesseract
- Markdown
- Git
- VS Code

Tecnologías futuras:

- OCR
- Modelos Vision
- LangChain
- ChromaDB
- FAISS

> Para OCR en imágenes se requiere tener instalado Tesseract OCR en el sistema.
>
> En Windows, si no está en `PATH`, puedes definir:
>
> ```powershell
> $env:DOC2MD_TESSERACT_CMD="C:\Program Files\Tesseract-OCR\tesseract.exe"
> ```
>
> El proyecto también intenta detectar automáticamente estas rutas:
>
> - `C:\Program Files\Tesseract-OCR\tesseract.exe`
> - `C:\Program Files (x86)\Tesseract-OCR\tesseract.exe`

---

# Arquitectura

```
Usuario
    │
    ▼
python main.py
    │
    ▼
main.py
    │
    ▼
controller.py
    │
    ├───────────────┐
    ▼               ▼
converter.py     ocr.py
    │               │
    └───────┬───────┘
            ▼
      cleaner.py
            │
            ▼
      exporter.py
            │
            ▼
         output/
```

---

# Estructura del proyecto

```
IA-Document-Converter/

│
├── input/
│
├── output/
│
├── logs/
│
├── tests/
│
├── src/
│   └── doc2markdown/
│       ├── __init__.py
│       ├── config.py
│       ├── controller.py
│       ├── converter.py
│       ├── exporter.py
│       ├── cleaner.py
│       ├── ocr.py
│       └── utils.py
│
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

# Responsabilidad de cada módulo

## main.py

Punto de entrada de la aplicación.

Responsabilidades:

- iniciar el programa
- invocar el controlador
- finalizar la ejecución

No contiene lógica de negocio.

---

## controller.py

Coordina todo el flujo de ejecución.

Responsabilidades:

- localizar archivos
- identificar el tipo de documento
- llamar al conversor adecuado
- controlar errores
- informar progreso

No realiza conversiones.

---

## converter.py

Convierte documentos PDF utilizando Docling.

Entrada:

- PDF

Salida:

- Markdown

No guarda archivos.

---

## ocr.py

Procesará imágenes cuando el documento no contenga texto.

Entrada:

- PNG
- JPG
- TIFF
- WEBP

Salida:

- Texto Markdown

---

## cleaner.py

Normaliza el Markdown generado.

Ejemplos:

- eliminar espacios innecesarios
- corregir encabezados
- limpiar tablas
- normalizar listas

---

## exporter.py

Responsable exclusivo del almacenamiento.

Funciones:

- guardar Markdown
- crear directorios
- escribir archivos

No realiza conversiones.

---

## config.py

Configuración global del proyecto.

Contendrá:

- rutas
- formatos soportados
- configuración OCR
- configuración de IA
- constantes

---

## utils.py

Funciones auxiliares reutilizables.

Ejemplos:

- validaciones
- temporizadores
- utilidades de rutas
- manejo de fechas

---

# Flujo de procesamiento

## PDF

```
PDF

↓

Docling

↓

Markdown

↓

Cleaner

↓

Exporter

↓

Archivo .md
```

---

## Imagen

```
Imagen

↓

OCR

↓

Markdown

↓

Cleaner

↓

Exporter

↓

Archivo .md
```

---

# Interfaces públicas

## converter.py

```python
convert_pdf_to_markdown(pdf_path: Path) -> str
```

Devuelve únicamente el contenido Markdown.

Nunca escribe archivos.

---

## exporter.py

```python
save_markdown(markdown: str, output_file: Path) -> None
```

Responsable de guardar el resultado.

---

## controller.py

```python
run() -> None
```

Punto central de ejecución.

---

# Principios del proyecto

## Responsabilidad única

Cada módulo debe hacer una sola cosa.

---

## Bajo acoplamiento

Los módulos deben depender lo menos posible entre sí.

---

## Alta cohesión

Cada archivo debe contener funcionalidades relacionadas.

---

## Escalabilidad

La incorporación de nuevos formatos no debe requerir modificar módulos existentes.

---

# Roadmap

## Versión 0.1

- [x] Arquitectura
- [x] Configuración
- [x] Exportador
- [ ] Conversión PDF
- [ ] Controlador
- [ ] Main

---

## Versión 0.2

- [ ] OCR
- [ ] Limpieza de Markdown
- [ ] Procesamiento por lotes

---

## Versión 0.3

- [x] Extracción de tablas (básica a Markdown)
- [x] Descripción de imágenes (orientación, tamaño y color)
- [x] Metadata (archivo, formato y propiedades base)

---

## Versión 1.0

- [x] Conversión PDF
- [x] Conversión de imágenes
- [x] OCR (básico con Tesseract)
- [x] Limpieza
- [x] Exportación
- [x] Optimización para RAG (normalización + segmentación de párrafos)
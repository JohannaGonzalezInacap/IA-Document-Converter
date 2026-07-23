# IA-Document-Converter

Herramienta desarrollada en Python para convertir documentos e imágenes a formato Markdown optimizado para su uso con modelos de Inteligencia Artificial (LLMs), sistemas RAG (Retrieval-Augmented Generation) y bases de conocimiento.

---

# Objetivos

El proyecto automatiza la conversión de distintos formatos de documentos hacia Markdown, preservando en la mayor medida posible:

- estructura
- títulos
- tablas
- imágenes
- listas
- metadatos

El sistema es escalable para soportar múltiples tipos de documentos y diferentes motores de extracción.

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

# Instalación

```bash
git clone https://github.com/JohannaGonzalezInacap/IA-Document-Converter.git
cd IA-Document-Converter
python -m venv .venv
.venv\Scripts\activate     # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

---

# Uso

1. Coloca los documentos o imágenes a convertir dentro de `input/`.
2. Ejecuta:

```bash
python main.py
```

3. Los archivos `.md` generados quedarán disponibles en `output/`.

---

# Tests

El proyecto cuenta con una suite de pruebas automatizadas con Pytest (100% aprobadas):

```bash
pytest
```

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

Procesa imágenes cuando el documento no contiene texto.

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

Contiene:

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

Cada módulo hace una sola cosa.

---

## Bajo acoplamiento

Los módulos dependen lo menos posible entre sí.

---

## Alta cohesión

Cada archivo contiene funcionalidades relacionadas.

---

## Escalabilidad

La incorporación de nuevos formatos no requiere modificar módulos existentes.

---

# Estado actual — Versión 1.0

- [x] Arquitectura modular (SOLID)
- [x] Configuración
- [x] Conversión de PDF (Docling)
- [x] Conversión de imágenes
- [x] OCR (Tesseract)
- [x] Limpieza y normalización de Markdown
- [x] Extracción de tablas (básica a Markdown)
- [x] Descripción de imágenes (orientación, tamaño y color)
- [x] Metadata (archivo, formato y propiedades base)
- [x] Exportación de archivos
- [x] Optimización para RAG (normalización + segmentación de párrafos)
- [x] Suite de pruebas automatizadas (Pytest)

---

# Próximos pasos

- [ ] Procesamiento por lotes
- [ ] Integración con LangChain
- [ ] Integración con ChromaDB / FAISS para indexación vectorial
- [ ] Soporte para modelos de Vision en la extracción de imágenes

---

# Autora

Johanna González — [GitHub](https://github.com/JohannaGonzalezInacap) · [LinkedIn](https://www.linkedin.com/in/johanna-gonzalez-desarrollador)

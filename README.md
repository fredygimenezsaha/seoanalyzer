# Analizador SEO

## Descripción
Este proyecto es una herramienta de análisis SEO desarrollada en Python. Evalúa diversos parámetros de optimización para motores de búsqueda en una página web específica y genera un informe detallado en formato Excel.

## Características principales
- Análisis completo de factores SEO, incluyendo:
  - Título y meta descripción
  - Uso de palabras clave
  - Estructura de encabezados
  - Enlaces internos y externos
  - Longitud del contenido
  - Optimización de imágenes
  - Detección de enlaces rotos
  - Adaptabilidad móvil
  - Tiempo de carga
  - Seguridad HTTPS
  - Datos estructurados
- Generación de informe en Excel con evaluación de optimización

## Requisitos
- Python 3.x
- Bibliotecas: requests, beautifulsoup4, pandas, openpyxl

## Instalación
1. Clona el repositorio:
   ```
   git clone [https://github.com/fredygimenezsaha/seoanalyzer.git]
   ```
2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Uso
1. Edita la URL en `main.py`:
   ```python
   url = 'https://tu-sitio-web.com/'
   ```
2. Ejecuta el script:
   ```
   python main.py
   ```
3. Revisa el informe generado en `seo_report.xlsx`

## Estructura del proyecto
- `main.py`: Código fuente principal
- `requirements.txt`: Dependencias del proyecto
- `seo_report.xlsx`: Informe SEO generado (se crea al ejecutar el script)

## Contribuciones
Agradecemos las contribuciones. Por favor, abre un issue para discutir cambios importantes antes de enviar un pull request.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
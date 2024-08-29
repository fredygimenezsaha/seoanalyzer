import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time

# Parámetros óptimos para SEO
OPTIMAL_PARAMS = {
    'Title Length': (50, 60),
    'Meta Description Length': (150, 160),
    'H1': 1,
    'Internal Links': 10,
    'Content Length': 300,
    'Keyword in Title': True,
    'Keyword in Meta Description': True,
    'Alt Text for Images': True,
    'Broken Links': 0,
    'Viewport Meta Tag': True,
    'Page Load Time': 2,  # Tiempo de carga óptimo en segundos
    'Keyword Density': (1, 3),  # Porcentaje de densidad de palabras clave óptimo
    'URL Structure': True,  # Estructura URL amigable
    'Backlinks': 5,  # Número mínimo de backlinks de calidad
    'Mobile Friendly': True,
    'HTTPS': True,
    'Structured Data': True,
    'Content Freshness': True  # Contenido actualizado recientemente
}

def is_keyword_present(text, keyword='SEO'):
    return keyword.lower() in text.lower()

def analyze_seo(url):
    try:
        # Medir el tiempo de carga de la página
        start_time = time.time()
        response = requests.get(url)
        response.raise_for_status()
        load_time = time.time() - start_time
        
        html_content = response.text
        
        # Analizar el contenido HTML
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Inicializar el informe
        report = []
        
        # Analizar el título
        title = soup.title.string if soup.title else 'No title found'
        title_length = len(title)
        title_optimized = 'Optimal' if OPTIMAL_PARAMS['Title Length'][0] <= title_length <= OPTIMAL_PARAMS['Title Length'][1] else 'Not Optimal'
        report.append(['Title', title, title_length, title_optimized])
        
        # Analizar la meta descripción
        meta_description = soup.find('meta', attrs={'name': 'description'})
        meta_description_content = meta_description['content'] if meta_description else 'No meta description found'
        meta_description_length = len(meta_description_content)
        meta_description_optimized = 'Optimal' if OPTIMAL_PARAMS['Meta Description Length'][0] <= meta_description_length <= OPTIMAL_PARAMS['Meta Description Length'][1] else 'Not Optimal'
        report.append(['Meta Description', meta_description_content, meta_description_length, meta_description_optimized])
        
        # Análisis de palabras clave
        keyword_in_title = 'Optimal' if is_keyword_present(title) == OPTIMAL_PARAMS['Keyword in Title'] else 'Not Optimal'
        keyword_in_meta_description = 'Optimal' if is_keyword_present(meta_description_content) == OPTIMAL_PARAMS['Keyword in Meta Description'] else 'Not Optimal'
        report.append(['Keyword in Title', is_keyword_present(title), '', keyword_in_title])
        report.append(['Keyword in Meta Description', is_keyword_present(meta_description_content), '', keyword_in_meta_description])
        
        # Analizar las etiquetas de encabezado
        headers = {f'H{level}': len(soup.find_all(f'h{level}')) for level in range(1, 7)}
        h1_optimized = 'Optimal' if headers.get('H1', 0) == OPTIMAL_PARAMS['H1'] else 'Not Optimal'
        report.append(['H1', headers.get('H1', 0), '', h1_optimized])
        
        # Analizar los enlaces internos y externos
        links = soup.find_all('a', href=True)
        internal_links = [urljoin(url, link['href']) for link in links if url in link['href']]
        external_links = [urljoin(url, link['href']) for link in links if url not in link['href']]
        internal_links_optimized = 'Optimal' if len(internal_links) >= OPTIMAL_PARAMS['Internal Links'] else 'Not Optimal'
        report.append(['Internal Links', len(internal_links), '', internal_links_optimized])
        
        # Analizar la longitud del contenido
        content_length = len(soup.get_text())
        content_length_optimized = 'Optimal' if content_length >= OPTIMAL_PARAMS['Content Length'] else 'Not Optimal'
        report.append(['Content Length', content_length, '', content_length_optimized])
        
        # Verificar atributos alt en imágenes
        images = soup.find_all('img')
        images_with_alt = sum(1 for img in images if img.get('alt'))
        alt_text_optimized = 'Optimal' if (images_with_alt / len(images)) >= 0.9 else 'Not Optimal'
        report.append(['Alt Text for Images', images_with_alt, len(images), alt_text_optimized])
        
        # Verificar enlaces rotos
        broken_links = 0
        for link in links:
            link_url = urljoin(url, link['href'])
            try:
                link_response = requests.head(link_url, allow_redirects=True)
                if link_response.status_code != 200:
                    broken_links += 1
            except requests.RequestException:
                broken_links += 1
        broken_links_optimized = 'Optimal' if broken_links <= OPTIMAL_PARAMS['Broken Links'] else 'Not Optimal'
        report.append(['Broken Links', broken_links, '', broken_links_optimized])
        
        # Verificar meta etiqueta viewport
        viewport_meta = soup.find('meta', attrs={'name': 'viewport'})
        viewport_meta_optimized = 'Optimal' if viewport_meta else 'Not Optimal'
        report.append(['Viewport Meta Tag', viewport_meta is not None, '', viewport_meta_optimized])
        
        # Verificar tiempo de carga
        load_time_optimized = 'Optimal' if load_time <= OPTIMAL_PARAMS['Page Load Time'] else 'Not Optimal'
        report.append(['Page Load Time', f'{load_time:.2f} seconds', '', load_time_optimized])
        
        # Verificar estructura URL
        url_structure_optimized = 'Optimal' if '/' in url else 'Not Optimal'
        report.append(['URL Structure', url_structure_optimized, '', url_structure_optimized])
        
        # Verificar adaptabilidad móvil
        mobile_friendly = 'Optimal' if viewport_meta else 'Not Optimal'
        report.append(['Mobile Friendly', mobile_friendly, '', mobile_friendly])
        
        # Verificar HTTPS
        https_status = 'Optimal' if url.startswith('https://') else 'Not Optimal'
        report.append(['HTTPS', https_status, '', https_status])
        
        # Verificar datos estructurados
        structured_data = soup.find('script', attrs={'type': 'application/ld+json'})
        structured_data_optimized = 'Optimal' if structured_data else 'Not Optimal'
        report.append(['Structured Data', structured_data is not None, '', structured_data_optimized])
        
        # Verificar frescura del contenido
        content_freshness = 'Not Optimal'  # Placeholder, requiere monitoreo regular
        report.append(['Content Freshness', content_freshness, '', content_freshness])
        
        # Convertir el informe a un formato de DataFrame donde cada parámetro está en una fila
        df = pd.DataFrame(report, columns=['Parameter', 'Value', 'Additional Info', 'Optimization Status'])
        
        # Calcular el resumen
        total_params = len(report)
        optimal_count = sum(1 for item in report if item[-1] == 'Optimal')
        optimal_percentage = (optimal_count / total_params) * 100
        summary = [
            ['Summary', '', '', f'Optimal Parameters: {optimal_count}/{total_params} ({optimal_percentage:.2f}%)']
        ]
        summary_df = pd.DataFrame(summary, columns=['Parameter', 'Value', 'Additional Info', 'Optimization Status'])
        
        # Concatenar el informe y el resumen
        final_df = pd.concat([df, summary_df], ignore_index=True)
        return final_df
    
    except requests.RequestException as e:
        return pd.DataFrame({'Parameter': ['Error'], 'Value': [str(e)], 'Additional Info': [''], 'Optimization Status': ['']})

# Ejemplo de uso
url = 'https://oesparaguay.com/'
seo_report_df = analyze_seo(url)

# Guardar el informe en un archivo Excel
excel_file = 'seo_report.xlsx'
seo_report_df.to_excel(excel_file, index=False, engine='openpyxl')

print(f'Informe SEO guardado en {excel_file}')

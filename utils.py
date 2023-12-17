XML_files_directory = "C:\\Users\\paleo\\OneDrive - Universita degli Studi Roma Tre\\Desktop\\Unimio\\OneDrive - Universita degli Studi Roma Tre\\magistrale\\Secondo Anno\\Ingegneria dei Dati\\Homework\\homework4\\XML_files"
Json_files_directory = "C:\\Users\\paleo\\OneDrive - Universita degli Studi Roma Tre\\Desktop\\Unimio\\OneDrive - Universita degli Studi Roma Tre\\magistrale\\Secondo Anno\\Ingegneria dei Dati\\Homework\\homework4\\JSON_files"
from bs4 import BeautifulSoup
import re, lxml
from lxml import etree
def remove_unicode(text):
    return text.encode('ascii', 'ignore').decode('ascii').strip('\n')

def get_clean_tag_soup(query_result):
    if query_result is not None and len(query_result) > 0:
        return _get_clean_tag_soup(query_result[0])
    return BeautifulSoup("", 'html.parser')

def _get_clean_tag_soup(elem):
    soup = BeautifulSoup(lxml.etree.tostring(elem, method='xml'), 'html.parser').find(True)
    # clear tag
    del soup['xmlns:mml']
    del soup['xmlns:xlink']

    return soup

def get_clean_tag_string(query_result):
    return remove_unicode(str(get_clean_tag_soup(query_result)))

def _get_clean_tag_string(elem):
    return remove_unicode(str(_get_clean_tag_soup(elem)))

def unwrap(html, unwrapping_content) :
    # Parsing dell'HTML
    soup_body = BeautifulSoup(html, 'html.parser')
    # Trova tutti gli elementi <table>
    tables = soup_body.find_all(unwrapping_content)
    # Rimuovi <table> e </table> mantenendo il contenuto
    for table in tables:
            table.unwrap()
    return str(soup_body)

def find_paragraphs_citations(xml_data, searching_element, type) :

    soup = BeautifulSoup(xml_data, 'xml')

    # Trova tutti gli elementi <p> che contengono <xref ref-type="table" rid="{searching_element}">
    target_paragraphs = [p for p in soup.find_all('p') if p.find('xref', {'ref-type': type, 'rid': searching_element})]

    results = {}

    for paragraph in target_paragraphs:
        # Trova tutti gli elementi <xref> con l'attributo ref-type="bibr"
        bibr_elements = paragraph.find_all('xref', {'ref-type': 'bibr'})
        
        # Lista dei valori di rid per il paragrafo corrente
        rid_values = [bibr_element.get('rid') for bibr_element in bibr_elements]
        
        # Aggiungi il risultato al dizionario
        results[str(paragraph)] = rid_values

    # per ogni paragrafo i suoi refeelements
    paragraphToRef = {}
    for paragraph, rid_values in results.items():
        ref_elements = []
        for r in rid_values :
            ref_elements += soup.find_all('ref', id=lambda value: r in value)
        ref_elements_string = []
        for ref_elem in ref_elements :
            ref_elements_string.append(str(ref_elem))
        paragraphToRef[str(paragraph)] = ref_elements_string
    return paragraphToRef

def find_caption_citations(caption) :
    soup = BeautifulSoup(caption, 'xml')
    bibr_elements = soup.find_all('xref', {'ref-type': 'bibr'})
    # Lista dei valori di rid per il paragrafo corrente
    rid_values = [bibr_element.get('rid') for bibr_element in bibr_elements]
    return rid_values

def find_cells(table_body, xml_data) :
    root = etree.fromstring(xml_data)
    # Parsing dell'HTML con BeautifulSoup
    soup = BeautifulSoup(table_body, 'html.parser')
    soup2 = BeautifulSoup(xml_data, 'xml')
    # Estrazione di tutte le celle che non sono nell'intestazione
    data_cells=[]
    for row in soup.find_all('tr'):
        row_cells = [remove_unicode(cell.get_text(strip=True)) for cell in row.find_all(['th', 'td'])]
        data_cells.extend(row_cells)
    #per ogni cella fai un dizionario cella --> lista paragrafi
    cellToPar = {}
    for cell in data_cells :
         # Trova tutti gli elementi <p> che contengono cell
        target_paragraphs = root.xpath("//p[contains(string(.), $target_text)]", target_text=cell)
        cleaned_target_paragraphs = []
        for t in target_paragraphs :
            cleaned_target_paragraphs.append(_get_clean_tag_string(t))
        if cleaned_target_paragraphs:
            cellToPar[cell] = cleaned_target_paragraphs
        else :
            cellToPar[cell] = []
    return cellToPar


def build_source(xlink_href_value, pmcid) : 
    return f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmcid}/{xlink_href_value}.jpg"
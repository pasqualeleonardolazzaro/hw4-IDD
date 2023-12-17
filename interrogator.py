from utils import *
from datetime import datetime
import os, json, lxml.etree
#funzione che trova l'id
def find_PMCID(xml_data) :
    # Creare un albero XML
    xml_tree = lxml.etree.fromstring(xml_data)
    article_id_elements = xml_tree.xpath('//article-id[@pub-id-type="pmc"]')
    # Fare una interrogazione XPath
    if article_id_elements:
        pmcid = article_id_elements[0].text
        pmcid_numero = pmcid[len("PMC"):]
        # Crea un dizionario con l'oggetto JSON
        json_data = {"pmcid": pmcid_numero}

        # Crea il percorso del file JSON nella cartella di output
        nome_file_json = "pmcid_" + pmcid_numero +".json"
        percorso_file_json = os.path.join(Json_files_directory, nome_file_json)

        # Scrivi il dizionario nel file JSON
        with open(percorso_file_json, 'w') as file_json:
            json.dump(json_data, file_json)
    else:
        print(f"Nessun elemento id trovato in {file}")
#funzione che trova il titolo
def find_title(xml_data, data_json, percorso_file_json) :
    # Creare un albero XML
    xml_tree = lxml.etree.fromstring(xml_data)
    article_title = xml_tree.xpath('//title-group/article-title/text()')
    # Fare una interrogazione XPath
    if article_title:
        title = article_title[0]
        # Crea un dizionario con l'oggetto JSON
        new_content = {
            "content": {
                "title": title
            }
        }
        # Add the new content to the existing data
        if not (any(obj == new_content for obj in data_json)) :
            data_json.update(new_content)
            # Write the updated data back to the JSON file
            with open(percorso_file_json, 'w') as f:
                json.dump(data_json, f, indent=2)
    else : 
        print(f"Content NOT added successfully to the JSON file: {percorso_file_json}")     
#funzione che trova l'abstract
def find_abstract(xml_data, data_json, percorso_file_json) :
    # Creare un albero XML
    xml_tree = lxml.etree.fromstring(xml_data)
    article_abstract_sec = xml_tree.xpath('//abstract')
    if len(article_abstract_sec) > 0 :
        html_abstract = lxml.etree.tostring(article_abstract_sec[0], encoding='unicode')
        abstract = unwrap(html_abstract, "abstract")
        data_json["content"]["abstract"] = abstract
        # Write the updated data back to the JSON file
        with open(percorso_file_json, 'w') as f:
            json.dump(data_json, f, indent=2)
        print("successo")
    else :
        data_json["content"]["abstract"] = ""
        print(f"abstract non trovato per : {percorso_file_json}")
        with open(percorso_file_json, 'w') as f:
            json.dump(data_json, f, indent=2)

#funzione che trova le keywords
def find_keywords(xml_data, data_json, percorso_file_json) :
    # Creare un albero XML
    xml_tree = lxml.etree.fromstring(xml_data)
    lista_keywords = xml_tree.xpath('//kwd-group/kwd/text()')
    # Fare una interrogazione XPath
    if lista_keywords:
        # Add the new content to the existing data
        if not (any(obj == lista_keywords for obj in data_json["content"])) :
            data_json["content"]["keywords"] = lista_keywords
            # Write the updated data back to the JSON file
            with open(percorso_file_json, 'w') as f:
                json.dump(data_json, f, indent=2)
        print("successo")
    else :
        data_json["content"]["keywords"] = []
        print(f"Keywords NOT added successfully to the JSON file: {percorso_file_json}")
        with open(percorso_file_json, 'w') as f:
                json.dump(data_json, f, indent=2)

#funzione per trovare le tabelle dei file
def find_tables(xml_data, data_json, percorso_file_json):
    xml_tree = lxml.etree.fromstring(xml_data)
    # Esecuzione della query XPath
    tab_element = xml_tree.xpath("//table-wrap/@id")
    # Verifica se l'elementoè stato trovato
    if "tables" not in data_json["content"]:
        data_json["content"]["tables"] = []
        i=0
        for tab in tab_element:
            body = xml_tree.xpath(f"//table-wrap[@id= '{tab}' ]/table")
            caption = xml_tree.xpath(f"//table-wrap[@id= '{tab}' ]/caption")
            foots = xml_tree.xpath(f"//table-wrap[@id= '{tab}' ]/table-wrap-foot")               
            if len(caption) > 0 :
                html_caption = lxml.etree.tostring(caption[0], encoding='unicode')
                cleaned_caption = unwrap(html_caption, "caption")   
            else :
                    cleaned_caption = ""
            if len(body) > 0 :
                html_body = lxml.etree.tostring(body[0], encoding='unicode')
                cleaned_body = unwrap(html_body, "table")
            else :
                cleaned_body = ""
            caption_citations = find_caption_citations(cleaned_caption)
            pToRef = find_paragraphs_citations(xml_data, f"{tab}", "table")
            cellToPar = find_cells(cleaned_body, xml_data)
            foots_list = []
            for f in foots : 
                    foots_list.append(unwrap(lxml.etree.tostring(f, encoding='unicode'),"table-wrap-foot" ))
            data_json["content"]["tables"].append( {"table_id": tab, "body": cleaned_body, "caption" : cleaned_caption, "caption_citations": caption_citations, "foots": foots_list, "paragraphs":[], "cells" : []})
            for p in pToRef.keys() :
                    data_json["content"]["tables"][i]["paragraphs"].append({"text" : p , "citations" : pToRef.get(p) })
            for c in cellToPar.keys() :
                    if c!="" :
                        data_json["content"]["tables"][i]["cells"].append({"content" : c , "cited_in" : cellToPar.get(c) })
            i+=1      
        # Write the updated data back to the JSON file
        with open(percorso_file_json, 'w') as f:
            json.dump(data_json, f, indent=2)
        print(f"Tables added successfully to the JSON file: {percorso_file_json}") 

#funzione che trova le figure
def find_figures(xml_data, data_json, percorso_file_json):
    xml_tree = lxml.etree.fromstring(xml_data)
    #print(article_abstract[0].xpath("string()"))
    fig_ids = xml_tree.xpath('//fig/@id')
    #Fare una interroìgazione XPath
    if fig_ids and ("figures" not in data_json["content"]) :
            data_json["content"]["figures"] = []
            i=0
            for fig_id in fig_ids:
                # Utilizza XPath per trovare la caption con un determinato id
                caption = xml_tree.xpath(f'//fig[@id="{fig_id}"]/caption')
                if len(caption) > 0 :
                    html_caption = lxml.etree.tostring(caption[0], encoding='unicode')
                    cleaned_caption = unwrap(html_caption, "caption")
                else :
                    cleaned_caption = ""
                # Definisci lo spazio dei nomi per xlink
                ns = {'xlink': 'http://www.w3.org/1999/xlink'}
                xlink_href_value0 = xml_tree.xpath(f'//fig[@id="{fig_id}"]/graphic/@xlink:href', namespaces=ns)
                if len(xlink_href_value0) > 0 :
                    xlink_href_value = xlink_href_value0[0]
                    source = build_source(xlink_href_value, data_json["pmcid"])
                else :
                    source = ""                   
                caption_citations = find_caption_citations(cleaned_caption)
                pToRef = find_paragraphs_citations(xml_data, f"{fig_id}", "fig")
                data_json["content"]["figures"].append( {"fig_id": fig_id, "src": source, "caption" : cleaned_caption, "caption_citations": caption_citations, "paragraphs":[]})
                for p in pToRef.keys() :
                        data_json["content"]["figures"][i]["paragraphs"].append({"text" : p , "citations" : pToRef.get(p) })
                i+=1
                # Write the updated data back to the JSON file
            with open(percorso_file_json, 'w') as f:
                json.dump(data_json, f, indent=2)
            print(f"Figure added successfully to the JSON file: {percorso_file_json}") 
  
    else:
        data_json["content"]["figures"] = []
        with open(percorso_file_json, 'w') as f:
            json.dump(data_json, f, indent=2) 

c=1
# scandisci la cartella in cui sono contenuti i file XML
for file in os.listdir(XML_files_directory):
    percorso_file = os.path.join(XML_files_directory, file)
    file_name = os.path.basename(percorso_file)
    file_json = "pmcid_" + file_name[len("PMC"):-4] + ".json"
    # Aprire il file XML
    with open(percorso_file, 'r') as f:
        xml_data = f.read()
    #find_PMCID(xml_data)
    percorso_file_json = os.path.join(Json_files_directory, "pmcid_5023793.json")
    with open(percorso_file_json, 'r') as f:
        data = json.load(f)
    print(xml_data)
    find_title(xml_data, data, percorso_file_json)
    find_abstract(xml_data, data, percorso_file_json)
    find_keywords(xml_data, data, percorso_file_json)
    find_tables(xml_data, data, percorso_file_json)
    find_figures(xml_data, data, percorso_file_json)
    print(c)
    c+=1
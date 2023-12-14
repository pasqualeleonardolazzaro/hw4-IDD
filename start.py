from utils import *
from bs4 import BeautifulSoup
import os, json, lxml.etree

# with open('C:\\Users\\paleo\\OneDrive - Universita degli Studi Roma Tre\\Desktop\\Unimio\\OneDrive - Universita degli Studi Roma Tre\\magistrale\\Secondo Anno\\Ingegneria dei Dati\\Homework\\homework4\\XML_files\\PMC497049.xml', 'r') as f:
#         xml_data = f.read()
# xml_tree = lxml.etree.fromstring(xml_data)
# #print(article_abstract[0].xpath("string()"))
# tab_element = xml_tree.xpath("//table-wrap/@id")
# #Fare una interroìgazione XPath
# if tab_element:
#         with open('C:\\Users\\paleo\\OneDrive - Universita degli Studi Roma Tre\\Desktop\\Unimio\\OneDrive - Universita degli Studi Roma Tre\\magistrale\\Secondo Anno\\Ingegneria dei Dati\\Homework\\homework4\\JSON_files\\pmcid_497049.json', 'r') as f:
#                 data = json.load(f)
#         data["content"]["tables"] = []
#         i=0
#         for tab in tab_element:
#                 body = xml_tree.xpath(f"//table-wrap[@id= '{tab}' ]/table[@frame='hsides' and @rules='groups']")
#                 caption = xml_tree.xpath(f"//table-wrap[@id= '{tab}' ]/caption")
#                 foots = xml_tree.xpath(f"//table-wrap[@id= '{tab}' ]/table-wrap-foot")
#                 html_body = lxml.etree.tostring(body[0], encoding='unicode')
#                 html_caption = lxml.etree.tostring(caption[0], encoding='unicode')
#                 cleaned_body = unwrap(html_body, "table")
#                 cleaned_caption = unwrap(html_caption, "caption")
#                 caption_citations = find_caption_citations(cleaned_caption)
#                 pToRef = find_paragraphs_citations(xml_data, f"{tab}")
#                 cellToPar = find_cells(cleaned_body, xml_data)
#                 foots_list = []
#                 for f in foots : 
#                         foots_list.append(unwrap(lxml.etree.tostring(f, encoding='unicode'),"table-wrap-foot" ))
#                 data["content"]["tables"].append( {"table_id": tab, "body": cleaned_body, "caption" : cleaned_caption, "caption_citations": caption_citations, "foots": foots_list, "paragraphs":[], "cells" : []})
#                 for p in pToRef.keys() :
#                         data["content"]["tables"][i]["paragraphs"].append({"text" : p , "citations" : pToRef.get(p) })
#                 for c in cellToPar.keys() :
#                         data["content"]["tables"][i]["cells"].append({"content" : c , "cited_in" : cellToPar.get(c) })
#                 i+=1
#         # Write the updated data back to the JSON file
#         with open('C:\\Users\\paleo\\OneDrive - Universita degli Studi Roma Tre\\Desktop\\Unimio\\OneDrive - Universita degli Studi Roma Tre\\magistrale\\Secondo Anno\\Ingegneria dei Dati\\Homework\\homework4\\JSON_files\\pmcid_497049.json', 'w') as f:
#                 json.dump(data, f, indent=2)

# # else : 
# #     print(f"Content NOT added successfully to the JSON file: ")

with open('C:\\Users\\paleo\\OneDrive - Universita degli Studi Roma Tre\\Desktop\\Unimio\\OneDrive - Universita degli Studi Roma Tre\\magistrale\\Secondo Anno\\Ingegneria dei Dati\\Homework\\homework4\\XML_files\\pmcid_4749569.json', 'r') as f:
        xml_data = f.read()
xml_tree = lxml.etree.fromstring(xml_data)
article_abstract_sec = xml_tree.xpath('//abstract')
if len(article_abstract_sec) > 0 :
        html_abstract = lxml.etree.tostring(article_abstract_sec[0], encoding='unicode')
        abstract = unwrap(html_abstract, "abstract")
        print
#print(article_abstract[0].xpath("string()"))
# fig_ids = xml_tree.xpath('//fig/@id')
# print(fig_ids)
# #Fare una interroìgazione XPath
# if fig_ids:
#         with open('C:\\Users\\paleo\\OneDrive - Universita degli Studi Roma Tre\\Desktop\\Unimio\\OneDrive - Universita degli Studi Roma Tre\\magistrale\\Secondo Anno\\Ingegneria dei Dati\\Homework\\homework4\\JSON_files\\pmcid_4749569.json', 'r') as f:
#                 data = json.load(f)
#         data["content"]["figures"] = []
#         i=0
#         for fig_id in fig_ids:
#                 # Utilizza XPath per trovare la caption con un determinato id
#                 caption = xml_tree.xpath(f'//fig[@id="{fig_id}"]/caption')
#                 html_caption = lxml.etree.tostring(caption[0], encoding='unicode')
#                 cleaned_caption = unwrap(html_caption, "caption")
#                 print(cleaned_caption)
#                 # Definisci lo spazio dei nomi per xlink
#                 ns = {'xlink': 'http://www.w3.org/1999/xlink'}
#                 xlink_href_value = xml_tree.xpath(f'//fig[@id="{fig_id}"]/graphic/@xlink:href', namespaces=ns)[0]
#                 print(xlink_href_value)
#                 source = build_source(xlink_href_value, data["pmcid"])
#                 print(source)
#                 caption_citations = find_caption_citations(cleaned_caption)
#                 print(caption_citations)
#                 pToRef = find_paragraphs_citations(xml_data, f"{fig_id}", "fig")
#                 print(pToRef)
#                 data["content"]["figures"].append( {"fig_id": fig_id, "src": source, "caption" : cleaned_caption, "caption_citations": caption_citations, "paragraphs":[]})
#                 for p in pToRef.keys() :
#                         data["content"]["figures"][i]["paragraphs"].append({"text" : p , "citations" : pToRef.get(p) })
#                 i+=1

                

        # # Write the updated data back to the JSON file
        # with open('C:\\Users\\paleo\\OneDrive - Universita degli Studi Roma Tre\\Desktop\\Unimio\\OneDrive - Universita degli Studi Roma Tre\\magistrale\\Secondo Anno\\Ingegneria dei Dati\\Homework\\homework4\\JSON_files\\pmcid_506784.json', 'w') as f:
        #         json.dump(data, f, indent=2)

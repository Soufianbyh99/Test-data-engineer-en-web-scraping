# -*- coding: utf-8 -*-
"""

@author: Soufiane Bouyahyaoui
"""
####################Question 1##########################


import requests
import re
from bs4 import BeautifulSoup



data = []
data1 = []
data2=[]
data_collecter = {}
def scraping_data():
    data = []
    data1 = []
    data2=[]
    data_collecter = {}
# URL des pages web à scraper        
    URLs=["https://www.creditmutuel.fr/fr/particuliers/epargne/livret-de-developpement-durable.html","https://www.monabanq.com/fr/produits-bancaires/livret-developpement-durable/en-resume.html","https://www.banquepopulaire.fr/bpaura/epargner/livret-transition-energetique/"]
    for url in URLs :
 # Envoi de la requête HTTP GET
      response = requests.get(url)
# Analyse du contenu HTML de la page
      soup = BeautifulSoup(response.text, 'html.parser')
      if url=="https://www.creditmutuel.fr/fr/particuliers/epargne/livret-de-developpement-durable.html":

# Extraction des informations sur les produits
# trouver les balises appropriées
          product_titles0 = soup.find_all('li', class_=re.compile(r'\bsummary__element\b'))
          taux_de_rémunération_= product_titles0[0].text.strip()
          taux_de_rémunération = re.sub(r'\xa0',' ',taux_de_rémunération_)
          niveaux_de_rémunération_=product_titles0[1].text.strip()
          niveaux_de_rémunération=re.sub(r'\xa0',' ',niveaux_de_rémunération_)
          versements_=product_titles0[2].text.strip()
#nettoyer les données
          versements=re.sub(r'\xa0',' ',versements_)
          disponibilté_dépargne_ =product_titles0[3].text.strip()
#nettoyer les données
          disponibilté_dépargne=re.sub(r'\xa0',' ',disponibilté_dépargne_)
          data.append({"taux de rémunération": taux_de_rémunération,
                       "niveaux de rémunération":niveaux_de_rémunération,
                       "versements":versements,
                       "disponibilté dépargne":disponibilté_dépargne
                       })
# Extraction des informations sur les produits
# trouver les balises appropriées
          product_titles1 = soup.select('table',class_='noslider list')
          for product_titles in product_titles1:
              products=product_titles.find_all('tr')
              for product_ in products :
        
        
                 product=product_.find_all('th',scope='row')
                 carac=product_.find_all('td')


        
                 if len(carac) == 2 and product:
                   nom_de_niveau_de_rémunération = product[0].text.strip()
                   description_ = carac[0].text.strip()
#nettoyer les données
                   description1 = re.sub(r'\xa0',' ',description_)
#nettoyer les données
                   description = re.sub(r':','',description1)
            
                   valeur_ = carac[1].text.strip()
#nettoyer les données            
                   valeur = re.sub(r'\xa0',' ',valeur_)

                   data.append( {
                       'nom_de_niveau_de_rémunération':nom_de_niveau_de_rémunération,
                       'Description': description,
                       'Valeur': valeur
                     })

       

# stockage des données collecter
              data_collecter['LDDS_creditmutuel']=data
     

        
      elif url == 'https://www.monabanq.com/fr/produits-bancaires/livret-developpement-durable/en-resume.html' :
 
# Extraction des informations sur les produits
# trouver les balises appropriées
         product_titles = soup.find_all('p',class_='paragraph white')
         data1.append({'nom de produit':product_titles[0].text.strip()})

         li_items = soup.find_all('li', class_=re.compile(r'\bitem-list\b'))
         for i in range(9):
             informations=li_items[i].text.strip().split(":")
#nettoyer les données
             b=re.sub(r'\s+',' ',informations[1])
#nettoyer les données          
             c=re.sub(r'\r\n','',b)
             informations[1]=c
             data1.append({informations[0]:informations[1]})
# stockage des données collecter

             data_collecter['monabanq']=data1
      else :
# Extraction des informations sur les produits
# trouver les balises appropriées
        product_titles = soup.find_all('h1', class_='font-title-page title')
        data.append({'produit': product_titles[0].text.strip()})
        li_items_a = soup.find_all('h3', class_=re.compile(
            r'\btext font-title-edito-light\b'))
        li_items_b = soup.find_all('dl', class_=re.compile(r'\baccordion-list\b'))
        for li_items in li_items_b:
            p = li_items.find_all('div', class_=re.compile(r'\bwysiwyg\b'))
            for i in range(5):
                p[i] = p[i].text.strip()
#nettoyer les données          
                c = re.sub(r'\r\n', ' ', p[i])
                p[i] = c
                data2.append({li_items_a[i].text.strip():p[i]})
# stockage des données collecter

            data_collecter['banquepopulaire']=data2

    return  data_collecter
        



####################Question2##########################




from flask import Flask, jsonify

app = Flask(__name__)

#Données extraites et nettoyées


@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(scraping_data())

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False  # Configuration de l'encodage UTF-8

    app.run()






import pandas as Pandas
import requests as Requests
import json

URL_PISCINE = ('https://data.montreal.ca/dataset/4604afb7-a7c4-4626-a3ca-'
               'e136158133f2/resource/cbdca706-569e-4b4a-805d-9af73af03b14/'
               'download/piscines.csv')

URL_PATINOIRE = ('https://data.montreal.ca/dataset/225ac315-49fe-476f-95bd'
                 '-a1ce1648a98c/resource/5d1859cc-2060-4def-903f-db24408bacd0/'
                 'download/l29-patinoire.xml')

URL_GLISSADE = ('http://www2.ville.montreal.qc.ca/services_citoyens/'
                'pdf_transfert/L29_GLISSADE.xml')


def parse(database):
    Parser.parse_piscine(database)
    Parser.parse_patinoire(database)
    Parser.parse_glissade(database)


def substring(string, first, last):
    try:
        start = string.index(first) + len(first)
        end = string.index(last, start)
        return string[start:end].strip()
    except ValueError:
        return ''


# Installer, analyser et enregistrer les données dans la base de données.
class Parser:
    def parse_piscine(database):
        df_piscine = Pandas.read_csv(URL_PISCINE, encoding='UTF-8')
        for i, row in df_piscine.iterrows():
            nom = row['NOM']
            arrondissement = row['ARRONDISSE']
            informations = {
                'id_uev': row['ID_UEV'],
                'type_piscine': row['TYPE'],
                'adresse': row['ADRESSE'],
                'propriete': row['PROPRIETE'],
                'gestion': row['GESTION'],
                'point_x': row['POINT_X'],
                'point_y': row['POINT_Y'],
                'equipement': row['EQUIPEME'],
                'long': row['LONG'],
                'lat': row['LAT']
            }
            infos = json.dumps(informations, indent=1, ensure_ascii=False)
            database.insert_installation(nom, arrondissement, 'piscine', infos)

    def parse_patinoire(database):
        response = Requests.get(URL_PATINOIRE)
        response.encoding = 'UTF-8'
        patinoire_file = response.text
        patinoire_file.replace('\\n', '')
        arrondissements_raw = patinoire_file.split('</arrondissement>')
        for arrondissement in arrondissements_raw:
            nom_arr = substring(arrondissement, '<nom_arr>', '</nom_arr>')
            if len(nom_arr) == 0:
                continue
            patinoires_raw = arrondissement.split('<nom_pat>')
            for patinoire in patinoires_raw:
                nom_pat = substring(patinoire, '', '</nom_pat>')
                if len(nom_pat) == 0:
                    continue
                conditions_raw = patinoire.split('</condition>')
                conditions = {'conditions': []}
                for condition in conditions_raw:
                    date_heure = substring(condition, '<date_heure>',
                                           '</date_heure>')
                    if len(date_heure) == 0:
                        continue
                    info = {
                      'date_heure': date_heure,
                      'ouvert': substring(condition, '<ouvert>', '</ouvert>'),
                      'deblaye': substring(condition, '<deblaye>',
                                           '</deblaye>'),
                      'arrose': substring(condition, '<arrose>', '</arrose>'),
                      'resurface': substring(condition, '<resurface>',
                                             '</resurface>')
                    }
                    conditions['conditions'].append(info)
            infos = json.dumps(conditions, indent=1, ensure_ascii=False)
            database.insert_installation(nom_pat, nom_arr, 'patinoire', infos)

    def parse_glissade(database):
        response = Requests.get(URL_GLISSADE)
        response.encoding = 'UTF-8'
        glissades = response.text.split('</glissade>')
        for glissade in glissades:
            nom = substring(glissade, '<nom>', '</nom>')
            if len(nom) == 0:
                continue
            nom_arr = substring(glissade, '<nom_arr>', '</nom_arr>')
            informations = {
                'cle': substring(glissade, '<cle>', '</cle>'),
                'date_maj': substring(glissade, '<date_maj>', '</date_maj>'),
                'ouvert': substring(glissade, '<ouvert>', '</ouvert>'),
                'deblaye': substring(glissade, '<deblaye>', '</deblaye>'),
                'condition': substring(glissade, '<condition>', '</condition>')
            }
            infos = json.dumps(informations, indent=1, ensure_ascii=False)
            database.insert_installation(nom, nom_arr, 'glissade', infos)

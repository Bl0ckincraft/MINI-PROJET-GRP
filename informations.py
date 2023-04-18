import csv

LANGUES_FILE = "resources/data/langues.csv"
PAYS_FILE = "resources/data/pays.csv"
VILLES_FILE = "resources/data/villes.csv"

with open(LANGUES_FILE, newline='', encoding='UTF-8') as fic:
    languesData = list(csv.DictReader(fic, delimiter=';'))

with open(VILLES_FILE, newline='', encoding='UTF-8') as fic:
    villesData = list(csv.DictReader(fic, delimiter=';'))

with open(PAYS_FILE, newline='', encoding='UTF-8') as fic:
    paysData = list(csv.DictReader(fic, delimiter=';'))


def capitale(pays):
    for ligne in paysData:
        if ligne['Nom'] == pays:
            capitaleId = ligne['Capitale']

            for ligne1 in villesData:
                if ligne1['Id'] == capitaleId:
                    return ligne1['Nom']


def esperances(pays):
    for ligne in paysData:
        if ligne['Nom'] == pays:
            esperance = ligne['EsperanceVie']
            return esperance


def pays_continent(continent):
    p = []

    for ligne in paysData:
        if ligne['Continent'] == continent:
            p.append(ligne['Nom'])
    return p


def classement(pays):
    continent = None
    esperance = None

    for ligne in paysData:
        if ligne['Nom'] == pays:
            continent = ligne['Continent']
            esperance = ligne['EsperanceVie']

    rang = 1

    for p in pays_continent(continent):
        if esperances(p) != 'NULL' and float(esperance) < float(esperances(p)):
            rang += 1

    return rang


def villes_pays(pays):
    code = None

    for ligne in paysData:
        if ligne['Nom'] == pays:
            code = ligne['Code']

    v = []

    for ligne in villesData:
        if ligne['CodePays'] == code:
            v.append(ligne)

    return v


def trois_villes(pays):
    villes = sorted(villes_pays(pays), key=lambda x:int(x['Population']), reverse=True)
    trois_v = []

    for i in range(3):
        if len(villes) > i:
            nom = villes[i]['Nom']
            trois_v.append(nom)

    return trois_v

print(trois_villes('France')[:3])
# A1 15xp
Le fichier `modules/initializer` contient les méthodes responsables de l'extraction de données.\
Pour valider le fonctionnement de l'extraction et de l'enregistrement des données, vous pouvez utiliser les fonctionnalités des points A3 et A4.

<br>

# A2  5xp
La fonction responsable de l'importation automatique des données se trouve à la ligne 74 dans le fichier `index.py`.

### *Test :*
1. Modifier les champs `hour` et `minute`, à la ligne 74 dans `index.py`.\
   Par exemple, si l'heure actuelle est '19:30', mettez '19' dans le champ `hour` et '31' dans le champ `minute`. L'importation de données se fera à '19:31'.
2. Decommenter la ligne 77. Un message va être affiché dans la console lorsque l'importation de données commence.
3. Executer le programme.

<br>

# A3  5xp
### *Chemin : /doc*
<br>
Le fichier doc.raml se trouve à la racine. La version HTML se trouve dans le dossier `templates`.

<br>

# A4 10xp
### *Chemin : /api/installations?arrondissement=**NomDeMonArrondissement***
<br>
Vouz pouvez tester manuellement, avec ctr-f + ' LaSalle ', selon le fichier de données, dans les différentes URL contenant les données originaux. Le nombre de résultats doit être identique à celui retourné par le service.

<br>

# A5 10xp
### *Chemin : /*
<br>
La gestion de requêtes asynchrones se trouve dans `static/js/script.js`.

La recherche dans le champ `input`, appelle le service `/api/installations` (voire point A4). Les résultats retournés par le service sont rangés dans un tableau qui sera par la suite affiché sur la page HTML.

### *Test :*
* Comparer les données dans le tableau avec ceux retournées par le service au point A4.

<br>

# A6 10xp
### *Chemin : /api/installations?installation=**NomDeMonInstallation***
<br>
Le champ `select` fait appelle au service du point A4 avec le paramètre installation.

Pour valider le fonctionnement correct de ce point, vous pouvez comparer les résultats dans le tableau avec les données retournées par le service :
  * `/api/installations?installation=NomDeMonInstallation`

<br>

# C1 10xp
### *Chemin : /api/installations*
<br>
  Utiliser Postman pour valider que les données sont correctes.

<br>

# C2 10xp
### *Chemin :*
 - */api/installations/xml*
 - */api/installations/xml?installation=NomDeMonInstallation*

Les données s'affiche bien dans un furteur.

Pour valider le fonctionnement correct de ce point, comparer les résultats de ce service avec ceux du service aux points A4 ou A5.

<br>

# C3  5xp
### *Chemin :*
 - */api/installations/csv*
 - */api/installations/csv?installation=NomDeMonInstallation*

Pour valider le fonctionnement correct de ce point, comparer les résultats de ce service avec ceux du service aux points A4 ou A5.

<br>

# D1 15xp (fonctionne pour tout les types d'installation)
### *Chemin : /api/installations/modifier?installation=**NomDeMonInstallation***
### *Method : PUT*
<br>
Les schémas pour chaque type d'installation se trouvent dans modules/schemas.py.

<br>

### *Description :*
1. Copier les informations de l'installation que vous voulez modifier à l'aide du service :\
    `/api/installations?installation=NomDeMonInstallation`
2. Collez les informations dans le payload de la requête.
3. Modifier ce que vous voulez.

Pour plus d'information regarder la doc.
<br>

### *Test : (Utiliser Yarc ou Postman)*
1. Modifier l'état d'une installation et vérifier à l'aide du service de A4 si les informations ont été bien modifiées
2. Entrer n'importe quoi dans le payload pour vérifier si la validation du json fonctionne correctement.
   * Remplacer un champ de type numbre par un string.
   * Supprimer un champ 'required'

<br>

# D2  5xp (fonctionne pour tout les types d'installation)
### *Chemin : /api/installations/supprimer?installation=**NomDeMonInstallation***
### *Method : DELETE*
### *Test : (Utiliser Yarc ou Postman)*
- Supprimer une installation et vérifier à l'aide des services A4-A5 si l'installation existe toujours.

<br>

# D3 20xp (Extra)
### Fonctionnalités implémentées:
1. Service pour modifier une installation de n'importe quel type (voir D1)
2. Service pour supprimer une installation de n'importe quel type (voir D2)

### Fonctionnalité non implémentée:
* Modifier/Supprimer une installation avec l'application faite en A5

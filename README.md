# INF5190 - H22

## :clipboard: Prérequis
- Python3
- Sqlite3
- Ram2html

## :wrench: Configuration

### Installer l'environnement virtuel
> Utiliser la commande `apt` pour installer virtualenv
```
$ sudo apt install python-virtualenv
```

### Créer un environnement virtuel
```
$ python3 -m venv inf5190-venv
```

### Activer l'environnement virtuel
```
$ source inf5190-venv/bin/activate
```

### Installer les dépendances
```
$ sudo pip install -r requirements.txt
```

## :rocket: Démarrer l'API
> Lors du premier request, les données vont être installées dans la base de données. L'exécution du premier request prend quelques secondes pour se compléter.
```
$ make
```

### Tests dans un fureteur
Une fois l'application lancée, utilisez le fureteur de votre ordinateur pour accéder à l'application Flask. Vous pouvez y accéder en utilisant l'adresse IP affichée dans la console.

Exemple : http://192.168.50.12:5000/
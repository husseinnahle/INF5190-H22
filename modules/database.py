import sqlite3
from .installation import Installation


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/database.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    # Inserer une installation
    def insert_installation(self, nom: str, arrondissement: str, type: str,
                            informations: str):
        connection = self.get_connection()
        # Remplacer les objets NaN par des string "NaN".
        # Sinon, on aurait un problème lorsqu'on transforme un string a un json object
        informations = informations.replace('NaN', '\"NaN\"')
        connection.execute('insert or ignore into installation(nom,'
                           'arrondissement, _type, informations)'
                           'values(?, ?, ?, ?)',
                           (nom, arrondissement, type, informations))
        connection.commit()

    # Rechercher toutes les installations
    def read_all_installations(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('select * from installation')
        installations = cursor.fetchall()
        return (Installation(installation[0], installation[1],
                             installation[2], installation[3],
                             installation[4])
                for installation in installations)

    # Rechercher les installations selon 'arrondissement'
    def read_all_installations_arrondissement(self, arrondissement: str):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('select * from installation where arrondissement=?',
                       (arrondissement,))
        installations = cursor.fetchall()
        return (Installation(installation[0], installation[1],
                             installation[2], installation[3],
                             installation[4])
                for installation in installations)

    # Rechercher une installation selon 'nom'
    def read_installation_nom(self, nom: str):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('select * from installation where nom=?', (nom,))
        installation = cursor.fetchone()
        return Installation(installation[0], installation[1],
                            installation[2], installation[3],
                            installation[4])

    # Rechercher les installations selon 'nom' #
    def read_all_noms(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('select nom from installation')
        installations = cursor.fetchall()
        return (installation[0] for installation in installations)

    # Rechercher une installation selon 'nom' et 'type'
    def read_installation_nom_type(self, nom: str, type: str):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('select * from installation where nom=? and _type=?',
                       (nom, type,))
        installation = cursor.fetchone()
        return Installation(installation[0], installation[1],
                            installation[2], installation[3],
                            installation[4])

    # Mettre à jour une installation
    def update_installation(self, installation: Installation):
        connection = self.get_connection()
        connection.execute("update installation set informations=? where id=?",
                           (installation.informations, installation.id))
        connection.commit()
        return installation

    # Supprimer une installation selon 'nom'
    def delete_installation(self, installation: Installation):
        connection = self.get_connection()
        connection.execute("delete from installation where id=?",
                           (installation.id,))
        connection.commit()

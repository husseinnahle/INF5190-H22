import json


class Installation:
    def __init__(self, id: int, nom: str, arrondissement: str,
                 type: str, informations: str):
        self.id = id
        self.nom = nom
        self.arrondissement = arrondissement
        self.type = type
        # Object string en format json
        self.informations = informations

    # Mettre à jour une installation. Seulement 'informations' est modifiable.
    def update_informations(self, informations: dict):
        self.informations = json.dumps(informations)

    # Retourner l'objet Installation en format dictionnaire (dict).
    def to_dictionary(self):
        dictionary = {
            "id": self.id, "nom": self.nom, "type": self.type,
            "arrondissement": self.arrondissement
        }
        dictionary.update(json.loads(self.informations))
        return dictionary

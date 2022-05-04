from jsonschema import validate

glissade_update_schema = {
    'type': 'object',
    'required': ['date_maj', 'ouvert', 'deblaye', 'condition'],
    'properties': {
        'date_maj': {
            'type': 'string'
        },
        'ouvert': {
            'type': 'string'
        },
        'deblaye': {
            'type': 'string'
        },
        'condition': {
            'type': 'string'
        }
    },
    'additionalProperties': {
        'properties': {
            'id': {
                'type': 'number'
            },
            'nom': {
                'type': 'string'
            },
            'arrondissement': {
                'type': 'string'
            },
            'type': {
                'type': 'string'
            },
            'cle': {
                'type': 'string'
            }
        }
    }
}


piscine_update_schema = {
    'type': 'object',
    'required': ['id_uev', 'adresse', 'type_piscine', 'propriete', 'gestion',
                 'point_x', 'point_y', 'equipement', 'long', 'lat'],
    'properties': {
        'id_uev': {
            'type': 'number'
        },
        'adresse': {
            'type': 'string'
        },
        'type_piscine': {
                'type': 'string'
        },
        'propriete': {
            'type': 'string'
        },
        'gestion': {
            'type': 'string'
        },
        'point_x': {
            'type': 'string'
        },
        'point_y': {
            'type': 'string'
        },
        'equipement': {
            'type': 'string'
        },
        'long': {
            'type': 'number'
        },
        'lat': {
            'type': 'number'
        }
    },
    'additionalProperties': {
        'properties': {
            'id': {
                'type': 'number'
            },
            'nom': {
                'type': 'string'
            },
            'arrondissement': {
                'type': 'string'
            },
            'type': {
                'type': 'string'
            }
        }
    }
}

patinoire_update_schema = {
    'type': 'object',
    'required': ['conditions'],
    'properties': {
        'conditions': {
            'type': 'array',
            'items': {
                'type': 'object',
                'required': ['date_heure', 'ouvert', 'deblaye',
                             'arrose', 'resurface'],
                'properties': {
                    'date_heure': {
                        'type': 'string'
                    },
                    'ouvert': {
                        'type': 'string'
                    },
                    'deblaye': {
                        'type': 'string'
                    },
                    'arrose': {
                        'type': 'string'
                    },
                    'resurface': {
                        'type': 'string'
                    }
                }
            }
        }
    },
    'additionalProperties': {
        'properties': {
            'id': {
                'type': 'number'
            },
            'nom': {
                'type': 'string'
            },
            'arrondissement': {
                'type': 'string'
            },
            'type': {
                'type': 'string'
            }
        }
    }
}


def validate_schema(type, data):
    informations = {}
    if type == "glissade":
        informations = Schema.validate_glissade_schema(data)
    elif type == "piscine":
        informations = Schema.validate_piscine_schema(data)
    elif type == "patinoire":
        informations = Schema.validate_patinoire_schema(data)
    return informations


class Schema:
    def validate_patinoire_schema(data):
        validate(data, patinoire_update_schema)
        informations = {"conditions": []}
        informations["conditions"] = data["conditions"]
        return informations

    def validate_glissade_schema(data):
        validate(data, glissade_update_schema)
        informations = {
            "date_maj": data["date_maj"],
            "ouvert": data["ouvert"],
            "deblaye": data["deblaye"],
            "condition": data["condition"]
        }
        return informations

    def validate_piscine_schema(data):
        validate(data, piscine_update_schema)
        informations = {
            "id_uev": data["id_uev"],
            "type_piscine": data["type_piscine"],
            "adresse": data["adresse"],
            "propriete": data["propriete"],
            "gestion": data["gestion"],
            "point_x": data["point_x"],
            "point_y": data["point_y"],
            "equipement": data["equipement"],
            "long": data["long"],
            "lat": data["lat"]
        }
        return informations

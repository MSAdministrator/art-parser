from .base import Base


class Navigator(Base):

    template = {
        "version": "4.2",
        "name": "Atomic Red Team",
        "description": "Atomic Red Team MITRE ATT&CK Navigator Layer",
        "domain": "mitre-enterprise",
        "gradient": {
            "colors": [
                "#ce232e",
                "#ce232e"
            ],
            "minValue": 0,
            "maxValue": 100
        },
        "legendItems": [
            {
                "label": "Has at least one test",
                "color": "#ce232e"
            }
        ],
        "techniques": []
    }
    technique_template = {
        "techniqueID": "T1611",
        "score": 100,
        "enabled": True,
        "comment": "https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1611/T1611.md"
    }

    pass
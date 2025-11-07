from pathlib import Path
import json
import gzip
import shutil

FACTIONS = [
    "Daedalus",
    "MegaCorp",
    "BitRunners",
    "The Black Hand",
    "NiteSec",
    "Aevum",
    "Chongqing",
    "Ishima",
    "New Tokyo",
    "Sector-12",
    "Volhaven",
    "Speakers for the Dead",
    "The Dark Army",
    "The Syndicate",
    "Tetrads",
    "Slum Snakes",
    "Netburners",
    "Tian Di Hui",
    "CyberSec",
    "Church of the Machine God",
    "Shadows of Anarchy",
]

class SaveGame:
    def __init__(self, savegame_path:Path) -> None:
        if not savegame_path.exists():
            raise ValueError(f"{savegame_path} does not exist")

        self.gzip = savegame_path
        self.outfile = Path(self.gzip.parent) / "bitburnerSave-modified.json.gz"
        self.ctor: str = ""
        self.data: dict[str] = {}
        self._json = {}

        self.load()

    def load(self):
        with gzip.open(self.gzip, 'rb') as f:
            self._json = json.load(f)
        
        self.player_save = json.loads(self._json["data"]["PlayerSave"])
        self.factions_save = json.loads(self._json["data"]["FactionsSave"])

    def save(self):
        self._json["data"]["PlayerSave"] = json.dumps(self.player_save)
        self._json["data"]["FactionsSave"] = json.dumps(self.factions_save)

        with gzip.open(self.outfile, 'wb') as f:
            f.write(json.dumps(self._json).encode("utf-8"))

    @property
    def money(self):
        return self.player_save["data"]["money"]
    
    @money.setter
    def money(self, amount=int(5E18)):
        self.player_save["data"]["money"] = amount

    @property
    def hack_exp(self):
        return self.player_save["data"]["mults"]["hacking_exp"]
    
    @hack_exp.setter
    def hack_exp(self, amount=int(1E100)):
        self.player_save["data"]["mults"]["hacking_exp"] = amount
        self.player_save["data"]["exp"]["hacking"] = amount

    def set_factions(self, rep=5_000_000):
        for faction in FACTIONS:
            self.factions_save[faction] = {
                "playerReputation": rep,
                "discovery": "known",
                "favor": 1000000,
            }
        
        self.player_save["data"]["factions"] = FACTIONS
        self.player_save["data"]["factionInvitations"] = []
        self.player_save["data"]["factionRumors"]["data"] = []

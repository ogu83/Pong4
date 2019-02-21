import json

class GameState(object):        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)    

    def __init__(self, H=0, W=0, FourPlayers=False, *args, **kwargs):
        self.H = H
        self.W = W
        self.FourPlayers = FourPlayers

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)    
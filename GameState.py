import json

class GameState(object):        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)    

    def __init__(self, H=0, W=0,
                 FourPlayers=False, 
                 p1x=0, p1y=0, 
                 p2x=0, p2y=0, 
                 p3x=0, p3y=0, 
                 p4x=0, p4y=0, 
                 ball_thrower=0,
                 p1score=0,p2score=0,p3score=0,p4score=0,
                 dmH=0,dmW=0,
                 paddle_width_v=0,paddle_height_v=0,
                 paddle_height_h=0,paddle_width_h=0,
                 bx=0,by=0,bw=0,
                 velocity_raito=0,
                 bxv=0,byv=0,
                 *args, **kwargs):
        self.H = H
        self.W = W
        self.FourPlayers = FourPlayers

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)    
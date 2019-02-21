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
        self.p1x = p1x
        self.p1y = p1y
        self.p2x = p2x
        self.p2y = p2y
        self.p3x = p3x
        self.p3y = p3y
        self.p4x = p4x
        self.p4y = p4y
        self.ball_thrower=ball_thrower
        self.p1score=p1score
        self.p2score=p2score
        self.p3score=p3score
        self.p4score=p4score
        self.dmH=dmH
        self.dmW=dmW
        self.paddle_width_v=paddle_width_v
        self.paddle_width_h=paddle_width_h
        self.paddle_height_v=paddle_height_v
        self.paddle_height_h=paddle_height_h
        self.bx=bx
        self.by=by
        self.bw=bw
        self.velocity_raito=velocity_raito
        self.bxv=bxv
        self.byv=byv

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)    
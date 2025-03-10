
class ScoreBoard:
    
    def __init__(self, title='', url=''):

        self.title = title
        self.url = url
        self.team_a = None
        self.team_b = None
        self.target = None
        self.result = None
        self.team_a_code = None
        self.team_b_code = None
        self.location = None
        self.date = None
        #self.year = None
        self.match = None
        self.series = None
        self.team_a_score = None
        self.team_b_score = None
        self.potm = None
        self.toss = None
        self.umpire_1 = None
        self.umpire_2 = None
        self.ref = None
        self.season = None

    def get_title(self):
        return self.title
    
    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def __str__(self):
        return f"""ScoreBoard(
            Title: {self.title}, 
            Team A: {self.team_a} ({self.team_a_code})  {self.team_a_score},
            Team B: {self.team_b} ({self.team_b_code})  {self.team_b_score}, 
            Toss: {self.toss}, 
            Target: {self.target}, Result: {self.result},
            Player of the Match: {self.potm},
            Location: {self.location}, Date: {self.date},
            Match: {self.match}, Series: {self.series},
            Umpires: {self.umpire_1}, {self.umpire_2},
            Referee: {self.ref} 
          )"""

class ScoreBoard:
    
    def __init__(self, title='', url=''):

        self.title = title
        self.url = url
        
    def get_title(self):
        return self.title
    
    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def __str__(self):
        return f'ScoreBoard(title={self.title})'
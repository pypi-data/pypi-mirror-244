
from .widgets.widget import Widget

class RawHtml(Widget):
    def __init__(self,html="",id=""):
        super().__init__(id=id)
        self.html = html

    def render(self):
        return self.html
    
    

from src.collie_watch.widgets.widget import Widget
from src.collie_watch.main_module import CollieWatch,CollieWatchHtmlEvents

class Button(Widget):
    def __init__(self, text="",callback=lambda x: x,id="",width="",height="",flex=""):
        super().__init__(id=id,flex=flex)
        self.text = text
        self.callback = callback
        

        CollieWatch.add_callback_by_id(self.id,[CollieWatchHtmlEvents.CLICK],self.callback)

        
    def render(self):
        return f'<button id="{self.id}">{self.text}</button>'

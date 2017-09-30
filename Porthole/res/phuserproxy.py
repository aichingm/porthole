from PortholeProxy import PortholeInstance
from PortholeProxy import PortholeProxy

class MyPortholeProxy(PortholeProxy):
    
    def __init__(self, porthole):
                super().__init__(porthole)
    
    def println(self, str):
        print(str)
        
#force your proxy onto Porthole (important!)
PortholeInstance.instance.setProxy(MyPortholeProxy(PortholeInstance.instance))

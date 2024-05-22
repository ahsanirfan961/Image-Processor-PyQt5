from package.welcome import Welcome
import sys 
from package.data import widget, app

welcome = Welcome() 
widget.addWidget(welcome)
widget.setFixedHeight(720)
widget.setFixedWidth(1280) 
widget.show()

try: 
    sys.exit(app.exec_())
except:
    print("Exiting") 
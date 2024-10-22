import sys
import threading

from interface.ui import *

if __name__ =='__main__' :
    app = QApplication(sys.argv)
    window = GameWindow()
    threading.Thread(target=window.type_move, daemon=True).start()

    sys.exit(app.exec_())

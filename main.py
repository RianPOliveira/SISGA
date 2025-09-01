import ttkbootstrap as ttk
from interface_grafica import SisgaGUI

if __name__ == "__main__":
    root = ttk.Window(themename="litera")

    app = SisgaGUI(root)

    root.mainloop()
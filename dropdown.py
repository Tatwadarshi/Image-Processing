from tkinter import*
from tkinter import ttk
import glob
import os


class MyDropDown:
    def __init__(self, 
                 drop_list:list,
                 window,
                 bind_fun,
                 label_str:str="My Dropdown",
                 grid_loc:tuple=(0, 0)):
        self.drop_list = drop_list
        self.__selected_obj = self.drop_list[0]
        self.window = window
        self.label_str = label_str
        self.grid_loc = grid_loc
        self.label = Label(self.window, text=self.label_str, font=("Arial", 10))
        self.label.grid(row=grid_loc[0], column=grid_loc[1], pady=10)
        self.drop_down = ttk.Combobox(self.window, values=self.drop_list, font=('Arial', 10), width=20)
        self.drop_down.bind("<<ComboboxSelected>>", bind_fun)
        self.drop_down.set(self.__selected_obj)
        self.drop_down.grid(row=grid_loc[0], column=grid_loc[1] + 1, pady=10, padx=10)
        # self.drop_down.grid(row=grid_loc[0], column=grid_loc[1] + 1, pady=10, columnspan=3)
        self.get_selection()

    def get_selection(self):
        self.__selected_obj = self.drop_down.get()
        return self.__selected_obj


if __name__=="__main__":
    folder_path = "./DATA_SET/"
    image_paths = glob.glob(f"{folder_path}/*.[jJpP][pPnN][gG]")
    image_names = images = [f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif"))]
    controls=Tk()
    controls.minsize(200, 200)
    controls.title('Controls')

    def change_lbl(e):
        val = drop.get_selection()
        lbl2.config(text=val)

    drop = MyDropDown(image_names, controls, change_lbl,"Choose Sample: ", (0, 0))
    lbl2 = Label(controls, text=drop.get_selection(), font=("Arial", 10))
    lbl2.grid(row=1, column=0, columnspan=2, pady=30)

    controls.mainloop()
    

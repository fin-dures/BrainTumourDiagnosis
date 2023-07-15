import PySimpleGUI as sg
from time import sleep

class base_window():

    def __init__(self, title, xres, yres):

        self.__xres = xres
        self.__yres = yres
        self.__layout = [[]]
        self.__title = title

    def open(self):

        self.__window = sg.Window(self.__title,self.__layout, size=(self.__xres,self.__yres), element_justification='c')

    def loop(self):
        
        event, values = self.__window.read()
        return event, values        

    def _clear_layout(self):

        self.__layout = [[]]

    def _append_layout(self, widget):

        self.__layout.append(widget)

    def add_text(self, text):
        
        self._append_layout([sg.Text(text)])

    def close(self):
        self.__window.close()

    def update(self):
        self.close()
        self.open()
        
            
class sized_window(base_window):

    def __init__(self, title):

        win_width, win_height = sg.Window.get_screen_size()
        width, height = int(win_width*0.3), int(win_height*0.5)
        super().__init__(title, width, height)

class button_window(sized_window):

    def __init__(self, title):
        super().__init__(title)

    def add_button(self, text):

        super()._append_layout([sg.Button(text)])


class input_window(sized_window):

    def __init__(self, title):
        super().__init__(title)

    def add_input(self, default_text):

        super()._append_layout([sg.Input(default_text)])

class slider_window(sized_window):
    def __init__(self, title):
        super().__init__(title)

    def add_slider(self, minimum, maximum, resolution, default):

        super()._append_layout([sg.Slider(range=(minimum, maximum), resolution=resolution, orientation=("horizontal"), default_value = default)])


class main_window(input_window, button_window, slider_window):

    def __init__(self, title):

        super().__init__(title)

    def clear(self):
        super()._clear_layout()
        


    def add_home_buttons(self):

        self.clear()
        super().add_button("Enter images for training")
        super().add_button("Enter images for diagnosis")
        super().add_button("Enter images for testing")


    def add_testing_buttons(self, result=''):

        self.clear()
        super().add_button("Select positive images for testing")
        super().add_button("Select negative images for testing")
        super().add_text("Enter Significance level:")
        super().add_slider(0.001,0.1,0.001, 0.05)
        super().add_button("Test")
        super().add_button("Back")
        if result:
            super().add_text(result)

    def add_training_buttons(self):

        self.clear()
        super().add_button("Select positive images for training")
        super().add_button("Select negative images for training")
        super().add_button("Train")
        super().add_button("Back")

    
    def add_diagnosis_buttons(self, result=''):
        
        self.clear()
        super().add_button("Select image for diagnosis")
        super().add_button("Diagnose")
        super().add_button("Back")
        if result:
            super().add_text(result)

    def add_error_message(self, error):

        self.clear()
        super().add_text(error)



        

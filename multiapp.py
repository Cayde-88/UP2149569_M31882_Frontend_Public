from streamlit_option_menu import option_menu
from tabs import home, aboutproj, contact, aboutme, portfolio

class MultiApp:
    def __init__(self):
        self.apps = []

    def run(self):
                        
        menu_dict = {
        "Home" : {"fn": home},
        "About Project" : {"fn": aboutproj},
        "My Portfolio": {"fn": portfolio},
        "About Me" : {"fn": aboutme},
        "Contact" : {"fn": contact}        
        }
        
        selected_page = option_menu(
                            menu_title=None,
                            options = ['Home', 'About Project', 'My Portfolio', 'About Me', 'Contact'],
                            icons = ["house", "question-circle-fill", "graph-up", "file-person-fill", "envelope-at-fill"],
                            menu_icon="list",
                            default_index=0,
                            orientation="horizontal"
                            )
        
        selected_page = menu_dict[selected_page]["fn"].app()
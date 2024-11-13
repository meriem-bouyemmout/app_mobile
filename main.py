import sqlite3
from datetime import datetime  # Ajoutez cette ligne
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen


# Connexion à la base de données SQLite
conn = sqlite3.connect("tools.db")
cursor = conn.cursor()

# Création des tables si elles n'existent pas
cursor.execute('''CREATE TABLE IF NOT EXISTS tools (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    status TEXT,
                    location TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS historique (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tool_id INTEGER,
                    modification_date TEXT,
                    details TEXT,
                    FOREIGN KEY (tool_id) REFERENCES tools(id))''')

class AddToolScreen(Screen):
    def __init__(self, **kwargs):
        super(AddToolScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.name_input = TextInput(hint_text='Nom de l\'outil', multiline=False)
        layout.add_widget(self.name_input)

        self.status_spinner = Spinner(
            text='Statut',
            values=('Disponible', 'En usage', 'En réparation'),
            size_hint=(None, None),
            size=(200, 44)
        )
        layout.add_widget(self.status_spinner)

        self.location_spinner = Spinner(
            text='Localisation',
            values=('Atelier A', 'Atelier B', 'Atelier C', 'Entrepôt', 'Garage'),
            size_hint=(None, None),
            size=(200, 44)
        )
        layout.add_widget(self.location_spinner)

        add_button = Button(text='Ajouter', on_press=self.add_tool)
        layout.add_widget(add_button)

        back_button = Button(text='Retour', on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_button)

        self.add_widget(layout)

    def add_tool(self, instance):
        name = self.name_input.text
        status = self.status_spinner.text
        location = self.location_spinner.text

        if name and status and location:
            cursor.execute("INSERT INTO tools (name, status, location) VALUES (?, ?, ?)", (name, status, location))
            conn.commit()
            self.name_input.text = ''
            popup = Popup(title='Succès', content=Label(text='Outil ajouté avec succès!'), size_hint=(0.6, 0.4))
            popup.open()
        else:
            popup = Popup(title='Erreur', content=Label(text='Veuillez remplir tous les champs!'), size_hint=(0.6, 0.4))
            popup.open()

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        header_label = Label(text='Suivi des Outils', font_size=36)
        layout.add_widget(header_label)

        search_input = TextInput(hint_text='Rechercher un outil...', multiline=False)
        layout.add_widget(search_input)

        tool_list_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        tool_list_layout.bind(minimum_height=tool_list_layout.setter('height'))

        # Récupérer les outils de la base de données
        cursor.execute("SELECT * FROM tools")
        tools = cursor.fetchall()

        for tool in tools:
            tool_button = Button(text=tool[1], size_hint_y=None, height=44)
            tool_button.bind(on_press=lambda btn, tool_id=tool[0]: self.show_tool_details(tool_id))
            tool_list_layout.add_widget(tool_button)

        layout.add_widget(tool_list_layout)

        add_tool_button = Button(text='+ Ajouter un outil', on_press=lambda x: setattr(self.manager, 'current', 'add_tool'))
        layout.add_widget(add_tool_button)

        self.add_widget(layout)

    def show_tool_details(self, tool_id):
        # Transitionner vers l'écran des détails et passer l'ID de l'outil
        self.manager.current = 'details'
        details_screen = self.manager.get_screen('details')
        details_screen.load_tool_details(tool_id)

class DetailsScreen(Screen):
    def __init__(self, **kwargs):
        super(DetailsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.tool_details_label = Label(text='Détails de l\'outil', font_size=20)
        layout.add_widget(self.tool_details_label)

        history_button = Button(text='Voir l\'historique', on_press=self.show_tool_history)
        layout.add_widget(history_button)

        self.modify_button = Button(text='Modifier', on_press=lambda x: self.modify_tool())
        layout.add_widget(self.modify_button)

        back_button = Button(text='Retour', on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_button)

        self.add_widget(layout)

    def load_tool_details(self, tool_id):
        self.tool_id = tool_id  # Stocker l'ID de l'outil pour l'utilisation ultérieure
        cursor.execute("SELECT * FROM tools WHERE id=?", (tool_id,))
        tool = cursor.fetchone()
        if tool:
            self.tool_details_label.text = f"Nom: {tool[1]}\nStatut: {tool[2]}\nLocalisation: {tool[3]}"

    def show_tool_history(self, instance):
        # Logique pour afficher l'historique
        cursor.execute("SELECT * FROM historique WHERE tool_id=?", (self.tool_id,))
        history_records = cursor.fetchall()
        
        if history_records:
            history_text = "\n".join([f"{record[2]}: {record[3]}" for record in history_records])
            popup = Popup(title='Historique', content=Label(text=history_text), size_hint=(0.8, 0.6))
            popup.open()
        else:
            popup = Popup(title='Historique', content=Label(text='Aucun historique disponible.'), size_hint=(0.6, 0.4))
            popup.open()

    def modify_tool(self):
        # Afficher une popup pour modifier les détails de l'outil
        layout = BoxLayout(orientation='vertical')

        self.name_input = TextInput(hint_text='Nom de l\'outil', multiline=False)
        self.status_spinner = Spinner(
            text='Statut',
            values=('Disponible', 'En usage', 'En réparation'),
            size_hint=(None, None),
            size=(200, 44)
        )
        self.location_spinner = Spinner(
            text='Localisation',
            values=('Atelier A', 'Atelier B', 'Entrepôt', 'Garage'),
            size_hint=(None, None),
            size=(200, 44)
        )

        # Récupérer les détails de l'outil à modifier
        cursor.execute("SELECT * FROM tools WHERE id=?", (self.tool_id,))
        tool = cursor.fetchone()
        if tool:
            self.name_input.text = tool[1]
            self.status_spinner.text = tool[2]
            self.location_spinner.text = tool[3]

        layout.add_widget(self.name_input)
        layout.add_widget(self.status_spinner)
        layout.add_widget(self.location_spinner)

        modify_button = Button(text='Modifier', on_press=lambda x: self.update_tool())
        layout.add_widget(modify_button)

        close_button = Button(text='Fermer', on_press=lambda x: self.dismiss_popup())
        layout.add_widget(close_button)

        self.popup = Popup(title='Modifier l\'outil', content=layout, size_hint=(0.8, 0.6))
        self.popup.open()

    def update_tool(self):
        new_name = self.name_input.text
        new_status = self.status_spinner.text
        new_location = self.location_spinner.text

        cursor.execute("UPDATE tools SET name=?, status=?, location=? WHERE id=?", (new_name, new_status, new_location, self.tool_id))
        conn.commit()

        # Enregistrement dans l'historique
        modification_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO historique (tool_id, modification_date, details) VALUES (?, ?, ?)",
                       (self.tool_id, modification_date, f'Modifié: {new_name}, {new_status}, {new_location}'))
        conn.commit()

        self.popup.dismiss()
        self.load_tool_details(self.tool_id)  # Recharger les détails mis à jour

    def dismiss_popup(self):
        self.popup.dismiss()

class ToolApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(AddToolScreen(name='add_tool'))
        sm.add_widget(DetailsScreen(name='details'))
        return sm

if __name__ == '__main__':
    ToolApp().run()

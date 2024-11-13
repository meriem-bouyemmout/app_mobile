import sqlite3
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.image import Image

# تعيين لون الخلفية
Window.clearcolor = (0.1, 0.1, 0.1, 1)

# كود Kivy للواجهات
KV = '''
ScreenManager:
    LoginScreen:
    SignupScreen:
    AccueilScreen:

<LoginScreen>:
    name: "login"
    
    FloatLayout:
        Image:
            source: "background.jpg"
            allow_stretch: True
            keep_ratio: False
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            opacity: 0.3

        MDCard:
            size_hint: None, None
            size: 400, 400
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            elevation: 12
            radius: [20,]

            FloatLayout:
                MDLabel:
                    text: "Connexion"
                    font_style: "H4"
                    halign: "center"
                    pos_hint: {"center_x": 0.5, "center_y": 0.85}

                MDTextField:
                    id: username_input
                    hint_text: "Nom d'utilisateur"
                    size_hint_x: 0.8
                    pos_hint: {"center_x": 0.5, "center_y": 0.6}
                    icon_left: "account"
                    mode: "rectangle"

                MDTextField:
                    id: password_input
                    hint_text: "Mot de passe"
                    size_hint_x: 0.8
                    pos_hint: {"center_x": 0.5, "center_y": 0.4}
                    password: True
                    icon_left: "key-variant"
                    mode: "rectangle"

                MDRaisedButton:
                    text: "Connexion"
                    pos_hint: {"center_x": 0.5, "center_y": 0.2}
                    on_release: app.login()

                MDRaisedButton:
                    text: "S'inscrire"
                    pos_hint: {"center_x": 0.5, "center_y": 0.1}
                    on_release: root.manager.current = "signup"

<SignupScreen>:
    name: "signup"
    
    FloatLayout:
        Image:
            source: "background.jpg"
            allow_stretch: True
            keep_ratio: False
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            opacity: 0.3

        MDCard:
            size_hint: None, None
            size: 400, 500
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            elevation: 12
            radius: [20,]

            FloatLayout:
                MDLabel:
                    text: "Inscription"
                    font_style: "H4"
                    halign: "center"
                    pos_hint: {"center_x": 0.5, "center_y": 0.9}

                MDTextField:
                    id: email_input
                    hint_text: "Email"
                    size_hint_x: 0.8
                    pos_hint: {"center_x": 0.5, "center_y": 0.7}
                    icon_left: "email"
                    mode: "rectangle"

                MDTextField:
                    id: signup_username_input
                    hint_text: "Nom d'utilisateur"
                    size_hint_x: 0.8
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    icon_left: "account"
                    mode: "rectangle"

                MDTextField:
                    id: signup_password_input
                    hint_text: "Mot de passe"
                    size_hint_x: 0.8
                    pos_hint: {"center_x": 0.5, "center_y": 0.3}
                    password: True
                    icon_left: "key-variant"
                    mode: "rectangle"

                MDRaisedButton:
                    text: "S'inscrire"
                    pos_hint: {"center_x": 0.5, "center_y": 0.1}
                    on_release: app.signup()

<AccueilScreen>:
    name: "accueil"
    
    BoxLayout:
        orientation: 'vertical'
        MDLabel:
            text: "Bienvenue à la Page d'Accueil"
            halign: 'center'
            font_style: "H4"
            theme_text_color: "Primary"
            size_hint_y: 0.2

        MDRaisedButton:
            text: "Déconnexion"
            pos_hint: {"center_x": 0.5}
            size_hint: None, None
            size: 200, 50
            on_release: root.manager.current = "login"
'''

# إنشاء وتكوين قاعدة البيانات
def initialize_db():
    conn = sqlite3.connect("myapp.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def add_user(email, username, password):
    conn = sqlite3.connect("myapp.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)", (email, username, password))
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect("myapp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# تعريف التطبيق الأساسي
class LoginScreen(Screen):
    pass

class SignupScreen(Screen):
    pass

class AccueilScreen(Screen):
    pass

class MyApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def show_error(self, message):
        error_label = MDLabel(
            text=message,
            halign="center", 
            theme_text_color="Error",
            pos_hint={"center_x": 0.5, "center_y": 0.1}
        )
        self.root.get_screen("login").add_widget(error_label)

    def signup(self):
        email = self.root.get_screen("signup").ids.email_input.text
        username = self.root.get_screen("signup").ids.signup_username_input.text
        password = self.root.get_screen("signup").ids.signup_password_input.text

        add_user(email, username, password)
        self.root.get_screen("signup").manager.current = "login"

    def login(self):
        username = self.root.get_screen("login").ids.username_input.text
        password = self.root.get_screen("login").ids.password_input.text

        if verify_user(username, password):
            self.root.get_screen("login").manager.current = "accueil"
        else:
            self.show_error("Nom d'utilisateur ou mot de passe est incorrect")

# تهيئة قاعدة البيانات وتشغيل التطبيق
if __name__ == '__main__':
    initialize_db()
    MyApp().run()

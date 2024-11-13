from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDIconButton
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class AccueilScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # حقل البحث
        self.search_input = TextInput(
            hint_text="Rechercher un outil...", 
            size_hint=(None, None), 
            size=(300, 40), 
            pos_hint={"center_x": 0.5, "y": 0.9}, 
            font_size=18,
            background_color=(0.8, 0.9, 1, 1),  # لون أزرق فاتح لحقل الإدخال
            foreground_color=(0, 0, 0, 1)
        )
        self.add_widget(self.search_input)

        # زر البحث
        search_button = Button(
            text="Rechercher", 
            size_hint=(None, None), 
            size=(150, 40), 
            pos_hint={"center_x": 0.8, "y": 0.9},
            background_color=(0, 0.5, 1, 1),  # لون أزرق غامق للزر
            color=(1, 1, 1, 1)
        )
        self.add_widget(search_button)

        # قائمة الأدوات
        self.scroll_view = ScrollView(size_hint=(1, None), height=400, pos_hint={"center_x": 0.5, "y": 0.15})
        self.grid_layout = GridLayout(cols=1, padding=10, spacing=10, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))

        # إضافة أدوات وهمية للعرض
        self.add_mock_tools()
        self.scroll_view.add_widget(self.grid_layout)
        self.add_widget(self.scroll_view)

    def add_mock_tools(self):
        # بيانات وهمية للأدوات
        tools_data = [
            ("Outil 1", "Location 1", "Disponible"),
            ("Outil 2", "Location 2", "Indisponible"),
            ("Outil 3", "Location 3", "Disponible")
        ]

        for tool in tools_data:
            tool_name, location, availability = tool
            tool_box = BoxLayout(size_hint_y=None, height=50, orientation='horizontal', padding=(10, 5))

            # إضافة تفاصيل الأداة مع محاذاة داخل BoxLayout وجعل النص أسود
            tool_box.add_widget(Label(text=tool_name, size_hint_x=0.4, font_size=16, color=(0, 0, 0, 1), halign="left"))
            tool_box.add_widget(Label(text=location, size_hint_x=0.3, font_size=16, color=(0, 0, 0, 1), halign="left"))
            tool_box.add_widget(Label(text=availability, size_hint_x=0.2, font_size=16, color=(0, 0, 0, 1), halign="left"))

            # زر تعديل الأداة
            edit_button = MDIconButton(icon="pencil", size_hint_x=None, width=40, theme_text_color="Custom", text_color=(0, 0.5, 1, 1))
            tool_box.add_widget(edit_button)

            # زر عرض السجل
            history_button = MDIconButton(icon="history", size_hint_x=None, width=40, theme_text_color="Custom", text_color=(0, 0.5, 1, 1))
            tool_box.add_widget(history_button)

            # إضافة الأداة إلى التخطيط
            self.grid_layout.add_widget(tool_box)

class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"  # يمكنك تغييره إلى "Dark" إذا أردت وضع مظلم
        self.theme_cls.primary_palette = "Blue"  # تغيير اللون الأساسي إلى الأزرق
        return AccueilScreen()

if __name__ == '__main__':
    MyApp().run()

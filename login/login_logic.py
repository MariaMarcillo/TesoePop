import ssl
# Asegura la descarga de recursos por HTTPS de forma segura
ssl._create_default_https_context = ssl._create_unverified_context

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage, Image
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.utils import platform  # <--- Necesario para detectar si es Android

# Intentar importar plyer para abrir la galería nativa
try:
    from plyer import filechooser
except ImportError:
    filechooser = None

# Estado global de sesión del usuario actual
CURRENT_USER = {
    "username": "usuario", 
    "role": "client",
    "name": "Jnombre y apellido",
    "email": "juan@example.com",
    "phone": "+000000000",
    "profile_pic": "imagenes/fotouser.png", 
    "is_local_pic": False
}

# --- COMPONENTES MÓVILES PREMIUM ---

class ModernTextInput(BoxLayout):
    def __init__(self, hint_text="", password=False, text="", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = (18, 6, 18, 6)
        self.size_hint_y = None
        self.height = 58
        
        with self.canvas.before:
            Color(0.85, 0.82, 0.8, 0.3) 
            self.shadow = RoundedRectangle(pos=(self.x, self.y - 3), size=self.size, radius=[16])
            Color(1, 1, 1, 1)  
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[16])
            
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        self.input = TextInput(
            text=text,
            hint_text=hint_text,
            password=password,
            multiline=False,
            background_normal='',
            background_active='',
            background_color=(0, 0, 0, 0),
            foreground_color=(0.2, 0.2, 0.2, 1),
            hint_text_color=(0.65, 0.65, 0.65, 1),
            cursor_color=(0.35, 0.2, 0.1, 1),
            font_name="Roboto",
            font_size=15,
            padding=(0, 12, 0, 12)
        )
        self.add_widget(self.input)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.shadow.pos = (self.x, self.y - 3)
        self.shadow.size = self.size

    @property
    def text(self):
        return self.input.text

    @text.setter
    def text(self, val):
        self.input.text = val


class ModernButton(Button):
    def __init__(self, bg_color=(0.92, 0.45, 0.55, 1), text_color=(1, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.color = text_color
        self.bold = True
        self.font_size = 15
        self.font_name = "Roboto"
        self.custom_bg = bg_color
        
        with self.canvas.before:
            Color(0.8, 0.75, 0.75, 0.4)
            self.shadow = RoundedRectangle(pos=(self.x, self.y - 4), size=self.size, radius=[16])
            self.bg_color_inst = Color(*self.custom_bg)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[16])
            
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.bind(state=self.on_state_change)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.shadow.pos = (self.x, self.y - 4)
        self.shadow.size = self.size

    def on_state_change(self, instance, value):
        if value == 'down':
            self.bg_color_inst.a = 0.85
            self.shadow.pos = (self.x, self.y - 1)
        else:
            self.bg_color_inst.a = 1.0
            self.shadow.pos = (self.x, self.y - 4)


class ClientOrdersScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        with self.canvas.before:
            Color(0.99, 0.97, 0.95, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
            
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        layout.add_widget(Label(text="Mis Pedidos", font_size=28, bold=True, color=(0.35, 0.2, 0.1, 1), size_hint_y=0.2))
        layout.add_widget(Label(text="Aquí aparecerá el historial de tus pedidos pronto.", color=(0.5, 0.5, 0.5, 1), halign="center"))
        
        btn_back = ModernButton(text="Volver al Perfil", bg_color=(0.45, 0.3, 0.2, 1), size_hint_y=None, height=50)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'profile'))
        layout.add_widget(btn_back)
        self.add_widget(layout)


class SplashScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        with self.canvas.before:
            Color(0.99, 0.97, 0.95, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        from kivy.uix.floatlayout import FloatLayout
        layout = FloatLayout()
        
        self.logo_galleta = AsyncImage(
            source="imagenes/galletaflotante.png", 
            size_hint=(None, None), size=(140, 140), pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        layout.add_widget(self.logo_galleta)
        
        anim_movimiento = Animation(pos_hint={'center_y': 0.63}, duration=1.5, t='in_out_sine') + \
                          Animation(pos_hint={'center_y': 0.57}, duration=1.5, t='in_out_sine')
        anim_movimiento.repeat = True
        anim_movimiento.start(self.logo_galleta)
        
        lbl_title = Label(
            text="Tesoe Pop", font_size=38, bold=True, color=(0.35, 0.2, 0.1, 1),
            font_name="Roboto", size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        layout.add_widget(lbl_title)
        
        self.progress = ProgressBar(max=100, value=0, size_hint=(0.6, None), height=15, pos_hint={'center_x': 0.5, 'center_y': 0.22})
        layout.add_widget(self.progress)
        self.add_widget(layout)
        
        self.progreso_actual = 0
        Clock.schedule_interval(self.actualizar_carga, 0.03)

    def actualizar_carga(self, dt):
        self.progreso_actual += 1
        self.progress.value = self.progreso_actual
        if self.progreso_actual >= 100:
            Clock.unschedule(self.actualizar_carga)
            Animation.cancel_all(self.logo_galleta)
            self.manager.current = 'login'

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size


class LoginScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        with self.canvas.before:
            Color(0.99, 0.97, 0.95, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        layout = BoxLayout(orientation='vertical', padding=[30, 40, 30, 30], spacing=15)
        
        header = BoxLayout(orientation='vertical', size_hint_y=0.25, spacing=5)
        header.add_widget(Label(text="¡Bienvenido de nuevo!", font_size=26, bold=True, color=(0.35, 0.2, 0.1, 1), font_name="Roboto"))
        header.add_widget(Label(text="Ingresa a tu cuenta de Tesoe Pop", font_size=14, color=(0.6, 0.55, 0.5, 1), font_name="Roboto"))
        layout.add_widget(header)
        
        self.username_input = ModernTextInput(hint_text="Nombre de Usuario")
        self.password_input = ModernTextInput(hint_text="Contraseña", password=True)
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        
        self.error_label = Label(text="", color=(0.9, 0.35, 0.35, 1), font_size=14, bold=True, font_name="Roboto", size_hint_y=0.05)
        layout.add_widget(self.error_label)
        
        btn_login = ModernButton(text="Iniciar Sesión", bg_color=(0.92, 0.45, 0.55, 1), size_hint_y=None, height=54)
        btn_login.bind(on_press=self.verify_login)
        
        btn_go_register = ModernButton(text="¿No tienes cuenta? Regístrate", bg_color=(0.88, 0.84, 0.8, 1), text_color=(0.35, 0.2, 0.1, 1), size_hint_y=None, height=54)
        btn_go_register.bind(on_press=lambda x: setattr(self.manager, 'current', 'register'))
        
        layout.add_widget(btn_login)
        layout.add_widget(btn_go_register)
        layout.add_widget(Label(size_hint_y=0.1))
        self.add_widget(layout)

    def verify_login(self, instance):
        user = self.username_input.text.strip()
        password = self.password_input.text.strip()
        if user == "admin" and password == "1234":
            CURRENT_USER["username"] = "admin"
            CURRENT_USER["role"] = "admin"
            self.manager.current = 'admin_panel'
        elif user != "" and password != "":
            CURRENT_USER["username"] = user
            CURRENT_USER["role"] = "client"
            self.manager.current = 'catalog' 
        else:
            self.error_label.text = "Por favor, completa todos los campos."

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size


class RegisterScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        with self.canvas.before:
            Color(0.99, 0.97, 0.95, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        layout = BoxLayout(orientation='vertical', padding=[30, 35, 30, 25], spacing=12)
        
        header = BoxLayout(orientation='vertical', size_hint_y=0.15, spacing=3)
        header.add_widget(Label(text="Crear Cuenta", font_size=26, bold=True, color=(0.35, 0.2, 0.1, 1), font_name="Roboto"))
        header.add_widget(Label(text="Únete y disfruta de los mejores postres", font_size=13, color=(0.6, 0.55, 0.5, 1), font_name="Roboto"))
        layout.add_widget(header)
        
        self.name_in = ModernTextInput(hint_text="Nombre Completo")
        self.email_in = ModernTextInput(hint_text="Correo Electrónico")
        self.phone_in = ModernTextInput(hint_text="Teléfono Celular")
        self.user_in = ModernTextInput(hint_text="Nombre de Usuario")
        self.pass_in = ModernTextInput(hint_text="Contraseña", password=True)
        
        layout.add_widget(self.name_in)
        layout.add_widget(self.email_in)
        layout.add_widget(self.phone_in)
        layout.add_widget(self.user_in)
        layout.add_widget(self.pass_in)
        
        layout.add_widget(Label(size_hint_y=0.02))
        
        btn_create = ModernButton(text="Registrarme", bg_color=(0.4, 0.65, 0.5, 1), size_hint_y=None, height=52)
        btn_create.bind(on_press=self.register_user)
        
        btn_back = ModernButton(text="Volver al Login", bg_color=(0.75, 0.7, 0.7, 1), size_hint_y=None, height=50)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'login'))
        
        layout.add_widget(btn_create)
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def register_user(self, instance):
        if self.user_in.text.strip():
            CURRENT_USER["username"] = self.user_in.text.strip()
            CURRENT_USER["name"] = self.name_in.text.strip() if self.name_in.text.strip() else CURRENT_USER["name"]
            CURRENT_USER["email"] = self.email_in.text.strip() if self.email_in.text.strip() else CURRENT_USER["email"]
            CURRENT_USER["phone"] = self.phone_in.text.strip() if self.phone_in.text.strip() else CURRENT_USER["phone"]
            CURRENT_USER["role"] = "client"
            self.manager.current = 'catalog'

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size


class ProfileScreen(Screen):
    def on_enter(self):
        self.is_editing = False  
        self.update_profile()

    def update_profile(self):
        self.clear_widgets()
        
        with self.canvas.before:
            Color(0.99, 0.97, 0.95, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        layout = BoxLayout(orientation='vertical', padding=[24, 24, 24, 20], spacing=12)
        
        header_box = BoxLayout(orientation='vertical', size_hint_y=None, height=125, spacing=6)
        
        if CURRENT_USER["is_local_pic"]:
            self.profile_image = Image(source=CURRENT_USER["profile_pic"], size_hint=(None, None), size=(90, 90), pos_hint={'center_x': 0.5})
        else:
            self.profile_image = AsyncImage(source=CURRENT_USER["profile_pic"], size_hint=(None, None), size=(90, 90), pos_hint={'center_x': 0.5})
            
        header_box.add_widget(self.profile_image)
        
        btn_change_pic = Button(
            text="[b]Cambiar Foto desde Galería[/b]", markup=True, size_hint=(None, None), size=(180, 25),
            pos_hint={'center_x': 0.5}, background_normal='', background_color=(0, 0, 0, 0),
            color=(0.92, 0.45, 0.55, 1), font_size=12, font_name="Roboto"
        )
        btn_change_pic.bind(on_press=self.open_gallery)
        header_box.add_widget(btn_change_pic)
        layout.add_widget(header_box)
        
        layout.add_widget(Label(text="Ajustes de la Aplicación", font_size=15, bold=True, color=(0.35, 0.2, 0.1, 1), font_name="Roboto", size_hint_y=None, height=22))
        
        self.edit_name = ModernTextInput(hint_text="Nombre Completo", text=CURRENT_USER["name"])
        self.edit_email = ModernTextInput(hint_text="Correo Electrónico", text=CURRENT_USER["email"])
        self.edit_phone = ModernTextInput(hint_text="Teléfono Celular", text=CURRENT_USER["phone"])
        
        self.edit_name.input.disabled = True
        self.edit_email.input.disabled = True
        self.edit_phone.input.disabled = True
        
        layout.add_widget(self.edit_name)
        layout.add_widget(self.edit_email)
        layout.add_widget(self.edit_phone)
        
        self.info_lbl = Label(text="", color=(0.4, 0.65, 0.5, 1), font_size=13, bold=True, size_hint_y=None, height=18)
        layout.add_widget(self.info_lbl)
        
        self.btn_action = ModernButton(text="Editar Datos", bg_color=(0.35, 0.45, 0.6, 1), size_hint_y=None, height=48)
        self.btn_action.bind(on_press=self.toggle_edit_state)
        layout.add_widget(self.btn_action)
        
        nav_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=46)
        btn_orders = ModernButton(text="Mis Pedidos", bg_color=(0.92, 0.45, 0.55, 1))
        btn_orders.bind(on_press=lambda x: setattr(self.manager, 'current', 'client_orders')) 
        btn_catalog = ModernButton(text="Catálogo", bg_color=(0.45, 0.3, 0.2, 1))
        btn_catalog.bind(on_press=lambda x: setattr(self.manager, 'current', 'catalog'))
        nav_box.add_widget(btn_orders)
        nav_box.add_widget(btn_catalog)
        layout.add_widget(nav_box)
        
        layout.add_widget(Label(text="Síguenos en nuestras Redes", font_size=13, color=(0.6, 0.5, 0.4, 1), font_name="Roboto", size_hint_y=None, height=18))
        
        social_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=44)
        btn_fb = ModernButton(text="Facebook", bg_color=(0.23, 0.35, 0.6, 1))
        btn_fb.bind(on_press=lambda x: self.open_social_link("https://www.facebook.com/share/1Df5DfZN4T/"))
        
        btn_ig = ModernButton(text="Instagram", bg_color=(0.88, 0.26, 0.43, 1))
        btn_ig.bind(on_press=lambda x: self.open_social_link("https://www.instagram.com/tesoepop?igsh=MWl2NDJ3cmRpNzNldg=="))
        
        btn_maps = ModernButton(text="Google Maps", bg_color=(0.2, 0.65, 0.35, 1))
        btn_maps.bind(on_press=lambda x: self.open_social_link("https://maps.google.com"))
        
        social_box.add_widget(btn_fb)
        social_box.add_widget(btn_ig)
        social_box.add_widget(btn_maps)
        layout.add_widget(social_box)
        
        btn_logout = ModernButton(text="Cerrar Sesión", bg_color=(0.85, 0.35, 0.35, 1), size_hint_y=None, height=42)
        btn_logout.bind(on_press=self.logout)
        layout.add_widget(btn_logout)
        
        self.add_widget(layout)

    def toggle_edit_state(self, instance):
        if not self.is_editing:
            self.is_editing = True
            self.edit_name.input.disabled = False
            self.edit_email.input.disabled = False
            self.edit_phone.input.disabled = False
            self.btn_action.text = "Guardar Cambios"
            self.btn_action.bg_color_inst.rgba = (0.4, 0.65, 0.5, 1) 
            self.info_lbl.text = "Modo edición activado. Modifique sus datos."
        else:
            CURRENT_USER["name"] = self.edit_name.text.strip()
            CURRENT_USER["email"] = self.edit_email.text.strip()
            CURRENT_USER["phone"] = self.edit_phone.text.strip()
            
            self.is_editing = False
            self.edit_name.input.disabled = True
            self.edit_email.input.disabled = True
            self.edit_phone.input.disabled = True
            self.btn_action.text = "Editar Datos"
            self.btn_action.bg_color_inst.rgba = (0.35, 0.45, 0.6, 1) 
            
            self.info_lbl.text = "¡Ajustes guardados correctamente!"
            Clock.schedule_once(self.clear_info_lbl, 2)

    def open_gallery(self, instance):
        if filechooser:
            filechooser.open_file(on_selection=self.handle_selection, filters=[("Imágenes", "*.png", "*.jpg", "*.jpeg")])
        else:
            self.info_lbl.text = "Instale 'plyer' para acceder a la galería."

    def handle_selection(self, selection):
        if selection and len(selection) > 0:
            CURRENT_USER["profile_pic"] = selection[0]
            CURRENT_USER["is_local_pic"] = True
            self.profile_image.source = CURRENT_USER["profile_pic"]
            self.profile_image.reload()

    def open_social_link(self, url):
        # Muestra el texto informativo verde que tenías originalmente
        nombre_red = "Facebook" if "facebook" in url else "Instagram" if "instagram" in url else "Google Maps"
        self.info_lbl.text = f"Redirigiendo al {nombre_red} de Tesoe Pop..."
        Clock.schedule_once(self.clear_info_lbl, 2)
        
        # Método universal seguro para Kivy independiente de la plataforma (Evita llamadas rotas a Jnius/Java)
        try:
            import webbrowser
            webbrowser.open(url)
        except Exception:
            pass

    def clear_info_lbl(self, dt):
        self.info_lbl.text = ""

    def logout(self, instance):
        CURRENT_USER["username"] = ""
        CURRENT_USER["role"] = "client"
        self.manager.current = 'login'

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size


class CatalogScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            Rectangle(pos=self.pos, size=self.size)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.add_widget(Label(text="Catálogo de Productos", font_size=24, bold=True, color=(0.35, 0.2, 0.1, 1)))
        
        btn_to_profile = ModernButton(text="Ir a Mi Perfil", bg_color=(0.35, 0.45, 0.6, 1), size_hint_y=None, height=50)
        btn_to_profile.bind(on_press=lambda x: setattr(self.manager, 'current', 'profile'))
        
        layout.add_widget(btn_to_profile)
        self.add_widget(layout)


class AdminPanelScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        
        with self.canvas.before:
            Color(0.99, 0.97, 0.95, 1)
            self.rect_bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        layout = BoxLayout(orientation='vertical', padding=[30, 40, 30, 30], spacing=15)
        
        header = BoxLayout(orientation='vertical', size_hint_y=0.22, spacing=5)
        header.add_widget(Label(text="Panel de Control", font_size=28, bold=True, color=(0.35, 0.2, 0.1, 1), font_name="Roboto"))
        header.add_widget(Label(text="Gestión Interna de Tesoe Pop", font_size=14, color=(0.55, 0.5, 0.45, 1), font_name="Roboto"))
        layout.add_widget(header)
        
        layout.add_widget(Label(text="Acciones Administrativas Disponibles", font_size=15, bold=True, color=(0.4, 0.35, 0.3, 1), size_hint_y=None, height=25))
        
        btn_products = ModernButton(text="Administrar Productos", bg_color=(0.35, 0.45, 0.6, 1), size_hint_y=None, height=52)
        btn_orders_adm = ModernButton(text="Ver Pedidos Globales", bg_color=(0.4, 0.65, 0.5, 1), size_hint_y=None, height=52)
        
        layout.add_widget(btn_products)
        layout.add_widget(btn_orders_adm)
        
        layout.add_widget(Label(size_hint_y=0.15))
        
        btn_logout = ModernButton(text="Cerrar Sesión", bg_color=(0.85, 0.35, 0.35, 1), size_hint_y=None, height=50)
        btn_logout.bind(on_press=lambda x: setattr(self.manager, 'current', 'login'))
        layout.add_widget(btn_logout)
        
        self.add_widget(layout)

    def update_bg(self, instance, value):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size


class TesoePopApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(CatalogScreen(name='catalog'))  
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(ClientOrdersScreen(name='client_orders'))
        sm.add_widget(AdminPanelScreen(name='admin_panel'))
        return sm

if __name__ == '__main__':
    TesoePopApp().run()

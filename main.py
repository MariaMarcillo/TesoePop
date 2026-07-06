from kivy.app import App
from kivy.utils import platform  # Agregamos esto para detectar el celular
from ui.ui_logic import build_screen_manager

class TesoePopApp(App):
    def build(self):
        # Configuración de la ventana principal
        self.title = "Tesoe Pop App"
        
        # --- CÓDIGO PARA PEDIR PERMISOS EN ANDROID ---
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            # Esto hace que salte la ventanita preguntando al usuario
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE, 
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_MEDIA_IMAGES
            ])
        # ----------------------------------------------
       
        # Retorna el ScreenManager completamente estilizado y unificado
        return build_screen_manager()

if __name__ == '__main__':
    TesoePopApp().run()
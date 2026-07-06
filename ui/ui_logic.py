from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.metrics import dp, sp  # <--- IMPORTANTE: Importamos las métricas independientes de densidad

from login.login_logic import SplashScreen, LoginScreen, RegisterScreen, ProfileScreen
from products.products_logic import CatalogScreen, ProductDetailScreen, ClientOrdersScreen
from cart.cart_logic import CartScreen, OrderSummaryScreen
from admin.admin_logic import AdminPanelScreen

def aplicar_estilos_pastel():
    # Establecer un color de fondo pastel para toda la aplicación
    Window.clearcolor = (0.98, 0.96, 0.95, 1)
    
    # Configuramos el tamaño de la ventana para pruebas en PC simulando un móvil
    # Usamos dp para que Kivy entienda la densidad de pixeles desde el arranque
    Window.size = (dp(360), dp(640))


def build_screen_manager():
    aplicar_estilos_pastel()
    sm = ScreenManager()
    
    # Inyección ordenada de las pantallas del ecosistema Tesoe Pop
    sm.add_widget(SplashScreen(name='splash'))
    sm.add_widget(LoginScreen(name='login'))
    sm.add_widget(RegisterScreen(name='register'))
    sm.add_widget(ProfileScreen(name='profile'))
    sm.add_widget(CatalogScreen(name='catalog'))
    sm.add_widget(ProductDetailScreen(name='product_detail'))
    sm.add_widget(ClientOrdersScreen(name='client_orders'))
    sm.add_widget(CartScreen(name='cart'))
    sm.add_widget(OrderSummaryScreen(name='order_summary'))
    sm.add_widget(AdminPanelScreen(name='admin_panel'))
    
    return sm
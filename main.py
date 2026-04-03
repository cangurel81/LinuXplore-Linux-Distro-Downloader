import flet as ft
import os
from src.ui.app_ui import LinuXploreApp

def main(page: ft.Page):
    page.title = "LinuXplore"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0
    
    # Pencere ikonu - eski flet sürümü için
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "linux.ico")
        if os.path.exists(icon_path):
            page.window_icon = icon_path
    except:
        pass
    
    page.theme = ft.Theme(
        color_scheme_seed=ft.colors.BLUE
    )
    
    app = LinuXploreApp(page)
    page.add(app)
    page.update()

if __name__ == "__main__":
    ft.app(main)

import flet as ft
import json
import os
import sys
import webbrowser
import subprocess
import threading
from src.logic.downloader import ISODownloader
from src.logic.scraper import DistroScraper
from pathlib import Path

LINUX_ICONS = {}

page_ref = None

if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def get_data_path(filename):
    return os.path.join(BASE_PATH, "src", "data", filename)

class LinuXploreApp(ft.Row):
    def __init__(self, page: ft.Page):
        global page_ref
        super().__init__()
        self.expand = True
        self.spacing = 0
        page_ref = page
        self._page = page
        self.current_language = "TR"
        self.locales = {}
        self.all_distros = []
        self.download_path = str(Path.home() / "Downloads")
        self.selected_iso = None
        self.is_refreshing = False
        self.downloader = ISODownloader()
        
        self.load_locales()
        self.load_distros()
        self.build_ui()
    
    @property
    def page(self):
        return self._page
    
    @page.setter
    def page(self, value):
        global page_ref
        self._page = value
        page_ref = value
    
    def get_data_path(self, filename):
        if getattr(sys, 'frozen', False):
            base = sys._MEIPASS
        else:
            base = os.path.abspath(__file__)
            # Go from src/ui/app_ui.py -> project root
            base = os.path.dirname(base)  # src/ui/
            base = os.path.dirname(base)  # src/
            base = os.path.dirname(base)  # project root
        return os.path.join(base, "src", "data", filename)
    
    def load_locales(self):
        path = self.get_data_path("locales.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.locales = json.load(f)

    def t(self, key):
        return self.locales.get(self.current_language, {}).get(key, key)

    def load_distros(self):
        path = self.get_data_path("distros.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.all_distros = json.load(f)
        
    def build_ui(self):
        self.search_field = ft.TextField(
            hint_text=self.t("search_hint"),
            prefix_icon=ft.icons.SEARCH,
            border_radius=10,
            on_change=self.on_search,
            text_size=11,
            expand=True
        )
        
        self.selected_category = "Tumu"
        
        self.language_btn = ft.ElevatedButton(
            "TR" if self.current_language == "TR" else "EN",
            height=32,
            bgcolor=ft.colors.BLUE_700,
            color=ft.colors.WHITE,
            on_click=self.toggle_language,
            width=230
        )
        
        self.refresh_btn = ft.ElevatedButton(
            self.t("refresh"),
            icon=ft.icons.REFRESH,
            height=32,
            bgcolor=ft.colors.WHITE,
            color=ft.colors.BLACK,
            on_click=self.refresh_data,
            width=230
        )
        
        self.sort_dropdown = ft.Dropdown(
            width=130,
            height=32,
            value="default",
            text_size=10,
            options=[
                ft.dropdown.Option("default", self.t("sort_default")),
                ft.dropdown.Option("populer", self.t("sort_populer")),
                ft.dropdown.Option("az", self.t("sort_az")),
                ft.dropdown.Option("za", self.t("sort_za")),
                ft.dropdown.Option("newest", self.t("sort_newest")),
                ft.dropdown.Option("oldest", self.t("sort_oldest")),
            ],
            on_change=self.on_sort_change,
            border_radius=6,
        )
        
        self.category_list = ft.ListView(expand=True, spacing=8, padding=15)
        self.category_tiles = {}
        self.usb_tools_label = ft.Text(self.t("usb_tools"), size=11, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_200)
        
        self.rebuild_categories()
        
        self.distro_grid = ft.GridView(
            expand=True,
            max_extent=300,
            child_aspect_ratio=0.9,
            spacing=10,
            run_spacing=10,
            padding=10
        )
        
        sidebar = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.icons.COMPUTER, size=28, color=ft.colors.BLUE_400),
                        ft.Text("LinuXplore", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_400),
                    ], spacing=8),
                    padding=15
                ),
                ft.Divider(height=1, color=ft.colors.BLUE_900),
                self.category_list,
                ft.Divider(height=1, color=ft.colors.BLUE_900),
                ft.Container(
                    content=ft.Column([
                        ft.Container(content=self.refresh_btn, width=230),
                        ft.Container(height=8),
                        self.language_btn,
                        ft.Divider(height=15),
                        self.usb_tools_label,
                        ft.Container(height=8),
                        ft.Column([
                            ft.ElevatedButton(
                                self.t("rufus_btn"),
                                icon=ft.icons.LAUNCH,
                                height=28,
                                bgcolor=ft.colors.WHITE,
                                color=ft.colors.BLACK,
                                on_click=lambda _: webbrowser.open("https://rufus.ie/tr/"),
                                width=210
                            ),
                            ft.Container(height=4),
                            ft.ElevatedButton(
                                self.t("etcher_btn"),
                                icon=ft.icons.LAUNCH,
                                height=28,
                                bgcolor=ft.colors.WHITE,
                                color=ft.colors.BLACK,
                                on_click=lambda _: webbrowser.open("https://etcher.balena.io/"),
                                width=210
                            ),
                        ], spacing=2),
                    ], spacing=3),
                    padding=ft.padding.all(10)
                ),
            ]),
            width=250,
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLUE_GREY_900),
            padding=10
        )
        
        main_content = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        self.search_field,
                    ], spacing=0, alignment=ft.MainAxisAlignment.START),
                    padding=ft.padding.only(left=20, right=20, top=20)
                ),
                self.distro_grid
            ], expand=True, spacing=10),
            expand=True,
            bgcolor=ft.colors.with_opacity(0.05, ft.colors.BLUE_GREY_900)
        )
        
        self.controls = [sidebar, main_content]
        self.update_grid(self.all_distros)

    def get_icon(self, name):
        return LINUX_ICONS.get(name, "🖥️")

    def create_card(self, distro):
        hardware = distro.get('hardware', '?')
        category = distro.get('category', 'Genel')
        icon_text = distro.get('icon_text', distro.get('name', '?')[0])
        
        cat_trans = {
            'Gunluk Kullanim': {'TR': 'Gunluk Kullanim', 'EN': 'Daily Use'},
            'Yeni Baslayanlar': {'TR': 'Yeni Baslayanlar', 'EN': 'Beginners'},
            'Hafif (Eski PC)': {'TR': 'Hafif (Eski PC)', 'EN': 'Lightweight'},
            'Pentest (Guvenlik)': {'TR': 'Pentest (Guvenlik)', 'EN': 'Security'},
            'Server': {'TR': 'Server', 'EN': 'Server'},
        }
        
        cat_key = category if self.current_language == 'TR' else {
            'Gunluk Kullanim': 'category_gunluk',
            'Hafif (Eski PC)': 'category_lightweight',
            'Pentest (Guvenlik)': 'category_pentest',
            'Server': 'category_server',
        }.get(category, 'category_gunluk')
        
        display_category = self.t(cat_key) if cat_key else cat_trans.get(category, {'TR': category, 'EN': category}).get(self.current_language, category)
        
        description = distro.get('description_en', '') if self.current_language == 'EN' else distro.get('description_tr', '')
        if not description:
            description = distro.get('description_tr', distro.get('description', ''))
        
        hw_text = hardware.replace("RAM+", "").replace("RAM", "").strip()
        if not hw_text:
            hw_text = hardware
        cat_text = cat_trans.get(category, {'TR': category, 'EN': category}).get(self.current_language, category)
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Text(icon_text, size=12, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                        bgcolor=ft.colors.BLUE_700,
                        width=36, height=36,
                        border_radius=18,
                        alignment=ft.alignment.center,
                        visible=True
                    ),
                    ft.Column([
                        ft.Text(distro["name"], size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(distro.get("version", ""), size=10, color=ft.colors.BLUE_200),
                    ], spacing=0, expand=True)
                ], spacing=8, alignment=ft.MainAxisAlignment.START),
                ft.Text(description, size=11, max_lines=None),
                ft.Divider(height=1, color=ft.colors.BLUE_GREY_700),
                ft.Column([
                    ft.Row([
                        ft.Icon(ft.icons.MEMORY, size=12, color=ft.colors.BLUE_300),
                        ft.Text(f" RAM: {hw_text}", size=10, color=ft.colors.GREY_300),
                    ]),
                    ft.Row([
                        ft.Icon(ft.icons.CATEGORY, size=12, color=ft.colors.GREEN_300),
                        ft.Text(f" {display_category}", size=10, color=ft.colors.GREY_300),
                    ]),
                ], spacing=4),
                ft.Container(height=6),
                ft.Row([
                    ft.IconButton(
                        icon=ft.icons.LINK,
                        tooltip=self.t("details"),
                        on_click=lambda _, d=distro: self.open_website(d),
                        icon_color=ft.colors.BLUE_300,
                        icon_size=20,
                    ),
                    ft.IconButton(
                        icon=ft.icons.DOWNLOAD,
                        tooltip=self.t("download"),
                        on_click=lambda _, d=distro: self.prompt_download(d),
                        icon_color=ft.colors.GREEN_400,
                        icon_size=20,
                    ),
                ], spacing=0, alignment=ft.MainAxisAlignment.END)
            ], spacing=3),
            padding=12,
            bgcolor=ft.colors.SURFACE,
            border_radius=8,
            border=ft.border.all(1, ft.colors.BLUE_GREY_700)
        )

    def update_grid(self, distros):
        self.distro_grid.controls = [self.create_card(d) for d in distros]
        self.page.update()

    def on_search(self, e):
        query = (self.search_field.value or "").lower()
        if not query:
            self.apply_sort()
        else:
            filtered = [d for d in self.all_distros 
                       if query in d["name"].lower() or query in d.get("description", "").lower()]
            self.apply_sort(filtered)

    def on_sort_change(self, e):
        self.sort_dropdown.value = e.control.value
        self.apply_sort()

    def apply_sort(self, distros=None):
        if distros is None:
            if self.selected_category == "Tumu":
                distros = self.all_distros.copy()
            else:
                distros = [d for d in self.all_distros if d.get("category") == self.selected_category]
        
        sort_type = self.sort_dropdown.value if self.sort_dropdown else "default"
        
        if sort_type == "az":
            distros = sorted(distros, key=lambda x: x.get("name", "").lower())
        elif sort_type == "za":
            distros = sorted(distros, key=lambda x: x.get("name", "").lower(), reverse=True)
        elif sort_type == "newest":
            distros = sorted(distros, key=lambda x: str(x.get("version", "")), reverse=True)
        elif sort_type == "oldest":
            distros = sorted(distros, key=lambda x: str(x.get("version", "")))
        elif sort_type == "populer":
            distros = sorted(distros, key=lambda x: not x.get("best_of_year", False))
        
        self.update_grid(distros)

    def rebuild_categories(self):
        categories = [
            (self.t("category_all"), "Tumu", ft.icons.LIST),
            (self.t("category_lightweight"), "Hafif (Eski PC)", ft.icons.LAPTOP),
            (self.t("category_gunluk"), "Gunluk Kullanim", ft.icons.HOME),
            (self.t("category_pentest"), "Pentest (Guvenlik)", ft.icons.SECURITY),
            (self.t("category_server"), "Server", ft.icons.STORAGE),
        ]
        
        self.category_list.controls.clear()
        self.category_tiles = {}
        for display, category, icon in categories:
            tile = ft.ListTile(
                leading=ft.Icon(icon, color=ft.colors.BLUE_200, size=20),
                title=ft.Text(display, size=14),
                on_click=lambda e, cat=category: self.filter_by_category(cat),
                bgcolor=ft.colors.BLUE_800 if category == self.selected_category else ft.colors.TRANSPARENT
            )
            self.category_tiles[category] = tile
            self.category_list.controls.append(tile)
        
        self.search_field.hint_text = self.t("search_hint")
        self.refresh_btn.text = self.t("refresh")
        self.usb_tools_label.value = self.t("usb_tools")

    def filter_by_category(self, category):
        self.selected_category = category
        
        for cat, tile in self.category_tiles.items():
            tile.bgcolor = ft.colors.BLUE_800 if cat == category else ft.colors.TRANSPARENT
        
        if category == "Tumu":
            self.apply_sort()
        else:
            filtered = [d for d in self.all_distros if d.get("category") == category]
            self.apply_sort(filtered)
        
        self.page.update()

    def toggle_language(self, e):
        self.current_language = "EN" if self.current_language == "TR" else "TR"
        self.language_btn.text = "TR" if self.current_language == "TR" else "EN"
        
        self.sort_dropdown.options = [
            ft.dropdown.Option("default", self.t("sort_default")),
            ft.dropdown.Option("populer", self.t("sort_populer")),
            ft.dropdown.Option("az", self.t("sort_az")),
            ft.dropdown.Option("za", self.t("sort_za")),
            ft.dropdown.Option("newest", self.t("sort_newest")),
            ft.dropdown.Option("oldest", self.t("sort_oldest")),
        ]
        
        self.rebuild_categories()
        self.apply_sort()
        self.page.update()

    def open_website(self, distro):
        url = distro.get("website_url") or distro.get("download_url", "https://distrowatch.com")
        webbrowser.open(url)

    def show_settings(self):
        content = ft.Column([
            ft.Container(height=10),
            ft.Text(self.t("download_folder_label"), size=16),
            ft.Container(height=5),
            ft.Text(self.download_path, size=14),
            ft.Container(height=10),
            ft.Divider(),
            ft.Container(height=10),
            ft.Text(self.t("usb_tools_label"), size=16),
            ft.Container(height=5),
            ft.ElevatedButton(
                self.t("rufus_download"), 
                icon=ft.icons.DOWNLOAD,
                on_click=lambda _: webbrowser.open("https://rufus.ie/tr/")
            ),
            ft.Container(height=5),
            ft.ElevatedButton(
                self.t("etcher_download"), 
                icon=ft.icons.DOWNLOAD,
                on_click=lambda _: webbrowser.open("https://etcher.balena.io/")
            ),
            ft.Container(height=10),
            ft.Divider(),
            ft.Container(height=10),
            ft.Text(self.t("about"), size=16),
            ft.Text(self.t("version_info"), size=14),
            ft.Text(self.t("about_desc"), size=12),
        ], scroll=ft.ScrollMode.AUTO)
        
        dialog = ft.AlertDialog(
            title=ft.Text(self.t("settings")),
            content=content,
            actions=[ft.TextButton(self.t("close"), on_click=lambda _: self.close_settings_dialog(dialog))],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def close_settings_dialog(self, dialog):
        dialog.open = False
        self.page.update()

    def show_usb_writer(self):
        self.iso_picker = ft.FilePicker(on_result=self.on_iso_selected)
        self.page.overlay.append(self.iso_picker)
        
        content = ft.Column([
            ft.Container(height=10),
            ft.Text(self.t("usb_iso_instruction"), size=14),
            ft.Container(height=15),
            ft.ElevatedButton(
                self.t("select_iso_file"),
                icon=ft.icons.FOLDER_OPEN,
                on_click=lambda _: self.iso_picker.pick_files(
                    allow_multiple=False,
                    file_type=ft.FilePickerFileType.ANY
                )
            ),
            ft.Container(height=15),
            ft.Divider(),
            ft.Container(height=10),
            ft.Text(self.t("usb_or_download"), size=12),
        ])
        
        dialog = ft.AlertDialog(
            title=ft.Text(self.t("usb_writer_title")),
            content=content,
            actions=[ft.TextButton(self.t("close"), on_click=lambda _: self.close_usb_dialog(dialog))],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def on_iso_selected(self, e):
        if e.files:
            self.selected_iso = e.files[0].path
            self.show_usb_drives()
        self.close_usb_dialog(None)

    def show_usb_drives(self):
        from src.logic.usb_manager import USBManager
        drives = USBManager.list_usb_drives()
        
        drive_items = []
        for d in drives:
            size = d['size'] / (1024**3)
            drive_items.append(
                ft.ListTile(
                    leading=ft.Icon(ft.icons.USB, color=ft.colors.BLUE_400),
                    title=ft.Text(d["device"]),
                    subtitle=ft.Text(f"{size:.1f} GB - {d['fstype']}"),
                    on_click=lambda _, drive=d: self.open_usb_tool(drive)
                )
            )
        
        content = ft.Column([
            ft.Container(height=10),
            ft.Text(f"{self.t('selected_iso')} {self.selected_iso}", size=12),
            ft.Container(height=10),
            ft.Text(self.t("select_usb_drive_label"), size=16),
            ft.Container(height=10),
        ], scroll=ft.ScrollMode.AUTO)
        
        if drives:
            content.controls.extend(drive_items)
        else:
            content.controls.append(ft.Text(self.t("no_usb_drives"), color=ft.colors.RED))
        
        dialog = ft.AlertDialog(
            title=ft.Text(self.t("select_usb_title")),
            content=content,
            actions=[ft.TextButton(self.t("close"), on_click=lambda _: self.close_usb_dialog(dialog))],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def open_usb_tool(self, drive):
        self.close_usb_dialog(None)
        
        rufus_path = r"C:\Program Files\Rufus\Rufus.exe"
        etcher_path = r"C:\Program Files\balenaEtcher\balenaEtcher.exe"
        
        content = ft.Column([
            ft.Container(height=10),
            ft.Icon(ft.icons.WARNING, color=ft.colors.ORANGE, size=48),
            ft.Container(height=10),
            ft.Text(f"{drive['device']} {self.t('warning_data_loss')}", 
                    color=ft.colors.RED, size=16),
            ft.Text(self.t("warning_irreversible"), size=12),
            ft.Container(height=15),
            ft.Text(self.t("which_tool"), size=14),
            ft.Container(height=10),
            ft.ElevatedButton(
                self.t("open_with_rufus"),
                on_click=lambda _: self.launch_tool(rufus_path, "rufus")
            ),
            ft.Container(height=5),
            ft.ElevatedButton(
                self.t("open_with_etcher"),
                on_click=lambda _: self.launch_tool(etcher_path, "etcher")
            ),
        ], alignment=ft.MainAxisAlignment.CENTER)
        
        dialog = ft.AlertDialog(
            title=ft.Text(self.t("confirm_title")),
            content=content,
            actions=[ft.TextButton(self.t("cancel"), on_click=lambda _: self.close_usb_dialog(dialog))],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def launch_tool(self, tool_path, tool_name):
        self.close_usb_dialog(None)
        
        if tool_name == "rufus":
            if os.path.exists(tool_path) and self.selected_iso:
                subprocess.Popen([tool_path, "-i", self.selected_iso])
            else:
                webbrowser.open("https://rufus.ie/tr/")
        else:
            if os.path.exists(tool_path) and self.selected_iso:
                subprocess.Popen([tool_path, self.selected_iso])
            else:
                webbrowser.open("https://etcher.balena.io/")

    def close_usb_dialog(self, dialog):
        if dialog:
            dialog.open = False
        self.page.update()

    def refresh_data(self, e):
        if self.is_refreshing:
            return
        
        self.is_refreshing = True
        self.refresh_btn.icon = ft.icons.HOURGLASS_EMPTY
        self.refresh_btn.disabled = True
        self.page.update()
        
        status_text = ft.Text(self.t("refresh_status"), size=14)
        spinner = ft.ProgressRing(width=30, height=30, stroke_width=3)
        
        dialog = ft.AlertDialog(
            title=ft.Text(self.t("refresh_title")),
            content=ft.Column([spinner, status_text], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
        
        def do_update():
            try:
                scraper = DistroScraper()
                new_distros = scraper.scrape_all(limit=100)
                self.all_distros = new_distros
                status_text.value = f"{len(new_distros)} {self.t('distros_updated_status')}"
            except Exception as ex:
                status_text.value = f"{self.t('error_prefix')} {ex}"
            finally:
                self.is_refreshing = False
                import time
                time.sleep(1)
                dialog.open = False
                self.refresh_btn.icon = ft.icons.REFRESH
                self.refresh_btn.disabled = False
                self.page.update()
                self.apply_sort()
        
        thread = threading.Thread(target=do_update, daemon=True)
        thread.start()

    def prompt_download(self, distro):
        self.selected_distro = distro
        
        if not os.path.exists(self.download_path):
            self.download_path = str(Path.home() / "Downloads")
        
        self.dir_picker = ft.FilePicker(on_result=self.on_dir_selected)
        self.page.overlay.append(self.dir_picker)
        self.dir_picker.get_directory_path(initial_directory=self.download_path)

    def on_dir_selected(self, e):
        if e.path:
            self.download_path = e.path
            self.start_download()
        elif self.selected_distro:
            self.download_path = str(Path.home() / "Downloads")
            self.start_download()

    def start_download(self):
        distro = self.selected_distro
        
        self.progress_bar = ft.ProgressBar(width=400, value=0)
        self.progress_text = ft.Text(self.t("ready"))
        
        dialog = ft.AlertDialog(
            title=ft.Text(f"{self.t('downloading_title')} {distro['name']}"),
            content=ft.Column([self.progress_text, self.progress_bar]),
            actions=[ft.TextButton(self.t("close"), on_click=lambda _: self.close_download_dialog(dialog))]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
        
        filename = f"{distro['id']}_{distro['version']}.iso"
        url = distro['download_url']
        
        threading.Thread(target=lambda: self.downloader.download(
            url, filename, self.update_download_progress
        ), daemon=True).start()

    def update_download_progress(self, downloaded, total, finished=False, path=None, error=None):
        if error:
            self.progress_text.value = f"{self.t('error_prefix')} {error}"
            self.progress_bar.color = ft.colors.RED
        elif finished:
            self.progress_text.value = f"{self.t('completed_prefix')} {path}"
            self.progress_bar.value = 1.0
            self.progress_bar.color = ft.colors.GREEN
        else:
            if total > 0:
                pct = downloaded / total
                self.progress_bar.value = pct
                self.progress_text.value = self.t("downloading_progress").replace("{percent}", str(int(pct*100)))
            else:
                self.progress_text.value = self.t("downloading_mb").replace("{mb}", f"{downloaded/1024/1024:.1f}")
        
        self.page.update()

    def close_download_dialog(self, dialog):
        dialog.open = False
        self.page.update()

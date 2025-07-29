import flet as ft
import sys
import os

# Explicitly add the project root to sys.path to ensure module imports work
# This handles cases where 'src' might not be found as a package automatically.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now, import the declarative function from manifest_manager
from src.manifest_manager import get_window_title

def main(page: ft.Page):
    """
    The main function for the Flet application.
    It initializes the page and sets the window title by declaratively consuming
    the window_title data from the manifest.
    """
    # Declaratively get the window title directly
    window_title = get_window_title()

    # Set the page title using the retrieved window_title
    page.title = window_title
    print(f"Application Window Title set to: '{page.title}'")

    # Basic page setup
    page.vertical_alignment = ft.CrossAxisAlignment.START
    page.window_width = 400
    page.window_height = 200
    page.window_min_width = 300
    page.window_min_height = 150
    page.theme_mode = ft.ThemeMode.DARK # Or ft.ThemeMode.LIGHT, based on preference

    # Add a simple text control to display the title on the page itself
    page.add(
        ft.Column(
            [
                ft.Text(
                    f"Welcome to {window_title}",
                    size=24,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Text("Manifest loaded successfully!")
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )

    # Update the page to apply changes
    page.update()

if __name__ == "__main__":
    # Run the Flet application, targeting the main function
    ft.app(target=main)

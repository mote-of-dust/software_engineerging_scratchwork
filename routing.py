import flet
from flet import ElevatedButton, Page, Text

def main(page: Page):
    page.add(Text(f"Initial route: {page.route}"))

    def route_change(route):
        page.add(Text(f"New route: {route}"))

    def go_store(e):
        page.route = "/store"
        page.update()

    page.on_route_change = route_change
    page.add(ElevatedButton("Go to Store", on_click=go_store))

flet.app(target=main, view=flet.WEB_BROWSER)
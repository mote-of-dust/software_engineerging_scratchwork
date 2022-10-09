import flet
from flet import IconButton, Page, Row, TextField, icons, ProgressBar, Text, Column, UserControl





def main(page: Page):
    page.title = "Flet counter example"
    page.vertical_alignment = "center"
    pb = ProgressBar(width=100, bar_height=20, bgcolor="#eeeeee", color="#A6E4EF")
    pb.value = 0.0
    classval = str(pb.value)

    txt_number = TextField(value="0", text_align="right", width=100)

    def minus_click(e):
        if txt_number.value > 0:
            txt_number.value = int(txt_number.value) - 1
            pb.value = pb.value - (txt_number.value * 0.01)
            page.update()

    def plus_click(e):
        txt_number.value = int(txt_number.value) + 1
        pb.value = pb.value + (txt_number.value * 0.01)
        if 0.42 < pb.value < 0.75:
            pb.color = "#A95DCE"
        elif pb.value > 0.75:
            pb.color = "#EF3479"
        classval = str(pb.value)
        print(classval)
        print(pb.color)
        page.update()

    page.add(
        Row(
            [
                Text("COSC 3337", style="headlineSmall"),
                Column([pb]),
                IconButton(icons.REMOVE, on_click=minus_click),
                txt_number,
                IconButton(icons.ADD, on_click=plus_click),
            ],
            alignment="center",
        )
    )



flet.app(target=main)

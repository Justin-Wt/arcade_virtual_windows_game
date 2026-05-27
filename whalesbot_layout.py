import customtkinter as ctk

ctk.set_appearance_mode("light")

app = ctk.CTk()
app.geometry("700x400")

code_view = False
model_view = False
# main_screen
main_screen = ctk.CTkFrame(app)
main_screen.place(relwidth=1, relheight=1.0)

# SIDEBAR
sidebar = ctk.CTkFrame(app)
sidebar.place(relwidth=1, relheight=0.05)


def toggle(item):
    if item == "code_view":
        # BUTTON AREA
        bottom_main_screen = ctk.CTkScrollableFrame(main_screen)
        bottom_main_screen.place(relx=0, rely=0.05, relwidth=0.2, relheight=0.95)

        # VERTICAL SEPARATOR
        separator = ctk.CTkFrame(app, width=2, fg_color="black")
        separator.place(relx=0.2, rely=0.05, relheight=0.95)

        # MAIN AREA
        main = ctk.CTkFrame(main_screen)
        main.place(relx=0.205, rely=0.05, relwidth=0.795, relheight=0.95)

        # BUTTONS
        buttons = []
        text = [
            ("Motion", "#EE1A5A"),
            ("Light Speaker", "#007ACC"),
            ("Sensor", "#610DB5"),
            ("Event", "#00FDD7"),
            ("Loop", "#FDB500"),
            ("Logic", "#10C0E8"),
            ("Math", "#1EFD00"),
            ("Variable", "#DBFD00"),
            ("AI", "#AA78FF"),
            ("Patrol Line", "#FDD700"),
            ("My Blocks", "#0050FD"),
            ("Advanced", "#FD4800"),
            ("C Code", "#FD6900"),
        ]
        for item in text:
            button = ctk.CTkButton(
                bottom_main_screen,
                text=item[0],
                height=35,
                hover_color="#ffffff",
                fg_color="#ffffff",
                text_color=item[1],
            )
            button.configure(command=lambda b=button, i=item: select_button(b, i))
            button.pack(fill="x", padx=5, pady=3)
            buttons.append(button)
        # HORIZONTAL SEPARATOR
        separator_horizontal = ctk.CTkFrame(main_screen, height=2, fg_color="black")
        separator_horizontal.place(relx=0, rely=0.05, relwidth=1)

        def select_button(clicked_button, item):
            print(f"{item[0]} button clicked")

            # reset all buttons
            for i, btn in enumerate(buttons):
                btn.configure(fg_color="#ffffff", text_color=text[i][1])

            # highlight clicked button
            clicked_button.configure(
                fg_color=item[1], text_color="#ffffff", hover_color=item[1]
            )


# TITLE BUTTON
CODE_BUTTON = ctk.CTkButton(
    sidebar, text="Code", command=lambda i="code_view": toggle(i)
)
CODE_BUTTON.pack(side="right", pady=(10, 5), padx=1)
MODEL_BUTTON = ctk.CTkButton(sidebar, text="Model")
MODEL_BUTTON.pack(side="right", pady=(10, 5), padx=1)
# HORIZONTAL SEPARATOR
separator_horizontal = ctk.CTkFrame(main_screen, height=2, fg_color="black")
separator_horizontal.place(relx=0, rely=0.05, relwidth=1)


app.mainloop()

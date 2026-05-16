import customtkinter as ctk

ctk.set_appearance_mode("light")

app = ctk.CTk()
app.geometry("700x400")

# SIDEBAR
sidebar = ctk.CTkFrame(app)
sidebar.place(relwidth=1, relheight=1.0)

# MAIN AREA
main = ctk.CTkFrame(sidebar)
main.place(relx=0.205, rely=0.1, relwidth=0.795, relheight=1)

# VERTICAL SEPARATOR
separator = ctk.CTkFrame(app, width=2, fg_color="black")
separator.place(relx=0.2, relheight=1.0)

# TITLE
label2 = ctk.CTkLabel(sidebar, text="Chat History", font=("Arial", 18, "bold"))
label2.pack(pady=(10, 5))

# HORIZONTAL SEPARATOR
separator_horizontal = ctk.CTkFrame(sidebar, height=2, fg_color="black")
separator_horizontal.pack(fill="x", padx=5)

# BUTTON AREA
bottom_sidebar = ctk.CTkScrollableFrame(sidebar)
bottom_sidebar.place(relx=0, rely=0.1, relwidth=0.2, relheight=1)

# MAIN CONTENT
label = ctk.CTkLabel(main, text="MAIN")
label.pack(pady=20)

# BUTTONS
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
buttons = []
for item in text:
    button = ctk.CTkButton(
        bottom_sidebar, text=item[0], height=35, fg_color="#ffffff", text_color=item[1]
    )
    button.configure(command=lambda b=button, i=item: select_button(b, i))
    button.pack(fill="x", padx=5, pady=3)
    buttons.append(button)


def select_button(clicked_button, item):
    print(f"{item[0]} button clicked")

    # reset all buttons
    for btn in buttons:
        btn.configure(fg_color="#ffffff")

    # highlight clicked button
    clicked_button.configure(fg_color=item[1])


app.mainloop()

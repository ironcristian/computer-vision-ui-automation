import tkinter
import customtkinter as ctk
import automation
import threading

#==================================
#Setup
#==================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


app = ctk.CTk()
app.geometry("650x470")
app.resizable(False, False)
app.title("Sonic speed simulator automator")
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=1)


#==================================
#Functions
#==================================


def start_zone(zone):
    thread = threading.Thread(
        target=automation.begin_automation,
        args=(zone,),
        # Need to add coma in (zone,) because the threading function internally calls *args so it means {Take this iterable and unpack its contents as separate arguments.
        # If we had only 1 argument without coma it would take each unpack each letter individually. Adding the coma makes it a tuple and it in fact unpacks each element indiviually,
        # resulting in the full string being unpacked instead of each letter.
        daemon=True # Makes such that this child process now die with its parent it the parent process is killed. For example when I press CTRL-C. This is to prevent freezing.
    )

    thread.start()

def make_button(row_, column_, zone):
    padx_ = 10
    if row_ == 0:       
        pady_ = 40
    elif row_ == 4:
        pady_ = 0
    else:
        pady_= 5

    button = ctk.CTkButton(
        zones_frame,
        text=zone,
        command=lambda: start_zone(zone),
        font=ctk.CTkFont(size=20, weight="bold", family="MADE TOMMY"),
        width=180,
        height=40
    )


    button.grid(
        row=row_,
        column=column_,
        padx=padx_,
        pady=(pady_, 10) 
    )


    return button


    


#==================================
#Header
#==================================

welcome_text = ctk.CTkLabel(
    app,
    text="Sonic Speed Simulator Automator",
    font=("MADE TOMMY",28, "bold")
)

welcome_text.grid(
    row=0,
    column=1,
    pady=(40, 10),
)


instructions = ctk.CTkLabel(
    app,
    text="If you haven't done the tutorial click the red button to start.",
    font=("MADE TOMMY",18, "normal")
)

instructions.grid(row=1, column=1, pady=(0, 20))




#==================================
#Tutorial Button
#==================================


tutorial_button = ctk.CTkButton(
        app,
        text="TUTORIAL",
        font=ctk.CTkFont(size=20, weight="bold",  family="MADE TOMMY"),
        width=200,
        height=60,
        fg_color="red",
        hover_color="darkred",
)

tutorial_button.grid(
    row=2,
    column=1,
    pady=(0, 20)
)

#==================================
#Zone Frame
#==================================


zones_frame = ctk.CTkFrame(
    app,
    width=600,
    height=210,
    corner_radius=20,
)


zones_frame.grid(
    row=3,
    column=1,
    padx=20,
    pady=20,
)

#==================================
#Zones info text
#==================================

zones_text = ctk.CTkLabel(
    zones_frame,
    text="Click a zone to start rebirthing and claiming eggs",
    font=(
        "MADE TOMMY",
        18,
        "normal"
    )
)

zones_text.grid(row=0, column=0, columnspan=3, pady=(10, 0))



#==================================
#Zone Buttons
#==================================

# Row 1 because first of all each frames get its own columns and second I already have text in the 0th row

green_hill_button = make_button(1, 0, "Green Hill")
lost_valley_button = make_button(1, 1, "Lost City")
testing_button = make_button(1, 2, "Green Hill")
emerald_hill_button = make_button(2, 0, "Emerald Hill")
hill_top_button = make_button(2, 1, "Hill Top")
speed_jungle_button = make_button(2, 2, "Speed Jungle")
some_button = make_button(3, 0, "Speed Jungle")
some_button_1 = make_button(3, 1, "Speed Jungle")
some_button_2 = make_button(3, 2, "Speed Jungle")


app.mainloop()



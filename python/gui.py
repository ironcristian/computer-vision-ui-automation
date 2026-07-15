import tkinter
import customtkinter as ctk
import automation
import threading
import pywinstyles

#==================================
#Setup
#==================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self):
        self.automation_thread = None # This is to check if the thread has been created.

        super().__init__()

        self.geometry("650x470")
        self.resizable(False, False)
        self.title("Sonic speed simulator automator")

        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        pywinstyles.change_header_color(self, "#000000")

        #==================================
        #Header
        #==================================

        welcome_text = ctk.CTkLabel(
                self,
                text="Sonic Speed Simulator Automator",
                font=("MADE TOMMY",28, "bold")
        )

        welcome_text.grid(
                row=0,
                column=1,
                pady=(40, 10),
        )


        instructions = ctk.CTkLabel(
                self,
                text="If you haven't done the tutorial click the red button to start.",
                font=("MADE TOMMY",18, "normal")
        )

        instructions.grid(row=1, column=1, pady=(0, 20))




        #==================================
        #Tutorial Button
        #==================================


        tutorial_button = ctk.CTkButton(
                self,
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


        self.zones_frame = ctk.CTkFrame(
            self,
            width=600,
            height=210,
            corner_radius=20,
            fg_color="#3E3E3E"
        )


        self.zones_frame.grid(
            row=3,
            column=1,
            padx=20,
            pady=20,
        )

        #==================================
        #Zones info text
        #==================================

        zones_text = ctk.CTkLabel(
            self.zones_frame,
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

        green_hill_button = self.make_button(1, 0, "Green Hill")
        lost_valley_button = self.make_button(1, 1, "Lost Valley")
        testing_button = self.make_button(1, 2, "Emerald Hill")
        emerald_hill_button = self.make_button(2, 0, "Hill Top")
        hill_top_button = self.make_button(2, 1, "Speed Jungle")
        speed_jungle_button = self.make_button(2, 2, "No Place")
        some_button = self.make_button(3, 0, "Cyber Station")
        some_button_1 = self.make_button(3, 1, "Cyber Station")
        some_button_2 = self.make_button(3, 2, "Metro City")



    #==================================
    #Functions
    #==================================

    def start_zone(self, zone):

        # if self.automation_thread is not None and self.automation_thread.is_alive():
            thread = threading.Thread(
                target=automation.begin_automation,
                args=(zone,),
                # Need to add coma in (zone,) because the threading function internally calls *args so it means {Take this iterable and unpack its contents as separate arguments.
                # If we had only 1 argument without coma it would take each unpack each letter individually. Adding the coma makes it a tuple and it in fact unpacks each element indiviually,
                # resulting in the full string being unpacked instead of each letter.
                daemon=True # Makes such that this child process now die with its parent it the parent process is killed. For example when I press CTRL-C. This is to prevent freezing.
            )

            thread.start()


    def make_button(self, row_, column_, zone):
        padx_ = 10
        if row_ == 0:       
            pady_ = 40
        elif row_ == 4:
            pady_ = 0
        else:
            pady_= 5

        button = ctk.CTkButton(
            self.zones_frame,
            text=zone,
            command=lambda: self.start_zone(zone),
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
        
    
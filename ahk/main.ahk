#Requires AutoHotkey v2.0
#Include constants.ahk
;By the way you need to be fully zoomed out of your screen for this to work.


SendMode "Event"

portal_button_x := IniRead("portal_coordinates.ini", "Portal", "portal_button_x") * A_ScreenWidth
portal_button_y := IniRead("portal_coordinates.ini", "Portal", "portal_button_y") * A_ScreenHeight

current_zone := ""

F8::
{
    FileOpen("../command.txt", "w").Close()
    ExitApp

}


Loop
{
    global current_zone
    if FileExist("../command.txt")
        {
            command := Trim(FileRead("../command.txt"))

        if command != ""
        {

            if command = "Rebirth"
            {
                Rebirth()
                ClearCommand()
            }
            else if command = "Claim_EGG"
            {
                Claim_EGG()
                ClearCommand()
            }
            else if command = "Claim_XP"
            {
                Claim_XP()
                ClearCommand()
            }
            else if command = "Click_Portal"
            {
                Click_Portal()
                ClearCommand()
            }
            else
            {
                current_zone := command ; Command in this case will be a zone name
                Choose_Walk(command)
                ClearCommand()
            }
        }

    }
    Sleep 50    ; Added small delay to reduce CPU busy waiting
}

ClearCommand()
{
    FileOpen("../command.txt", "w").Close()
    FileOpen("../done.txt", "w").Close()
}

Zoom_Out()
{
    Send "{WheelDown 70}"
    Sleep 200
}


Rebirth() 
{   
    ; In this version variables need to be declared global inside functions unless defined INSIDE the function
    global current_zone, CLOSE_X, CLOSE_Y, YES_X, YES_Y, REBIRTH_BUTTON_X, REBIRTH_BUTTON_Y, REBIRTH_PRICE_X, REBIRTH_PRICE_Y
    MouseClick("Left", CLOSE_X, CLOSE_Y)     ;Click Close button
    Sleep 1500

    MouseClick("Left", YES_X, YES_Y)     ;Click Yes
    Sleep 1500

    MouseClick("Left", REBIRTH_BUTTON_X, REBIRTH_BUTTON_Y)      ;Click rebirth button
    Sleep 1500
    
    MouseClick("Left", REBIRTH_PRICE_X, REBIRTH_PRICE_Y)     ;Click rebirth price button
    Sleep 2000

    Walk_To(current_zone)
}


Claim_XP()
{
    global CLAIM_XP_X, CLAIM_XP_Y
    MouseClick("Left", CLAIM_XP_X, CLAIM_XP_Y)
}

Click_Portal()
{
    global portal_button_x, portal_button_y

    MouseClick("Left", portal_button_x, portal_button_y)     ;Click the portal travel button
    Sleep 300

}



Claim_EGG()
{
    global current_zone, CLOSE_X, CLOSE_Y, YES_X, YES_Y, EGG_NOTIFICATION_X, EGG_NOTIFICATION_Y, CLAIM_BUTTON_X, CLAIM_BUTTON_Y, X_BUTTON_X, X_BUTTON_Y
    MouseClick("Left", CLOSE_X, CLOSE_Y)     ;Click Close button
    Sleep 1000

    MouseClick("Left", YES_X, YES_Y)     ;Click Yes
    Sleep 3000

    MouseClick("Left", EGG_NOTIFICATION_X, EGG_NOTIFICATION_Y)     ;Click egg notification
    Sleep 2000

    MouseClick("Left", CLAIM_BUTTON_X, CLAIM_BUTTON_Y)     ;Click CLAIM
    Sleep 4000

    MouseClick("Left", X_BUTTON_X, X_BUTTON_Y)     ;Click X
    Sleep 2000

    MouseClick("Left", X_BUTTON_X, X_BUTTON_Y)     ;Click X
    Sleep 1000

    Walk_To(current_zone)
}


;----------------------------------------------------------------------------------
;--------------LOST CITY WALK AND TELEPORTATION FUNCTIONS------------------------
;----------------------------------------------------------------------------------
Lost_City_Walk()
{
    Zoom_Out()
    global YES_X, YES_Y
    ;Walk to Auto-Run area
    Sleep 1000
    Send "{w down}"
    Sleep 200
    Send "{w up}"
    Sleep 100

    Send "{d down}"
    Sleep 1800
    Send "{d up}"
    Sleep 1000


    MouseClick("Left", YES_X, YES_Y)      ;Click Yes
    Sleep 2000
}

;Teleports the player to Lost City zone
Lost_City_Portal(next_clicks)
{
    
    global LOST_CITY_BUTTON_X, LOST_CITY_BUTTON_Y, TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y, YES_X, YES_Y

    MouseClick("Left", LOST_CITY_BUTTON_X, LOST_CITY_BUTTON_Y)  ;Click the zone we want to go to
    Sleep 300

    MouseClick("Left", TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y)    ;Click the green travel button that will teleport the player there
    Sleep 300

    MouseClick("Left", YES_X, YES_Y)
    Sleep 10000


}

;----------------------------------------------------------------------------------
;--------------EMERALD HILL WALK AND TELEPORTATION FUNCTIONS-----------------------
;----------------------------------------------------------------------------------
Emerald_Hill_Walk()
{
    Zoom_Out()
    global YES_X, YES_Y

    Sleep 1000
    Send "{d down}"
    Sleep 1900
    Send "{d up}"
    Sleep 100

    Send "{s down}"
    Sleep 500
    Send "{s up}"
    Sleep 1000

    MouseClick("Left", YES_X, YES_Y)      ;Click Yes
    Sleep 2000


}

;Teleports the player to the Emerald Hill zone
Emerald_Hill_Portal(next_clicks)
{
    
    global EMERALD_HILL_BUTTON_X, EMERALD_HILL_BUTTON_Y, TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y, YES_Y, YES_X

    
    MouseClick("Left", EMERALD_HILL_BUTTON_X, EMERALD_HILL_BUTTON_Y)  ;Click the zone we want to go to
    Sleep 300

    MouseClick("Left", TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y)    ;Click the green travel button that will teleport the player there
    Sleep 300

    MouseClick("Left", YES_X, YES_Y)
    Sleep 10000

}


;----------------------------------------------------------------------------------
;--------------GEEN HILL WALK AND TELEPORTATION FUNCTIONS--------------------------
;----------------------------------------------------------------------------------


Green_Hill_Walk()
{
    Zoom_Out()
    global YES_X, YES_Y

    Sleep 1000
    Send "{d down}"
    Sleep 800
    Send "{d up}"
    Sleep 200

    Sleep 200
    Send "{s down}"
    Sleep 1300
    Send "{s up}"
    Sleep 300

    Send "{d down}"
    Sleep 1800
    Send "{d up}"

    Send "{s down}"
    Sleep 2500
    Send "{s up}"
    Sleep 500

    MouseClick("Left", YES_X, YES_Y)      ;Click Yes
    Sleep 2000
}

Green_Hill_Portal(next_clicks)
{
    
    global GREEN_HILL_BUTTON_X, GREEN_HILL_BUTTON_Y, TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y, YES_Y, YES_X

    MouseClick("Left", GREEN_HILL_BUTTON_X, GREEN_HILL_BUTTON_Y)
    Sleep 300

    MouseClick("Left", TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y)
    Sleep 300

    MouseClick("Left", YES_X, YES_Y)
    Sleep 10000

}


;----------------------------------------------------------------------------------
;--------------GEEN HILL WALK AND TELEPORTATION FUNCTIONS--------------------------
;----------------------------------------------------------------------------------



Hill_Top_Walk()
{
    Zoom_Out()
    global YES_X, YES_Y

    Sleep 1000
    Send "{w down}"
    Sleep 400
    Send "{w up}"
    Sleep 200

    Send "{a down}"
    Sleep 1500
    Send "{a up}"
    Sleep 400

    Send "{w down}"
    Sleep 300
    Send "{w up}"
    Sleep 400

    Send "{a down}"
    Sleep 1000
    Send "{a up}"
    Sleep 400

    MouseClick("Left", YES_X, YES_Y)      ;Click Yes
    Sleep 2000
}

Hill_Top_Portal(next_clicks)
{
    global portal_button_x, portal_button_y, HILL_TOP_BUTTON_X, HILL_TOP_BUTTON_Y, TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y, YES_Y, YES_X

    MouseClick("Left", portal_button_x, portal_button_y)    ;Click the portal travel button
    Sleep 300

    MouseClick("Left", HILL_TOP_BUTTON_X, HILL_TOP_BUTTON_Y)
    Sleep 300

    MouseClick("Left", TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y)
    Sleep 300

    MouseClick("Left", YES_X, YES_Y)
    Sleep 10000
}


; Teleport o chosen zone and walk to auto-run
Choose_Walk(zone)
{
    if zone = "Green Hill"
    {
        Green_Hill_Portal()
        Green_Hill_Walk()
    }
    else if zone = "Emerald Hill"
    {
        Emerald_Hill_Portal()
        Emerald_Hill_Walk()
    }
    else if zone = "Lost City"
    {
        Lost_City_Portal()
        Lost_City_Walk()
    }
    else if zone = "Hill Top"
    {
        Hill_Top_Portal()
        Hill_Top_Walk()
    }

}

; Walk to auto-run area in chosen zone
Walk_to(zone)
{
    if zone = "Green Hill"
    {
        Green_Hill_Walk()
    }
    else if zone = "Emerald Hill"
    {
        Emerald_Hill_Walk()
    }
    else if zone = "Lost City"
    {
        Lost_City_Walk()
    }
    else if zone = "Hill Top"
    {
        Hill_Top_Walk()
    }

}
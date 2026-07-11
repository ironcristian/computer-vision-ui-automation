#Requires AutoHotkey v2.0
#Include constants.ahk
;By the way you need to be fully zoomed out of your screen for this to work.




portal_button_x := IniRead("portal_coordinates.ini", "Portal", "portal_button_x") * A_ScreenWidth
portal_button_y := IniRead("portal_coordinates.ini", "Portal", "portal_button_y") * A_ScreenHeight
SendMode "Event"
F8::
{
    FileOpen("../command.txt", "w").Close()
    ExitApp

}


Loop
{
    if FileExist("../command.txt")
    {
        command := Trim(FileRead("../command.txt"))
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
        else if command = "EXIT"
        {
            FileOpen("../command.txt", "w").Close() ; I know python already clears the file on exit. This is just in case python crashes, as atexit doesnt work in that case.
            FileDelete("../done.txt")
            ExitApp
        }
        else
        {
            Choose_Walk(command)
            ClearCommand()
        }
    }

    Sleep 50    ; Added smal delay to reduce CPU busy waiting
}

ClearCommand()
{
    FileOpen("../command.txt", "w").Close()
    FileOpen("../done.txt", "w").Close()
}


Rebirth() 
{   
    ; In this version variables need to be declared global inside functions unless defined INSIDE the function
    global CLOSE_X, CLOSE_Y, YES_X, YES_Y, REBIRTH_BUTTON_X, REBIRTH_BUTTON_Y, REBIRTH_PRICE_X, REBIRTH_PRICE_Y
    MouseClick("Left", CLOSE_X, CLOSE_Y)     ;Click Close button
    Sleep 1500

    MouseClick("Left", YES_X, YES_Y)     ;Click Yes
    Sleep 1500

    MouseClick("Left", REBIRTH_BUTTON_X, REBIRTH_BUTTON_Y)      ;Click rebirth button
    Sleep 1500
    
    MouseClick("Left", REBIRTH_PRICE_X, REBIRTH_PRICE_Y)     ;Click rebirth price button
    Sleep 2000

    Lost_City_Walk()
}


Claim_XP()
{
    global CLAIM_XP_X, CLAIM_XP_Y
    MouseClick("Left", CLAIM_XP_X, CLAIM_XP_Y)
}


Claim_EGG()
{
    global CLOSE_X, CLOSE_Y, YES_X, YES_Y, EGG_NOTIFICATION_X, EGG_NOTIFICATION_Y, CLAIM_BUTTON_X, CLAIM_BUTTON_Y, X_BUTTON_X, X_BUTTON_Y
    MouseClick("Left", CLOSE_X, CLOSE_Y)     ;Click Close button
    Sleep 1000

    MouseClick("Left", YES_X, YES_Y)     ;Click Yes
    Sleep 3000

    MouseClick("Left", EGG_NOTIFICATION_X, EGG_NOTIFICATION_Y)     ;Click egg notification
    Sleep 2000

    MouseClick("Left", CLAIM_BUTTON_X, CLAIM_BUTTON_Y)     ;Click CLAIM
    Sleep 4000

    MouseClick("Left", X_BUTTON_X, X_BUTTON_Y)     ;Click X
    Sleep 1000

    Lost_City_Walk()
}


;----------------------------------------------------------------------------------
;--------------LOST VALLEY WALK AND TELEPORTATION FUNCTIONS------------------------
;----------------------------------------------------------------------------------
Lost_City_Walk()
{
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
Lost_City_Portal()
{
    global portal_button_x, portal_button_y, LOST_CITY_BUTTON_X, LOST_CITY_BUTTON_Y, TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y, YES_X, YES_Y

    Sleep 1000
    MouseClick("Left", portal_button_x, portal_button_y)     ;Click the portal travel button
    Sleep 1000

    MouseClick("Left", LOST_CITY_BUTTON_X, LOST_CITY_BUTTON_Y)  ;Click the zone we want to go to
    Sleep 1000

    MouseClick("Left", TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y)    ;Click the green travel button that will teleport the player there
    Sleep 1000

    MouseClick("Left", YES_X, YES_Y)
    Sleep 10000


}

;----------------------------------------------------------------------------------
;--------------EMERALD HILL WALK AND TELEPORTATION FUNCTIONS-----------------------
;----------------------------------------------------------------------------------
Emerald_Hill_Walk()
{
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
Emerald_Hill_Portal()
{
    
    global portal_button_x, portal_button_y, EMERALD_HILL_BUTTON_X, EMERALD_HILL_BUTTON_Y, TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y, YES_Y, YES_X

    MouseClick("Left", portal_button_x, portal_button_y)    ;Click the portal travel button
    Sleep 1000

    MouseClick("Left", EMERALD_HILL_BUTTON_X, EMERALD_HILL_BUTTON_Y)  ;Click the zone we want to go to
    Sleep 1000

    MouseClick("Left", TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y)    ;Click the green travel button that will teleport the player there
    Sleep 1000

    MouseClick("Left", YES_X, YES_Y)
    Sleep 10000

}

;-----------------------------------------------------------
;-----------------------------------------------------------
;-----------------------------------------------------------



Choose_Walk(zone)
{
    if zone = "Green Hill"
    {
        ;Green_Hill_Portal()
        ;Green_Hill_Walk()
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
    else if zone = "Hill Top"w
    {
        ;Hill_Top_Portal()
        ;Hill_Top_Walk()
    }





}
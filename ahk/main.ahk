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
            else if IsInteger(command) {
                Page_Change(command)
                ClearCommand()
            }
            else if command = "Set_Speed" {
                Set_Speed_To_1()
                ClearCommand()
            }
            else if SubStr(command, -7) = "_portal"
            {
                Choose_Portal(command)
                ClearCommand()
            }
            else    
            {
                current_zone := command ; Command in this case will be a zone name
                Walk_to(command)
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
    Sleep 1000

    MouseClick("Left", YES_X, YES_Y)     ;Click Yes
    Sleep 1000

    MouseClick("Left", REBIRTH_BUTTON_X, REBIRTH_BUTTON_Y)      ;Click rebirth button
    Sleep 500
    
    MouseClick("Left", REBIRTH_PRICE_X, REBIRTH_PRICE_Y)     ;Click rebirth price button
    Sleep 1000

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
    Sleep 1000 ; Add a long delay here so then python doesnt take a screenshot of the portal too fast resulting in an incorrect portal screenshot

}

Choose_Portal(zone)
{
    switch zone
    {
        case "Green_Hill_Portal":
            Green_Hill_Portal()

        case "Lost_Valley_Portal":
            Lost_Valley_Portal()

        case "Emerald_Hill_Portal":
            Emerald_Hill_Portal()

        case "Hill_Top_Portal":
            Hill_Top_Portal()

        case "Speed_Jungle_Portal":
            Speed_Jungle_Portal()

        case "No_Place_Portal":
            No_Place_Portal()

        case "Cyber_Station_Portal":
            Cyber_Station_Portal()

        case "New_Yoke_Portal":
            New_Yoke_Portal()

        case "Metro_City":
            Metro_City_Portal()
    }
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

Page_Change(page_distance)
{
    global NEXT_BUTTON_PORTAL_X, NEXT_BUTTON_PORTAL_Y, BACK_BUTTON_PORTAL_X, BACK_BUTTON_PORTAL_Y
    
    if page_distance = 0 {
        return
    }
    else if page_distance > 0 {
        Loop page_distance 
        {
            MouseClick("Left", NEXT_BUTTON_PORTAL_X, NEXT_BUTTON_PORTAL_Y)
            Sleep 1500
        }
    }
    else if page_distance < 0 {
        Loop page_distance * -1
        {
            MouseClick("Left", BACK_BUTTON_PORTAL_X, BACK_BUTTON_PORTAL_Y)
            Sleep 1500
        } 
    }


}

Set_Speed_To_1()
{

    global SETTINGS_BUTTON_X, SETTINGS_BUTTON_Y, SETTINGS_X_BUTTON_X, SETTINGS_X_BUTTON_Y, SPEED_TEXTBOX_X, SPEED_TEXTBOX_Y

    MouseClick("left", SETTINGS_BUTTON_X, SETTINGS_BUTTON_Y)
    Sleep 200

    MouseMove(screenWidth * 0.5, screenHeight * 0.5)

    Send "{WheelUp 70}"
    Sleep 100
   
    MouseClick("left", SPEED_TEXTBOX_X, SPEED_TEXTBOX_Y)
    Sleep 100

    Send "{1}"
    Sleep 100

    MouseClick("left", SETTINGS_X_BUTTON_X, SETTINGS_X_BUTTON_Y)

}


;----------------------------------------------------------------------------------
;--------------LOST CITY WALK AND TELEPORTATION FUNCTIONS------------------------
;----------------------------------------------------------------------------------
Lost_Valley_Walk()
{
    Zoom_Out()
    global YES_X, YES_Y
    ;Walk to Auto-Run area

    Send "{d down}"
    Sleep 3000
    Send "{d up}"
    Sleep 400

    Send "{s down}"
    Sleep 1500
    Send "{s up}"
    Sleep 200


    MouseClick("Left", YES_X, YES_Y)      ;Click Yes
    Sleep 3500
}

;Teleports the player to Lost City zone
Lost_Valley_Portal()
{
    
    global LOST_VALLEY_BUTTON_X, LOST_VALLEY_BUTTON_Y, TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y, YES_X, YES_Y

    MouseClick("Left", LOST_VALLEY_BUTTON_X, LOST_VALLEY_BUTTON_Y)  ;Click the zone we want to go to
    Sleep 150

    MouseClick("Left", TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y)    ;Click the green travel button that will teleport the player there
    Sleep 150

    MouseClick("Left", YES_X, YES_Y)

}

;----------------------------------------------------------------------------------
;--------------EMERALD HILL WALK AND TELEPORTATION FUNCTIONS-----------------------
;----------------------------------------------------------------------------------
Emerald_Hill_Walk()
{
    Zoom_Out()
    global YES_X, YES_Y

    Send "{d down}"
    Sleep 2500
    Send "{d up}"
    Sleep 100

    Send "{s down}"
    Sleep 2000
    Send "{s up}"
    Sleep 100

    MouseClick("Left", YES_X, YES_Y)      ;Click Yes
    Sleep 3500 ; Short delay to make the Auto-Run UI pop up

}

;Teleports the player to the Emerald Hill zone
Emerald_Hill_Portal()
{
    
    global EMERALD_HILL_BUTTON_X, EMERALD_HILL_BUTTON_Y, TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y, YES_Y, YES_X

    
    MouseClick("Left", EMERALD_HILL_BUTTON_X, EMERALD_HILL_BUTTON_Y)  ;Click the zone we want to go to
    Sleep 150

    MouseClick("Left", TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y)    ;Click the green travel button that will teleport the player there
    Sleep 150

    MouseClick("Left", YES_X, YES_Y)

}


;----------------------------------------------------------------------------------
;--------------GREEN HILL WALK AND TELEPORTATION FUNCTIONS--------------------------
;----------------------------------------------------------------------------------


Green_Hill_Walk()
{
    Zoom_Out()
    global YES_X, YES_Y

    Send "{s down}"
    Sleep 4000
    Send "{s up}"
    Sleep 200
  
    Send "{d down}"
    Sleep 3000
    Send "{d up}"
    Sleep 300

    MouseClick("Left", YES_X, YES_Y)      ;Click Yes
    Sleep 3500
}

Green_Hill_Portal()
{
    
    global GREEN_HILL_BUTTON_X, GREEN_HILL_BUTTON_Y, TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y, YES_Y, YES_X

    MouseClick("Left", GREEN_HILL_BUTTON_X, GREEN_HILL_BUTTON_Y)
    Sleep 150

    MouseClick("Left", TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y)
    Sleep 150

    MouseClick("Left", YES_X, YES_Y)

}


;----------------------------------------------------------------------------------
;--------------HILL TOP WALK AND TELEPORTATION FUNCTIONS--------------------------
;----------------------------------------------------------------------------------



Hill_Top_Walk()
{
    Zoom_Out()
    global YES_X, YES_Y

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
    Sleep 3500
}

Hill_Top_Portal()
{
    global HILL_TOP_BUTTON_X, HILL_TOP_BUTTON_Y, TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y, YES_Y, YES_X

    MouseClick("Left", HILL_TOP_BUTTON_X, HILL_TOP_BUTTON_Y)
    Sleep 150

    MouseClick("Left", TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y)
    Sleep 150

    MouseClick("Left", YES_X, YES_Y)

}


;----------------------------------------------------------------------------------
;--------------SPEED JUNGLE WALK AND TELEPORTATION FUNCTIONS--------------------------
;----------------------------------------------------------------------------------

Speed_Jungle_Walk()
{
    Zoom_Out()
    global YES_X, YES_Y

    Send "{w down}"
    Sleep 2500
    Send "{w up}"
    Sleep 200

    Send "{d down}"
    Sleep 6000
    Send "{d up}"
    Sleep 400

    Send "{s down}"
    Sleep 1700
    Send "{s up}"
    Sleep 200

    Send "{d down}"
    Sleep 3000
    Send "{d up}"
    Sleep 200

    MouseClick("Left", YES_X, YES_Y)      ;Click Yes
    Sleep 3500
}

Speed_Jungle_Portal()
{
    global SPEED_JUNGLE_BUTTON_X, SPEED_JUNGLE_BUTTON_X, TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y, YES_Y, YES_X

    MouseClick("Left", SPEED_JUNGLE_BUTTON_X, SPEED_JUNGLE_BUTTON_Y)
    Sleep 150

    MouseClick("Left", TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y)
    Sleep 150

    MouseClick("Left", YES_X, YES_Y)
}

;----------------------------------------------------------------------------------
;--------------NO PLACE WALK AND TELEPORTATION FUNCTIONS--------------------------
;----------------------------------------------------------------------------------

No_Place_Walk()
{

}

No_Place_Portal()
{
    global NO_PLACE_BUTTON_X, NO_PLACE_BUTTON_Y, TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y, YES_Y, YES_X

    MouseClick("Left", NO_PLACE_BUTTON_X, NO_PLACE_BUTTON_Y)
    Sleep 150

    MouseClick("Left", TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y)
    Sleep 150

    MouseClick("Left", YES_X, YES_Y)
}

;----------------------------------------------------------------------------------
;--------------CYBER STATION WALK AND TELEPORTATION FUNCTIONS--------------------------
;----------------------------------------------------------------------------------

Cyber_Station_Walk()
{

}

Cyber_Station_Portal()
{
    global CYBER_STATION_BUTTON_X, CYBER_STATION_BUTTON_Y, TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y, YES_Y, YES_X

    MouseClick("Left", CYBER_STATION_BUTTON_X, CYBER_STATION_BUTTON_Y)
    Sleep 150

    MouseClick("Left", TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y)
    Sleep 150

    MouseClick("Left", YES_X, YES_Y)
}

;----------------------------------------------------------------------------------
;--------------CYBER STATION WALK AND TELEPORTATION FUNCTIONS--------------------------
;----------------------------------------------------------------------------------

New_Yoke_Walk()
{

}

New_Yoke_Portal()
{
    global NEW_YOKE_BUTTON_X, NEW_YOKE_BUTTON_Y, TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y, YES_Y, YES_X

    MouseClick("Left", NEW_YOKE_BUTTON_X, NEW_YOKE_BUTTON_Y)
    Sleep 150

    MouseClick("Left", TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y)
    Sleep 150

    MouseClick("Left", YES_X, YES_Y)
}


;----------------------------------------------------------------------------------
;--------------CYBER STATION WALK AND TELEPORTATION FUNCTIONS--------------------------
;----------------------------------------------------------------------------------

Metro_City_Walk()
{

}

Metro_City_Portal()
{
    global METRO_CITY_BUTTON_X, METRO_CITY_BUTTON_Y, TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y, YES_Y, YES_X

    MouseClick("Left", METRO_CITY_BUTTON_X, METRO_CITY_BUTTON_Y)
    Sleep 150

    MouseClick("Left", TRAVEL_BUTTON_X, TRAVEL_BUTTON_Y)
    Sleep 150

    MouseClick("Left", YES_X, YES_Y)
}



; Walk to auto-run area in chosen zone
Walk_to(zone)
{   
    switch zone
    {
    case "Green Hill":
        Green_Hill_Walk()

    case "Lost Valley":
        Lost_Valley_Walk()

    case "Emerald Hill":
        Emerald_Hill_Walk()

    case "Hill Top":
        Hill_Top_Walk()

    case "Speed Jungle":
        Speed_Jungle_Walk()

    case "No Place":
        No_Place_Walk()

    case "Cyber Station":
        Cyber_Station_Walk()

    case "New Yoke":
        New_Yoke_Walk()

    case "Metro City":
        Metro_City_Walk()
    }

}
;By the way you need to be fully zoomed out of your screen for this to work.


SendMode "Event"
F8::
{
    FileOpen("command.txt", "w").Close()
    ExitApp

}
; Screen size
screenWidth := A_ScreenWidth
screenHeight := A_ScreenHeight

; Scaled coordinates
; Got the ratio and multipled by my screen resolution already so i get the coordinates. This will make it such that it works on any resolution
CLOSE_X := Round((1294 / 1920) * screenWidth)
CLOSE_Y := Round((796 / 1080) * screenHeight)

YES_X := Round((860 / 1920) * screenWidth)
YES_Y := Round((623 / 1080) * screenHeight)

REBIRTH_BUTTON_X := Round((945 / 1920) * screenWidth)
REBIRTH_BUTTON_Y := Round((48 / 1080) * screenHeight)

REBIRTH_PRICE_X := Round((955 / 1920) * screenWidth)
REBIRTH_PRICE_Y := Round((876 / 1080) * screenHeight)

CLAIM_XP_X := Round((869 / 1920) * screenWidth)
CLAIM_XP_Y := Round((978 / 1080) * screenHeight)

EGG_NOTIFICATION_X := Round((189 / 1920) * screenWidth)
EGG_NOTIFICATION_Y := Round((596 / 1080) * screenHeight)

CLAIM_BUTTON_X := Round((1381 / 1920) * screenWidth)
CLAIM_BUTTON_Y := Round((933 / 1080) * screenHeight)

X_BUTTON_X := Round((1202 / 1920) * screenWidth)
X_BUTTON_Y := Round((672 / 1080) * screenHeight)

Loop
{
    if FileExist("command.txt")
    {
        command := Trim(FileRead("command.txt"))

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
        else if command = "Walk"
        {
            Lost_City_Walk()
            ClearCommand()
        }
    }

    Sleep 50    ; Added smal delay to reduce CPU busy waiting
}

ClearCommand()
{
    FileOpen("command.txt", "w").Close()
    FileOpen("done.txt", "w").Close()
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
    Click CLAIM_XP_X, CLAIM_XP_Y
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


Lost_City_Walk()
{
    global YES_X, YES_Y
    ;Walk to Auto-Run area
    Sleep 1000
    Send "{w down}"
    Sleep 800
    Send "{w up}"
    Sleep 100

    Send "{d down}"
    Sleep 1430
    Send "{d up}"

    Send "{s down}"
    Sleep 500
    Send "{s up}"
    Sleep 1000

    MouseClick("Left", YES_X, YES_Y)      ;Click Yes
    Sleep 2000
}



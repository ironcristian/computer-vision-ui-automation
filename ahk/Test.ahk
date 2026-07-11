#Requires AutoHotkey v2.0

SendMode "Event"
F8::
{
    ExitApp

}

Lost_City_Walk()
{
    Sleep 5000
    Send "{s down}"
    Sleep 200
    Send "{e down}"
    Sleep 4000
    Send "{Space down}"
    Sleep 50
    Send "{Space up}"
    Sleep 1200
    Send "{s up}"
    Send "{e up}"
    Sleep 2000

    Send "{Right down}"
    Sleep 600
    Send "{Right up}"
    Sleep 200
    Send "{w down}"
    Sleep 1000
    Send "{w up}"



}

Lost_City_Walk()


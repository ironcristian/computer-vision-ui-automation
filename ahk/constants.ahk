#Requires AutoHotkey v2.0


;Primary Screen size
screenWidth := A_ScreenWidth
screenHeight := A_ScreenHeight

; Scaled coordinates
; Got the ratio and multipled by my screen resolution already so i get the coordinates. This will make it such that it works on any resolution#Requires AutoHotkey v2.0


;Close auto-run buttons
CLOSE_X := Round((1294 / 1920) * screenWidth)
CLOSE_Y := Round((796 / 1080) * screenHeight)

YES_X := Round((860 / 1920) * screenWidth) ;YES buttons work for any feature where you can choose yes or no
YES_Y := Round((623 / 1080) * screenHeight)

;Rebirth buttons coordinates
REBIRTH_BUTTON_X := Round((945 / 1920) * screenWidth)
REBIRTH_BUTTON_Y := Round((48 / 1080) * screenHeight)

REBIRTH_PRICE_X := Round((955 / 1920) * screenWidth)
REBIRTH_PRICE_Y := Round((876 / 1080) * screenHeight)



;Claim XP button coordinates
CLAIM_XP_X := Round((869 / 1920) * screenWidth)
CLAIM_XP_Y := Round((978 / 1080) * screenHeight)



;Egg claim buttons
EGG_NOTIFICATION_X := Round((189 / 1920) * screenWidth)
EGG_NOTIFICATION_Y := Round((596 / 1080) * screenHeight)

CLAIM_BUTTON_X := Round((1381 / 1920) * screenWidth)
CLAIM_BUTTON_Y := Round((933 / 1080) * screenHeight)

X_BUTTON_X := Round((1202 / 1920) * screenWidth)
X_BUTTON_Y := Round((672 / 1080) * screenHeight)


;Travel button inside portal traversal menu coordinates
TRAVEL_BUTTON_X := Round((952 / 1920) * screenWidth)
TRAVEL_BUTTON_Y := Round((563 / 1080) * screenHeight)


;Portal zones button coordinates
GREEN_HILL_BUTTON_X := Round((959 / 1920) * screenWidth)
GREEN_HILL_BUTTON_Y := Round((202 / 1080) * screenHeight)

LOST_CITY_BUTTON_X := Round((1216 / 1920) * screenWidth)
LOST_CITY_BUTTON_Y := Round((396 / 1080) * screenHeight)

EMERALD_HILL_BUTTON_X := Round((1119 / 1920) * screenWidth)
EMERALD_HILL_BUTTON_Y := Round((702 / 1080) * screenHeight)

HILL_TOP_BUTTON_X := Round((701 / 1920) * screenWidth)
HILL_TOP_BUTTON_Y := Round((396 / 1080) * screenHeight)


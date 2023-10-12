SetWinDelay, -1
global gui_W:=300, gui_H:=166  
, OPT_STARTUP_FOCUS_TAGS:= true
, TargetFile:= a_args[1]? a_args[1] : "C:\Users\ninj\Desktop11\test.png"

WS_POPUP = 0x80000000
WS_CHILD = 0x40000000


Gui, 1: +LastFound +hWndhGui1 +Owner +AlwaysOnTop +hwndghwnd +0x40000 -0x400000
Gui, 1: Color, 181535
Gui, 1: Font, s11 bold, Segoe UI
 
Parent_ID := WinExist()
Gui, 2: +hwndbumhwnd +e0x2000000
Gui, 2: Font, s10 , Segoe UI
;Gui, 2:margin,1,1
Gui, 2: -Caption +hWndhGui2 +parent1 ;+%WS_CHILD% -%WS_POPUP%
gui, 2: Color, 000000
WinSet, TransColor, 000000, % "ahk_id " hGui2
Gui, 2: Font, s10 , Segoe UI
Gui, 1: Add, Edit, x53 +hwndedTitlewnd y+12 r1 w237 Limit80 vDeviationTitle,PSYCHO515
Gui, 1: Add, Edit, x53 +hwndedDescwnd y54 w237 vDeviationDesc 
Gui, 1: Add, Edit, x53 +hwndedTagswnd y94 w237 vtags,% "Psychosis "
Gui, 2: Add, Text, vtext0 w44 x7 y56 AltSubmit, Desc:  
Gui, 2: Add, Text, vtext1 w44 x7 y96 AltSubmit, Tags:  
gui,1:	Add,Picture,X0 Y0 BackgroundTrans,% "C:\Script\AHK\GDI\images\glass.png"
Gui, 1: Add, Button,% "x" (.5*gui_W-40) " y128 w80 h30  gguiSubmit Default", Submit
Gui, 1: Add, Button,% "x" (.5*gui_W+55) " y128 w80 h30  gcancel Default", Cancel
Gui, 2: +LastFound
Child_ID := WinExist() ;DllCall("SetParent", "uint",  Child_ID, "uint", Parent_ID)
Gui, 2: Add, Text, vtext2 w270 x7 y14 AltSubmit, Title:  
OnMessage(0x6,"col")
Gui, 1: Show,x-300 y-200 w%gui_W% h%gui_H%,no_glass
;Gui, 1: Add, Text, vtext2 w270 x15 y15 AltSubmit, Please enter the Password:
Gui, 2: Show, x0 y0 w300 h135,no_glass
Gui, 1: hide
EnableBlur(ghwnd)
win_move(ghwnd,A_screenwidth*.5-gui_W,A_screenheight*.5-gui_H,"","","")
winset redraw,,ahk_id %bumhwnd%
Gui, 1: show

Win_Animate(ghwnd,"hneg slide",200)
winactivate, ahk_id %ghwnd%
if OPT_STARTUP_FOCUS_TITLE {
	GuiControl,Focus,% edTitlewnd
	SendMessage,0xB1,0,-1,,ahk_id %edTitlewnd% ;EM_SETSEL 177 0xB1
} else if OPT_STARTUP_FOCUS_DESC {
	GuiControl,Focus,% edDescwnd
	SendMessage,0xB1,0,-1,,ahk_id %edDescwnd%
} else if OPT_STARTUP_FOCUS_TAGS {
	GuiControl,Focus,% edTagswnd
	ControlSend,,{end},ahk_id %edTagswnd% 
	; SendMessage,0xB1,0,0,,ahk_id %edTagswnd%
}
onmessage(0x201,"ONLbutton") ;lmb-drag window movement mouse handler
return,

guiescape:
guicancel:
exitapp,
return,

ONLbutton(){
	PostMessage,0xA1,2 ; 0xA1- WM_NCLBUTTONDOWN - Same as dragging window by its title-bar.
}

col() {
	static go:= !false
	go:= winactive(ghwnd)? true : false 
	(go? (col:=181535,col2:="c220040", col3:="c99aafe") :  (col:= 050513, col2:= "c200570", col3:="c6688aff"))
	Gui, 1: Color,%col%
	Gui, 1: Font,%col2%
	Gui, 2: Font,%col3%
	guicontrol,Font,text1
	guicontrol,Font,text2
}

~^rbutton::
mousegetpos,,,win
EnableBlur(win)
 return

guiSubmit:
Gui, 1: Submit, NoHide
charsToReplace:= """,.!/[]()\£$%^&*#"""
loop,parse,% charsToReplace
	tags:= strreplace(tags,a_loopfield,chr(32)) ;replace all undesirables with space
loop.2
	tags:= strreplace(tags,chr(32) . chr(32),chr(32)) ;eliminate all consecutive spaces
tags:= rTrim(tags,chr(32)) ;remove any trailing spaces

upload:
string:= "python.exe " . chr(34) . "C:\Script\Python\DAUpload.py" . chr(34)
string.=  " --title " . chr(34) . "PSYCHO515" . chr(34) . " --artist_comments " . chr(34) . DeviationDesc . chr(34) . " --tags " . tags . " --is_dirty --file " . chr(34) . TargetFile . chr(34)
Gui, 1: Destroy 
;python.exe "C:\Script\Python\DAUpload.py" --title "PSYCHO515" --artist_comments "" --tags psychosis --is_dirty --file "%l"

;msgbox % 
1stoutcome:= RunWait1(string)
if instr(poo,"Bad token: The access token is invalid") {
	string2:= "python.exe " . chr(34) . "C:\Script\Python\DAAuthorization" . chr(34)
;	msgbox % 
	2ndtoutcome:= RunWait1(string2)
	if instr(2ndtoutcome,"Authorization code received") {
		string3:= "python.exe " . chr(34) . "C:\Script\Python\DATokenRetrieval.py" . chr(34)
		;msgbox % "ni out  " poo3:= RunWait1(string3)
		goto,upload
	}
} else {
	; Define the regex needle for an HTTPS URL
	needle := "https:\/\/\S+"

	; Search for the needle in the haystack
	if RegExMatch(1stoutcome, needle, match) {
    url := match
 msgbox,0,% "upload successful",% "upload successful and published to:`n" url,3
}

 }
;} else msgbox,4, upload successful, publish now?

; if msgbox,yes {

; }

; if msgbox,no {
	; ExitApp,
; }

ExitApp,
return,

RunWait1(command) {
	DllCall("AllocConsole")
	WinHide,% "ahk_id " DllCall("GetConsoleWindow","ptr")
	shell:=ComObjCreate("WScript.Shell")
	exec:=shell.Exec(ComSpec " /C " command)
	return,exec.StdOut.ReadAll()
}

EnableBlur(hWnd) {
  ;Function by qwerty12 and jNizM (found on https://autohotkey.com/boards/viewtopic.php?t=18823)

  ;WindowCompositionAttribute
  WCA_ACCENT_POLICY := 19 
 
  ;AccentState
  ACCENT_DISABLED := 0,
  ACCENT_ENABLE_GRADIENT := 1,
  ACCENT_ENABLE_TRANSPARENTGRADIENT := 2,
  ACCENT_ENABLE_BLURBEHIND := 3,
  ACCENT_INVALID_STATE := 4

  accentStructSize := VarSetCapacity(AccentPolicy, 4*4, 0)
  NumPut(ACCENT_ENABLE_BLURBEHIND, AccentPolicy, 0, "UInt")
 
  padding := A_PtrSize == 8 ? 4 : 0
  VarSetCapacity(WindowCompositionAttributeData, 4 + padding + A_PtrSize + 4 + padding)
  NumPut(WCA_ACCENT_POLICY, WindowCompositionAttributeData, 0, "UInt")
  NumPut(&AccentPolicy, WindowCompositionAttributeData, 4 + padding, "Ptr")
  NumPut(accentStructSize, WindowCompositionAttributeData, 4 + padding + A_PtrSize, "UInt")
 
  DllCall("SetWindowCompositionAttribute", "Ptr", hWnd, "Ptr", &WindowCompositionAttributeData)
} 
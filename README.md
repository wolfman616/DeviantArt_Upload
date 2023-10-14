# DeviantArt_Upload
Added mature optional tickbox
requires python 3.7 or greater

requires ahk v1 

![dfdfd](https://github.com/wolfman616/DeviantArt_Upload/assets/62726599/efe1d847-017e-4001-9f4e-9ecb2d416b33)

make a shell menu which invokes the command autohotkey.exe "C:\Script\AHK\z_ConTxt\DA_UPLOAD.ahk" "%l"
or EXE

![image](https://github.com/wolfman616/DeviantArt_Upload/assets/62726599/831344e8-63d3-42ed-9de3-faf20afc29a1)

at the moment these need to be added manually by the user. Copy them from the Applications API page


Computer\HKEY_CURRENT_USER\Software\_MW\deviantartClientSecret
Computer\HKEY_CURRENT_USER\Software\_MW\deviantartClientID

as this screenshot illustrates

![image](https://github.com/wolfman616/DeviantArt_Upload/assets/62726599/295cbd4a-132d-45aa-bcb9-ccd7a97f0cfd)


When invoked, you will see this:
![image](https://github.com/wolfman616/DeviantArt_Upload/assets/62726599/2b17b319-88db-43d7-bbc6-f34baeaf1529)

![image](https://github.com/wolfman616/DeviantArt_Upload/assets/62726599/5ccc4a6e-33dc-421e-9fb1-346c46ba11a1)

It has the ability to initially leave the cursor in whichever field you want it to, I have it set to the tags field as every Deviation I make has the same title usually, but you may prefer something else. see the OPT options like OPT_STARTUP_FOCUS_TITLE, beware only set one to true at a time or it will try and initially highligh mutliple fields which will not work.

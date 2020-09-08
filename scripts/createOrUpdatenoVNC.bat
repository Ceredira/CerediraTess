@ECHO OFF

CHCP 65001

REM \\dpc.tax.nalog.ru\root\GRs\NPK\gr375\DevOpsAT\
SET pathToSecuredShare=\\dpc.tax.nalog.ru\root\GRs\NPK\gr375\DevOpsAT\

REM "uvnc.7z"
SET portablenoVNCArchive=%pathToSecuredShare:"=%\%~1

REM "C:\DevOpsAT\uvnc"
SET pathToInstallnoVNC=%~2

REM "REINSTALL"
SET installType=%~3

REM Добавил все exe-файлы которые могут работать из решения noVNC, но большинства из них в процессах никогда не видел
REM для ускорения времени выполнения, часть файлов закомментирую, при необходимости раскомментировать

REM TASKKILL /F /IM MELT Command Websocket.exe /T
REM TASKKILL /F /IM MELT Command Websocket.vshost.exe /T
REM TASKKILL /F /IM w9xpopen.exe /T
TASKKILL /F /IM websockify.exe /T
REM TASKKILL /F /IM MSLogonACL.exe /T
TASKKILL /F /IM repeater.exe /T
REM TASKKILL /F /IM setcad.exe /T
REM TASKKILL /F /IM setpasswd.exe /T
REM TASKKILL /F /IM testauth.exe /T
REM TASKKILL /F /IM unins000.exe /T
REM TASKKILL /F /IM uvnckeyboardhelper.exe /T
REM TASKKILL /F /IM UVNC_Launch.exe /T
REM TASKKILL /F /IM uvnc_settings.exe /T
TASKKILL /F /IM vncviewer.exe /T
TASKKILL /F /IM winvnc.exe /T

REM Если указана опция REINSTALL, то удалить каталог с текущей версией noVNC, если он существует
IF "%installType%" EQU "REINSTALL" (
    IF EXIST "%pathToInstallnoVNC%\" (
        REM DEL /F /Q /S "%pathToInstallnoVNC%"
        RMDIR /Q /S "%pathToInstallnoVNC%"
    )
)

REM Если опция REINSTALL не указана и исполняемый файл startVNC.bat существует, то считаем что с дистрибутивом все ок!
REM При необходимости, можно добавить более тонкие проверки.
IF EXIST "%pathToInstallnoVNC%\startVNC.bat" (
    ECHO noVNC ALREADY INSTALLED!!!
) ELSE (
    MKDIR "%pathToInstallnoVNC%"
    "%pathToSecuredShare:"=%\7-Zip\7z.exe" x "%portablenoVNCArchive%" -o"%pathToInstallnoVNC%" -y && ECHO noVNC INSTALL PASSED!!!
)

powershell.exe -command "(gc '%pathToInstallnoVNC%\UltraVNC\ultravnc.ini') -replace '###pathTouvnc###', '%pathToInstallnoVNC%\UltraVNC' | Out-File -encoding ASCII '%pathToInstallnoVNC%\UltraVNC\ultravnc.ini'"
REM RUNAS /USER:DPC\n7701_svc_ais2_aft "\"%pathToInstallnoVNC%\startVNC.bat\" \"%pathToInstallnoVNC:\\=\\\\%\""
REM START /B "" cmd.exe /C "%pathToInstallnoVNC%\startVNC.bat" %pathToInstallnoVNC%

SCHTASKS /Create /tn noVNC /tr "%pathToInstallnoVNC%\startVNC.bat %pathToInstallnoVNC% " /sc ONLOGON /f /ru DPC\n7701_svc_ais2_aft && ECHO SERVICE RUN AFTER LOGON!!!
SCHTASKS /Run /TN "noVNC"
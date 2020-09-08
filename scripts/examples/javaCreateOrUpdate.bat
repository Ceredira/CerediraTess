@ECHO OFF

CHCP 65001

REM \\dpc.tax.nalog.ru\root\GRs\NPK\gr375\DevOpsAT\
SET pathToSecuredShare=\\dpc.tax.nalog.ru\root\GRs\NPK\gr375\DevOpsAT\

REM "jdk1.8.0_221.7z"
SET portableJavaArchive=%pathToSecuredShare:"=%\%~1

REM "C:\DevOpsAT\Java\jdk1.8.0_221"
SET pathToInstallJava=%~2

REM "REINSTALL"
SET installType=%~3

REM Убиваем задачи, которые могут быть запущены
REM Добавил все exe-файлы которые могут работать из Java, но большинства из них в процессах никогда не видел
REM для ускорения времени выполнения, часть файлов закомментирую, при необходимости раскомментировать

REM TASKKILL /F /IM jabswitch.exe /T
REM TASKKILL /F /IM java-rmi.exe /T
TASKKILL /F /IM java.exe /T
REM TASKKILL /F /IM javacpl.exe /T
TASKKILL /F /IM javaw.exe /T
TASKKILL /F /IM javaws.exe /T
REM TASKKILL /F /IM jjs.exe /T
REM TASKKILL /F /IM jp2launcher.exe /T
REM TASKKILL /F /IM keytool.exe /T
REM TASKKILL /F /IM kinit.exe /T
REM TASKKILL /F /IM klist.exe /T
REM TASKKILL /F /IM ktab.exe /T
REM TASKKILL /F /IM orbd.exe /T
REM TASKKILL /F /IM pack200.exe /T
REM TASKKILL /F /IM policytool.exe /T
REM TASKKILL /F /IM rmid.exe /T
REM TASKKILL /F /IM rmiregistry.exe /T
REM TASKKILL /F /IM servertool.exe /T
REM TASKKILL /F /IM ssvagent.exe /T
REM TASKKILL /F /IM tnameserv.exe /T
REM TASKKILL /F /IM unpack200.exe /T

REM Если указана опция REINSTALL, то удалить каталог с текущей версией Java, если он существует
IF "%installType%" EQU "REINSTALL" (
    IF EXIST "%pathToInstallJava%\" (
        REM DEL /F /Q /S "%pathToInstallJava%"
        RMDIR /Q /S "%pathToInstallJava%"
    )
)

REM Если опция REINSTALL не указана и исполняемый файл java.exe существует, то считаем что с дистрибутивом все ок!
REM При необходимости, можно добавить более тонкие проверки.
IF EXIST "%pathToInstallJava%\bin\java.exe" (
    ECHO JAVA ALREADY INSTALLED!!!
) ELSE (
    MKDIR "%pathToInstallJava%"
    "%pathToSecuredShare:"=%\7-Zip\7z.exe" x "%portableJavaArchive%" -o"%pathToInstallJava%" -y && ECHO JAVA INSTALL PASSED!!!
)

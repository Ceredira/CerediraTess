@ECHO OFF

SETLOCAL enableDelayedExpansion

REM Изменить кодировку консоли на UTF-8
CHCP 65001

REM Боевые параметры приходят на вход при вызове скрипта
REM Имя или ip-адрес хоста для выполнения автотеста
SET host=%~1

SET pathToJavaHome=%~2

REM "C:\DevOpsAT\apache-maven-3.6.2" от которого строится путь \bin\mvn.cmd
SET pathToMavenInstallDir=%~3

SET pathToMavenRepository=%~4

REM "C:\DevOpsAT\AutomationTestingNalogTests"
SET testsPath=%~5

REM "--tags @dev" или любой другой вариант запуска теста используя синтаксис cucumber
SET tests=%~6

SET testStand=%~7

SET influx_enabled=%~8

SET jenkinsBuildUrl=%~9

SHIFT /1
SET runType=%~9

TITLE TEST RUNNING %host%
REM Убить все запущенные автотесты, кроме текущего
TASKKILL /FI "WINDOWTITLE EQ TEST RUNNING*" /FI "WINDOWTITLE NE TEST RUNNING %host%" /IM cmd.exe /F /T

SET logFilePath=D:\Temp\DevOpsAT\logs\%random%%random%%random%%random%%random%%random%.txt


REM Получить имя пользователя, под которым запущен сервис WSWA
REM FOR /F "usebackq" %%i IN (`whoami`) DO SET domainAndUsername=%%i
REM Необходимо указать пароль пользователя, потому что без него, хоть сервис и запускается от имени того же самого пользователя,
REM но есть лаги GUI приложения браузера, из-за которых тесты не идут, и браузер нормально не отображается
REM SET password=here is pass

FOR /F "tokens=* USEBACKQ" %%f IN (`%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe -command "$pathToSecuredShare='\\dpc.tax.nalog.ru\root\GRs\NPK\gr375\creds\' + '%testStand%'; $userRole='service_user'; $AESKey = [System.IO.File]::ReadAllBytes($pathToSecuredShare + '\hash.info'); $login = ConvertTo-SecureString -String ( Get-Content $($pathToSecuredShare + '\' + $userRole + '.login.cypher') ) -Key $AESKey; $BSTR=[System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($login) ; [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)" `) DO ( SET domainAndUsername=%%f )

FOR /F "tokens=* USEBACKQ" %%f IN (`%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe -command "$pathToSecuredShare='\\dpc.tax.nalog.ru\root\GRs\NPK\gr375\creds\' + '%testStand%'; $userRole='service_user'; $AESKey = [System.IO.File]::ReadAllBytes($pathToSecuredShare + '\hash.info'); $password = ConvertTo-SecureString -String ( Get-Content $($pathToSecuredShare + '\' + $userRole + '.password.cypher') ) -Key $AESKey; $BSTR=[System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password) ; [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)" `) DO ( SET password=%%f )

REM Для открытия RDP-сесси без ввода пароля
CMDKEY /add:%host% /user:%domainAndUsername% /pass:%password%


SET RUN_MSTSC_RETRY_COUNT=0

:RUN_MSTSC

REM Перед попыткой запустить новый RDP убить старый, если остался.
call %~dp0\mstscConnectionClose.bat %host%

REM Открыть RDP сессию к удаленной машине
REM Можно использовать только PsExec, если использовать cmd /C или start /B mstsc не возвращает управление в консоль, пока не завершится процессс mstsc
REM cmdkey /add:vm-autotst-psz2.rosenergo.com /user:ats\g.dzhamalov /pass:123456789
%~dp0\psexec.exe -d CMD.exe /C START "MSTSC %host%" /MIN /B MSTSC /v:%host% /w:1920 /h:1080 /noConsentPrompt ^&EXIT
REM CMD.EXE /C START /MIN "MSTSC %host%" MSTSC /v:%host% /w:1920 /h:1080 /noConsentPrompt ^&EXIT

SET CHECK_USER_LOGGED_RETRY_COUNT=0

REM Маркер для организации цикла
:CHECK_USER_LOGGED

REM Цикл ожидания создания сессии RDP на удаленном хосте
FOR /f "skip=1 tokens=1-4" %%a IN ('QUERY SESSION /SERVER:%host% %username%') DO (
    REM Если в строке подключения есть сессия RDP - можно выполнять тест
    ECHO %%a | FINDSTR /C:"rdp-tcp" 1>nul

    REM Если сессии RDP нет
    IF ERRORLEVEL 1 (
        ECHO "No logged in session. Waiting for login."
        REM Ожидание в 5 секунд до следующей проверки
        PING -n 5 127.0.0.1 > NUL
        REM Переход на метку для организации цикла
        IF %CHECK_USER_LOGGED_RETRY_COUNT% LEQ 5 (
            SET /a "CHECK_USER_LOGGED_RETRY_COUNT=%CHECK_USER_LOGGED_RETRY_COUNT%+1"
            GOTO :CHECK_USER_LOGGED
        ) ELSE (
            IF %RUN_MSTSC_RETRY_COUNT% LEQ 3 (
                SET /a "RUN_MSTSC_RETRY_COUNT=%RUN_MSTSC_RETRY_COUNT%+1"
                GOTO :RUN_MSTSC
            ) ELSE (
                ECHO FAILED CONNECT TO %host% BY RDP
                GOTO EXITL
            )
        )
    ) ELSE (
        ECHO Get logged in session id %%c

        ECHO Running test on host %host% with command
        ECHO "nalogTestRun.bat" "%pathToJavaHome%" "%pathToMavenInstallDir%" "%pathToMavenRepository%" "%testsPath%" "%tests%" "%logFilePath%" "%testStand%" "%influx_enabled%" "%jenkinsBuildUrl%" "%runType%"

        REM Запускаем тест на удаленном хосте
        REM Параметры -u и -p нужны обязательно в случае запуска GUI приложения на удаленной машине
        REM runas /user:%domainAndUsername% /savecred "%~dp0\PsExec.exe \\%host% -i %%c -h -f -c %~dp0\nalogTestRun.bat \"%pathToJavaHome%\" \"%pathToMavenInstallDir%\" \"%pathToMavenRepository%\" \"%testsPath%\" \"%tests%\" \"%logFilePath%\" \"%testStand%\" \"%influx_enabled%\" \"%jenkinsBuildUrl%\""
        REM %~dp0\PsExec.exe \\%host% -u %domainAndUsername% -i %%c -h -f -c %~dp0\nalogTestRun.bat "%pathToJavaHome%" "%pathToMavenInstallDir%" "%pathToMavenRepository%" "%testsPath%" "%tests%" "%logFilePath%" "%testStand%" "%influx_enabled%" "%jenkinsBuildUrl%"
        %~dp0\PsExec.exe \\%host% -u %domainAndUsername% -p %password% -i %%c -h -f -c %~dp0\nalogTestRun.bat "%pathToJavaHome%" "%pathToMavenInstallDir%" "%pathToMavenRepository%" "%testsPath%" "%tests%" "%logFilePath%" "%testStand%" "%influx_enabled%" "%jenkinsBuildUrl%" "%runType%"

        REM %~dp0\PsExec.exe \\%host% CMD.EXE /C "TYPE %logFilePath% && DEL /Q /F %logFilePath%"
        REM Решение проблемы с выводом содержимого файла с кодировкой cp1251
        %~dp0\PsExec.exe \\%host% powershell.exe "Get-Content -Path '%logFilePath%' -ReadCount 50 | foreach { $_; Start-Sleep -milliseconds 100 }; Remove-Item -Force -Path %logFilePath%;"

        REM После завершения выполнения теста, закрыть сессию RDP
        %~dp0\mstscConnectionClose.bat %host%
    )
)
:EXITL
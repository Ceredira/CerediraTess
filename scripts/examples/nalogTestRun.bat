@ECHO OFF

CHCP 65001

TITLE TEST RUNNING %logFilePath%

SET pathToJavaHome=%~1

REM "C:\DevOpsAT\apache-maven-3.6.2" от которого строится путь \bin\mvn.cmd
SET pathToMavenInstallDir=%~2

SET pathToMavenRepository=%~3

REM "C:\DevOpsAT\AutomationTestingNalogTests"
SET testsPath=%~4

REM "--tags @dev" или любой другой вариант запуска теста используя синтаксис cucumber
SET tests=%~5

SET logFilePath=%~6

SET testStand=%~7

SET influx_enabled=%~8

SET jenkinsBuildUrl=%~9

REM В cmd.exe нельзя прочитать %10 %11 и далее параметры, для этого нужно делать сдвиг
REM всех параметров на 1, и тогда 10 параметр можно будет получить используя %9
SHIFT /1
SET runType=%~9

REM Перейти в каталог с проектом автотестов
ECHO "%testsPath%"
CD /D "%testsPath%"

SET JAVA_HOME=%pathToJavaHome%
SET BUILD_URL=%jenkinsBuildUrl%

REM Создать каталог для вывода логов
FOR %%a IN ("%logFilePath%") DO SET "logsParentDir=%%~dpa"
IF NOT EXIST "%logsParentDir%" (
    MKDIR "%logsParentDir%"
)

SCHTASKS /Create /tn noScreenLock /tr "reg.exe add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI\SessionData /t REG_DWORD /v AllowLockScreen /d 0 /f" /sc ONLOGON /f /ru DPC\n7701_svc_ais2_aft
SCHTASKS /Run /TN "noScreenLock"

REM Убить все запущенные автотесты, кроме текущего
TASKKILL /FI "WINDOWTITLE EQ TEST RUNNING*" /FI "WINDOWTITLE NE TEST RUNNING %logFilePath%" /IM cmd.exe /F /T
REM Убить процессы, которые зависли, потому что кто-то кликнул в них и они перешли в режим выделения и зависли
TASKKILL /FI "WINDOWTITLE EQ Select Administrator:  TEST RUNNING *" /FI "WINDOWTITLE NE TEST RUNNING %logFilePath%" /IM cmd.exe /F /T > NUL
TASKKILL /FI "WINDOWTITLE EQ Select TEST RUNNING*" /FI "WINDOWTITLE NE TEST RUNNING %logFilePath%" /IM cmd.exe /F /T > NUL

REM Если будут нужные Java процессы убиваться, то заменить на фильтрацию по commandLine и т.п.
TASKKILL /F /IM java.exe /T
TASKKILL /F /IM iexplore.exe /T
TASKKILL /F /IM chromedriver.exe /T

REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Internet Explorer\Main" /v DisableFirstRunCustomize /t REG_DWORD /d 1 /f

IF EXIST "%testsPath%\target" (
    DEL /F /S /Q "%testsPath%\target"
)

REM Запустить автотест для выполнения
"%pathToMavenInstallDir%\bin\mvn.cmd" "-Dmaven.repo.local=%pathToMavenRepository%\repository" clean -U test "-Dcucumber.options=%tests%" "-DtestStand=%testStand%" "-Dinflux.enabled=%influx_enabled%" "-DrunType=%runType%" "-DCREDS_PATH=\\dpc.tax.nalog.ru\root\GRs\NPK\gr375\creds\%testStand%" 1>>"%logFilePath%" 2>&1

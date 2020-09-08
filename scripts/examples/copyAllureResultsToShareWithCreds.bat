@ECHO OFF
CHCP 65001

SET host=%~1

REM Путь до директории с тестами, например
REM C:\DevOpsAT\AutomationTestingNalogTests
SET pathToTestsRoot=%~2

REM Путь до шары на Jenkins, куда класть результаты, чтобы сгенерировался Allure отчет
REM Например, \\vm-jenkins-1c\users\Jenkins\.jenkins\workspace\DevOpsAT\AISNalog3\Nalog_Full_Pipeline_For_Automation_Testing
SET pathToJenkinsShare=%~3

SET testStand=%~4

REM Получить имя пользователя, под которым запущен сервис WSWA
REM FOR /F "usebackq" %%i IN (`whoami`) DO SET domainAndUsername=%%i
REM Необходимо указать пароль пользователя, потому что без него, хоть сервис и запускается от имени того же самого пользователя,
REM но есть проблема при подключении к удаленным ресурсам
REM SET password=here is pass

FOR /F "tokens=* USEBACKQ" %%f IN (`%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe -command "$pathToSecuredShare='\\dpc.tax.nalog.ru\root\GRs\NPK\gr375\creds\' + '%testStand%'; $userRole='service_user'; $AESKey = [System.IO.File]::ReadAllBytes($pathToSecuredShare + '\hash.info'); $login = ConvertTo-SecureString -String ( Get-Content $($pathToSecuredShare + '\' + $userRole + '.login.cypher') ) -Key $AESKey; $BSTR=[System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($login) ; [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)" `) DO ( SET domainAndUsername=%%f )

FOR /F "tokens=* USEBACKQ" %%f IN (`%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe -command "$pathToSecuredShare='\\dpc.tax.nalog.ru\root\GRs\NPK\gr375\creds\' + '%testStand%'; $userRole='service_user'; $AESKey = [System.IO.File]::ReadAllBytes($pathToSecuredShare + '\hash.info'); $password = ConvertTo-SecureString -String ( Get-Content $($pathToSecuredShare + '\' + $userRole + '.password.cypher') ) -Key $AESKey; $BSTR=[System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password) ; [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)" `) DO ( SET password=%%f )

%~dp0\PsExec.exe \\%host% -u %domainAndUsername% -p %password% -h -f -C %~dp0\copyAllureResultsToShare.bat "%pathToTestsRoot%" "%pathToJenkinsShare:\\=\%"
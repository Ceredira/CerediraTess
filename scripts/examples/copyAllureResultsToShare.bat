@ECHO OFF
CHCP 65001

ECHO Копирование результатов запуска тестов для генерации отчета Allure

REM Путь до директории с тестами, например
REM C:\DevOpsAT\AutomationTestingNalogTests
SET pathToTestsRoot=%~1

REM Путь до шары на Jenkins, куда класть результаты, чтобы сгенерировался Allure отчет
REM Например, \\vm-jenkins-1c\users\Jenkins\.jenkins\workspace\DevOpsAT\AISNalog3\Nalog_Full_Pipeline_For_Automation_Testing
SET pathToJenkinsShare=%~2

REM /F – выводить полные имена копируемых файлов
REM /Y - автоматически подтверждать создание отсутствующих каталогов
ECHO Копирование результатов...
XCOPY /F /Y /E /R "%pathToTestsRoot%\target\allure-results\*" "%pathToJenkinsShare%\allure-results\"
REM XCOPY /F /Y /S /H "%pathToTestsRoot%\target\surefire-reports\*" "%pathToJenkinsShare%\surefire-reports\"
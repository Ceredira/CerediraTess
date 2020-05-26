@ECHO OFF
CHCP 65001

REM SCRIPT DESCRIPTION: Скрипт для установки клиента Git
REM SCRIPT DESCRIPTION: Пример запуска: йцу

REM Путь к репозиторию ПО
REM \\rrr\root\GRs\NPK\gr375\DevOpsAT\
SET pathToSecuredShare=\\rrr\root\GRs\NPK\gr375\DevOpsAT\


REM ARG DESCRIPTION: Название архива, содержащего пакет Git для установки
REM ARG EXAMPLE: Git-2.23.2.7z
SET portableGitArchive=%pathToSecuredShare:"=%\%~1

REM ARG DESCRIPTION: Путь установки клиента Git
REM ARG EXAMPLE: C:\DevOpsAT\Git-2.23.2\
SET pathToInstallGit=%~2
ECHO %pathToInstallGit%

REM "REINSTALL"
SET installType=%~3

REM Убиваем задачи, которые могут быть запущены
TASKKILL /F /IM bash.exe /T
TASKKILL /F /IM git.exe /T
TASKKILL /F /IM sh.exe /T


REM CHECKING [ "1", "2"]
REM CHECKING [ "3" ]
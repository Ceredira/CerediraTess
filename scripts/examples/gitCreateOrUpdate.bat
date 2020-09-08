@ECHO OFF
CHCP 65001

REM SCRIPT DESCRIPTION: Скрипт для установки клиента Git
REM SCRIPT DESCRIPTION: Пример запуска: йцу

REM "Git-2.23.2.7z"
REM PARAM DESCRIPTION: Название архива, содержащего пакет Git для установки
REM PARAM EXAMPLE: Git-2.23.2.7z
SET portableGitArchive=%pathToSecuredShare:"=%\%~1

REM "C:\DevOpsAT\Git-2.23.2\"
SET pathToInstallGit=%~2

REM "REINSTALL"
SET installType=%~3

REM Убиваем задачи, которые могут быть запущены
TASKKILL /F /IM bash.exe /T
TASKKILL /F /IM git.exe /T
TASKKILL /F /IM sh.exe /T

REM Если указана опция REINSTALL, то удалить каталог с текущей версией Git, если он существует
IF "%installType%" EQU "REINSTALL" (
    IF EXIST "%pathToInstallGit%\" (
        REM DEL /F /Q /S "%pathToInstallGit%"
        RMDIR /Q /S "%pathToInstallGit%"
    )
)

REM Если опция REINSTALL не указана и исполняемый файл git.exe существует, то считаем что с дистрибутивом все ок!
REM При необходимости, можно добавить более тонкие проверки.
IF EXIST "%pathToInstallGit%\bin\git.exe" (
    ECHO GIT ALREADY INSTALLED!!!
) ELSE (
    MKDIR "%pathToInstallGit%"
    "%pathToSecuredShare:"=%\7-Zip\7z.exe" x "%portableGitArchive%" -o"%pathToInstallGit%" -y && ECHO GIT INSTALL PASSED!!!
)

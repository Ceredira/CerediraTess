@ECHO OFF
REM Отключить вывод выполняемых команд

ECHO Изменить кодировку на UTF-8
CHCP 65001

REM Объявление глобальных переменных

REM Путь к репозиторию с дистрибутивами
REM \\192.168.1.5\share
SET pathToSecuredShare=\\192.168.1.5\share


REM SCRIPT DESCRIPTION: Скрипт для установки клиента Git
REM SCRIPT DESCRIPTION: Пример запуска: createOrUpdateGit.bat "PortableGit.7z" "C:\DevOpsAT\Git\"


ECHO.
ECHO Аргументы запуска:

REM ARG DESCRIPTION: Название архива, содержащего пакет Git для установки
REM ARG EXAMPLE: PortableGit.7z
SET portableGitArchive=%pathToSecuredShare:"=%\%~1
ECHO Название архива с дистрибутивом: %portableGitArchive%

REM ARG DESCRIPTION: Путь установки клиента Git
REM ARG EXAMPLE: C:\DevOpsAT\Git\
SET pathToInstallGit=%~2
ECHO Путь установки клиента Git: %pathToInstallGit%

REM ARG DESCRIPTION: Тип установки, если REINSTALL, то удалит существующую сборку и установит заново
REM ARG EXAMPLE: REINSTALL
SET installType=%~3
ECHO Тип установки: %installType%

ECHO.
ECHO Завершение программ, мешающих установке.
ECHO Если выводится ошибка not found, значит программа не запущена - это не ошибка.
TASKKILL /F /IM bash.exe /T
TASKKILL /F /IM git.exe /T
TASKKILL /F /IM sh.exe /T

ECHO.
ECHO Если указана опция REINSTALL, то удалить каталог с текущей версией Git, если он существует
IF "%installType%" EQU "REINSTALL" (
    IF EXIST "%pathToInstallGit%\" (
        ECHO Удаление каталога %pathToInstallGit%
        RMDIR /Q /S "%pathToInstallGit%"
    ) ELSE (
        ECHO Каталог %pathToInstallGit% уже удален
    )
)

ECHO.
ECHO Если исполняемый файл %pathToInstallGit%\bin\git.exe существует, то считаем что с дистрибутив уже установлен!
REM При необходимости, можно добавить более тонкие проверки.
IF EXIST "%pathToInstallGit%\bin\git.exe" (
    ECHO GIT ALREADY INSTALLED!!!
) ELSE (
    MKDIR "%pathToInstallGit%"
    ECHO Распаковка дистрибутива %portableGitArchive% в каталог %pathToInstallGit%
    "%pathToSecuredShare:"=%\7-Zip\7z.exe" x "%portableGitArchive%" -o"%pathToInstallGit%" -y && ECHO GIT INSTALL PASSED!!!
)

REM SCRIPT CHECKING: GIT INSTALL PASSED!!! || GIT ALREADY INSTALLED!!!
@ECHO OFF
REM Отключить вывод выполняемых команд

ECHO Изменить кодировку на UTF-8
CHCP 65001

REM Объявление глобальных переменных

REM Путь к репозиторию с дистрибутивами
REM \\192.168.1.5\share
SET pathToSecuredShare=\\192.168.1.5\share


REM SCRIPT DESCRIPTION: Скрипт для установки клиента Maven
REM SCRIPT DESCRIPTION: Пример запуска: createOrUpdateMaven.bat "Maven.7z" "C:\DevOpsAT\Maven\"


ECHO.
ECHO Аргументы запуска:

REM ARG DESCRIPTION: Название архива, содержащего пакет Maven для установки
REM ARG EXAMPLE: Maven.7z
SET portableMavenArchive=%pathToSecuredShare:"=%\%~1
ECHO Название архива с дистрибутивом: %portableMavenArchive%

REM ARG DESCRIPTION: Путь установки клиента Maven
REM ARG EXAMPLE: C:\DevOpsAT\Maven\
SET pathToInstallMaven=%~2
ECHO Путь установки клиента Git: %pathToInstallMaven%

REM ARG DESCRIPTION: Тип установки, если REINSTALL, то удалит существующую сборку и установит заново
REM ARG EXAMPLE: REINSTALL
SET installType=%~3
ECHO Тип установки: %installType%

ECHO.
ECHO Если указана опция REINSTALL, то удалить каталог с текущей версией Maven, если он существует
IF "%installType%" EQU "REINSTALL" (
    IF EXIST "%pathToInstallMaven%\" (
        ECHO Удаление каталога %pathToInstallMaven%
        RMDIR /Q /S "%pathToInstallMaven%"
    ) ELSE (
        ECHO Каталог %pathToInstallMaven% уже удален
    )
)

ECHO.
ECHO Если исполняемый файл bin\mvn.cmd существует, то считаем что с дистрибутивом все ок!
REM При необходимости, можно добавить более тонкие проверки.
IF EXIST "%pathToInstallMaven%\bin\mvn.cmd" (
    ECHO MAVEN ALREADY INSTALLED!!!
) ELSE (
    MKDIR "%pathToInstallMaven%"
    ECHO Распаковка дистрибутива %portableMavenArchive% в каталог %pathToInstallMaven%
	"%pathToSecuredShare:"=%\7-Zip\7z.exe" x "%portableMavenArchive%" -o"%pathToInstallMaven%" -y && ECHO MAVEN INSTALL PASSED!!!
)

REM SCRIPT CHECKING: MAVEN INSTALL PASSED!!! || MAVEN ALREADY INSTALLED!!!
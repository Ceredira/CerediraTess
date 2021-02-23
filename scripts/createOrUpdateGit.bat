@echo off
rem Отключить вывод выполняемых команд

echo Изменить кодировку на UTF-8
chcp 65001

rem Объявление глобальных переменных

rem Путь к репозиторию с дистрибутивами
rem \\192.168.1.5\share
set pathToSecuredShare=\\192.168.1.5\share


rem script description: Скрипт для установки клиента Git
rem script description: Пример запуска: createOrUpdateGit.bat "PortableGit.7z" "C:\DevOpsAT\Git\"


echo.
echo Аргументы запуска:

rem arg description: Название архива, содержащего пакет Git для установки
rem arg example: PortableGit.7z
set portableGitArchive=%pathToSecuredShare:"=%\%~1
echo Название архива с дистрибутивом: %portableGitArchive%

rem arg description: Путь установки клиента Git
rem arg example: C:\DevOpsAT\Git\
set pathToInstallGit=%~2
echo Путь установки клиента Git: %pathToInstallGit%

rem arg description: Тип установки, если reinstall, то удалит существующую сборку и установит заново
rem arg example: reinstall
set installType=%~3
echo Тип установки: %installType%

echo.
echo Завершение программ, мешающих установке.
echo Если выводится ошибка not found, значит программа не запущена - это не ошибка.
taskkill /f /im bash.exe /t
taskkill /f /im git.exe /t
taskkill /f /im sh.exe /t

echo.
echo Если указана опция reinstall, то удалить каталог с текущей версией Git, если он существует
if "%installType%" equ "reinstall" (
    if exist "%pathToInstallGit%\" (
        echo Удаление каталога %pathToInstallGit%
        rmdir /q /s "%pathToInstallGit%"
    ) else (
        echo Каталог %pathToInstallGit% уже удален
    )
)

echo.
echo Если исполняемый файл %pathToInstallGit%\bin\git.exe существует, то считаем что с дистрибутив уже установлен!
rem При необходимости, можно добавить более тонкие проверки.
if exist "%pathToInstallGit%\bin\git.exe" (
    echo GIT ALREADY INSTALLED!!!
) else (
    mkdir "%pathToInstallGit%"
    echo Распаковка дистрибутива %portableGitArchive% в каталог %pathToInstallGit%
    "%pathToSecuredShare:"=%\7-Zip\7z.exe" x "%portableGitArchive%" -o"%pathToInstallGit%" -y && echo GIT INSTALL PASSED!!!
)

rem script checking: GIT INSTALL PASSED!!! || GIT ALREADY INSTALLED!!!
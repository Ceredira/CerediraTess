@ECHO OFF
CHCP 65001

ECHO Скрипт установки дистрибутива АИС Налог 3

REM Путь к каталогу, в котором будет лежать архив для установки
REM \\dpc.tax.nalog.ru\root\GRs\NPK\gr375\DevOpsAT\
SET pathToSecuredShare=\\dpc.tax.nalog.ru\root\GRs\NPK\gr375\DevOpsAT\

REM Имя архива дистрибутива для установки, можно любые архивы,
REM которые может распаковать 7Zip, также можно указать
REM каталог\имя_архива
REM "AISNalog3\Client_pp_19.10.9.1.7z"
SET aisNalog3InstallatorArchive=%pathToSecuredShare:"=%\%~1

REM Путь к каталогу распаковки дистрибутива на агенте
REM Тут можно не использовать в пути имя версии, а указать
REM каталог, например C:\Temp и опцию REINSTALL, таким образом
REM избежать складирования дистрибутивов на машине
REM "C:\DevOpsAT\AISNalog3\Client_pp_19.10.9.1"
SET pathToUnpackAisNalog3=%~2

REM Если указать опцию REINSTALL, то на агенте при обнаружении в
REM каталоге распаковке дистрибутива, будет производится его удаление
REM и повторная распаковка из архива, при любом другом значении,
REM будет использоваться дистрибутив, который будет обнаружен в целевом
REM каталоге
REM "REINSTALL"
SET installType=%~3

REM Окружение установки ppk или kpe
REM Если пустое значение, то скрипт завершит выполнение с ошибкой,
REM если любое значение, кроме kpe, то будет использоваться ppk
SET stand=%~4

REM Проверка, что переменная stand указана
IF "%stand%" == "" (
    ECHO Не указано название стенда для установки, нужно указать первым параметром kpe или ppk
    EXIT /B
)

REM В зависимости от стенда, установить пути к каталогу установки
REM и пути к ключам установки в реестре для разной битности ОС
IF "%stand%" == "kpe" (
    SET reg64Path=HKEY_LOCAL_MACHINE\Software\Wow6432Node\Ais3Prom\Client\Setup
    SET reg86Path=HKEY_LOCAL_MACHINE\Software\Ais3Prom\Client\Setup
    SET "diskPath=C:\Program Files (x86)\Ais3Prom\"
) ELSE (
    SET reg64Path=HKEY_LOCAL_MACHINE\Software\WOW6432Node\Ais3Pp\Client\Setup
    SET reg86Path=HKEY_LOCAL_MACHINE\Software\Ais3PP\Client\Setup
    SET "diskPath=C:\Program Files (x86)\Ais3PredProm\"
)

ECHO Убить все приложения, которые могут быть запущены из каталога установки,
ECHO и которые могут помешать процессу установки, если приложение не найдено
ECHO будет распечатываться ошибка - что является штатной ситуацией
TASKKILL /F /IM CommonComponents.Catalog.IndexationUtility.exe /T
TASKKILL /F /IM CommonComponents.Catalog.InstallationUtility.exe /T
TASKKILL /F /IM CommonComponents.Distribution.DeploymentAgent.exe /T
TASKKILL /F /IM CommonComponents.UnifiedClient.exe /T
TASKKILL /F /IM Common.Agent.exe /T
TASKKILL /F /IM Coral.Anemon.Profiling.Transport.exe /T
TASKKILL /F /IM CommonComponents.UserAgent.exe /T
TASKKILL /F /IM ARJ32.EXE /T
TASKKILL /F /IM ReportViewer.exe /T
TASKKILL /F /IM DNP.Host.Executor.exe /T

IF EXIST "%diskPath%" (
    ECHO Удаление содержимого каталога "%diskPath%"
    RMDIR /Q /S "%diskPath%"
)

REM Если указана опция REINSTALL, то удалить каталог с текущей версией инсталлятора, если он существует
IF "%installType%" EQU "REINSTALL" (
    ECHO Указана опция REINSTALL
    IF EXIST "%pathToUnpackAisNalog3%\" (
        ECHO Удаление каталога "%pathToUnpackAisNalog3%"
        RMDIR /Q /S "%pathToUnpackAisNalog3%"
    )
)

REM Если опция REINSTALL не указана и исполняемый файл git.exe существует, то считаем что с дистрибутивом все ок!
REM При необходимости, можно добавить более тонкие проверки.
IF NOT EXIST "%pathToUnpackAisNalog3%\Ais3Client.msi" (
    ECHO Создание каталога "%pathToUnpackAisNalog3%"
    MKDIR "%pathToUnpackAisNalog3%"
    ECHO Распаковка архива "%aisNalog3InstallatorArchive%" в каталог "%pathToUnpackAisNalog3%"
    "%pathToSecuredShare:"=%\7-Zip\7z.exe" x "%aisNalog3InstallatorArchive%" -o"%pathToUnpackAisNalog3%" -y
)

ECHO Начало процесса установки АИС Налог 3, ничего не нажимайте
ECHO и дождитесь появления сообщения INSTALL SUCCESS...
MSIEXEC /i %pathToUnpackAisNalog3%\Ais3Client.msi /qn /passive /L*V %TMP%\install.log && ECHO INSTALL SUCCESS!!!

REM Часто, установка АИС Налог 3 завершается с кодом 1603, что является допустимым,
REM поэтому подавляем вывод этой ошибки и успешно завершаемся, в противном случае,
REM распечатываем код ошибки
IF "%ERRORLEVEL%" == "1603" (
    ECHO Ошибка которую можно будет пропустить 1603.
    EXIT /B 0
) ELSE (
    IF "%ERRORLEVEL%" == "0" (
        EXIT /B
    ) ELSE (
        ECHO Произошло необработанное исключение с кодом %ERRORLEVEL%
        EXIT /B %ERRORLEVEL%
    )
)
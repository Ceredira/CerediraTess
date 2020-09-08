@ECHO OFF
CHCP 65001

ECHO Скрипт удаления дистрибутива АИС Налог 3

REM Окружение установки ppk или kpe
REM Если пустое значение, то скрипт завершит выполнение с ошибкой,
REM если любое значение, кроме kpe, то будет использоваться ppk
SET stand=%~1

REM Если указать путь до дистрибутива, то удаление можно произвести
REM используя его, но лучше пользоваться вариантом удаления по коду
REM из реестра
REM Путь до файла Ais3Client.msi
SET distribPath=%~2

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

REM Если путь к дистрибутиву не указан
IF "%distribPath%" == "" (
    ECHO Путь к файлу установки АИС Налог 3 не указан. Будет использоваться версия установленной системы из реестра.
    FOR /F "tokens=2* skip=2" %%a IN ('REG QUERY "%reg64Path%" /v "ProductCode"') DO (
        ECHO GUID установленного продукта %%b
        ECHO Начало процесса удаления дистрибутива, ничего не нажимайте и дождитесь
        ECHO появления сообщения UNINSTALL SUCCESS...
        MSIEXEC /x "%%b" /qn /passive /L*V %TMP%\uninstall.log && ECHO UNINSTALL SUCCESS!!!
        GOTO :END
    )

    IF ERRORLEVEL 1 (
        ECHO Не найден ключ в реестре, попытка поиска в x86 версии продукта.

        FOR /F "tokens=2* skip=2" %%a IN ('REG QUERY "%reg86Path%" /v "ProductCode"') DO (
            ECHO GUID установленного продукта %%b
            MSIEXEC /x "%%b" /qn /passive /L*V %TMP%\uninstall.log && ECHO UNINSTALL SUCCESS!!!
            GOTO :END
        )

        IF ERRORLEVEL 1 (
            ECHO x86 версия продукта не обнаружена, удалять нечего.
            ECHO UNINSTALL SUCCESS!!!
        )
    )
) ELSE (
    ECHO Начало процесса удаления дистрибутива, ничего не нажимайте и дождитесь
    ECHO появления сообщения UNINSTALL SUCCESS...
    MSIEXEC /x "%distribPath%\Ais3Client.msi" /qn /passive /L*V %TMP%\uninstall.log && ECHO UNINSTALL SUCCESS!!!
    GOTO :END
)

:END

REM Если при удалении вернулась ошибка 1605, значит продукт уже удален,
REM подавляем вывод ошибки и пишем что все хорошо, в случае других
REM ошибок, возвращаем код ошибки
IF "%ERRORLEVEL%" == "1605" (
    ECHO Продукт уже удален. UNINSTALL SUCCESS!!!
    ECHO Удаление содержимого каталога "%diskPath%"
    IF EXIST "%diskPath%" (
        DEL /F /Q "%diskPath%*"
    )
    EXIT /B
) ELSE (
    IF "%ERRORLEVEL%" == "0" (
        EXIT /B
    ) ELSE (
        ECHO Произошло необработанное исключение с кодом %ERRORLEVEL%
        EXIT /B %ERRORLEVEL%
    )
)
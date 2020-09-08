@ECHO OFF
CHCP 65001

ECHO Версия системы установки 1.0

REM SET distrRoot=%~1
SET distrRoot=\\dpc.tax.nalog.ru\root\GRs\NPK\gr375\DevOpsAT

REM SET destinationPath=%~2
SET destinationPath=C:\Temp\DevOpsAT\

MKDIR %destinationPath%

SET installAll=n
SET installGIT=n
SET installTESTS=n
SET installMAVENCACHE=n
SET installJAVA=n
SET installIDEA=n
SET installIDEASETTINGS=n
SET autorunIDEA=n

ECHO Добро пожаловать в систему установки среды автоматизации тестирования АИС Налог 3

IF NOT "%PROCESSOR_ARCHITECTURE%" == "AMD64" (
    ECHO К сожалению, установка возможна только на операционные системы Microsoft Windows 10 x64, у вас используется не 64 версия ОС.
    EXIT /B
)

SET /P installAll="Установить полный пакет для разработки автотестов АИС Налог 3 (y - Да, все остальное - Нет)? "

IF %installAll%==y (
    SET installGIT=y
    SET installTESTS=y
    SET installMAVENCACHE=y
    SET installJAVA=y
    SET installIDEA=y
    SET installIDEASETTINGS=y
) ELSE (
    SET /P installGIT="Установить клиент GIT (y - Да, все остальное - Нет)? "
    SET /P installJAVA="Установить полный набор Oracle Java Development Kit для возможности разработки и запуска автотестов (y - Да, все остальное - Нет)? "
    SET /P installIDEA="Установить среду разработки JetBrains intelliJIDEA (y - Да, все остальное - Нет)? "
    SET /P installIDEASETTINGS="Установить настройки для среды intelliJIDEA - не придется настраивать самому плагины, открытие проекта и много других вещей (y - Да, все остальное - Нет)? "
    SET /P installTESTS="Развернуть проект автотестов АИС Налог 3 - при запуске автотестов проект откроется сразу (y - Да, все остальное - Нет)? "
    SET /P installMAVENCACHE="Развернуть кеш Maven репозитория - для более быстрого запуска проекта в первый раз (y - Да, все остальное - Нет)? "
)

SET /P autorunIDEA="Запустить среду intelliJIDEA автоматически после установки (y - Да, все остальное - Нет)? "

IF %installGIT%==y (
    "%distrRoot%\7-Zip\7z.exe" x "%distrRoot%\Git-2.23.2.7z" -o"%destinationPath%\Git-2.23.2\" -y && ECHO Клиент Git установлен успешно
)
IF %installJAVA%==y (
    "%distrRoot%\7-Zip\7z.exe" x "%distrRoot%\jdk1.8.0_221.7z" -o"%destinationPath%\Java\jdk1.8.0_221\" -y && ECHO Oracle Java Development Kit установлен успешно
)
IF %installIDEA%==y (
    "%distrRoot%\7-Zip\7z.exe" x "%distrRoot%\IntelliJIDEA_CE_2019.3.3.7z" -o"%destinationPath%\IntelliJIDEA_CE_2019.3.3\" -y && ECHO Среда разработки JetBrains intelliJIDEA установлена успешно
)
IF %installIDEASETTINGS%==y (
    "%distrRoot%\7-Zip\7z.exe" x "%distrRoot%\.IdeaIC2019.3.7z" -o"%destinationPath%\.IdeaIC2019.3\" -y && ECHO Настройки для среды intelliJIDEA установлены успешно
)
IF %installTESTS%==y (
    "%distrRoot%\7-Zip\7z.exe" x "%distrRoot%\AutomationTestingNalogTests.7z" -o"%destinationPath%\AutomationTestingNalogTests\" -y && ECHO Проект автотестов установлен успешно
)
IF %installMAVENCACHE%==y (
    "%distrRoot%\7-Zip\7z.exe" x "%distrRoot%\.m2.7z" -o"%destinationPath%\.m2\" -y && ECHO Кеш Maven репозитория установлен успешно
)

ECHO @ECHO OFF> "%destinationPath%\Start IntelliJ IDEA.bat"
ECHO SET JAVA_HOME=C:\Temp\DevOpsAT\Java\jdk1.8.0_221>> "%destinationPath%\Start IntelliJ IDEA.bat"
ECHO START C:\Temp\DevOpsAT\IntelliJIDEA_CE_2019.3.3\bin\idea64.exe>> "%destinationPath%\Start IntelliJ IDEA.bat"

IF %autorunIDEA%==y (
    ECHO Запуск среды разработки автотестов intelliJIDEA, если не запустилось автоматически, откройте вручную %destinationPath%\IntelliJIDEA_CE_2019.3.3\bin\idea64.exe
    ECHO или запустите %destinationPath%\Start IntelliJ IDEA.bat
    ECHO Не забудьте сразу после запуска среды выполнить обновление версии автотестов до актуальной, выбрав из меню системы разработки автотестов пункты:
    ECHO 1. VCS -^> Git -^> Fetch
    ECHO 2. VCS -^> Git -^> Pull
    ECHO Для запуска автотеста нажать правой кнопкой мыши по открывшемуся сценарию с автотестом и выбрать пункт Выполнить: имя_теста
    START /B /MAX "" "%destinationPath%\Start IntelliJ IDEA.bat"
)

PAUSE
# CerediraTess

HTTP-сервис для выполнения скриптов (.bat, .sh) на удаленных агентах (Windows, Linux).

__Проект находится в разработке!!!__

По всем вопросам обращаться в телеграм чат поддержки: [t.me/CerediraTess](http://t.me/CerediraTess).

## Содержание <a name="content"></a>
1. [Содержание](#content)
1. [Описание инструмента CerediraTess](#description)
   1. [Для кого предназначен этот инструмент](#who_is_it_for)
   1. [Какие проблемы, решает этот инструмент](#problems)
   1. [Основные задачи инструмента](#main_tasks)
   1. [Второстепенные задачи инструмента](#minor_tasks)
   1. [Особенности инсрумента](#features)
1. [Системные требования](#system_requiremets)
1. [Установка и настройка](#setup)
   1. [Первый запуск](#first_run)
   1. [Установка в качестве сервиса](#service)
1. [Дополнительная информация](#additional_info)
   1. [Кто создал CerediraTess?](#creator)
   1. [Почему изначально была создана CerediraTess?](#why)
   1. [Хорошо, а в чём подвох? Что вы получаете распространяя CerediraTess?](#why2)

[English version](#english)


## Описание инструмента CerediraTess <a name="description"></a>

__Для кого предназначен этот инструмент:__<a name="who_is_it_for"></a>
* DevOps-инженерам;
* Администраторам операционных систем;
* Тестировщики;
* Автоматизаторам;
* Программистам.

__Какие проблемы, решает этот инструмент:__<a name="problems"></a>
1. Администраторам операционных систем, необходимо разрешить команде разработки выполнять перезагрузку сервиса Windows на машине, без возможности выполнять любые другие действия на этой машине и без необходимости выдачи каждому пользователю прав для входа на машину.
1. Администраторам операционных систем, необходимо обеспечить тестировщикам возможность очистки логов сервисов Windows на серверах, без возможности выполнять любые другие действия на этих серверах, без необходимости предоставления прав именно на разрешенные действия.
1. Администраторам операционных систем, по запросу пользователей, устанавливать на рабочих виртуальных машинах пользователей различное ПО вида Java JDK, Python интерпретатор, Maven, среды разработки и любой другой софт, без необходимости ручного вмешательства в процесс установки.
1. DevOps-инженерам, если у вас автоматизация тестирования, в качестве агентов выступают Windows машины, пул машин меняется или растет, то необходимо устанавливать ПО и настраивать одни и те же параметры на каждой машине, и велика вероятность возникновения ошибки.
1. Автоматизаторам при проведении нагрузочного тестирования необходимо приводить стенд нагрузочного тестирования в изначальное положение: выполнять перезагрузку, чистить логи, чистить таблицы баз данных и т.п.
1. Тестировщикам, при обновлении кода эмуляторов или заглушек, необходимо выполнять редеплой.

__Основные задачи инструмента:__<a name="main_tasks"></a>
* Предоставление широкому кругу пользователей возможность выполнения действий, согласованных с администратором, на удаленных агентах.
* Сокрытие от пользователей используемых учетных данных, для подключения к удаленным агентам.
* API-интерфейс, для возможности использования в связке с инструментами организации CI\CD.

__Второстепенные задачи инструмента:__<a name="minor_tasks"></a>
* Файловый сервер.
* Пользовательский интерфейс для удобства администрирования инструмента.
* Пользовательский интерфейс для удобства ручного использования инструмента/отладки скриптов.

__Особенности инсрумента:__<a name="features"></a>
* Не нужно устанавливать на удаленных агентах для выполнения действий дополнительное ПО и выполнять настройки.
* Встроенный широкий набор скриптов, который позволит выполнить быстрый старт.
* Открытость набора встроенных скриптов позволит быстро обучится написанию собственных.


## Системные требования <a name="system_requiremets"></a>

__Информация в данном разделе будет уточнения после проведения дополнительных испытаний. Все очень сильно зависит от задач.__
* Конфигурация с количеством параллельных агентов до 50 штук:
   1. ЦП: 4 ядра;
   1. ОП: 6-8 Гб;
   1. Диск: 50 Гб или больше.
* Конфигурация для запуска UI автотестов с открытием RDP сессий, агентов до 20-30 штук одновременно:
   1. ЦП: 8 ядер;
   1. ОП: 16 Гб;
   1. Диск: 100 Гб или больше.


## Как собрать приложение из исходного кода <a name="packaging"></a>

__Сборка приложения под ОС Windows__<a name="packaging_command"></a>
```
pyinstaller --name CerediraTess --add-data="venv\Lib\site-packages\flask_admin\static\admin\css\bootstrap4;ceredira_tess\static\admin\css\bootstrap4" --add-data="venv\Lib\site-packages\flask_admin\static\admin\js;ceredira_tess\static\admin\js" --add-data="venv\Lib\site-packages\flask_admin\static\bootstrap\bootstrap4\css;ceredira_tess\static\bootstrap\bootstrap4\css" --add-data="venv\Lib\site-packages\flask_admin\static\bootstrap\bootstrap4\fonts;ceredira_tess\static\bootstrap\bootstrap4\fonts" --add-data="venv\Lib\site-packages\flask_admin\static\bootstrap\bootstrap4\js;ceredira_tess\static\bootstrap\bootstrap4\js" --add-data="venv\Lib\site-packages\flask_admin\static\bootstrap\bootstrap4\swatch\flatly;ceredira_tess\static\bootstrap\bootstrap4\swatch\flatly" --add-data="venv\Lib\site-packages\flask_admin\static\vendor\bootstrap-daterangepicker\daterangepicker-bs4.css;ceredira_tess\static\vendor\bootstrap-daterangepicker" --add-data="venv\Lib\site-packages\flask_admin\static\vendor\bootstrap-daterangepicker\daterangepicker.js;ceredira_tess\static\vendor\bootstrap-daterangepicker" --add-data="venv\Lib\site-packages\flask_admin\static\vendor\bootstrap-daterangepicker\README.MD;ceredira_tess\static\vendor\bootstrap-daterangepicker" --add-data="venv\Lib\site-packages\flask_admin\static\vendor\bootstrap4;ceredira_tess\static\vendor\bootstrap4" --add-data="venv\Lib\site-packages\flask_admin\static\vendor\leaflet;ceredira_tess\static\vendor\leaflet" --add-data="venv\Lib\site-packages\flask_admin\static\vendor\multi-level-dropdowns-bootstrap;ceredira_tess\static\vendor\multi-level-dropdowns-bootstrap" --add-data="venv\Lib\site-packages\flask_admin\static\vendor\select2;ceredira_tess\static\vendor\select2" --add-data="venv\Lib\site-packages\flask_admin\static\vendor\x-editable;ceredira_tess\static\vendor\x-editable" --add-data="venv\Lib\site-packages\flask_admin\static\vendor\jquery.min.js;ceredira_tess\static\vendor" --add-data="venv\Lib\site-packages\flask_admin\static\vendor\moment.min.js;ceredira_tess\static\vendor" --add-data="venv\Lib\site-packages\flask_admin\static\vendor\popper.min.js;ceredira_tess\static\vendor" --add-data="venv\Lib\site-packages\flask_admin\templates\bootstrap4\admin;ceredira_tess\templates\admin" --add-data="venv\Lib\site-packages\flask_admin\translations\ru;flask_admin\translations\ru" --add-data "www;www" --add-data "scripts;scripts" --add-data "resources;resources" --add-data="ceredira_tess\static;ceredira_tess\static" --add-data="ceredira_tess\templates;ceredira_tess\templates" run.py
```


## Установка и настройка <a name="setup"></a>

__Первый запуск__<a name="first_run"></a>
1. Скачать архив с последней версией CerediraTess со страницы релизов https://github.com/Ceredira/CerediraTess/releases.
1. Создать каталог, например: _C:\\Temp\\CerediraTess\_{ProjectName1}\\_, который будет является корнем проекта, где {ProjectName1} - желаемое имя проекта.
1. Распаковать содержимое архива в созданный каталог.
1. Перейти в каталог CerediraTess и переименовать _CerediraTess.exe_ в _CerediraTess\_{ProjectName1}.exe_.
1. Вернутся в каталог на уровень выше.
1. Запустить командную строку в данно каталоге.
1. Выполнить команду _CerediraTess\\CerediraTess\_{ProjectName1}.exe_.
1. Правка файлов конфигурации:
   1. На текущий момент в файле users.json зашито 2 пользователя:
      1. usr_1 с паролем 1qaz@WSX
      1. usr_2 с паролем !QAZ2wsx
      1. В дальнейшем это будет разрешено редактировать через странице Администрирования в UI.
   1. На текущий момент в файле agents.json зашито 2 агента, один локальный, другой удаленный. Их можно использовать как шаблоны для добавления новых агентов в конфигурационный файл, пока не будет реализован функционал страницы Администрирование.
1. Загрузка необходимых сторонних утилит, для выполнения удаленных команд:
   1. С сайта https://live.sysinternals.com/ скачать утилиту _psexec.exe_ и положить в каталог _resources_ проекта. Для возможности выполнения запросов к удаленным Windows-машинам.
   1. С сайта https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html скачать утилиту _plink.exe_ и положить в каталог _resources_ проекта. Для возможности выполнения запросов к удаленным Linux-машинам.
1. Утилита работает.

__Установка в качестве сервиса__<a name="service"></a>

Для уставноки в качестве сервиса используется утилита nssm.exe.


## Принцип работы с системы

Варианты работы системы

<a name="problems"></a>


## Дополнительная информация <a name="additional_info"></a>

### Кто создал CerediraTess? <a name="creator"></a>
CerediraTess (CT) как концепт, был создан unixshaman (Джамалов Газимагомед) в январе 2018 года на проектах по автоматизации тестирования программного обеспечения компании AppLine.ru. Проект назывался WindowsServiceWebAPI (WSWA) и был написан на C# и .NET Framework. Большой вклад в рефакторинг первой версии WSWA был внесен Дильдиным Николаем.

CT, как текущая реализация - это результат упорного труда и целеустремленности. В разработке не принимали участие крупные компании, или команда разработчиков, и не было никакого бюджета - только я один.

Однако, теперь CT - это проект с открытым исходным кодом, и я не могу сказать, что все что тут сделано, будет только моим. Возможно, у проекта появятся соавторы, которые помогли бы сделать CT еще лучше. Также нельзя забывать о всех тех прекрасных библиотеках и инструментах, благодаря которым стало возможным создание CT, в особенности psexec.exe, без которого проект выглядел бы не так минималистично, как сейчас. Отдельное спасибо, Богачеву Никите, чьи наработки в части сервиса из проекта KeyWordAutomation я смог использовать.

CT не стал бы тем, чем он является сегодня, без помощи моих родителей и других людей, поддерживавших меня во всём что я здесь делаю.

Спасибо вам всем за помощь в разработке CerediraTess!


### Почему изначально была создана CerediraTess? <a name="why"></a>

Основной целью создания CT было получить инструмент с удобным интерфейсом (как GUI, так и API для возможности использования в автоматизации) для возможности выполнения команд или скриптов (набора команд) на удаленных агентах (Windows\Linux), без необходимости предварительной установки дополнительного программного обеспечения или выполнения иных конфигурационных действий на них. Фактически, это все еще так и остается его основной целью, поскольку моя концепция не менялась с 2018 года, и я все еще следую ей. Разумеется, с тех пор было сделано много изменений в части стабильности, доработок в части безопасности и нововведений, включая полное переписывание с технологического стека C# и .NET Framework на Python.

Важно отметить, что CT не стремится соперничать с другими программами для удаленного исполнения команд. Существуют множество программ, похожих на CT, но на момент начала разработки не было ничего, что бы меня устраивало (и нет по сей день), поэтому я создал свою собственную программу, такой, как мне хотелось. С течением времени, это экономило мне большое количество времени, которое я затрачивал на установку и настройку сторонних решений.


### Хорошо, а в чём подвох? Что вы получаете распространяя CerediraTess? <a name="why2"></a>

Нет никакого подвоха, я создал CT для себя и поделился им с остальным сообществом в надежде, что он окажется полезным. То же самое случилось в 1991 году, когда Линус Торвальдс поделился своим первым ядром Linux с остальным миром. В нём нет скрытых вредоносных программ, сбора данных, майнинга криптовалют или других функций, которые принесут мне денежную выгоду. Проект CT поддерживается исключительно необязательными пожертвованиями от довольных пользователей, таких же, как вы. Вы можете использовать CT точно так же как его использую я, и если он вам нравится - вы всегда можете спонсировать меня, чтобы показать свою благодарность за то, что я делаю.

Также, я использую CT, как пример для обучения в разработке современного проекта на Python, который всегда стремится к совершенству и лучшим практикам, будь то касательно технологий, управления проектами или самого кода. Поэтому если вы сможете чему-то научиться из моего проекта - это только сделает меня счастливее.



# CerediraTess. English Version <a name="english"></a>

Service for script execution on remote hosts.  
Must be running on Windows as executable, or as a windows service with nssm.exe using.  
Run .bat scripts on Windows hosts.
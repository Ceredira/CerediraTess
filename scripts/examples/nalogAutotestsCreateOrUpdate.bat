@ECHO OFF
SET autotests_repo=http://qa-service.dpc.tax.nalog.ru/devopsat/AutomationTestingNalogTests.git
SET autotests_path=%~1
SET branch_name=%~2
SET pathToInstallGit=%~3

IF NOT EXIST "%autotests_path%" (MKDIR "%autotests_path%")

"%pathToInstallGit%\bin\git.exe" config --global core.longpaths true

"%pathToInstallGit%\bin\git.exe" clone "%autotests_repo%" "%autotests_path%" || (
    "%pathToInstallGit%\bin\git.exe" --git-dir="%autotests_path%\.git" --work-tree="%autotests_path%" fetch --all
    "%pathToInstallGit%\bin\git.exe" --git-dir="%autotests_path%\.git" --work-tree="%autotests_path%" reset --hard %branch_name%
)
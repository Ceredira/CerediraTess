chcp 65001

echo asdf

rem call %~dp0\func.bat



echo asdf
call %~dp0\func.bat :wait 5
echo asdf
call %~dp0\func.bat :wait 2
echo asdf


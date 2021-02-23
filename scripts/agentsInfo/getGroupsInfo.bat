@echo OFF

chcp 65001

rem script encoding: 866
rem script description: Получить список групп и пользователей в группах

net localgroup

net localgroup Администраторы
net localgroup Пользователи

net localgroup Administrators
net localgroup Users

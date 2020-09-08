@ECHO OFF

CHCP 65001

REM SCRIPT ENCODING: utf-8
REM SCRIPT DESCRIPTION: Получить список групп и пользователей в группах

NET LOCALGROUP

NET LOCALGROUP Администраторы
NET LOCALGROUP Пользователи

NET LOCALGROUP Administrators
NET LOCALGROUP Users

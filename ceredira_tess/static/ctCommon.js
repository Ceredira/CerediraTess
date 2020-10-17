var ctHost = window.location.origin;

function showError(label, body) {
    $('#errorModalLabel').html(label);
    $('#errorModalBody').html(body);
    $('#errorModal').modal({show: true});
};

/**
 * Получение base64 строки с логином и паролем
 */
function getAuth() {
    return btoa($('#username').val() + ':' + $('#password').val());
};

function uuidv4() {
    return 'Rxxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
};

function getCurrentDateTime() {
    var currentdate = new Date();
    return currentdate.getFullYear() + '.'
        + (currentdate.getMonth()+1)  + '.'
        + currentdate.getDate() + ' '
        + currentdate.getHours() + ':'
        + currentdate.getMinutes() + ':'
        + currentdate.getSeconds();
};

function checkAgentsSelected() {
    if ($("#ctAgents").val() !== null && $("#ctAgents").val().length !== 0) {
        return true;
    } else {
        showError('Ошибка выполнения запроса', 'Не выбраны агент/агенты для выполнения запроса');
        return false;
    }
};

function checkAuth() {
    if ($('#username').val() !== null && $('#username').val() !== '') {
        if ($('#password').val() !== null && $('#password').val() !== '') {
            return true;
        } else {
            showError('Ошибка выполнения запроса', 'Не указан Пароль для выполнения запроса');
            return false;
        }
    } else {
        showError('Ошибка выполнения запроса', 'Не указан Логин для выполнения запроса');
        return false;
    }
};
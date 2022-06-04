var scriptsMeta = {};

function fillScriptsList() {
    $.ajax({
        url: 'getAvailableScripts',
        method: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: '',
        cache: false,
        success: function (data, status) {
            scriptsMeta = JSON.parse(data);

            var ctScripts = $('#ctScripts');
            ctScripts.html(`<option value='' selected disabled>Выберите скрипт для выполнения</option>`);

            for (var key in scriptsMeta) {
                var op = document.createElement('option');
                op.setAttribute('value', key);
                if ('exception' in scriptsMeta[key]) {
                    op.text = key + ': ' + scriptsMeta[key].exception;
                    op.setAttribute('disabled', 'disabled');
                } else {
                    op.text = key + ': ' + scriptsMeta[key].description;
                }
                ctScripts.append(op);
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert( jqXHR.responseText );
        }
    });
};

function fillScriptBodyAfterSelectScript(scriptName) {
    $.ajax({
        url: `getScript/${scriptName}`,
        method: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: '',
        cache: false,
        success: function (data, status) {
            scriptsBody = JSON.parse(data);

            //var ctScriptBody = $('#ctScriptBody');
            // ctScriptBody.val(scriptsBody[scriptName]);
            if (editor != 'undefined') {
                editor.setValue(scriptsBody[scriptName], -1)
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert( jqXHR.responseText );
        }
    });
};

function checkScriptSelected() {
    if ($("#ctScripts").val() !== null && $("#ctScripts").val() !== "") {
        return true;
    } else {
        showError('Ошибка сохранения скрипта', 'Не выбран скрипт для сохранения');
        return false;
    }
};

function saveScript(scriptName, body) {
    $.ajax({
        url: `saveScript/${scriptName}`,
        method: "POST",
        contentType: "application/text; charset=utf-8",
        data: body,
        cache: false,
        success: function (data, status) {
            // setAgentRowResult(agentResultRowId, status, data, 'success', scriptsMeta[scriptName]['executionCheck']);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            // setAgentRowResult(agentResultRowId, jqXHR.status, jqXHR.responseText, 'error', scriptsMeta[scriptName]['executionCheck']);
        }
    });
};

function checkScriptBody() {
    if (editor.getValue().trim() != "") {
        return true;
    } else {
        showError('Тело скрипта пусто!');
        return false;
    }
};

$(document).ready(function(){
    $("#updateCT").click(function(){
        fillScriptsList();
    });

    $("#ctScripts").change(function(){
        fillScriptBodyAfterSelectScript(this.value);
    });

    $("#saveCTScript").click(function(){
        if (checkScriptSelected() === true) {
            if (checkScriptBody() === true) {
                saveScript($("#ctScripts").val(), editor.getValue());
            }
        }
    });

    fillScriptsList();
});
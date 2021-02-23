var scriptsMeta = {};

function showScriptParametersDescription() {
    var script = $('#ctScripts').val();
    if (script) {
        var argNumber = 1;
        var htmlTable = `<label>${scriptsMeta[script]['description']}</label><table class='table'>`;
        for (var argDesc of scriptsMeta[script]['argumentsDescription']) {
            htmlTable += `<tr><td rowspan='2'>${argNumber}</td><td>${scriptsMeta[script]['arguments'][argNumber - 1]}</td></tr>
            <tr><td>${argDesc}</td></tr>`;
            argNumber += 1;
        }
        htmlTable += '</table>';

        $('#errorModalLabel').html('Описание параметров ' + script);
        $('#errorModalBody').html(htmlTable);
        $('#errorModal').modal({show: true});
    }
};

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

function fillAgentsListAfterSelectScript(scriptName) {
    var ctAgents = $("#ctAgents");
    ctAgents.html('<option value="" selected disabled>Выберите агент или агенты</option>');

    for (var agent of scriptsMeta[scriptName]['agents']) {
        var op = document.createElement("option");
        op.setAttribute("value", agent);
        op.text = agent;
        ctAgents.append(op);
    }

    reqBody = {};
    reqBody.hostname = '{hostname}';
    reqBody.args = scriptsMeta[scriptName]['arguments'];
    if (scriptsMeta[scriptName]['recommendedEncoding'] !== undefined) {
        reqBody.encoding = scriptsMeta[scriptName]['recommendedEncoding'];
    }
    if (scriptsMeta[scriptName]['timeout'] !== undefined) {
        reqBody.timeout = scriptsMeta[scriptName]['timeout'];
    }

    $("#ctRequestBody").val(JSON.stringify(reqBody, null, 4));
};

function getCTResponseBlock(parentId, agents, executedScript, executedScriptBody){
    var uid = uuidv4();
    var headerUid = uuidv4();

    var table = `<table class="table table-bordered">
        <thead>
            <tr class="d-flex">
                <th class="col-1">#</th>
                <th class="col-2">Агент</th>
                <th class="col-1">Статус</th>
                <th class="col-7">Результат</th>
                <th class="col-1">Проверка</th>
            <tr>
        </thead>
        <tbody>
    `;

    var agentsNumbering = 1;
    var agentsResultRows = {};
    for (var agent of agents) {
        var rowUID = uuidv4();
        agentsResultRows[agent] = rowUID;
        table += `<tr class="d-flex" id=${rowUID}>
            <td class="col-sm-1">${agentsNumbering}</td>
            <td class="col-sm-2">${agent}</td>
            <td class="col-sm-1"><div class="spinner-border" role="status"></div></td>
            <td class="col-sm-7"><textarea class="form-control" rows="5"></textarea></td>
            <td class="col-sm-1"></td>
        </tr>
        `;
        agentsNumbering++;
    }

    table += `
        </tbody>
    </table>
    `;

    var htmlRequestBlock = `<div class="card">
            <div class="card-header" id="${headerUid}">
                <h5 class="mb-0">
                    <button class="btn btn btn-secondary btn-sm" type="button" data-toggle="collapse" data-target="#${uid}"
                            aria-expanded="true" aria-controls="${uid}">
                        Свернуть/развернуть
                    </button>
                    <button class="btn btn-danger btn-sm" type="button" onclick="$(this).closest('.card').remove();">Удалить</button>
                    <input type="hidden" value="${btoa(executedScript)}">
                    <input type="hidden" value="${btoa(executedScriptBody)}">
                    <button class="btn btn-primary btn-sm" type="button" onclick="useCurrentRequest(this)">Использовать</button>
                    <label>Результат выполнения скрипта (${getCurrentDateTime()}): ${executedScript}</label>
                </h5>
            </div>

            <div id="${uid}" class="collapse show" aria-labelledby="${headerUid}">
                <div class="card-body">
                    ${table}
                </div>
            </div>
        </div>
    `;

    return { "tableHTML" : htmlRequestBlock, "agentsResultRows": agentsResultRows };
};

function useCurrentRequest(useButton) {
    $('#ctRequestBody').val(atob($(useButton).prev().attr('value')));
    $('#ctScripts').val(atob($(useButton).prev().prev().attr('value')));
};

function setAgentRowResult(agentResultRowId, status, data, result, executionCheck) {
    var agentRow = $("#" + agentResultRowId);

    if (agentRow.length) {
        if (result == 'success') {
            agentRow.addClass('ct-table-row-success');
        } else if (result == 'error') {
            agentRow.addClass('ct-table-row-error');
        }
        $(agentRow.children()[3].children[0]).val(data);
        agentRow.children()[2].innerHTML = getCurrentDateTime() + ": " + status;

        var responseCheckingResult = true;
        for (var logicalAnd of executionCheck) {
            var logicalOrResult = false;

            for (var logicalOr of logicalAnd) {
                var regex = new RegExp(logicalOr, "i");
                if (regex.test(data)) {
                    logicalOrResult = true;
                    break;
                }
            }
            responseCheckingResult = responseCheckingResult && logicalOrResult;
        }

        if (responseCheckingResult) {
            $(agentRow.children()[4]).addClass('ct-response-check-success');
            $(agentRow.children()[4]).html('SUCCESS');
        } else {
            $(agentRow.children()[4]).addClass('ct-response-check-error');
            $(agentRow.children()[4]).html('FAILED');
        }
    }
};

function checkRequestBody() {
    try {
        JSON.parse($("#ctRequestBody").val());
        return true;
    } catch(e) {
        showError('Ошибка валидации тела запроса', e.toString());
        return false;
    }
};

function checkScriptSelected() {
    if ($("#ctScripts").val() !== null && $("#ctScripts").val() !== "") {
        return true;
    } else {
        showError('Ошибка выполнения запроса', 'Не выбран скрипт для выполнения запроса');
        return false;
    }
};

function executeScript(agentsResultRows, scriptName, body) {
    for (let agent in agentsResultRows) {
        let agentResultRowId = agentsResultRows[agent];
        $.ajax({
            url: `executeScript/${scriptName}`,
            method: "POST",
            contentType: "application/json; charset=utf-8",
            data: body.replace("{hostname}", agent),
            cache: false,
            success: function (data, status) {
                setAgentRowResult(agentResultRowId, status, data, 'success', scriptsMeta[scriptName]['executionCheck']);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                setAgentRowResult(agentResultRowId, jqXHR.status, jqXHR.responseText, 'error', scriptsMeta[scriptName]['executionCheck']);
            }
        });
    }
};

function addCTHistoryBlock() {
    var requestDict = getCTResponseBlock("#CTRequestsHistory", $("#ctAgents").val(), $("#ctScripts").val(), $("#ctRequestBody").val());
    $("#CTRequestsHistory").prepend(requestDict["tableHTML"]);
    executeScript(requestDict["agentsResultRows"], $("#ctScripts").val(), $("#ctRequestBody").val());
};

function setParamInRequestBody(param, value) {
    var obj = JSON.parse($('#ctRequestBody').val());
    if (value !== null && value !== "") {
        obj[param] = value;
    } else {
        delete obj[param];
    }
    $('#ctRequestBody').val(JSON.stringify(obj, null, 4));
};

$(document).ready(function(){
    $("#updateCT").click(function(){
        fillScriptsList();
    });

    $("#ctScripts").change(function(){
        fillAgentsListAfterSelectScript(this.value);
    });

    $("#executeCTRequest").click(function(){
        if (checkScriptSelected() === true) {
            if (checkAgentsSelected() === true) {
                if (checkRequestBody() === true) {
                    addCTHistoryBlock();
                }
            }
        }
    });

    $("#setEncodingParam").change(function(){
        var value = $(this).val();
        setParamInRequestBody('encoding', value);
    });

    $("#setTimeoutParam").change(function(){
        var value = $(this).val();
        setParamInRequestBody('timeout', parseInt(value, 10));
    });

    $("#setCredsParam").change(function(){
        var value = $(this).val();
        setParamInRequestBody('creds', value);
    });

    $("#requestParametersDescription").click(function(){
        showScriptParametersDescription();
    });

    $("#requestValidation").click(function(){
        checkRequestBody();
    });

    fillScriptsList();
});
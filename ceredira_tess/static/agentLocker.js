$(document).ready(function(){
    $("#updateCT").click(function(){
        //if (checkAuth() === true) {
            fillAgentsStatusList();
        //}
    });

    $("#agentsLock").click(function(){
        //if (checkAuth() === true) {
            if (checkCauseSelected() === true) {
                if (checkAgentsSelected() === true) {
                    addCTLockingBlock();
                }
            }
        //}
    });

    $("#agentsUnlock").click(function(){
        //if (checkAuth() === true) {
            if (checkCauseSelected() === true) {
                if (checkAgentsSelected() === true) {
                    addCTUnlockingBlock();
                }
            }
        //}
    });

    if (document.getElementById('username') == null) {
        fillAgentsStatusList();
    }
});

function fillAgentsStatusList() {
    $.ajax({
        url: 'agentsStatus',
        method: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: '{}',
        cache: false,
//        beforeSend: function (xhr) {
//            /* Authorization header */
//            xhr.setRequestHeader('Authorization', getAuth());
//        },
        success: function (data, status) {
            agentsStatus = JSON.parse(data);

            var ctAgents = $('#ctAgents');
            ctAgents.html('<option value="" selected disabled>Выберите агент для блокировки</option>');
            var htmlTable = '';
            for (agent of agentsStatus) {
                var op = document.createElement('option');
                op.setAttribute('value', agent['hostname']);
                op.text = agent['hostname'];
                ctAgents.append(op);

                htmlTable += `<tr class="row m-0">
                    <td class="d-inline-block col-2">${agent['hostname']}</td>
                    <td class="d-inline-block col-2">${agent['lock_user']}</td>
                    <td class="d-inline-block col-8">${agent['lock_cause']}</td>
                </tr>`;
            }
            $('#ctAgentsStatus').html(htmlTable);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert( jqXHR.responseText );
        }
    });
};

function useCurrentLockCause(useButton) {
    $('#ctCause').val(atob($(useButton).prev().attr('value')));
};

function getCTLockingBlock(parentId, agents, cause, lockOrUnlock) {
    var uid = uuidv4();
    var headerUid = uuidv4();

    var table = `<table class="table table-bordered">
        <thead>
            <tr class="d-flex">
                <th class="col-2">Агенты</th>
                <th class="col-2">Статус</th>
                <th class="col-6">Результат блокировки</th>
                <th class="col-6">Проверка</th>
            <tr>
        </thead>
        <tbody>
    `;

    var rowUID = uuidv4();
    var agentsResultRow = rowUID;
    table += `<tr class="d-flex" id=${rowUID}>
        <td class="col-sm-2">${agents.join('; ')}</td>
        <td class="col-sm-2"><div class="spinner-border" role="status"></div></td>
        <td class="col-sm-6"></td>
        <td class="col-sm-2"></td>
    </tr>
    `;

    table += `
        </tbody>
    </table>
    `;

    var blockTitle = '';
    if (lockOrUnlock === 'lock') {
        blockTitle = 'Результат блокировки агентов';
    } else {
        blockTitle = 'Результат разблокировки агентов';
    }

    var htmlRequestBlock = `<div class="card">
            <div class="card-header" id="${headerUid}">
                <h5 class="mb-0">
                    <button class="btn btn btn-secondary btn-sm" type="button" data-toggle="collapse" data-target="#${uid}"
                            aria-expanded="true" aria-controls="${uid}">
                        Свернуть/развернуть
                    </button>
                    <button class="btn btn-danger btn-sm" type="button" onclick="$(this).closest('.card').remove();">Удалить</button>
                    <input type="hidden" value="${btoa(cause)}">
                    <button class="btn btn-primary btn-sm" type="button" onclick="useCurrentLockCause(this)">Использовать</button>
                    <label>${blockTitle} (${getCurrentDateTime()}): ${cause}</label>
                </h5>
            </div>

            <div id="${uid}" class="collapse show" aria-labelledby="${headerUid}">
                <div class="card-body">
                    ${table}
                </div>
            </div>
        </div>
    `;

    return { 'tableHTML' : htmlRequestBlock, 'agentsResultRow': agentsResultRow };
};

function checkCauseSelected() {
    if ($('#ctCause').val() !== null && $('#ctCause').val() !== '') {
        return true;
    } else {
        showError('Ошибка выполнения запроса', 'Не указана Причина блокировки для выполнения запроса');
        return false;
    }
};

function setAgentRowResult(agentResultRowId, status, data, result) {
    var agentRow = $('#' + agentResultRowId);

    if (agentRow.length) {
        if (result == 'success') {
            agentRow.addClass('ct-table-row-success');
        } else if (result == 'error') {
            agentRow.addClass('ct-table-row-error');
        }

        $(agentRow.children()[1]).html(getCurrentDateTime() + ': ' + status);
        $(agentRow.children()[2]).html(data);

        var responseCheckingResult = false;
        var regex = new RegExp('"result": true', 'i');
        if (regex.test(data)) {
            responseCheckingResult = true;
        }

        if (responseCheckingResult) {
            $(agentRow.children()[3]).addClass('ct-response-check-success');
            $(agentRow.children()[3]).html('SUCCESS');
        } else {
            $(agentRow.children()[3]).addClass('ct-response-check-error');
            $(agentRow.children()[3]).html('FAILED');
        }

        fillAgentsStatusList();
    }
};

function addCTLockingBlock() {
    var requestDict = getCTLockingBlock('#CTLockingHistory', $('#ctAgents').val(), $('#ctCause').val(), 'lock');
    $('#CTLockingHistory').prepend(requestDict['tableHTML']);
    agentsLocking(requestDict['agentsResultRow'], $('#ctAgents').val(), getAuth(), $('#ctCause').val());
};

function agentsLocking(agentsResultRow, agents, auth, cause) {
    let body = {
         'hostnames': agents,
         'lockCause': cause
    };

    $.ajax({
        url: 'agentsLock',
        method: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(body, null, 4),
        cache: false,
//        beforeSend: function (xhr) {
//            /* Authorization header */
//            xhr.setRequestHeader('Authorization', auth);
//        },
        success: function (data, status) {
            setAgentRowResult(agentsResultRow, status, data, 'success');
        },
        error: function (jqXHR, textStatus, errorThrown) {
            setAgentRowResult(agentsResultRow, jqXHR.status, jqXHR.responseText, 'error');
        }
    });
};

function addCTUnlockingBlock() {
    var requestDict = getCTLockingBlock('#CTLockingHistory', $('#ctAgents').val(), $('#ctCause').val(), 'unlock');
    $('#CTLockingHistory').prepend(requestDict['tableHTML']);
    agentsUnlocking(requestDict['agentsResultRow'], $('#ctAgents').val(), getAuth(), $('#ctCause').val());
};

function agentsUnlocking(agentsResultRow, agents, auth, cause) {
    let body = {
         'hostnames': agents,
         'lockCause': cause
    };

    $.ajax({
        url: 'agentsUnlock',
        method: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(body, null, 4),
        cache: false,
//        beforeSend: function (xhr) {
//            /* Authorization header */
//            xhr.setRequestHeader('Authorization', auth);
//        },
        success: function (data, status) {
            setAgentRowResult(agentsResultRow, status, data, 'success');
        },
        error: function (jqXHR, textStatus, errorThrown) {
            setAgentRowResult(agentsResultRow, jqXHR.status, jqXHR.responseText, 'error');
        }
    });
};

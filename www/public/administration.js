var agentsList = {};
var scripts = {};
var users = {};

$(document).ready(function(){
    $("#updateCT").click(function(){
        admin_updateCT();
    });
});

function selectAgent() {

};


function admin_updateCT() {
    $.ajax({
        url: 'getAgents',
        method: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: '',
        cache: false,
        beforeSend: function (xhr) {
            /* Authorization header */
            xhr.setRequestHeader('Authorization', getAuth());
        },
        success: function (data, status) {
            // alert("Data: " + data + "\nStatus: " + status);
            agentsList = JSON.parse(data);

            var ctAgents = $('#ctAgents');
            ctAgents.html(`<option value='' selected disabled>Выберите агент</option>`);

            for (var agent in agentsList) {
                var op = document.createElement('option');
                op.setAttribute('value', agentsList[agent].hostname);
                op.text = agentsList[agent].hostname + ': ' + agentsList[agent].description;
                ctAgents.append(op);
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert( jqXHR.responseText );
        }
    });

    $.ajax({
        url: 'getAvailableScripts',
        method: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: '',
        cache: false,
        beforeSend: function (xhr) {
            /* Authorization header */
            xhr.setRequestHeader('Authorization', getAuth());
        },
        success: function (data, status) {
            // alert("Data: " + data + "\nStatus: " + status);
            scriptsMeta = JSON.parse(data);

            var ctScripts = $('#ctScripts');
            ctScripts.html(`<option value='' selected disabled>Выберите скрипт для выполнения</option>`);

            for (var key in scriptsMeta) {
                var op = document.createElement('option');
                op.setAttribute('value', key);
                op.text = key + ': ' + scriptsMeta[key].description;
                ctScripts.append(op);
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert( jqXHR.responseText );
        }
    });
};
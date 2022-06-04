var editor = null;

$(document).ready(function(){
    ace.config.set("workerPath", "build/src-min");
    editor = ace.edit("ctScriptBody");
    editor.container.style.opacity = "";

    editor.setOptions({
        maxLines: 30,
        mode: "ace/mode/batchfile",
        autoScrollEditorIntoView: true
    });

    ace.config.loadModule("ace/ext/emmet", function() {
        ace.require("ace/lib/net").loadScript("static/ace/1.5.0/emmet-core/emmet.js", function() {
            editor.setOption("enableEmmet", true);
        });
    });

    ace.config.loadModule("ace/ext/language_tools", function() {
        editor.setOptions({
            enableSnippets: true,
            enableBasicAutocompletion: true
        });
    });

    const snippetManager = ace.require('ace/snippets').snippetManager;

    snippetManager.register([
        {
            "tabTrigger": "desc",
            "name": "desc1",
            "description": "Описание",
            "content": "rem script description: ${1:описание скрипта}"
        },
        {
            "tabTrigger": "descdesc",
            "name": "descdesc",
            "description": "Двойное описание",
            "content": "rem script description: ${1:описание скрипта}\nrem script description: ${2:дополнительное описание скрипта}"
        },
        {
            "tabTrigger": "test_snippet",
            "name": "test_snippet",
            "description": "Какой-то левый сниппет из примера",
            "content": "echo \"This is a test snippet\";\";"
        }
    ], "batchfile");

    editor.setValue("\n", 1);
});
const url = new URL(window.location.href)
const editor = ace.edit('editor')
const client = uuid.v4()

editor.setOptions({
    showPrintMargin: false,
    readOnly: true,
    fontSize: 18,
    theme: 'ace/theme/monokai'
})
editor.session.setOptions({
    tabSize: 4,
    useSoftTabs: true,
    mode: 'ace/mode/plain_text',
    useWorker: false
})

$.ajaxSetup({
    headers: {
        'X-CSRFToken': $.cookie('csrftoken')
    }
})

let note = {
    'language': 'plain_text',
    'read': false,
    'edit': false,
    'source': ''
}

let ISMINE = false,
    READ_LINK = undefined,
    EDIT_LINK = undefined


if (url.pathname === '/') {
    $('#language-select')[0].value = 'plain_text'
    $('#editor').click(() => $.post('/', {
        language: $('#language-select')[0].value
    }, (data) => {
        location.href = data['edit_link']
    }))
} else {
    let ws = new WebSocket('ws://' + url.host + url.pathname + '/' + client)
    ws.onmessage = (event) => {
        data = JSON.parse(event['data'])
        console.log(data)
        ISMINE = data['ismine']
        note['language'] = data['language']
        note['source'] = data['source']
        note['read'] = data['read']
        note['edit'] = data['edit']
        if (ISMINE) {
            READ_LINK = data['read_link']
            EDIT_LINK = data['edit_link']
        }
        if (client !== data['client'])
            update_editor()
    }
    ws.onopen = () => {
        $('#editor').keyup(() => {
            note['source'] = editor.getValue()
            ws.send(JSON.stringify(note))
        })
    }
    $('#language-select').change(() => {
        note['language'] = $('#language-select')[0].value
        editor.session.setMode('ace/mode/' + note['language'])
        ws.send(JSON.stringify(note))
    })
}

update_editor = () => {
    $('#language-select')[0].value = note['language']
    editor.setReadOnly(ISMINE && !note['edit'] || url.pathname.length != 7)
    editor.setValue(note['source'])
    editor.clearSelection()
    editor.navigateFileEnd()
    editor.focus()
    editor.session.setMode('ace/mode/' + note['language'])
}
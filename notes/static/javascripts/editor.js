const url = new URL(window.location.href)
const editor = ace.edit('editor')

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
    'ismine': false,
    'read': false,
    'read_link': undefined,
    'edit': false,
    'edit_link': undefined,
    'source': ''
}

if (url.pathname === '/') {
    $('#language-select')[0].value = 'plain_text'
    $('#editor').click(() => $.post('/', {
        language: $('#language-select')[0].value
    }, (data) => {
        location.href = data['edit_link']
    }))
} else {
    let ws = new WebSocket('ws://' + url.host + url.pathname)
    ws.onmessage = (event) => {
        data = JSON.parse(event['data'])
        note['ismine'] = data['ismine']
        note['language'] = data['language']
        note['source'] = data['source']
        if (note['ismine']) {
            note['read'] = data['read']
            note['read_link'] = data['read_link']
            note['edit'] = data['edit']
            note['edit_link'] = data['edit_link']
        }
        update_editor()
    }
    ws.onopen = () => {
        $('#editor').keyup(() => {
            note['source'] = editor.getValue()
            ws.send(JSON.stringify(note))
        })
    }
}

update_editor = () => {
    $('#language-select')[0].value = note['language']
    editor.setReadOnly(!note['ismine'])
    editor.setValue(note['source'])
    editor.clearSelection()
    editor.navigateFileEnd()
    editor.focus()
    editor.session.setMode('ace/mode/' + note['language'])
}
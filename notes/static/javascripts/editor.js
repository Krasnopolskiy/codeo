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


if (url.pathname === '/') {
    $('#editor').click(() => $.post('/', {
        language: $('#language-select')[0].value
    }, (data) => {
        location.href = data['edit_link']
    }))
} else {
    const ws = new WebSocket('ws://' + url.host + url.pathname)
    ws.onmessage = (event) => {
        console.log(event)
    }
    ws.onopen = () => {
        ws.send('hello!')
    }
}
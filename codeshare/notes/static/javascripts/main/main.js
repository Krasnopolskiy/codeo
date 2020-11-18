const url = new URL(window.location.href)
const name = url.pathname.split('/')[1]
const api = new Api_tunnel(Cookies.get('csrftoken'), name)
const editor = ace.edit('editor')


let ismine = false,
    read = false,
    edit = false,
    edit_link = '',
    error = false


editor.setOptions({
    showPrintMargin: false,
    readOnly: true,
    fontSize: 18,
    theme: 'ace/theme/monokai'
})
editor.session.setOptions({
    tabSize: 4,
    useSoftTabs: true,
    mode: 'ace/mode/plain_text'
})
$('#settings-btn').prop('disabled', true)
editor.$enableAutoIndent


let update = (onclose = false) => {
    if (edit || ismine)
        api.update({
            'source': editor.getValue(),
            'language': editor.session.getMode().$id,
            'read': read,
            'edit': edit
        }, onclose)
            .then(data => {
                console.log(data)
                if (data['message'] == 'error') {
                    error = true
                    location = url.origin
                }
            })
}

$('#editor').click(() => {
    if ((!edit || name != edit_link) && !ismine) {
        let body = {}
        if (url.pathname != '/')
            body = {
                'source': editor.getValue(),
                'language': editor.session.getMode().$id,
                'read': read,
                'edit': edit
            }
        api.create(body)
            .then(data => {
                if (data['message'] == 'created')
                    location = url.origin + '/' + data['name']
            })
    }
})

$('#editor').keyup(() => { update() })

$(window).on('beforeunload', () => { if (ismine && !error) update(true) })

$(document).ready(() => {
    $('#inputGroupSelectLanguage').click(() => {
        editor.session.setMode('ace/mode/' + $('#inputGroupSelectLanguage')[0].value)
        setTimeout(() => { update() }, 1000)
    })
    if (name.length > 0) {
        api.retrieve()
            .then(data => {
                if (data['message'] == 'retrieved') {
                    console.log(data)

                    ismine = data.ismine
                    read = data.note.read
                    edit = data.note.edit
                    edit_link = data.edit_link

                    editor.setValue(data.source)
                    editor.session.setMode(data.note.language)
                    editor.clearSelection()
                    editor.navigateFileEnd()
                    editor.focus()
                    editor.setReadOnly(!ismine && (!edit || name != edit_link))

                    if (ismine || (edit && name == edit_link))
                        $('#settings-btn').prop('disabled', false)
                    if (!ismine)
                        $('#main-settings-block').css('display', 'none')

                    $('#inputGroupSelectLanguage')[0].value = data.note.language.split('/')[2]

                    if (read) {
                        $('#read-link-input')[0].value = url.origin.replace('http://', '') + '/' + name
                        $('#allow-reading-btn').css('display', 'none')
                        $('#disallow-reading-btn').css('display', 'block')
                    }

                    if (edit && name == edit_link) {
                        $('#edit-link-input')[0].value = url.origin.replace('http://', '') + '/' + edit_link
                        $('#allow-editing-btn').css('display', 'none')
                        $('#disallow-editing-btn').css('display', 'block')
                    }
                } else {
                    error = true
                    location = url.origin
                }
            })
    }
})

$('#settings-btn').click(() => {
    if ($('#settings-drawer').css('transform') == 'matrix(1, 0, 0, 1, 420, 0)')
        $('#settings-drawer').css('transform', 'translateX(0)')
    else
        $('#settings-drawer').css('transform', 'translateX(420px)')
})

$('#allow-reading-btn').click(() => {
    read = true
    $('#read-link-input')[0].value = url.origin.replace('http://', '') + '/' + name
    $('#allow-reading-btn').css('display', 'none')
    $('#disallow-reading-btn').css('display', 'block')

    $('#read-link-input')[0].select()
    document.execCommand('copy')
    window.getSelection().removeAllRanges()

    update()
})

$('#disallow-reading-btn').click(() => {
    read = false
    $('#read-link-input')[0].value = ''
    $('#allow-reading-btn').css('display', 'block')
    $('#disallow-reading-btn').css('display', 'none')

    edit = false
    $('#edit-link-input')[0].value = ''
    $('#allow-editing-btn').css('display', 'block')
    $('#disallow-editing-btn').css('display', 'none')

    update()
})

$('#allow-editing-btn').click(() => {
    read = true
    $('#read-link-input')[0].value = url.origin.replace('http://', '') + '/' + name
    $('#allow-reading-btn').css('display', 'none')
    $('#disallow-reading-btn').css('display', 'block')

    edit = true
    $('#edit-link-input')[0].value = url.origin.replace('http://', '') + '/' + edit_link
    $('#allow-editing-btn').css('display', 'none')
    $('#disallow-editing-btn').css('display', 'block')


    $('#edit-link-input')[0].select()
    document.execCommand('copy')
    window.getSelection().removeAllRanges()

    update()
})

$('#disallow-editing-btn').click(() => {
    edit = false
    $('#edit-link-input')[0].value = ''
    $('#allow-editing-btn').css('display', 'block')
    $('#disallow-editing-btn').css('display', 'none')
    update()
})

$('#delete-btn').click(() => {
    api.delete()
    location = '/'
})
const url = new URL(window.location.href)
const notename = url.pathname.split('/')[1]
const api = new Api_tunnel(Cookies.get('csrftoken'), notename)
const editor = ace.edit("editor")
let ismine = false,
    published = false,
    protected = false


editor.setOptions({
    showPrintMargin: false,
    readOnly: true,
    fontSize: 18,
    theme: "ace/theme/monokai"
})
editor.session.setOptions({
    tabSize: 4,
    useSoftTabs: true,
    mode: "ace/mode/plain_text"
})
editor.$enableAutoIndent


let error = false


let update = () => {
    if (ismine)
        api.update({
            "source": editor.getValue(),
            "language": editor.session.getMode().$id,
            "published": published,
            "protected": protected
        })
            .then(data => {
                console.log(data)
                if (data["message"] == "error") {
                    error = true
                    location = url.origin
                }
            })
}

$('#editor').click(() => {
    if (!ismine) {
        let body = {}
        if (url.pathname != '/')
            body = {
                "source": editor.getValue(),
                "language": editor.session.getMode().$id
            }
        api.create(body)
            .then(data => {
                if (data["message"] == "created")
                    location = url.origin + '/' + data["notename"]
            })
    }
})

$('#editor').keyup(() => { update() })

$(window).on('beforeunload', () => {
    if (ismine && !error)
        api.update({ "source": editor.getValue() }, true)
            .then(data => {
                console.log(data)
            })
})

$(document).ready(() => {
    $('#inputGroupSelectLanguage').click(() => {
        editor.session.setMode("ace/mode/" + $('#inputGroupSelectLanguage')[0].value)
        setTimeout(() => { update() }, 1000)
    })
    if (notename.length > 0) {
        api.retrieve()
            .then(data => {
                if (data["message"] == "retrieved") {
                    console.log(data)

                    editor.setValue(data.source)
                    editor.session.setMode(data.note.language)
                    editor.clearSelection()
                    editor.navigateFileEnd()
                    editor.focus()
                    if (!data.ismine)
                        editor.setReadOnly(true)
                    else
                        editor.setReadOnly(false)

                    ismine = data.ismine
                    published = data.note.published
                    protected = data.note.protected

                    if (!ismine)
                        $('#settings-btn').prop('disabled', true)

                    $('#inputGroupSelectLanguage')[0].value = data.note.language.split('/')[2]
                    if (published) {
                        $('#viewer-input')[0].value = url.href.replace('http://', '')
                        $('#invite-viewer-btn').css('display', 'none')
                        $('#block-viewer-btn').css('display', 'block')
                    }
                } else {
                    error = true
                    location = url.origin
                }
            })
    }
})

$('#settings-btn').click(() => {
    console.log($('#settings-drawer').css('transform'))
    if ($('#settings-drawer').css('transform') == 'matrix(1, 0, 0, 1, 420, 0)')
        $('#settings-drawer').css('transform', 'translateX(0)')
    else
        $('#settings-drawer').css('transform', 'translateX(420px)')
})

$('#invite-viewer-btn').click(() => {
    published = true
    $('#viewer-input')[0].value = url.href.replace('http://', '')
    $('#invite-viewer-btn').css('display', 'none')
    $('#block-viewer-btn').css('display', 'block')
    update()
})

$('#block-viewer-btn').click(() => {
    published = false
    $('#viewer-input')[0].value = ''
    $('#invite-viewer-btn').css('display', 'block')
    $('#block-viewer-btn').css('display', 'none')
    update()
})
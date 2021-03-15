let popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
let popoverList = popoverTriggerList.map((popoverTriggerEl) => new bootstrap.Popover(popoverTriggerEl))

$('.copy-btn').click((event) => {
    $(event.target).parent().children('input').select()
    document.execCommand('copy')
    window.getSelection().removeAllRanges()
})

$(".alert").fadeTo(4000, 500).slideUp(500, () => {
    $(".alert").slideUp(500)
})
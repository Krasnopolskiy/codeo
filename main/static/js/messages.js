iziToast.settings({
    timeout: 6000,
    position: 'topRight'
})

messages.forEach(message => {
    switch (message.tags) {
        case 'green':
            iziToast.success({
                title: 'Success',
                message: message.message
            })
            break;
        case 'blue':
            iziToast.info({
                title: 'Info',
                message: message.message
            })
            break;
        case 'yellow':
            iziToast.warning({
                title: 'Warning',
                message: message.message
            })
            break;
        case 'red':
            iziToast.error({
                title: 'Error',
                message: message.message
            })
            break;
    }
})
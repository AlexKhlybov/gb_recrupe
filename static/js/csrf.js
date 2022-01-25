const csrf_token = () => {
    const csrf = document.querySelector('form > input[name="csrfmiddlewaretoken"]')
    return csrf.value
}

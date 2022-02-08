
async function getModalMessage(args) {
    const event = args.event
    const action = args.action
    const msgID = args.msgID
    const formID = args.form
    const sender = args.sender
    event.preventDefault();
    event.stopPropagation();


    let request = {
        csrf: getCookieCSRF(),
        url: '',
        body: {},
    }
    const url = {
        detail: `${window.location.href}detail/`,
        create: `${window.location.href}create/`,
    }
    const alert = {
        succesfull: {
            title: "Отправлено!",
            text: "Ваше сообщение успешно отправлено!",
            type: "alert-success"
        },
        errLoad: {
            title: "Ошибка!",
            text: "Ошибка загрузки сообщения. Попробуйте чуть позже!",
            type: "alert-danger"
        },
        errSend: {
            title: "Ошибка!",
            text: "Ошибка отправки. Попробуйте чуть позже!",
            type: "alert-danger"
        }
    }
    const resumeData = {}
    const modal = document.querySelector('.modal-dialog');


    if (action !== 'send') {
        modal.textContent = '';
    }

    // Блок выбора ACTION'a
    switch (action) {
        case 'answer':
            modal.insertAdjacentHTML('beforeend', renderAnswerMsgForm(sender));
            break;
        case 'new':
            modal.insertAdjacentHTML('beforeend', renderNewMsgForm());
            break;
        case 'detail':
            request.body = `id=${msgID}`;
            request.url = url.detail;
            requestServer();
            break;
        case 'send':
            const form = document.getElementById(formID);
            form.classList.add('was-validated');

            if (form.checkValidity()) {
                resumeData.email = document.querySelector('#sendMessage').value
                resumeData.subject = document.querySelector('#messageInput').value
                resumeData.text = document.querySelector('#messageTextarea').value
                request.url = url.create;
    
                parceData(resumeData);
                requestServer();
            }
            break;
    }

    // Парсит данные с формы и возвращает объект -> {'csrf': token, 'body': body}
    function parceData(data) {
        let str = '';
        Object.keys(data).forEach(name => {
            str += `${name}=${data[name]}&`
            });
        request.body = str.slice(0, -1)
    }

    // Получаем csrf из cookie если нет формы
    function getCookieCSRF() {
        let matches = document.cookie.match(new RegExp(
            "(?:^|; )" + "csrftoken".replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
        ));
        return matches ? decodeURIComponent(matches[1]) : undefined;
    }

    // Отрисовываем Сообщение
    function renderMsg(data) {
        return `<div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title" id="staticBackdropTitle">${data.title}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body px-4">
            <div class="d-flex justify-content-between mb-3">
                <div class="d-flex align-items-center">
                    <p style="margin: 0px;" >от: </p>
                    <small class="text-muted ms-3" id="staticBackdropSender" value="${data.sender}">${data.sender}</small>
                </div>
                
                <div class="d-flex align-items-center">
                    <p style="margin: 0px;">дата: </p>
                    <small class="text-muted ms-3" id="staticBackdropDate">${data.send_at}</small>
                </div>
            </div>
            <p id="staticBackdropBody">${data.text}</p>
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-primary" id="btnAnswerGetForm">Ответить</button>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">OK</button>
        </div>
    </div>`
    }

     // Отрисовывает Форму "Ответное сообщение"
     function renderAnswerMsgForm(sender) {
        return `<div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title" id="staticBackdropTitle">Новое сообщение</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body px-4">
            <form method="POST" name="AnswerForm" id="formAnswerMessage">
                <div class="mb-3 row">
                    <label for="SendInput" class="col-sm-2 col-form-label">Кому:</label>
                    <div class="col-sm-10">
                        <input type="text" readonly class="form-control-plaintext" id="sendMessage" value="${sender}">
                    </div>
                </div>
                <div class="mb-3">
                    <label for="messageInput" class="form-label">Тема</label>
                    <input type="text" class="form-control" id="messageInput" required>
                    <div class="invalid-feedback">Введите тему сообщения!</div>
                </div>
                <div class="mb-3">
                    <label for="messageTextarea" class="form-label">Сообщение</label>
                    <textarea class="form-control" id="messageTextarea" rows="3" required></textarea>
                    <div class="invalid-feedback">Введите текст сообщения!</div>
                </div>
                <button type="submit" class="btn btn-primary" id="btnAnswerSend">Отправить</button>
            </form>
        </div>
    </div>`
    };

    // Отрисовывает Форму "Новое сообщение"
    function renderNewMsgForm() {
        return `<div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title" id="staticBackdropTitle">Новое сообщение</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body px-4">
            <form method="POST" name="NewMsgForm" id="formNewMessage">
                <div class="mb-3">
                    <label for="SendInput" class="form-label">Кому:</label>
                    <input type="email" class="form-control" id="sendMessage" placeholder="E-mail пользователя" required>
                    <div class="invalid-feedback">Введите корректный e-mail (пользователя)</div>
                </div>
                <div class="mb-3">
                    <label for="messageInput" class="form-label">Тема</label>
                    <input type="text" class="form-control" id="messageInput" required>
                    <div class="invalid-feedback">Введите тему сообщения!</div>
                </div>
                <div class="mb-3">
                    <label for="messageTextarea" class="form-label">Сообщение</label>
                    <textarea class="form-control" id="messageTextarea" rows="3" required></textarea>
                    <div class="invalid-feedback">Введите текст сообщения!</div>
                </div>
                <button type="submit" class="btn btn-primary" id="btnMessageSend">Отправить</button>
            </form>
        </div>
    </div>`
    }

    // Отрисовывает DONE сообщение
    function renderDoneMsg(alert) {
        return `<div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title" id="staticBackdropTitle">${alert.title}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
            <div class="mb-3">
                <div class="alert ${alert.type}" role="alert">${alert.text}</div>
            </div>
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">OK</button>
        </div>
    </div>`
    }

    // Делает запрос на сервер и разбирает ответ
    async function requestServer () {
        const response = await fetch(request.url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-CSRFToken': request.csrf,
            },
            body: request.body,
        })

        if (response.ok) {
            let data = await response.json();
            modal.textContent = '';

            if (action == 'detail') {
                modal.insertAdjacentHTML('beforeend', renderMsg(data));
            } else if (action == 'send') {
                modal.insertAdjacentHTML('beforeend', renderDoneMsg(alert.succesfull));
            }
        } else {
            if (action == 'detail') {
                modal.insertAdjacentHTML('beforeend', renderDoneMsg(alert.errLoad));
            } else if (action == 'send') {
                modal.insertAdjacentHTML('beforeend', renderDoneMsg(alert.errSend));
            }
        }
    }

}

//Ловим событие клика на сообщение для подробного просмотра
document.querySelectorAll("#btnMessageDetail").forEach(el => {
    el.addEventListener('click', event => {
        const messageID = event.currentTarget.dataset.messageid;
        getModalMessage({event: event, action: 'detail', msgID: messageID}).then();
    })
});

//Ловим событие кнопок "Ответить", "Отправить", "Новое сообщение"
document.addEventListener('click', event => {
    if (event.target.id == 'btnAnswerGetForm') {
        const emailSender = document.getElementById('staticBackdropSender')
        const valuee = emailSender.getAttribute('value');
        getModalMessage({event: event, action: 'answer', sender: emailSender}).then();
    } else if (event.target.id == 'createNewMessage') {
        getModalMessage({event: event, action: 'new'}).then();
    } else if (event.target.id == 'btnAnswerSend') {
        const formID = 'formAnswerMessage';
        getModalMessage({event: event, action: 'send', form: formID}).then();
    } else if (event.target.id == 'btnMessageSend') {
        const formID = 'formNewMessage';
        getModalMessage({event: event, action: 'send', form: formID}).then();
    };
})

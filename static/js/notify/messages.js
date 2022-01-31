window.onload = function () {
    async function getModalMessage(event, action, messageID = null, formID = null) {
        event.preventDefault();

        const request = {}
        const resumeData = {}

        // Парсит данные с формы и возвращает объект -> {'csrf': token, 'body': body}
        function parceData(data) {
            let str = '';
            Object.keys(data).forEach(name => {
                str += `${name}=${data[name]}&`
              });
            request.body = str.slice(0, -1)
        }

        // Получаем csrf из cookie если нет формы
        function getCookie(name) {
            let matches = document.cookie.match(new RegExp(
                "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
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
            <div class="modal-body">
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
                <button type="button" class="btn btn-primary btn-answer" id="staticBackdropSend">Ответить</button>
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">OK</button>
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

        request.csrf = getCookie('csrftoken');
        if (!formID) {
            request.body = `id=${messageID}`;
            request.url = `${window.location.href}detail/`;
        } else {
            resumeData.email = document.querySelector('#sendMessage').value
            resumeData.subject = document.querySelector('#messageInput').value
            resumeData.text = document.querySelector('#messageTextarea').value
            parceData(resumeData);
            request.url = `${window.location.href}create/`;
        }

        const response = await fetch(request.url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-CSRFToken': request.csrf,
            },
            body: request.body,
        })

        let alert = {}
        if (response.ok) {
            let data = await response.json();
            const modal = document.querySelector('.modal-dialog');
            modal.textContent = '';
            modal.insertAdjacentHTML('beforeend', renderMsg(data));
            console.log(action == 'answer')
            if (action == 'answer') {
                alert = {
                    title: "Отправлено!",
                    text: "Ваше сообщение успешно отправлено!",
                    type: "alert-success"
                }
                const modal = document.querySelector('.modal-dialog');
                modal.textContent = '';
                modal.insertAdjacentHTML('beforeend', renderDoneMsg(alert));
            }
        } else {
            if (action == 'show') {
                alert = {
                    title: "Ошибка",
                    text: "Ошибка загрузки сообщения. Попробуйте чуть позже!",
                    type: "alert-danger"
                }
            } else if (action == 'answer') {
                alert = {
                    title: "Ошибка",
                    text: "Ошибка отправки. Попробуйте чуть позже!",
                    type: "alert-danger"
                }
            }

            const modal = document.querySelector('.modal-dialog');
            modal.textContent = '';
            modal.insertAdjacentHTML('beforeend', renderDoneMsg(alert));
        }
    }

    //Ловим событие клика на сообщение для подробного просмотра
    const btnMessage = document.querySelectorAll("#btnMessageDetail");
    btnMessage.forEach(el => {
        el.addEventListener('click', event => {
            const messageID = event.currentTarget.dataset.messageid;
            getModalMessage(event, action='show', messageID).then();
        })
    });


    function getFormMessgas(event) {

        // Отрисовывает форму ответа на сообщение
        function renderAnswerMsgForm(sender) {
            return `<div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="staticBackdropTitle">Новое сообщение</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <form method="POST" name="AnswerForm" id="formAnswerMessage">
                    <div class="mb-3 row">
                        <label for="SendInput" class="col-sm-2 col-form-label">Кому:</label>
                        <div class="col-sm-10">
                            <input type="text" readonly class="form-control-plaintext" id="sendMessage" value="${sender}">
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="messageInput" class="form-label">Тема</label>
                        <input type="text" class="form-control" id="messageInput" placeholder="Привет!">
                    </div>
                    <div class="mb-3">
                        <label for="messageTextarea" class="form-label">Сообщение</label>
                        <textarea class="form-control" id="messageTextarea" rows="3"></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary btn-send" id="btnMessage">Отправить</button>
                </form>
            </div>
        </div>`
        };

        const modal = document.querySelector('.modal-dialog');
        const sender = document.getElementById('staticBackdropSender').getAttribute('value');
        modal.textContent = '';
        modal.insertAdjacentHTML('beforeend', renderAnswerMsgForm(sender));
    };


    //Ловим событие кнопок "Ответить" и "Отправить"
    document.addEventListener('click', event => {
        if (event.target.classList.contains('btn-answer')) {
            getFormMessgas(event).then();
        };
        if (event.target.classList.contains('btn-send')) {
            const form = 'formAnswerMessage';
            getModalMessage(event, action='answer', null, form).then()
        };
    })

    // //Ловим событие кнопки "Новое сообщение"
    // document.querySelector("#recalcBtn").addEventListener('click', event => {
    //     let formID = 'recalculations_form';
    //     let reDrawDiv = '.recalc_list';
    //     saveDataForm(event, formID, reDrawDiv).then()})

}

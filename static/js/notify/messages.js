window.onload = function() {
    async function getModalMessage(event, messageID, formID=null) {
        event.preventDefault();
    
        const request = {}
    
        // Парсит данные с формы и возвращает объект -> {'csrf': token, 'body': body}
        function parceFormData (formData) {
            let str = '';
            let token = formData.get("csrfmiddlewaretoken")
            for(let [name, value] of formData) {
                str += `${name}=${value}&`};
            request.csrf = token
            request.body = str.slice(0, -1)}
    
        // Получаем csrf из cookie если нет формы
        function getCookie(name) {
            let matches = document.cookie.match(new RegExp(
                "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
            ));
            return matches ? decodeURIComponent(matches[1]) : undefined;}
    
        console.log(!formID)
        if (!formID) {
            request.csrf = getCookie('csrftoken');
            request.body = {};
        } else {
            const formData = new FormData(document.getElementById(formID));
            parceFormData(formData);
        }
    
        const response = await fetch(`${window.location.href}detail/${messageID}/`, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-CSRFToken': request.csrf,
            },
            body: request.body,})
    
        if (response.ok) {
            let data = await response.json();
            document.getElementById("staticBackdropTitle").innerHTML = data.title;
            document.getElementById("staticBackdropSender").innerHTML = data.sender;
            document.getElementById("staticBackdropDate").innerHTML = data.send_at;
            document.getElementById("staticBackdropBody").innerHTML = data.text;
            // let say = `Данные успешно приняты!`;
            // let time = 15000;
            // let typeAlert = `success`;
            // displayCounterAlert(say, typeAlert, time, event.target.id);
            // document.querySelector(reDrawDiv).innerHTML = json.instance;
        } else {
            console.log("NOT NOT COOL!!!")
            document.getElementById("staticBackdropTitle").innerHTML = "Ошибка загрузки сообщения!";
            document.getElementById("staticBackdropBody").innerHTML = "Попытайте удачу чуть позже";
        }
    }
    
    //Ловим событие клика на сообщение для подробного просмотра
    const btnMessage = document.querySelectorAll("#btnMessageDetail");
    btnMessage.forEach(el => {
        el.addEventListener('click', event => {
            const messageID = event.currentTarget.dataset.messageid;
            getModalMessage(event, messageID).then();
        })
    });
    
    
    // //Ловим событие кнопки "Ответить"
    // document.querySelector("#recalcBtn").addEventListener('click', event => {
    //     let formID = 'recalculations_form';
    //     let reDrawDiv = '.recalc_list';
    //     saveDataForm(event, formID, reDrawDiv).then()})
    
    // //Ловим событие кнопки "Новое сообщение"
    // document.querySelector("#recalcBtn").addEventListener('click', event => {
    //     let formID = 'recalculations_form';
    //     let reDrawDiv = '.recalc_list';
    //     saveDataForm(event, formID, reDrawDiv).then()})
    
}

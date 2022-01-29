/************************************************************************************
 Пожаловаться на вакансию или резюме
************************************************************************************/

document.querySelectorAll('.complaint_resume').forEach(elem => {
    elem.addEventListener('click', e => complaint_resume(e))
})

document.querySelectorAll('.complaint_vacancy').forEach(elem => {
    elem.addEventListener('click', e => complaint_vacancy(e))
})

function complaint_resume(event) {
    // Пожаловаться на резюме
    const target = event.target
    complaint_request(`/resume/complaint/${target.dataset.id}`, target).then()
}

function complaint_vacancy(event) {
    // Пожаловаться на вакансию
    const target = event.target
    complaint_request(`/vacancies/complaint/${target.dataset.id}`, target).then()
}

async function complaint_request(url, target) {
    let response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
        },
    })

    if (response.ok) {
        target.disabled = true
    } else {
        // Не технологично, зато надежно, качественно и практично
        alert(`Ошибка HTTP: ${response.status}`)
    }
}

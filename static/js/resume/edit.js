const resumeData = {
    experiences: [],    // Опыт работы
    education: [],      // Образование
    courses: [],        // Курсы
};


const months = [
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
];

(() => {
    loadResumeData().then()
})()

document.querySelectorAll('select[class$="select-month"]').forEach(select => {
    for (let i = 0; i < months.length; i++) {
        const opt = document.createElement('option')
        opt.value = `${i + 1}`
        opt.text = months[i]
        select.appendChild(opt)
    }
})

async function loadResumeData() {
    let response = await fetch(window.location.href, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': csrf_token(),
        },
        body: ''})
    
    if (response.ok) {
        let json = await response.json()
        //let json = await response.text()
        // console.log(JSON.stringify(json))
        resumeData.experiences = Array.isArray(json.experiences) ? json.experiences: []
        resumeData.education = Array.isArray(json.education) ? json.education: []
        resumeData.courses = Array.isArray(json.courses) ? json.courses: []

        renderExperience()
        renderEducation()
        renderCourses()

        document.querySelector('form').style.display = ''
    } else {
        const errorAlert = document.querySelector('.alert')
        errorAlert.innerHTML = `Ошибка HTTP: ${response.status}`
        errorAlert.style.display = ''
    }
    document.querySelector('.spinner-loading').style.display = 'none'
}

async function saveResume(event, draft) {
    const form = document.querySelector('#resume-form')
    const errorAlert = document.querySelector('.alert')
    form.classList.add('was-validated')
    errorAlert.style.display = 'none'
    const resumeTitle = {
        draft: draft,
        name: document.getElementById('id_name').value,
        price: document.getElementById('id_price').value ? parseInt(document.getElementById('id_price').value) : null,
        skills: document.getElementById('id_skills').value ? JSON.parse(document.getElementById('id_skills').value): [],
        about_me: document.getElementById('id_about_me').value,
    }

    event.stopPropagation()
    event.preventDefault()

    if (form.checkValidity()) {
        let response = await fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
                'X-CSRFToken': csrf_token(),
            },
            body: JSON.stringify({...resumeTitle, ...resumeData})})

        if (response.ok) {
            let json = await response.json();
            //let json = await response.text()
            // console.log(JSON.stringify(json))
            // window.location.href = '/resume/my-resume/'
            window.location.href = document.referrer;
        } else {
            let text = ''
            try {
                let json = await response.json()
                text = json.detail
            } catch (e) {
                text = `JS error ${e}`
            }
            errorAlert.innerHTML = `Ошибка HTTP: ${response.status} <br> ${text}`
            errorAlert.style.display = ''
        }
    }
}

document.querySelectorAll('#saveResume').forEach(elem => {
    // Сохранить и опубликовать
    elem.addEventListener('click', event => saveResume(event, false).then())
})

document.querySelectorAll('#saveResumeAsDraft').forEach(elem => {
    // Сохранить как черновик
    elem.addEventListener('click', event => saveResume(event, true).then())
})

/********************************************************************
    Опыт работы
********************************************************************/

document.getElementById('btnAppendExperience').addEventListener('click', () => {
    createExperience(obj => {
        // alert(JSON.stringify(obj))
        resumeData.experiences.push(obj)
        renderExperience()
    })
})

function renderExperience() {
    const elem = document.querySelector('#experience-container')
    elem.innerHTML = ''
    for (let i in resumeData.experiences) {
        elem.insertAdjacentHTML('beforeend', createExperienceCard(resumeData.experiences[i], i))
    }
}

function removeExperience_Click(index) {
    resumeData.experiences.splice(index, 1)
    renderExperience()
}

function editExperience_Click(index) {
    editExperience(resumeData.experiences[index], obj => {
        resumeData.experiences[index] = obj
        renderExperience()
    })
}

function createExperienceCard(obj, index) {
    const periodToStr = (month, year) => {
        if (month && year) {
            return `${months[month -1]} ${year}`
        }
        return 'по настоящее время'
    }

    return `
<div class="d-flex border mb-3">
    <div class="w-100" style="cursor: pointer" onclick="editExperience_Click(${index})">
        <div class="offcanvas-header pb-0">
            <h5 class="offcanvas-title">${obj.organisationName}</h5>
            <!--<button type="button" class="btn-close text-reset" aria-label="Close"></button>-->
        </div>
        <div class="offcanvas-body pt-0">
            <p class="text-muted">${periodToStr(obj.startMonth, obj.startYear)} — ${periodToStr(obj.endMonth, obj.endYear)}</p>
            <p class="m-0"><strong>${obj.positionName}</strong></p>
        </div>
    </div>
    <button type="button" class="btn-close text-reset m-3" aria-label="Close" onclick="removeExperience_Click(${index})"></button>
</div>`
}

/********************************************************************
    Образование
********************************************************************/

document.getElementById('btnAppendEducation').addEventListener('click', () => {
    createEducation(obj => {
        console.log(obj)
        resumeData.education.push(obj)
        renderEducation()
    })
})

function renderEducation() {
    const elem = document.querySelector('#education-container')
    elem.innerHTML = ''
    for (let i in resumeData.education) {
        elem.insertAdjacentHTML('beforeend', createEducationCard(resumeData.education[i], i))
    }
}

function removeEducation_Click(index) {
    resumeData.education.splice(index, 1)
    renderEducation()
}

function editEducation_Click(index) {
    editEducation(resumeData.education[index], obj => {
        resumeData.education[index] = obj
        renderEducation()
    })
}

function createEducationCard(obj, index) {
    let level = `${obj.yearOfEnding ? obj.yearOfEnding: ''}`
    const select = document.getElementById('modalEducationLevel')
    for (let o of select.options) {
        // levels.push({id: o.value, text: o.text})
        if (parseInt(o.value) === obj.level)
            level += (level.length > 0) ? ` - ${o.text}`: o.text
    }

    return `
<div class="d-flex border mb-3">
    <div class="w-100" style="cursor: pointer" onclick="editEducation_Click(${index})">
        <div class="offcanvas-header pb-0">
            <h5 class="offcanvas-title">${obj.institution}</h5>
            <!--<button type="button" class="btn-close text-reset" aria-label="Close"></button>-->
        </div>
        <div class="offcanvas-body pt-0">
            <p class="text-muted m-0">${level}</p>
        </div>
    </div>
    <button type="button" class="btn-close text-reset m-3" aria-label="Close" onclick="removeEducation_Click(${index})"></button>
</div>`
}

/********************************************************************
    Повышение квалификации, курсы
********************************************************************/

document.getElementById('btnAppendCourses').addEventListener('click', () => {
    createCourses(obj => {
        console.log(obj)
        resumeData.courses.push(obj)
        renderCourses()
    })
})

function renderCourses() {
    const elem = document.querySelector('#courses-container')
    elem.innerHTML = ''
    for (let i in resumeData.courses) {
        elem.insertAdjacentHTML('beforeend', createCoursesCard(resumeData.courses[i], i))
    }
}

function removeCourses_Click(index) {
    resumeData.courses.splice(index, 1)
    renderCourses()
}

function editCourses_Click(index) {
    editCourses(resumeData.courses[index], obj => {
        resumeData.courses[index] = obj
        renderCourses()
    })
}

function createCoursesCard(obj, index) {
    let year = `
        <div class="offcanvas-body pt-0">
            <p class="text-muted m-0">${obj.yearOfEnding}</p>
        </div>`
    if (!obj.yearOfEnding)
        year = ''


    return `
<div class="d-flex border mb-3">
    <div class="w-100" style="cursor: pointer" onclick="editCourses_Click(${index})">
        <div class="offcanvas-header pb-0">
            <h5 class="offcanvas-title">${obj.institution}</h5>
            <!--<button type="button" class="btn-close text-reset" aria-label="Close"></button>-->
        </div>
        ${year}
    </div>
    <button type="button" class="btn-close text-reset m-3" aria-label="Close" onclick="removeCourses_Click(${index})"></button>
</div>`
}

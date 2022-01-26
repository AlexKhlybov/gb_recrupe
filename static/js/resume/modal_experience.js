let _experienceSubmitCallback = function(obj){}
const experienceObject = {
    startMonth: null,
    startYear: null,
    endMonth: null,
    endYear: null,
    currentTimeFlag: false,

    organisationName: null,
    positionName: null,
    duties: null,
};

document.querySelector('#modalExperienceCheckedCurrentDate').addEventListener('change', function()  {
    const div = document.querySelector('#modalDivExperienceEnd')
    div.style.display = (this.checked) ? 'none': ''
})

document.querySelector('#experienceModalSave').addEventListener('click', function (event) {
    // Сохранение
    const modal = document.querySelector('#experienceModal')
    const dialog = bootstrap.Modal.getInstance(modal)

    const modalExperienceEndMonth = document.getElementById('modalExperienceEndMonth')
    const modalExperienceEndYear = document.getElementById('modalExperienceEndYear')
    const currentDateFlag = document.getElementById('modalExperienceCheckedCurrentDate').checked

    // По настоящее время
    if (!currentDateFlag) {
        modalExperienceEndMonth.setAttribute("required", "")
        modalExperienceEndYear.setAttribute("required", "")
    }
    else {
        modalExperienceEndMonth.removeAttribute("required")
        modalExperienceEndYear.removeAttribute("required")
        modalExperienceEndMonth.value = null
        modalExperienceEndYear.value = null
    }

    event.stopPropagation()

    const form = document.querySelector('#experienceModal > form')
    form.classList.add('was-validated')

    if (form.checkValidity()) {
        event.preventDefault()

        if (_experienceSubmitCallback) {
            const obj = {...experienceObject}
            obj.startMonth = parseInt(document.getElementById('modalExperienceStartMonth').value)
            obj.startYear = parseInt(document.getElementById('modalExperienceStartYear').value)
            obj.endMonth = parseInt(modalExperienceEndMonth.value)
            obj.endYear = parseInt(modalExperienceEndYear.value)
            obj.currentTimeFlag = currentDateFlag

            obj.startMonth = isNaN(obj.startMonth) ? null: obj.startMonth
            obj.startYear = isNaN(obj.startYear) ? null: obj.startYear
            obj.endMonth = isNaN(obj.endMonth) ? null: obj.endMonth
            obj.endYear = isNaN(obj.endYear) ? null: obj.endYear

            obj.organisationName = document.getElementById('modalExperienceCompanyName').value
            obj.positionName = document.getElementById('modalExperiencePositionName').value
            obj.duties = document.getElementById('modalExperienceDuties').value

            dialog.hide()
            _experienceSubmitCallback(obj)
            renderExperienceFromObject(obj)
        }
    }
})

function createExperience(callback = null) {
    showExperienceModal({...experienceObject}, callback)
}

function editExperience(obj, callback = null) {
    const data = {...experienceObject, ...obj}
    data.currentTimeFlag = !data.endYear && !data.endMonth

    showExperienceModal(data, callback)
}

function showExperienceModal(obj, callback) {
    const modal = document.getElementById('experienceModal')
    const dialog = new bootstrap.Modal(modal)
    const form = document.querySelector('#experienceModal > form')
    form.classList.remove('was-validated')

    renderExperienceFromObject(obj)

    dialog.show(null)
    _experienceSubmitCallback = callback
}

function renderExperienceFromObject(obj) {
    // Начало работы
    document.getElementById('modalExperienceStartMonth').value = obj.startMonth
    document.getElementById('modalExperienceStartYear').value = obj.startYear
    // Окончание
    if (obj.currentTimeFlag) {
        obj.endMonth = null
        obj.endYear = null
    }
    const div = document.querySelector('#modalDivExperienceEnd')
    div.style.display = (obj.currentTimeFlag) ? 'none': ''
    document.getElementById('modalExperienceCheckedCurrentDate').checked = obj.currentTimeFlag
    document.getElementById('modalExperienceEndMonth').value = obj.endMonth
    document.getElementById('modalExperienceEndYear').value = obj.endYear

    // Описание
    document.getElementById('modalExperienceCompanyName').value = obj.organisationName
    document.getElementById('modalExperiencePositionName').value = obj.positionName
    document.getElementById('modalExperienceDuties').value = obj.duties
}

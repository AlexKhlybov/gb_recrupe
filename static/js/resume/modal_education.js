let _educationSubmitCallback = function(obj){}
const educationObject = {
    level: 1,
    institution: null,
    faculty: null,
    specialization: null,
    yearOfEnding: null,
};

document.querySelector('#educationModalSave').addEventListener('click', function (event) {
    // Сохранение
    const modal = document.querySelector('#educationModal')
    const dialog = bootstrap.Modal.getInstance(modal)

    event.stopPropagation()

    const form = document.querySelector('#educationModal > form')
    form.classList.add('was-validated')

    if (form.checkValidity()) {
        event.preventDefault()

        if (_educationSubmitCallback) {
            const obj = {...educationObject}
            obj.level = parseInt(document.getElementById('modalEducationLevel').value)
            obj.institution = document.getElementById('modalEducationInstitution').value
            obj.faculty = document.getElementById('modalEducationFaculty').value
            obj.specialization = document.getElementById('modalEducationSpecialization').value
            obj.yearOfEnding = parseInt(document.getElementById('modalEducationYearOfEnding').value)

            obj.level = isNaN(obj.level) ? null: obj.level
            obj.yearOfEnding = isNaN(obj.yearOfEnding) ? null: obj.yearOfEnding

            dialog.hide()
            _educationSubmitCallback(obj)
            renderExperienceFromObject(obj)
        }
    }
})

function createEducation(callback = null) {
    showEducationModal({...educationObject}, callback)
}

function editEducation(obj, callback = null) {
    const data = {...educationObject, ...obj}
    data.currentTimeFlag = !data.endYear && !data.endMonth

    showEducationModal(data, callback)
}

function showEducationModal(obj, callback) {
    const modal = document.getElementById('educationModal')
    const dialog = new bootstrap.Modal(modal)
    const form = document.querySelector('#educationModal > form')
    form.classList.remove('was-validated')

    renderEducationFromObject(obj)

    dialog.show(null)
    _educationSubmitCallback = callback
}

function renderEducationFromObject(obj) {
    document.getElementById('modalEducationLevel').value = obj.level
    document.getElementById('modalEducationInstitution').value = obj.institution
    document.getElementById('modalEducationFaculty').value = obj.faculty
    document.getElementById('modalEducationSpecialization').value = obj.specialization
    document.getElementById('modalEducationYearOfEnding').value = obj.yearOfEnding
}

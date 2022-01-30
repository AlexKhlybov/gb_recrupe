let _coursesSubmitCallback = function(obj){}
const MessageObject = {
    sender: null,
    title: null,
    text: null,
    send_at: null,
};

document.querySelector('#coursesModalSave').addEventListener('click', function (event) {
    // Сохранение
    const modal = document.querySelector('#coursesModal')
    const dialog = bootstrap.Modal.getInstance(modal)

    event.stopPropagation()

    const form = document.querySelector('#coursesModal > form')
    form.classList.add('was-validated')

    if (form.checkValidity()) {
        event.preventDefault()

        if (_coursesSubmitCallback) {
            const obj = {...coursesObject}
            obj.institution = document.getElementById('modalCoursesInstitution').value
            obj.faculty = document.getElementById('modalCoursesFaculty').value
            obj.specialization = document.getElementById('modalCoursesSpecialization').value
            obj.yearOfEnding = parseInt(document.getElementById('modalCoursesYearOfEnding').value)

            obj.yearOfEnding = isNaN(obj.yearOfEnding) ? null: obj.yearOfEnding

            dialog.hide()
            _coursesSubmitCallback(obj)
            renderExperienceFromObject(obj)
        }
    }
})

function showMessageModal(obj, callback) {
    const modal = document.getElementById('messageModal')
    const dialog = new bootstrap.Modal(modal)

    renderMessage(obj)

    dialog.show(null)
    _coursesSubmitCallback = callback
}

function renderCoursesFromObject(obj) {
    document.getElementById('modalCoursesInstitution').value = obj.institution
    document.getElementById('modalCoursesFaculty').value = obj.faculty
    document.getElementById('modalCoursesSpecialization').value = obj.specialization
    document.getElementById('modalCoursesYearOfEnding').value = obj.yearOfEnding
}

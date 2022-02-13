class Answers {
    constructor() {
        this.url_vacancy_answer = "/answers/vacancy";
        this.url_resume_answer = "/answers/resume";

        document.querySelectorAll('.btn--vacancy-answer').forEach(elem => {
            elem.addEventListener('click', e => this.onAddOrRemoveAnswer(e))
        })
        document.querySelectorAll('.btn--resume-answer').forEach(elem => {
            elem.addEventListener('click', e => this.onAddOrRemoveAnswer(e))
        })
    };

    onAddOrRemoveAnswer(e) {
        const target = e.target
        const vacancyId = target.dataset.vacancyId
        const resumeId = target.dataset.resumeId

        if (e.target.classList.contains('btn--vacancy-answer')) {
            const api_url = `${this.url_vacancy_answer}/${vacancyId}/${resumeId}/`
            fetch(api_url).then(() => location.reload())
        } else if (e.target.classList.contains('btn--resume-answer')) {
            const api_url = `${this.url_resume_answer}/${resumeId}/${vacancyId}/`
            fetch(api_url).then(() => location.reload())
        }
    }
}

const answers = new Answers();
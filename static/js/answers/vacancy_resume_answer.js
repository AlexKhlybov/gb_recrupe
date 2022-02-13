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

        document.querySelectorAll('[class^="answer-vacancy-change-"]').forEach(elem => {
            elem.addEventListener('click', e => this.onChangeVacancyAnswerStatus(e))
        })
        document.querySelectorAll('[class^="answer-resume-change-"]').forEach(elem => {
            elem.addEventListener('click', e => this.onChangeResumeAnswerStatus(e))
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

    onChangeVacancyAnswerStatus(e) {
        const base_url = '/answers/change/vacancy'
        const id = e.target.dataset.id
        let api_url = `${base_url}/${id}/1/`
        if (e.target.classList.contains('answer-vacancy-change-accept')) {
            api_url = `${base_url}/${id}/2/`
        } else if (e.target.classList.contains('answer-vacancy-change-cancel')) {
            api_url = `${base_url}/${id}/3/`
        }
        fetch(api_url).then(() => location.reload())
    }

    onChangeResumeAnswerStatus(e) {
        const base_url = '/answers/change/resume'
        const id = e.target.dataset.id
        let api_url = `${base_url}/${id}/1/`
        if (e.target.classList.contains('answer-resume-change-accept')) {
            api_url = `${base_url}/${id}/2/`
        } else if (e.target.classList.contains('answer-resume-change-cancel')) {
            api_url = `${base_url}/${id}/3/`
        }
        fetch(api_url).then(() => location.reload())
    }
}

const answers = new Answers();
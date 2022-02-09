class Answers {
    constructor() {
//        console.log("?????");
        this.url_vacancy_answer = "/answers/edit-vacancy-answer";
        this.url_resume_answer = "/answers/edit-resume-answer";

        this.answer_id;

        document.querySelectorAll('.btn--vacancy-answer').forEach(elem => {
            elem.addEventListener('click', e => this._onAddRemoveAnswer(e))
        })
        document.querySelectorAll('.btn--resume-answer').forEach(elem => {
            elem.addEventListener('click', e => this._onAddRemoveAnswer(e))
        })
//        console.log(document);
//        console.log(document.querySelectorAll('.btn--resume-answer'));
    };

    // Слушает кнопку "Избранное"
    _onAddRemoveAnswer(e) {
        if (e.target.attributes.id === undefined) return;

        this.answer_id = e.target.attributes.id.value;
//        console.log(e.target.attributes.id);
        if (e.target.classList.contains('btn--vacancy-answer')) {
            let resume_name = document.getElementById("resume_" + this.answer_id.replace("answ_", "")).textContent.trim()
//            console.log(resume_name)
            let api_url = `${this.url_vacancy_answer}/${this.answer_id.replace("answ_", "")}/${resume_name}`
            this.fethFavorites(api_url);
        } else if (e.target.classList.contains('btn--resume-answer')) {
            let vac_name = document.getElementById("vac_" + this.answer_id.replace("offer_", "")).textContent.trim()
//            console.log(vac_name)
            let api_url = `${this.url_resume_answer}/${this.answer_id.replace("offer_", "")}/${vac_name}`
            this.fethFavorites(api_url);
        };
    };

    fethFavorites(url) {
        fetch(`${url}`)
        // fetch(
        //     url = `${url}`,
        //     headers = {
        //         "X-Requested-With": "XMLHttpRequest"
        //     })
//        .then((response) => {
//            return response.json();
//        })
//        .then((data) => {
//            let element = document.getElementById(`${this.favorites_id}`);
//            if (!data['delete']) {
//                element.classList.remove("text-primary");
//                element.classList.add("text-success");
//                element.innerText = "В избранном";
//            } else {
//                element.classList.add("text-primary");
//                element.classList.remove("text-success");
//                element.innerText = "В избранное";
//            };
//        })
//        .catch((error) => {
//            console.log(error.text);
//        });
    };
};

const answers = new Answers();

class Favorites {
    constructor() {
        this.url_vacancy = "/vacancies/edit-favorites";
        this.url_resume = "/resume/edit-favorites";

        this.favorite_id;

        document.querySelectorAll('.btn--vacancy').forEach(elem => {
            elem.addEventListener('click', e => this._onAddRemoveFavorites(e))
        })
        document.querySelectorAll('.btn--resume').forEach(elem => {
            elem.addEventListener('click', e => this._onAddRemoveFavorites(e))
        })
    };

    // Слушает кнопку "Избранное"
    _onAddRemoveFavorites(e) {
        if (e.target.attributes.id === undefined) return;

        this.favorites_id = e.target.attributes.id.value;
        if (e.target.classList.contains('btn--vacancy')) {
            let api_url = `${this.url_vacancy}/${this.favorites_id}/`
            this.fethFavorites(api_url);
        } else if (e.target.classList.contains('btn--resume')) {
            let api_url = `${this.url_resume}/${this.favorites_id}/`
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
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            let element = document.getElementById(`${this.favorites_id}`);
            console.log(this.favorites_id);
            if (!data['delete']) {
                element.classList.remove("text-primary");
                element.classList.add("text-success");
                element.innerText = "В избранном";
            } else {
                element.classList.add("text-primary");
                element.classList.remove("text-success");
                element.innerText = "В избранное";
            };
        })
        .catch((error) => {
            console.log(error.text);
        });
    };
};

const favorites = new Favorites();

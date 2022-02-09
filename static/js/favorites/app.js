
class Favorites {
    constructor() {
        this.url_vacancy = "/vacancies/edit-favorites";
        this.url_resume = "/resume/edit-favorites";

        this.favorite_id;

        this.target;
        this.currentTarget;

        document.querySelectorAll('.btn--vacancy').forEach(elem => {
            elem.addEventListener('click', e => this._onAddRemoveFavorites(e))
        })
        document.querySelectorAll('.btn--resume').forEach(elem => {
            elem.addEventListener('click', e => this._onAddRemoveFavorites(e))
        })
    };

    // Слушает кнопку "Избранное"
    _onAddRemoveFavorites(e) {
        this.target = e.target;
        this.currentTarget = e.currentTarget;
        if (this.currentTarget.attributes.id === undefined) return;

        this.favorites_id = this.currentTarget.attributes.id.value;
        if (this.currentTarget.classList.contains('btn--vacancy')) {
            let api_url = `${this.url_vacancy}/${this.favorites_id}/`
            this.fethFavorites(api_url);
        } else if (this.currentTarget.classList.contains('btn--resume')) {
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
            // let use = document.getElementById()
            console.log(this.favorites_id);
            let chield = this.currentTarget.children[0].children[0];
            if (!data['delete']) {
                element.classList.add("text-warning");
                element.classList.remove("text-secondary");

                chield.setAttribute('href', "/static/bootstrap/icons/favorite.svg#favorite-fill");
            } else {
                element.classList.add("text-secondary");
                element.classList.remove("text-warning");

                chield.setAttribute('href', "/static/bootstrap/icons/favorite.svg#favorite");
            };
        })
        .catch((error) => {
            console.log(error.text);
        });
    };
};

const favorites = new Favorites();

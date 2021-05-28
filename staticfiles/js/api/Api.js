function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

class Api {
    constructor(apiUrl) {
        this.apiUrl =  apiUrl;
        this.headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
      }
    }
    getPurchases() {
    return fetch(`/purchases`, {
      headers: this.headers
    })
      .then(e => {
        if (e.ok) {
          return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
  addPurchases(id) {
    return fetch(`${this.apiUrl}/purchases/`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify({
        id: id
      })
    })
      .then(e => {
        if (e.ok) {
          return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
  removePurchases(id) {
    return fetch(`${this.apiUrl}/purchases/${id}/`, {
      method: 'DELETE',
      headers: this.headers
    })
      .then(e => {
        if (e.ok) {
          return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
  addSubscriptions(id) {
  return fetch(`${this.apiUrl}/subscriptions/`, {
    method: 'POST',
    headers: this.headers,
    body: JSON.stringify({
      id: id
    })
  })
    .then( e => {
        if(e.ok) {
            return e.json()
        }
        return Promise.reject(e.statusText)
    })
}
  removeSubscriptions (id) {
  return fetch(`${this.apiUrl}/subscriptions/${id}/`, {
    method: 'DELETE',
    headers: this.headers,
  })
    .then( e => {
        if(e.ok) {
            return e.json()
        }
        return Promise.reject(e.statusText)
    })
}
  addFavorites (id)  {
    return fetch(`${this.apiUrl}/favorites/`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify({
        id: id
      })
    })
        .then( e => {
            if(e.ok) {
                return e.json()
            }
            return Promise.reject(e.statusText)
        })
  }
  removeFavorites (id) {
    return fetch(`${this.apiUrl}/favorites/${id}/`, {
      method: 'DELETE',
      headers: this.headers,

    })
        .then( e => {
            if(e.ok) {
                return e.json()
            }
            return Promise.reject(e.statusText)
        })
  }
    getIngredients  (text)  {
        return fetch(`${this.apiUrl}/ingredients?query=${text}`, {
            headers: this.headers,
        })
            .then( e => {
                if(e.ok) {
                    return e.json()
                }
                return Promise.reject(e.statusText)
            })
    }
}

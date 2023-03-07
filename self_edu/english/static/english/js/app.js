new Vue({
    el: '#words_app',                   // к этому элементу подключается view
    data: {                             // словарик с данными из запроса, пока пустой
    words: []
    },
    created: function () {              // функция выполнится при рендере страницы
        const vm = this;                // экземпляр класса
        axios.get('/words/')        // отправляем запрос
        .then(function (response) {     // и после выполняем функцию
        vm.words = response.data        // получаем ответ от сервера и кладем его в переменную
        })
    }
}

)
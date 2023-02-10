new Vue({
    el: '#words_app',
    data: {
    words: []
    },
    created: function () {
        const vm = this;
        axios.get('/api/words/')
        .then(function (response) {
        vm.words = response.data
        })
    }
}

)
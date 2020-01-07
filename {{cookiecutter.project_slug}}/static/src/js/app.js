import Vue from 'vue';
import App from './app/App.vue';

/*
    aliasing createElement to (h) is common practice
    see: https://vuejs.org/v2/guide/render-function.html
*/
new Vue({
    el: '#app',
    render: (h) => h(App)
});

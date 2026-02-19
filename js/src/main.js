import { createApp } from 'vue';
import App from './App.vue';
import 'vuetify/dist/vuetify.min.css';
import 'vuetify/styles';
import '@mdi/font/css/materialdesignicons.css'
import {aliases,mdi} from 'vuetify/iconsets/mdi' 
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import axios from 'axios'

const app = createApp(App);

const vuetify = createVuetify({
    components,
    directives,
    icons:{
        defaultSet:'mdi',
        aliases,
        sets:{
            mdi
        }
    }
});

app.config.globalProperties.$axios=axios;
app.use(vuetify);
app.mount('#app');
import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import inject from "@rollup/plugin-inject";
import vuetify from 'vite-plugin-vuetify'

export default defineConfig({
    css: {
        devSourcemap: true,
    },
    plugins: [
        vue(),
        inject({
            $: 'jquery',
            jQuery: 'jquery',
        }),
        vuetify()
    ]
    ,
    server: {
        host: '0.0.0.0',
        port: 8080,
        hot: true
    }
})

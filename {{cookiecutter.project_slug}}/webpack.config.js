'use strict';

var path = require('path');
var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var styleLintPlugin = require('stylelint-webpack-plugin');
var BrowserSyncPlugin = require('browser-sync-webpack-plugin');

var django_ip = process.env.DJANGO_IP || '127.0.0.1';
var django_port = parseInt(process.env.DJANGO_PORT || 8000);
var browsersync_port = parseInt(process.env.BROWSERSYNC_PORT || django_port + 1);
var browsersyncui_port = browsersync_port + 1;

require('es6-promise').polyfill();

module.exports = {
    entry: {
        main: ['./static/src/js/main.js'],
{%- if cookiecutter.wagtail == 'n' %}
        styles: ['./static/src/scss/styles.scss']
{%- else %}
        styles: ['./static/src/scss/styles.scss'],
        admin: ['./static/src/js/admin.js', './static/src/scss/admin_styles.scss']
{%- endif %}
    },

    output: {
        path: path.resolve('./static/dist/'),
        filename: 'js/[name].js'
    },

    plugins: [
        // Set css name
        new ExtractTextPlugin({
            filename: 'css/[name].css'
        }),

        // Stylelint plugin
        new styleLintPlugin({
            configFile: '.stylelintrc',
            context: '',
            files: '/static/src/scss/**/*.scss',
            syntax: 'scss',
            failOnError: false,
            quiet: false
        }),

        // BrowserSync
        new BrowserSyncPlugin(
            {
                host: django_ip,
                port: browsersync_port,
                injectCss: true,
                logLevel: 'silent',
                files: ['./static/dist/css/*.css', './static/dist/js/*.js'],
                ui: {
                    port: browsersyncui_port
                }
            },
            {
                reload: false
            }
        )
    ],

    module: {
        rules: [
            {
                enforce: 'pre',
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'eslint-loader',
                    options: {
                        configFile: path.resolve('.eslintrc.js'),
                        fix: true
                    }
                }
            },
            {
                test: /\.(png|jpg)$/,
                loader: 'url-loader',
                exclude: /node_modules/
            },
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['babel-preset-env']
                    }
                }
            },
            {
                test: /\.scss$/,
                use: ExtractTextPlugin.extract({
                    fallback: 'style-loader',
                    use: ['css-loader', 'postcss-loader', 'sass-loader']
                })
            }
        ]
    },

    stats: {
        // Colors and log settings
        colors: true,
        version: true,
        timings: true,
        assets: true,
        chunks: false,
        source: true,
        errors: true,
        errorDetails: true,
        warnings: true,
        hash: false,
        modules: false,
        reasons: false,
        children: false,
        publicPath: false
    },

    resolve: {
        alias: {
            vue$: 'vue/dist/vue.esm.js' // 'vue/dist/vue.common.js' for webpack 1
        }
    },

    // Create Sourcemaps for the files
    devtool: 'source-map'
};

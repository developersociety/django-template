'use strict';

var path = require('path');
var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var styleLintPlugin = require('stylelint-webpack-plugin');

require('es6-promise').polyfill();

module.exports = {
    entry: {
        main: ['./static/src/js/main.js'],
        styles: ['./static/src/scss/styles.scss'],
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
        // Specify the resulting CSS filename
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
        })
    ],

    module: {
        rules: [
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
                test: /\.(png|jpg)$/,
                loader: 'url-loader',
                exclude: /node_modules/
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

    resolve: {
        alias: {
            vue$: 'vue/dist/vue.esm.js' // 'vue/dist/vue.common.js' for webpack 1
        }
    }
};

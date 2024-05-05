/* eslint-disable radix */
const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const StyleLintPlugin = require('stylelint-webpack-plugin');
const ESLintPlugin = require('eslint-webpack-plugin');
const BrowserSyncPlugin = require('browser-sync-webpack-plugin');
const WebpackNotifierPlugin = require('webpack-notifier');
const SVGSpritemapPlugin = require('svg-spritemap-webpack-plugin');

// Webpack clean dist
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

// Vue
const { VueLoaderPlugin } = require('vue-loader');

const django_ip = process.env.DJANGO_IP || '127.0.0.1';
const django_port = parseInt(process.env.DJANGO_PORT || 8000);
const browsersync_port = parseInt(process.env.BROWSERSYNC_PORT || django_port + 1);
const browsersyncui_port = browsersync_port + 1;

const config = {
    entry: {
        base: ['./static/src/js/base.js'],
        app: ['./static/src/js/app.js'],
        styles: ['./static/src/scss/styles.scss'],
    },
    output: {
        path: path.resolve('./static/dist/'),
        filename: 'js/[name].js',
        assetModuleFilename: 'assets/[hash][ext][query]',
    },
};

module.exports = [
    // Development webpack config
    {
        name: 'development',
        entry: config.entry,
        output: config.output,

        plugins: [
            // Dist clean
            new CleanWebpackPlugin({
                cleanStaleWebpackAssets: false,
            }),

            // SVG sprite
            new SVGSpritemapPlugin('./static/src/sprite/*.svg', {
                output: {
                    filename: './svg/sprite.svg',
                },
                sprite: {
                    prefix: false,
                },
            }),

            // Set css name
            new MiniCssExtractPlugin({
                filename: 'css/[name].css',
                chunkFilename: 'css/[id].css',
            }),

            // Stylelint plugin
            new StyleLintPlugin({
                files: 'static/src/scss',
                failOnError: false,
            }),

            // eslint plugin
            new ESLintPlugin(),

            // BrowserSync
            new BrowserSyncPlugin(
                {
                    host: django_ip,
                    port: browsersync_port,
                    injectCss: true,
                    ghostMode: false,
                    logLevel: 'silent',
                    files: ['./static/dist/css/*.css', './static/dist/js/*.js'],
                    ignore: ['./static/dist/js/styles.js'],
                    ui: {
                        port: browsersyncui_port,
                    },
                },
                {
                    reload: false,
                },
            ),

            new VueLoaderPlugin(),
            new WebpackNotifierPlugin(),
        ],

        module: {
            rules: [
                {
                    test: /\.(png|jpg|woff|woff2|eot|ttf|svg|otf)$/,
                    exclude: /node_modules/,
                    type: 'asset/resource',
                },
                {
                    test: /\.js$/,
                    exclude: /node_modules/,
                    use: {
                        loader: 'babel-loader',
                        options: {
                            presets: [
                                [
                                    '@babel/preset-env',
                                    {
                                        useBuiltIns: 'usage',
                                        corejs: 3,
                                    },
                                ],
                            ],
                        },
                    },
                },
                {
                    test: /\.vue$/,
                    use: 'vue-loader',
                },
                {
                    test: /\.scss$/,
                    exclude: /node_modules/,
                    use: [
                        MiniCssExtractPlugin.loader,
                        {
                            loader: 'css-loader',
                            options: { sourceMap: true },
                        },
                        {
                            loader: 'postcss-loader',
                            options: { sourceMap: true },
                        },
                        {
                            loader: 'sass-loader',
                            options: { sourceMap: true },
                        },
                    ],
                },
                {
                    test: /\.css$/,
                    exclude: /node_modules/,
                    use: [
                        'style-loader',
                        {
                            loader: 'css-loader',
                            options: { sourceMap: true },
                        },
                    ],
                },
            ],
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
            publicPath: false,
        },

        // Create Sourcemaps for the files
        devtool: 'source-map',
    },
    // Production webpack config
    {
        name: 'production',
        entry: config.entry,
        output: config.output,

        plugins: [
            // SVG sprite
            new SVGSpritemapPlugin('./static/src/sprite/*.svg', {
                output: {
                    filename: './svg/sprite.svg',
                },
                sprite: {
                    prefix: false,
                },
            }),

            // Specify the resulting CSS filename
            new MiniCssExtractPlugin({
                filename: 'css/[name].css',
            }),

            // Stylelint plugin
            new StyleLintPlugin({
                configFile: '.stylelintrc',
                context: '',
                files: '/static/src/scss/**/*.scss',
                syntax: 'scss',
                failOnError: false,
                quiet: false,
            }),

            new VueLoaderPlugin(),
        ],

        module: {
            rules: [
                {
                    test: /\.js$/,
                    exclude: /node_modules/,
                    use: {
                        loader: 'babel-loader',
                        options: {
                            presets: [
                                [
                                    '@babel/preset-env',
                                    {
                                        useBuiltIns: 'usage',
                                        corejs: 3,
                                    },
                                ],
                            ],
                        },
                    },
                },
                {
                    test: /\.vue$/,
                    use: 'vue-loader',
                },
                {
                    test: /\.(png|jpg|woff|woff2|eot|ttf|svg|otf)$/,
                    exclude: /node_modules/,
                    type: 'asset/resource',
                },
                {
                    test: /\.scss$/,
                    use: [
                        MiniCssExtractPlugin.loader,
                        'css-loader',
                        'postcss-loader',
                        'sass-loader',
                    ],
                },
            ],
        },
    },
];

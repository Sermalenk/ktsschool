const path = require('path');
const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
// const src = path.resolve(__dirname, 'src');
const build = path.resolve(__dirname, 'assets');
const isProd = process.env.NODE_ENV === 'production';
const publicPath = isProd ? '/static/' : '/assets/bundles/';
const BundleTracker = require('webpack-bundle-tracker');
const extractCSS = new ExtractTextPlugin('css/[name].[hash:5].css');

module.exports = {
    entry: {
        vendor: ['jquery'],
        main: path.resolve('./core/static/core/js/chat.js')
    },
    output: {
        path: build,
        filename: 'js/[name].bundle.js',
        publicPath
    },
    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery'
        }),
        extractCSS
    ],
    module: {
        rules: [
            {
                test: /\.js/,
                exclude: /(node_modules)/,
                use: {
                    loader: 'babel-loader'
                }
            },
            {
                test: /\.(png|jpg|ico)$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: 'img/[name].[ext]'
                        }
                    }
                ]
            },
            {
                test: /\.s?css/,
                loader: extractCSS.extract({
                    use: [
                        {
                            loader: `css-loader`,
                            options: {
                                sourceMap: !isProd,
                                importLoaders: 1,
                            }
                        },
                        {
                            loader: `resolve-url-loader`,
                            options: {
                                sourceMap: !isProd,
                            }
                        },
                        {
                            loader: `sass-loader`,
                            options: {
                                sourceMap: !isProd,
                            }
                        }
                    ]
                })
            }
        ]
    }
};

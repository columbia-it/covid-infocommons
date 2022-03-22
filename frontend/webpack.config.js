const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
console.log(__dirname)
const static_dir = '/Users/sg3847/PycharmProjects/covid-infocommons/backend/static/'
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    entry: path.join(__dirname, "src", "index.tsx"),
    output: { 
        path: static_dir,
        filename: 'main.js'
     },
    mode: process.env.NODE_ENV || "development",
    resolve: { 
            extensions: [".tsx", ".ts", ".js"],
    },
    devServer: { static: { directory: path.join(__dirname, "src") } },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: ["babel-loader"],
            },
            {
                test: /\.(ts|tsx)$/,
                exclude: /node_modules/,
                use: ["ts-loader"],
            },
            {
                test: /\.(sa|sc|c)ss$/i,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader",
                ],
              }
        ]
    },
    plugins: [new MiniCssExtractPlugin()],

    // plugins: [
    //     new HtmlWebpackPlugin({
    //       template: path.join(__dirname, "src", "index.html"),
    //     }),
    // ],
}
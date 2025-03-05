const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

const static_dir = path.resolve("../../").concat("/backend/search/static/search")

const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    entry: {
	main: path.join(__dirname, "src", "index.tsx"),
	adv_search: path.join(__dirname, "src", "adv_search.tsx"),
    },
    output: { 
        path: static_dir,
        filename: '[name].js'
    },
    optimization: {
        minimize: true,
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
    plugins: [new MiniCssExtractPlugin()]
}

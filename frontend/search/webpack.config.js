const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

const static_dir = path.resolve("../../").concat("/backend/search/static/search")

const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    entry: path.join(__dirname, "src", "index.tsx"),
    output: { 
        path: static_dir,
        filename: '[name].bundle.js'
    },
    optimization: {
        splitChunks: {
          chunks: 'async',
          minSize: 20000,
          maxSize: 500000,
          minRemainingSize: 0,
          minChunks: 1,
          maxAsyncRequests: 30,
          maxInitialRequests: 30,
          enforceSizeThreshold: 50000,
          cacheGroups: {
            defaultVendors: {
              test: /[\\/]node_modules[\\/]/,
              priority: -10,
              reuseExistingChunk: true,
            },
            default: {
              minChunks: 2,
              priority: -20,
              reuseExistingChunk: true,
            },
          },
        },
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
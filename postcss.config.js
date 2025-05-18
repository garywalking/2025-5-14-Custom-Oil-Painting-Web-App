// custom_oil_painting_app/postcss.config.js
// PostCSS 配置文件
// 核心功能摘要: 配置 PostCSS 插件，通常与 Tailwind CSS 一起使用。

module.exports = {
  plugins: {
    tailwindcss: {}, // 启用 Tailwind CSS 插件
    autoprefixer: {}, // 启用 Autoprefixer 插件，自动添加 CSS 浏览器前缀
    // 其他 PostCSS 插件可以在这里添加
    // 例如，cssnano 用于压缩 CSS (通常在生产构建中)
    // ...(process.env.NODE_ENV === 'production' ? { cssnano: {} } : {})
  },
}

// 打印日志到控制台，确认配置文件被加载 (Node.js 环境)
console.log("LOG: postcss.config.js loaded.");
// custom_oil_painting_app/tailwind.config.js
// Tailwind CSS 配置文件
// 核心功能摘要: 配置 Tailwind CSS，例如内容扫描路径、主题扩展等。

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // 配置 Tailwind CSS 扫描 HTML 和 Python 文件以查找类名
    // 确保路径正确指向你的模板文件和任何可能动态生成类名的 Python 文件
    './app/templates/**/*.html', // 扫描 app/templates 目录下所有的 .html 文件
    './app/static/js/**/*.js',   // 如果你在 JS 中动态添加 Tailwind 类
    // 如果你使用 Python 生成包含 Tailwind 类的 HTML (例如通过 f-strings 或其他方式)
    // './app/**/*.py', // 谨慎使用，可能会扫描过多不必要的文件
    // 更具体的路径，例如：
    // './app/api/routers/some_router_that_generates_html_with_tailwind.py'
  ],
  theme: {
    extend: {
      // 在这里扩展 Tailwind 的默认主题
      // 例如，添加自定义颜色、字体、断点等
      // colors: {
      //   'brand-blue': '#1976D2',
      //   'brand-pink': '#E91E63',
      // },
      // fontFamily: {
      //   'sans': ['Inter', 'sans-serif'], // 示例：使用 Inter 字体
      // },
    },
  },
  plugins: [
    // 在这里添加 Tailwind CSS 插件
    // require('@tailwindcss/forms'), // 示例：官方表单插件
    // require('@tailwindcss/typography'), // 示例：官方排版插件
    // require('@tailwindcss/aspect-ratio'), // 示例：官方宽高比插件
  ],
}

// 打印日志到控制台，确认配置文件被加载 (Node.js 环境)
console.log("LOG: tailwind.config.js loaded.");
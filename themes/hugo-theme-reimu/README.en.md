<img src="https://cdn.jsdelivr.net/gh/D-Sketon/hugo-theme-reimu@main/images/screenshot.png"/>
<div align = center>
  <h1>hugo-theme-reimu</h1>
  <img alt="version" src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fgithub.com%2FD-Sketon%2Fhugo-theme-reimu%2Fraw%2Fmain%2Fpackage.json&query=%24.version&label=version">
  <img alt="GitHub License" src="https://img.shields.io/github/license/D-Sketon/hugo-theme-reimu">
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/D-Sketon/hugo-theme-reimu">
  <p align="center">
  <p align="center">
  💘 Hakurei Reimu 💘
  </p>

[Demo](https://d-sketon.github.io/hugo-theme-reimu)

[简体中文](https://github.com/D-Sketon/hugo-theme-reimu/blob/main/README.md) | English

</div>

A Hakurei Reimu style Hugo theme. Migrated from [hexo-theme-reimu](https://github.com/D-Sketon/hexo-theme-reimu).

---

|framework|repository|version|stars|
|-|-|-|-|
|[Hexo](https://hexo.io/)|[hexo-theme-reimu](https://github.com/D-Sketon/hexo-theme-reimu)|<img alt="version" src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fgithub.com%2FD-Sketon%2Fhexo-theme-reimu%2Fraw%2Fmain%2Fpackage.json&query=%24.version&label=version">|<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/D-Sketon/hexo-theme-reimu">|
|[Astro](https://astro.build)|[astro-theme-reimu](https://github.com/D-Sketon/astro-theme-reimu)|<img alt="version" src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fgithub.com%2FD-Sketon%2Fastro-theme-reimu%2Fraw%2Fmain%2Fpackage.json&query=%24.version&label=version">|<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/D-Sketon/astro-theme-reimu">|
|[Hugo](https://gohugo.io)|[hugo-theme-reimu](https://github.com/D-Sketon/hugo-theme-reimu)|<img alt="version" src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fgithub.com%2FD-Sketon%2Fhugo-theme-reimu%2Fraw%2Fmain%2Fpackage.json&query=%24.version&label=version">|<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/D-Sketon/hugo-theme-reimu">|

**ISSUE and PR Welcome!**

## Features

- All the regular features of the blog
- Compatible with Hugo 0.116.0 and above
- Responsive Layout
- Code Highlighting, Code Pasting
- KaTeX for displaying math formulas
- Mermaid for flowcharts
- Algolia search
- valine / waline / twikoo / gitalk / giscus comment system
- valine / waline article reading statistics
- Busuanzi Visitor Statistics
- RSS support
- Both iconfont and fontawesome are supported.
- Night mode
- Lazy image loading
- Load Animation
- TOC
- Mouse firework animation
- pjax
- ServiceWorker
- live2d
- reimu Mouse Pointer
- Internal shortcode for providing internal/external/friendly link cards
- Support the bottom of the article copyright statement
- Support for configuring custom CDN sources
- Highly customizable

## Installation

```bash
cd themes
git clone --single-branch --branch main https://github.com/D-Sketon/hugo-theme-reimu.git
```

And modify the theme in `hugo.toml`

```toml
theme = 'hugo-theme-reimu'
```

## Usage

<details>
<summary>Create Configuration</summary>

### Creating Configuration

#### Theme Configuration

Create a `_default` folder within the outer `config` directory, then copy `config/_default/params.yml` from the theme into this `_default` folder. This file serves as the theme configuration file, allowing theme settings to be modified.

#### Data Configuration

Copy all files from the theme's `config/data/` folder to the outer `data` folder. These files in the data folder are used to configure theme data:

- `covers.yml` to configure random cover images
- `friends.yml` to configure friend links
- `vendor.yml` to configure CDN sources for third-party libraries

#### Static Resource Configuration

Static resources for the theme (favicon, header images, etc.) are located in the `static` folder. You can create corresponding folders in the outer `static` directory and copy files from the theme to replace default files.

> In general, it is recommended not to modify the theme files directly. Instead, create corresponding folders in the outer directories and copy theme files into them to overwrite defaults. This makes upgrading the theme easier.

</details>
<details>

<summary>Basic Structure</summary>

### Basic Structure

To ensure correct display, refer to `_example` and create `archives` and `post` folders in the `content` directory (the `_index.md` inside cannot be omitted, and note that the `draft` in `post` is `true`)

#### archives

- `_index.md` used to display the archive page, cannot be omitted

#### post

Create articles in this directory, and note that articles with `draft` set to `true` will not be displayed on the homepage

- `_index.md` used to ignore the generation of `post/index.html`, cannot be omitted

#### about\.md

About page

#### friend\.md

Friend link page

</details>

<details>
<summary>Cover, Banner, and favicon</summary>

#### Cover

The logic for displaying the cover is as follows

- If the article's Front matter contains the url for cover, the article's header image and home page thumbnails display that url

```yaml
---
title: Hello World
cover: https://example.com
---
```

- If the article's Front matter contains cover as `false`, the article doesn't show the header image (it's still a random image on the front page)

```yaml
---
title: Hello World
cover: false
---
```

- If the article's Front matter contains cover as `rgb(xxx,xxx,xxx)`, the article's header image is the corresponding gradient solid color (still a random image on the front page)

```yaml
---
title: Hello World
cover: rgb(255,117,117)
---
```

- Otherwise, look for the `data` folder and `covers.yml` and pick a random image from it
- If none of these files exist, display the banner

#### banner

The banner is stored in `themes/hugo-theme-reimu/static/images/banner.webp` and can be modified in the `params.yml`

```yaml
banner: "images/banner.webp"
```

#### favicon

The icon is stored in `themes/hugo-theme-reimu/static/favicon.ico` and can be replaced by overwriting it

</details>
<details>
<summary>Code Highlighting</summary>

### Code Highlighting

To ensure that the code blocks are displayed correctly, please ensure that the `hugo.yml` is configured as follows

```toml
[markup.highlight]
guessSyntax = true
noClasses = false
```

The code block also provides a code paste function. Click the copy button in the upper right corner of the code block to copy the code. In the `params.yml`, you can configure the copy function.  
`success` is the prompt when the copy is successful, and `fail` is the prompt when the copy fails. In addition, you can configure the copyright statement. When the number of characters copied is greater than `count`, the content copied will be followed by the `content` copyright.

```yaml
clipboard:
  success: 复制成功(*^▽^*)
  fail: 复制失败 (ﾟ⊿ﾟ)ﾂ
  copyright:
    enable: false
    count: 50 # The number of characters when the copyright is displayed
    content: 本文版权：本博客所有文章除特别声明外，均采用 BY-NC-SA 许可协议。转载请注明出处！
```

</details>
<details>
<summary>Site comments</summary>

### Site comments

> In-site comments can be controlled independently of each post using `comments` in Front matter.  
> Comments are not shown when `comments` is `false`, and are shown or not shown when `true` or not filled in, depending on the `_config.yml` configuration.

If based on [Valine](https://valine.js.org/)  
Please refer to its official documentation to complete the configuration of `LeanCloud` and change `valine.enable` to `true` in the `params.yml` and fill in your own `appId` and `appKey`

```yaml
valine:
  enable: true
  appId: "your appId"
  appKey: "your appKey"
```

If based on [Waline](https://waline.js.org/)  
Please refer to its [official documentation](https://waline.js.org/guide/get-started/) to complete the `LeanCloud` configuration and change `waline.enable` to `true` in the `params.yml`, and fill in your own `serverURL`

```yaml
waline:
  enable: true
  serverURL: "your server url"
  lang: zh-CN
  locale: {} # https://waline.js.org/guide/features/i18n.html#%E8%87%AA%E5%AE%9A%E4%B9%89%E8%AF%AD%E8%A8%80
  emoji:
    - https://unpkg.com/@waline/emojis@1.2.0/weibo
    - https://unpkg.com/@waline/emojis@1.2.0/alus
    - https://unpkg.com/@waline/emojis@1.2.0/bilibili
    - https://unpkg.com/@waline/emojis@1.2.0/qq
    - https://unpkg.com/@waline/emojis@1.2.0/tieba
    - https://unpkg.com/@waline/emojis@1.2.0/tw-emoji
  meta:
    - nick
    - mail
    - link
  requiredMeta:
    - nick
    - mail
  wordLimit: 0
  pageSize: 10
  pageview: true
```

If based on [twikoo](https://twikoo.js.org)  
Please refer to its [official documentation](https://twikoo.js.org/quick-start.html) to complete the Tencent Cloud or Vercel deployment, and change `twikoo.enable` to `true` in the `params.yml`, and fill in your own `envId`.

```yml
twikoo:
  enable: true
  envId: # Tencent cloud environment fill envId; Vercel environment fill address (https://xxx.vercel.app)
  region:
```

If based on [giscus](https://giscus.app/zh-CN), please refer to the documentation to complete the configuration of the repository and change `giscus.enable` to `true` in the `params.yml`, and fill in the corresponding data.

```yml
giscus:
  enable: true
  repo: "your repo"
  repoId: "your repoId"
  category: "your category"
  categoryId: "your categoryId"
  mapping: mapping
  strict: 0
  reactionsEnabled: 1
  emitMetadata: 0
  inputPosition: bottom
  # commentTheme: preferred_color_scheme invalid
  lang: zh-CN
```

If based on [gitalk](https://gitalk.github.io/)  
Please refer to its [official documentation](https://github.com/gitalk/gitalk?tab=readme-ov-file#usage) to complete the repository configuration, and change `gitalk.enable` to `true` in the `params.yml` and fill in the corresponding data.

```yml
gitalk:
  enable: true
  clientID: "your application client ID"
  clientSecret: "your application client secret"
  repo: "your repo"
  owner: "repo owner"
  admin: "repo owner and collaborators"
  md5: false # Whether to use md5 to encrypt the path
```

</details>
<details>
<summary>Site search</summary>

Based on [Algolia](https://www.algolia.com/), please add the following configuration in the outer `hugo.toml`

```toml
[outputs]
home = ["Algolia", "HTML", "RSS"]

[outputFormats.Algolia]
baseName = "algolia"
isPlainText = true
mediaType = "application/json"
notAlternative = true
```

This will generate an `algolia.json` file in the `public` folder for Algolia search. Then you can use plugins such as `atomic-algolia` to upload it to Algolia.

At the same time, change `algolia_search.enable` to `true` in the `params.yml` and fill in the relevant information (**Note! The Search-Only Key is filled in here, and the Admin Key is not allowed to be filled in! Otherwise, it may be attacked**)

```yaml
algolia_search:
  enable: true
```

</details>
<details>

<summary>Mathematical formulas</summary>

### Mathematical formulas

Math formulas are based on [Katex](https://github.com/KaTeX/KaTeX), please add the following configuration in the outer `hugo.toml`

```toml
[markup.goldmark.extensions.passthrough]
enable = true
delimiters.block = [["\\[", "\\]"], ["$$", "$$"]]
delimiters.inline = [["\\(", "\\)"], ["$", "$"]]
```

And add `math` as `true` in the Front matter of the article that needs to use mathematical formulas

```yaml
---
math: true
---
```

</details>
<details>
<summary>Mermaid</summary>

### Mermaid

Diagram based on [Mermaid](https://mermaid.js.org/#/), please add `mermaid` as `true` in the Front matter of the article that needs to use the diagram

```yaml
---
mermaid: true
---
```

</details>
<details>
<summary>RSS</summary>

### RSS

RSS is built-in and does not require additional configuration

</details>

<details>
<summary>Icon</summary>

### Icon

Icon defaults to the iconfont provided with this project

```yml
icon_font: 4552607_tq6stt6tcg
```

If you want to continue using fontawesome icons, set `icon_font` to `false`, which will use the corresponding fontawesome in `vendor.yml`.

```yml
fontawesome:
  high_priority:
    - webcache|@fortawesome/fontawesome-free@6.5.1/css/regular.min.css
    - webcache|@fortawesome/fontawesome-free@6.5.1/css/solid.min.css
  low_priority:
    - webcache|@fortawesome/fontawesome-free@6.5.1/css/brands.min.css
    - webcache|@fortawesome/fontawesome-free@6.5.1/css/v5-font-face.min.css
    - webcache|@fortawesome/fontawesome-free@6.5.1/css/v4-font-face.min.css
```

</details>

<details>
<summary>Advanced features</summary>

### Advanced features

#### firework

Enabled by default

```yaml
firework:
  enable: true
```

See [mouse-firework](https://github.com/D-Sketon/mouse-firework) for more information

#### pjax

Disabled by default

```yaml
pjax:
  enable: false
```

> pjax was introduced for those who need to add music players and other users who need SPA. However, it is still experimental and may cause bugs such as **scripts not executing**, **scripts repeating**, **pages rendering mess**, etc. Please consider it carefully!

#### ServiceWorker

Disabled by default

```yaml
service_worker:
  enable: false
```

#### live2d

Disabled by default

```yaml
live2d:
  enable: false
```

#### reimu cursor

Enabled by default

```yml
reimu_cursor: true
```

#### Responsive Banner Image

Disabled by default, enable it on and providing the corresponding size of the image and media query can improve the LCP on mobile to some extent

```yml
banner_srcset:
enable: false
srcset:
  - src: "images/banner-600w.webp"
    media: "(max-width: 479px)"
  - src: "images/banner-800w.webp"
    media: "(max-width: 799px)"
  - src: "images/banner.webp"
    media: "(min-width: 800px)"
```

#### Article copyright notice

Disabled by default

```yml
article_copyright:
enable: false # Is the copyright card displayed?
content: # true | false Does the copyright card show the author?
  author: # true | false Do copyright cards show author?
  link: # true | false Do you want to show links?
  title: # true | false Do you show the title of the copyrighted card?
  date: # true | false The date the copyrighted card was created?
  updated: # true | false Copyright card show updated date?
  license: # true | false Copyright Card Showcase Agreement?
```

Besides, you can also control it through the front-matter of the article, which takes precedence over the global configuration

```yaml
---
copyright: true # Whether to display the copyright card
---
```

#### quicklink

Enabled by default

```yaml
quicklink:
  enable: true
  timeout: 3000 # Timeout for quicklink
  priority: true # Whether to prioritize loading the page
  ignores: [] # Ignore the specified link, only support string
```

#### outdate warning

Disabled by default

```yaml
outdate:
  enable: false
  daysAgo: 180 # The number of days after which the article is considered outdated
  message: 本文最后更新于 {time}，请注意文中内容可能已经发生变化。
```

#### sponsor

Disabled by default

```yaml
sponsor:
  enable: false # Whether to enable sponsorship
  tip: 请作者喝杯咖啡吧！ # Sponsorship prompt
  icon:
    url: "../images/taichi.png" # this path is relative to the css/style.css, so it needs to go up one level to reach the images folder
    rotate: true
    mask: true # whether to use the images as a mask
  qr:
    - name: 支付宝 # Payment method
      src: "sponsor/alipay.jpg" # QR code
```

Besides, you can also control it through the front-matter of the article, which takes precedence over the global configuration

```yaml
---
sponsor: true # Whether to display the sponsorship
---
```

</details>
<details>
<summary>Vendor</summary>

The `vendor.yml` path is now composed of `:cdn|:package@:version/:file`, and `:cdn` can be configured in `vendor` itself. It currently comes with the following CDN sources:

```yaml
cdn_jsdelivr_gh: https://cdn.jsdelivr.net/gh/ # github acceleration only
cdn_jsdelivr_npm: https://cdn.jsdelivr.net/npm/ # npm acceleration only
fastly_jsdelivr_gh: https://fastly.jsdelivr.net/gh/ # github acceleration only
fastly_jsdelivr_npm: https://fastly.jsdelivr.net/npm/ # npm acceleration only
unpkg: https://unpkg.com/ # npm acceleration only
webcache: https://npm.webcache.cn/ # npm acceleration only
```

Users can switch between CDN sources according to network conditions.

</details>

## License

MIT

function e(){let e=document.createElement(`canvas`),t=e.getContext(`webgl`,{failIfMajorPerformanceCaveat:!0})||e.getContext(`experimental-webgl`,{failIfMajorPerformanceCaveat:!0});return e.getContext(`webgl`)||e.getContext(`experimental-webgl`)?t?{webglSupported:!0,hardwareAccelerated:!0}:{webglSupported:!0,hardwareAccelerated:!1}:{webglSupported:!1,hardwareAccelerated:!1}}function t(){let e=document.createElement(`canvas`),t=e.getContext(`webgl`)||e.getContext(`experimental-webgl`);if(!t)return null;let n=t,r=n.getExtension(`WEBGL_debug_renderer_info`);if(r){let e=n.getParameter(r.UNMASKED_RENDERER_WEBGL),t=n.getParameter(r.UNMASKED_VENDOR_WEBGL);return{isSoftwareRenderer:[`swiftshader`,`software`,`llvmpipe`,`microsoft basic render`].some(t=>e.toLowerCase().includes(t)),renderer:e,vendor:t}}return null}var n=`axi-blog-graphics-warning-shown`,r=`axi-blog-webgl-support`;function i(){try{return localStorage.getItem(n)===`true`}catch{return!1}}function a(){try{localStorage.setItem(n,`true`)}catch{}}function o(){try{let e=localStorage.getItem(r);if(!e)return null;let t=JSON.parse(e),n=Date.now();return t.version!==`1.0`||n-t.timestamp>6048e5?(localStorage.removeItem(r),null):t}catch{return null}}function s(e){try{let t={...e,timestamp:Date.now(),version:`1.0`};localStorage.setItem(r,JSON.stringify(t))}catch{}}function c(){let e=window.location.pathname;return e.includes(`/en/`)||e.endsWith(`/en`)?`en`:`zh`}var l={zh:{performanceWarning:{title:`新版博客发布`,content:`
        <strong>新版博客已经发布</strong>，从 astro v5 升级到了 astro v7。
        
        <p><a href="https://github.com/rusin-dev/astro-theme-cyanwind">点击前往 github 查看</a></p>
        
        <p style="margin-top: 16px; opacity: 0.8; font-size: 14px;">
          💡 如果您只是访问我的博客，网站仍可正常使用。
        </p>
      `},button:`我知道了`},en:{performanceWarning:{title:`New Blog Version Released`,content:`
        <strong>The new blog version has been released</strong>, upgraded from Astro v5 to Astro v7.
        
        <p><a href="https://github.com/rusin-dev/astro-theme-cyanwind">Click here to view on GitHub</a></p>
        
        <p style="margin-top: 16px; opacity: 0.8; font-size: 14px;">
          💡 If you are just visiting my blog, the site will still work as usual.
        </p>
      `},button:`Got it`}},u=`axi-blog-graphics-warning-shown`;function d(e,t,n=`warning`){let r=l[c()].button,i=document.createElement(`div`);i.className=`graphics-warning-overlay`;let o=document.createElement(`div`);o.className=`graphics-warning-dialog`,o.innerHTML=`
    <div class="graphics-warning-header">
      <div class="${n===`error`?`graphics-warning-icon error`:`graphics-warning-icon`}">${n===`error`?`🚫`:`⚠️`}</div>
      <h3 class="graphics-warning-title">${e}</h3>
    </div>
    <div class="graphics-warning-content">
      ${t}
    </div>
    <div class="graphics-warning-actions">
      <button class="graphics-warning-btn" onclick="this.closest('.graphics-warning-overlay').remove(); localStorage.setItem('${u}', 'true')">
        ${r}
      </button>
    </div>
  `,i.appendChild(o),document.body.appendChild(i),i.addEventListener(`click`,e=>{e.target===i&&(a(),i.remove())});let s=e=>{e.key===`Escape`&&(a(),i.remove(),document.removeEventListener(`keydown`,s))};document.addEventListener(`keydown`,s),a()}function f(){let e=document.getElementById(`gradient-background`);e&&(e.style.display=`block`,e.style.opacity=`1`);let t=document.createElement(`style`);t.textContent=`
    header-component.not-top {
      background-color: hsl(var(--background) / 0.0) !important;
    }
    .dark header-component.not-top {
      background-color: hsl(var(--muted) / 0.0) !important;
    }
  `,document.head.appendChild(t)}function p(){let e=document.getElementById(`gradient-background`);e&&(e.style.opacity=`0`,setTimeout(()=>{e.style.display=`none`},1e3))}function m(e,t){document.getElementById(`gradient-background`)&&(!e||!t?p():f())}function h(){try{let n=e(),r=t();s({webglSupported:n.webglSupported,hardwareAccelerated:n.hardwareAccelerated&&!(r&&r.isSoftwareRenderer)});let i=o();i&&(!i.webglSupported||!i.hardwareAccelerated?p():f())}catch(e){console.log(e)}}function g(){if(!i())try{let n=c(),r=e(),i=t();if(s({webglSupported:r.webglSupported,hardwareAccelerated:r.hardwareAccelerated&&!(i&&i.isSoftwareRenderer)}),r.hardwareAccelerated)f();else{p();let e=l[n].performanceWarning;d(e.title,e.content,`warning`)}}catch(e){console.log(e)}}function _(){let e=o();e&&e?(m(e.webglSupported,e.hardwareAccelerated),setTimeout(h,1500)):setTimeout(g,1500)}document.readyState===`loading`?document.addEventListener(`DOMContentLoaded`,_):_();
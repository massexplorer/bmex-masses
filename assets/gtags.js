//async src="https://www.googletagmanager.com/gtag/js?id=G-F1LVDNTJDL"
function loadScript(src) {
    return new Promise(function (resolve, reject) {
        var s;
        s = document.createElement('script');
        s.src = src;
        s.onload = resolve;
        s.onerror = reject;
        document.head.appendChild(s);
    });
}

loadScript("https://www.googletagmanager.com/gtag/js?id=G-F1LVDNTJDL");

window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-F1LVDNTJDL');
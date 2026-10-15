from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,zipfile,re
root=Path('/home/user')
for size in [192,512]:
 im=Image.new('RGB',(size,size),'#173d32');d=ImageDraw.Draw(im)
 d.rounded_rectangle((size*.19,size*.29,size*.81,size*.72),radius=int(size*.06),fill='#dcf783')
 d.rounded_rectangle((size*.26,size*.38,size*.42,size*.57),radius=int(size*.025),fill='#173d32')
 for y,w in [(.4,.24),(.48,.19),(.61,.44)]:d.rounded_rectangle((size*.49 if y<.6 else size*.27,size*y,size*(.49+w) if y<.6 else size*.71,size*(y+.035)),radius=int(size*.008),fill='#173d32')
 d.ellipse((size*.65,size*.17,size*.79,size*.31),fill='#ffffff')
 im.save(root/f'icon-{size}.png')
manifest={'id':'./','name':'MAO Baggao Farmer ID Generator','short_name':'Fieldcard','description':'Create farmer IDs from RSBSA CSV records. MAO Baggao, Cagayan.','start_url':'./index.html','scope':'./','display':'standalone','background_color':'#f5f6f0','theme_color':'#173d32','icons':[{'src':f'icon-{n}.png','sizes':f'{n}x{n}','type':'image/png','purpose':'any maskable'} for n in [192,512]]}
(root/'manifest.webmanifest').write_text(json.dumps(manifest,indent=2))
(root/'sw.js').write_text('''const CACHE='fieldcard-pwa-v1';
const ASSETS=['./','./index.html','./manifest.webmanifest','./icon-192.png','./icon-512.png'];
self.addEventListener('install',event=>{event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(ASSETS)))});
self.addEventListener('activate',event=>{event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>key.startsWith('fieldcard-pwa-')&&key!==CACHE).map(key=>caches.delete(key)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',event=>{
 if(event.request.method!=='GET'||new URL(event.request.url).origin!==self.location.origin)return;
 if(event.request.mode==='navigate'){
  event.respondWith(fetch(event.request).then(response=>{if(response.ok){const copy=response.clone();event.waitUntil(caches.open(CACHE).then(cache=>cache.put('./index.html',copy)))}return response}).catch(()=>caches.match('./index.html')));return;
 }
 event.respondWith(caches.match(event.request).then(cached=>cached||fetch(event.request)));
});
''')
p=root/'index.html';s=p.read_text();s=s.replace('<title>Fieldcard • MAO Baggao</title>', '<title>Fieldcard • MAO Baggao</title><link rel="manifest" href="./manifest.webmanifest"><meta name="theme-color" content="#173d32"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="default"><link rel="apple-touch-icon" href="./icon-192.png">')
s=s.replace('<button onclick="openSettings()">⚙ Settings</button>','<button id="installApp" onclick="installPWA()" class="hidden">↓ Install app</button><button onclick="openSettings()">⚙ Settings</button>',1)
s=s.replace('refresh();\n</script>', '''let installPrompt=null;
window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();installPrompt=e;$('installApp').classList.remove('hidden')});
window.addEventListener('appinstalled',()=>{installPrompt=null;$('installApp').classList.add('hidden');notify('Fieldcard installed.')});
async function installPWA(){if(!installPrompt)return;await installPrompt.prompt();await installPrompt.userChoice;installPrompt=null;$('installApp').classList.add('hidden')}
if('serviceWorker' in navigator&&/^https?:$/.test(location.protocol)){
 window.addEventListener('load',()=>navigator.serviceWorker.register('./sw.js').then(reg=>{
  const updateReady=()=>notify('App update ready. Close all Fieldcard windows and reopen to apply.');
  if(reg.waiting)updateReady();
  reg.addEventListener('updatefound',()=>{const worker=reg.installing;if(worker)worker.addEventListener('statechange',()=>{if(worker.state==='installed'){if(navigator.serviceWorker.controller)updateReady();else notify('App cached. Ready for offline use.')}})});
 }).catch(()=>notify('Offline installation is unavailable here. Host all app files on HTTPS to enable the PWA.')));
}
refresh();
</script>''')
p.write_text(s)
r=root/'README.md';t=r.read_text();t+='''
## PWA installation and deployment
This app is now a Progressive Web App (PWA). Upload all files from the ZIP, keeping them together, to a static **HTTPS** host. No backend is needed. Do not host only index.html: the manifest, service worker, and icons are required. The host must serve sw.js as JavaScript and must not redirect it to HTML. A dedicated directory/subdomain is recommended.

1. Visit the hosted app online once and wait for the offline-ready message.
2. Chrome/Edge (Android or desktop): use **Install app** when shown, or the browser's Install app menu.
3. iPhone/iPad: open the HTTPS URL in Safari, then Share → Add to Home Screen.
4. Launch the installed app. The interface, QR codes, CSV imports, printing, and image generation work offline after caching. Download and printing capabilities depend on the device/browser.

Opening index.html directly still works as a standalone static app, but file:// cannot install or cache a PWA. Local development can use http://localhost. The in-app file preview is not a PWA host.

The PWA caches the app files only, not farmer records. Farmer records/photos are still session-only: closing/reloading the app clears them. Installation does not create a farmer database. Office settings/logo remain in local browser storage and are specific to that host/browser.

For updates, deploy the updated files and bump CACHE in sw.js (e.g. fieldcard-pwa-v2). Revisit online, then close all app windows and reopen when prompted. Clear site data/unregister the service worker to completely remove cached app files and settings.

Files: index.html, manifest.webmanifest, sw.js, icon-192.png, icon-512.png, README.md.
''';r.write_text(t)
with zipfile.ZipFile(root/'MAO-Baggao-Farmer-ID.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in ['index.html','manifest.webmanifest','sw.js','icon-192.png','icon-512.png','README.md']:z.write(root/f,f)
(root/'check.js').write_text('\n'.join(re.findall(r'<script>(.*?)</script>',s,re.S)))

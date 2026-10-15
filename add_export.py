from pathlib import Path
p=Path('/home/user/index.html');s=p.read_text()
s=s.replace('<button id="printAll" onclick="printIDs(true)" disabled>Print filtered IDs</button>','<button id="printAll" onclick="printIDs(true)" disabled>Print filtered IDs</button><button id="saveImages" onclick="saveImages()" disabled>↓ Save as images</button>')
s=s.replace('<div id="printZone"></div>','<dialog id="imageDownloads"><h2>Your ID images are ready.</h2><p>Download each side as a separate high-resolution PNG. Both files include the current office settings and farmer details.</p><div class="actions"><a id="downloadFront" class="image-link" download>↓ Download front</a><a id="downloadBack" class="image-link" download>↓ Download back</a><button onclick="document.getElementById(\'imageDownloads\').close()">Done</button></div><p class="small">Keep these images secure: they contain personal information. Printed size depends on your print settings.</p></dialog><div id="printZone"></div>')
s=s.replace('</style>', '.image-link{display:inline-block;padding:12px 16px;border-radius:10px;background:var(--green);color:white;text-decoration:none;font-size:14px;font-weight:600}</style>')
s=s.replace('<script>\nconst $=', '<script>'+Path('/home/user/html2canvas.min.js').read_text()+'</script><script>\nconst $=')
s=s.replace("$('photoBtn').disabled=!f}","$('photoBtn').disabled=!f;$('saveImages').disabled=!f}")
s=s.replace('function openSettings(){',r'''let exportURLs=[];
function releaseImages(){exportURLs.forEach(u=>URL.revokeObjectURL(u));exportURLs=[];['downloadFront','downloadBack'].forEach(id=>$(id).removeAttribute('href'))}
$('imageDownloads').addEventListener('close',releaseImages);
async function saveImages(){
 const f=farmers[selected];if(!f)return;
 const button=$('saveImages');button.disabled=true;button.textContent='Preparing images…';
 releaseImages();
 const stage=document.createElement('div');stage.style.cssText='position:fixed;left:-10000px;top:0;width:360px;pointer-events:none;';
 stage.innerHTML=card(f,false)+card(f,true);document.body.appendChild(stage);
 try{
  addQR(stage);
  await Promise.all([...stage.querySelectorAll('img')].map(im=>im.decode?im.decode():Promise.resolve()));
  const cards=[...stage.querySelectorAll('.idcard')];
  const filename=(f.rsbsa||f.name).replace(/[^a-zA-Z0-9_-]/g,'_').slice(0,100);
  for(let i=0;i<cards.length;i++){
   const canvas=await html2canvas(cards[i],{scale:4,backgroundColor:null,logging:false,scrollX:0,scrollY:0});
   const blob=await new Promise((resolve,reject)=>canvas.toBlob(b=>b?resolve(b):reject(Error('Image export failed.')),'image/png'));
   const url=URL.createObjectURL(blob);exportURLs.push(url);
   const link=$(i===0?'downloadFront':'downloadBack');link.href=url;link.download=`MAO-Baggao-${filename}-${i===0?'front':'back'}.png`;
  }
  $('imageDownloads').showModal();
 }catch(err){releaseImages();notify('Could not create images. Please try again or use Print this ID.');console.error(err)}
 finally{stage.remove();button.disabled=!farmers[selected];button.textContent='↓ Save as images'}
}
function openSettings(){''')
s=s.replace("farmers=[];selected=-1;isDemo=false;", "releaseImages();farmers=[];selected=-1;isDemo=false;")
p.write_text(s)
r=Path('/home/user/README.md');t=r.read_text();t=t.replace('## Data and limitations','6. Click **Save as images** for the selected farmer. Download the front and back separately from the dialog as 1440 × 908 pixel PNG files. Both sides render regardless of the currently visible preview side. Export is entirely local and works offline.\n\n## Data and limitations');t+='\nImage export: html2canvas 1.4.1 (MIT), bundled inside index.html.\n';r.write_text(t)
import zipfile,re
with zipfile.ZipFile('/home/user/MAO-Baggao-Farmer-ID.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in ['index.html','README.md']:z.write('/home/user/'+f,f)
Path('/home/user/check.js').write_text('\n'.join(re.findall(r'<script>(.*?)</script>',s,re.S)))

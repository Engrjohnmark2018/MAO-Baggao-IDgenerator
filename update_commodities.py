from pathlib import Path
p=Path('index.html');s=p.read_text()
s=s.replace("<div class=\"idfoot\">ROOTED HERE. GROWING FORWARD.<span>${isDemo?'SAMPLE ONLY · NOT VALID FOR IDENTIFICATION':'RSBSA-REGISTERED · MAO BAGGAO'}</span></div>",'<div class="idfoot"><div style="max-width:260px;font-size:7px;line-height:1.5;letter-spacing:.2px">THIS WILL SERVE AS YOUR VALID ID WHEN TRANSACTING TO MAO-BAGGAO,CAGAYAN.</div></div>')
s=s.replace('<button id="saveImages"', '<button id="commodityBtn" onclick="openCommodities()" disabled>Edit commodities</button><button id="saveImages"')
s=s.replace('<dialog id="imageDownloads">','<dialog id="commoditiesDialog"><h2>Farmer commodities</h2><p>Select all crops this farmer tills. Changes apply to the preview, printed ID, and image exports for this session.</p><label><input type="checkbox" id="cropRice"> Rice</label><label><input type="checkbox" id="cropCorn"> Corn</label><label><input type="checkbox" id="cropVegetables"> Vegetables</label><label for="otherCrops">Other commodities (separate with commas)</label><input id="otherCrops" placeholder="e.g. Banana, Coconut"><div class="actions"><button onclick="document.getElementById(\'commoditiesDialog\').close()">Cancel</button><button class="primary" onclick="saveCommodities()">Save commodities</button></div></dialog><dialog id="imageDownloads">')
s=s.replace("$('saveImages').disabled=!f}","$('saveImages').disabled=!f;$('commodityBtn').disabled=!f}")
s=s.replace("['commodity','Commodity / livelihood',['commodity','crop','livelihood','main livelihood']]", "['commodity','Commodities / livelihood',['commodity','commodities','crop','crops','livelihood','main livelihood']]")
s=s.replace("d.name=d.full||", "d.commodity=splitCommodities(d.commodity).join(', ');d.name=d.full||")
s=s.replace("${f.commodity?'<br>'+esc(f.commodity):''}","${f.commodity?'<br><span style=\"display:block;max-height:20px;overflow:hidden;line-height:10px\">Crops: '+esc(f.commodity)+'</span>':''}")
s=s.replace('let exportURLs=[];',r'''function splitCommodities(value){return [...new Map(String(value||'').split(/[,;|\n]+/).map(x=>x.trim()).filter(Boolean).map(x=>[x.toLowerCase(),x])).values()]}
function openCommodities(){const f=farmers[selected];if(!f)return;let values=splitCommodities(f.commodity);['Rice','Corn','Vegetables'].forEach(c=>$('crop'+c).checked=values.some(x=>x.toLowerCase()===c.toLowerCase()));$('otherCrops').value=values.filter(x=>!['rice','corn','vegetables'].includes(x.toLowerCase())).join(', ');$('commoditiesDialog').showModal()}
function saveCommodities(){const f=farmers[selected];if(!f)return;f.commodity=splitCommodities([...['Rice','Corn','Vegetables'].filter(c=>$('crop'+c).checked),$('otherCrops').value].filter(Boolean).join(', ')).join(', ');$('commoditiesDialog').close();releaseImages();$('printZone').innerHTML='';renderPreview();notify('Farmer commodities updated for this session.')}
let exportURLs=[];''')
s=s.replace("commodity:'Rice'", "commodity:'Rice, Corn'")
p.write_text(s)
r=Path('README.md');t=r.read_text();t+='''
## Multiple commodities
Click **Edit commodities** for the selected farmer. Select Rice, Corn, Vegetables, and/or enter other commodities. The ID displays the selected crops; changes last for the current session.
In CSV, use a quoted value such as `"Rice, Corn"` in the Commodity column, or `Rice; Corn` / `Rice|Corn`. Duplicate values are removed. Inspect the preview if a farmer has many crops, since card space is limited.

The front footer now reads: THIS WILL SERVE AS YOUR VALID ID WHEN TRANSACTING TO MAO-BAGGAO,CAGAYAN. This wording is user-configured; office approval is still required before issuance. Demo farmers remain marked DEMO in the farmer heading.
''';r.write_text(t)
import zipfile,re
with zipfile.ZipFile('MAO-Baggao-Farmer-ID.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in ['index.html','README.md']:z.write(f)
Path('check.js').write_text('\n'.join(re.findall(r'<script>(.*?)</script>',s,re.S)))

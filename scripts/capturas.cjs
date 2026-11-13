// Uso: node scripts/capturas.cjs; requiere Playwright y Chromium/Edge.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
 const root=path.resolve(__dirname,'..'), out=path.join(root,'evidencia');
 fs.mkdirSync(out,{recursive:true});
 const browser=await chromium.launch({channel:'msedge',headless:true});
 try {
  const page=await browser.newPage({viewport:{width:1280,height:950},deviceScaleFactor:1.5});
  await page.goto('http://127.0.0.1:8000/');
  const base='http://127.0.0.1:8000/api/vehiculos/';
  const vehicle={marca:'Toyota',modelo:'Corolla',anio:2024,color:'Blanco'};
  const results=[];
  async function run(title,method,url,body,expected){
   await page.locator('#case').evaluate((el,t)=>el.textContent=t,title);
   await page.locator('#method').selectOption(method);
   await page.locator('#url').fill(url);
   await page.locator('#body').fill(body?JSON.stringify(body,null,2):'');
   const responsePromise=page.waitForResponse(r=>r.url()===url&&r.request().method()===method);
   await page.locator('#send').click();
   const response=await responsePromise;
   await page.waitForFunction(()=>!document.querySelector('#send').disabled);
   if(response.status()!==expected) throw Error(title+': '+response.status());
   const result=response.status()===204?null:await response.json();
   results.push({titulo:title,metodo:method,url,enviado:body,estado:response.status(),respuesta:result});
   await page.screenshot({path:path.join(out,title.slice(0,2)+'.png'),fullPage:true});
   return result;
  }
  const created=await run('01 Crear vehículo','POST',base,vehicle,201);
  const detail=base+created.id+'/';
  await run('02 Listar vehículos','GET',base,null,200);
  await run('03 Consultar por ID','GET',detail,null,200);
  const updated=await run('04 Actualizar vehículo','PUT',detail,{...vehicle,color:'Azul'},200);
  if(updated.color!=='Azul') throw Error('Actualización no persistida');
  await run('05 Validar datos inválidos','POST',base,{marca:'',anio:1800},400);
  await run('06 Eliminar vehículo','DELETE',detail,null,204);
  const deleted=await page.request.get(detail);
  if(deleted.status()!==404) throw Error('Eliminación no persistida');
  fs.writeFileSync(path.join(out,'pruebas-capturadas.json'),JSON.stringify(results,null,2));
  console.log('6 capturas reales y estados HTTP verificados.');
 } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exit(1)});

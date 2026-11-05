const $=s=>document.querySelector(s),F=(a,b)=>`<span class="fr"><i>${a}</i><i>${b}</i></span>`;
const root=document.documentElement,saved=(()=>{try{return localStorage.theme}catch(e){}})();
function setT(t){root.dataset.theme=t;$('#th').textContent=t=='dark'?'☀️ Claro':'🌙 Escuro';try{localStorage.theme=t}catch(e){}}
setT(saved||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'));
$('#th').onclick=()=>setT(root.dataset.theme=='dark'?'light':'dark');
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{document.querySelectorAll('nav button,section').forEach(e=>e.classList.remove('on'));b.classList.add('on');$('#'+b.dataset.t).classList.add('on')});
async function demo(p,q){if(p){$('#p').value=p;$('#q').value=q}
 const r=await(await fetch(`/api/decompose?p=${$('#p').value}&q=${$('#q').value}`)).json();
 if(r.error){$('#out').innerHTML=`<div class="card"><span class="bad">${r.error}</span></div>`;return}
 let h=`<div class="card gold big">${F(r.p,r.q)} = ${r.steps.map(s=>F(1,s.k)).join(' + ')}</div>`;
 r.steps.forEach((s,i)=>{const end=s.p1=='0';h+=`<div class="card"><b>Passo ${i+1}.</b> Fração atual ${F(s.p,s.q)}<br>
 k = ⌈${s.q}/${s.p}⌉ = <b>${s.k}</b>, logo ${F(1,s.k)} ≤ ${F(s.p,s.q)} &lt; ${F(1,s.k-1)}<br>
 Resto = ${F(s.p+'·'+s.k+' − '+s.q,s.q+'·'+s.k)} = ${F(s.p1,s.q1)}${end?'':' = '+F(s.rn,s.rd)}<br>
 ${end?'<span class="ok">Caso (i): a fração era unitária - fim.</span>':`Caso (ii): numerador caiu de ${s.p} para ${s.p1} (p₁ = pk − q &lt; p). Continua com ${F(s.rn,s.rd)}.`}</div>`});
 h+='<div class="card"><b>Verificações automáticas</b><br>'+Object.entries(r.checks).map(([k,v])=>`<span class="${v?'ok':'bad'}">${v?'✓':'✗'}</span> ${k}`).join('<br>')+'</div>';
 $('#out').innerHTML=h}
async function test(){$('#tout').innerHTML='<div class="card">Executando…</div>';
 const r=await(await fetch('/api/test?n='+$('#n').value)).json(),mx=Math.max(...Object.values(r.hist));
 $('#tout').innerHTML=`<div class="card gold big"><span class="${r.fails.length?'bad':'ok'}">${r.ok} de ${r.total}</span> frações aprovadas em todas as verificações (q ≤ ${r.n}).${r.fails.length?'<br>Falhas: '+r.fails.join(', '):''}</div>
 <div class="card">Maior nº de termos: <b>${r.maxterms[0]}</b> (${F(r.maxterms[1],r.maxterms[2])}) · Maior denominador: <b>${r.maxdigits[0]} dígitos</b> (${F(r.maxdigits[1],r.maxdigits[2])})</div>
 <h3>Distribuição do nº de termos</h3>`+Object.entries(r.hist).map(([k,v])=>`<div class="bar"><b style="width:28px">${k}</b><span style="width:${v/mx*60}%"></span>${v}</div>`).join('')+
 `<h3>Tabela 2/n (n ímpar, 5 a 101)</h3><table><tr><th>n</th><th>2/n pelo algoritmo voraz</th></tr>${r.t2n.map(([n,t])=>`<tr><td>${n}</td><td>${t}</td></tr>`).join('')}</table>`}
demo();

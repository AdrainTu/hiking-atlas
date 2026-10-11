/* Anonymous first-party measurement. Browser IDs never link to accounts. */
(() => {
 const random=()=>Array.from(crypto.getRandomValues(new Uint8Array(16)),x=>x.toString(16).padStart(2,'0')).join('');
 let visitor;
 try {visitor=localStorage.getItem('atlas-visitor');if(!/^[a-f0-9]{32}$/.test(visitor||'')){visitor=random();localStorage.setItem('atlas-visitor',visitor);}}catch{visitor=random();}
 let last=null;
 function track(){if(document.visibilityState!=='visible')return;let route;try{route=decodeURIComponent(location.hash.slice(1));}catch{return;}if(route===last)return;last=route;fetch('/api/analytics/event',{method:'POST',credentials:'same-origin',keepalive:true,headers:{'Content-Type':'application/json','X-Atlas-Request':'1'},body:JSON.stringify({visitor,event:random(),route})}).catch(()=>{});}
 track();window.addEventListener('hashchange',track);document.addEventListener('visibilitychange',track);
 let revision=0;
 async function permission(){const current=++revision;document.getElementById('analytics-open')?.remove();try{const r=await fetch('/api/analytics/permissions',{cache:'no-store'});const data=await r.json();if(current!==revision||!data.canView)return;const link=document.createElement('a');link.id='analytics-open';link.href='/dashboard.html';link.textContent='▥ 访问统计';link.style.cssText='color:inherit;margin-left:12px;white-space:nowrap';document.getElementById('account-open').parentElement.append(link);}catch{}}
 window.addEventListener('atlas-account',permission);permission();
})();

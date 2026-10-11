/* Province cartogram: each block is a touch target, not an administrative boundary. */
(()=>{
 const provinces=[['新疆',0,1],['西藏',0,3],['青海',1,2],['甘肃',2,2],['宁夏',3,2],['内蒙古',4,0],['黑龙江',7,0],['吉林',7,1],['辽宁',6,1],['北京',5,1],['天津',6,2],['河北',5,2],['山西',4,2],['陕西',3,3],['四川',2,4],['重庆',3,4],['云南',2,6],['贵州',3,5],['广西',4,6],['海南',5,7],['河南',4,3],['山东',5,3],['江苏',6,3],['上海',7,3],['安徽',5,4],['湖北',4,4],['湖南',4,5],['江西',5,5],['浙江',6,4],['福建',6,5],['广东',5,6],['香港',6,6],['澳门',6,7],['台湾',7,5]];
 const root=document.createElement('section');root.id='region-browser';root.hidden=true;root.setAttribute('aria-label','按省区浏览徒步线路');
 document.querySelector('.map-stage').append(root);
 let config,mode='blocks';
 const el=(tag,text,cls)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;};
 function render(next){config=next;const visible=next.scope==='china'&&!next.selected&&mode==='blocks';root.hidden=!visible;document.querySelector('.map-stage').classList.toggle('region-mode',visible);if(!visible)return;
 root.replaceChildren();const head=el('div',undefined,'region-heading');const title=el('div');title.append(el('small','CHINA · EXPLORE BY REGION'),el('h2',next.province?next.province+' · 山野线路':'先选一片山野'));head.append(title);const mapButton=el('button','切换地图');mapButton.onclick=()=>{mode='map';render(config);};head.append(mapButton);root.append(head);
 const controls=el('div',undefined,'region-controls');if(next.province){const back=el('button','← 全部省区');back.onclick=()=>next.choose('');controls.append(back);}controls.append(el('p',next.province?'点击线路查看照片、难度、装备与详细介绍。':'点击省区色块，展开当地路线。颜色越亮，当前筛选下的路线越多。'));root.append(controls);
 if(next.province){const routes=el('div',undefined,'region-routes');for(const route of next.filtered){const b=el('button',undefined,'region-route');const photo=window.AtlasRegionPhotos?.[route.id]?.[0];if(photo){const img=el('img');img.src=photo.url;img.alt=route.name;img.loading='lazy';b.append(img);}const body=el('span');body.append(el('strong',route.name),el('small',`${route.level===2?'中等':route.level===3?'困难':'挑战'} · ${route.duration} · ${route.distance?'约 '+route.distance+' km':'里程待核实'}`));if(route.infoOnly)body.append(el('small','资料展示 · 出发前核实通行'));b.append(body,el('span','↗'));b.onclick=()=>next.select(route.id);routes.append(b);}if(!next.filtered.length)routes.append(el('p','当前筛选下暂无线路。可清除难度、月份等筛选，或分享你的线路。'));root.append(routes);
 }else{const grid=el('div',undefined,'province-grid');for(const [name,x,y] of provinces){const count=next.filtered.filter(r=>r.province?.split(' / ').includes(name)).length;const button=el('button',undefined,'province-block'+(count?' has-routes':''));button.style.gridColumn=x+1;button.style.gridRow=y+1;button.style.setProperty('--block-alpha',String(.15+Math.min(count,15)/20));button.append(el('strong',name),el('small',count+' 条'));button.setAttribute('aria-label',name+'，'+count+' 条线路');button.onclick=()=>next.choose(name);grid.append(button);}root.append(grid);}
 root.append(el('p','省区色块按大致方位排列，属于浏览示意，不表示行政边界；跨省线路会出现在相关省区。','region-note'));
 }
 const toggle=el('button','▦ 省区色块','region-toggle');toggle.hidden=true;document.querySelector('.map-tools').prepend(toggle);toggle.onclick=()=>{mode='blocks';render(config);};
 window.AtlasRegions={render(next){toggle.hidden=next.scope!=='china';render(next);},provinces:provinces.map(x=>x[0])};
})();

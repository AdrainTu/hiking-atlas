/* Filled province polygons; display geometry sourced from Alibaba DataV. */
(()=>{
 const provinces=[['新疆',0,1],['西藏',0,3],['青海',1,2],['甘肃',2,2],['宁夏',3,2],['内蒙古',4,0],['黑龙江',7,0],['吉林',7,1],['辽宁',6,1],['北京',5,1],['天津',6,2],['河北',5,2],['山西',4,2],['陕西',3,3],['四川',2,4],['重庆',3,4],['云南',2,6],['贵州',3,5],['广西',4,6],['海南',5,7],['河南',4,3],['山东',5,3],['江苏',6,3],['上海',7,3],['安徽',5,4],['湖北',4,4],['湖南',4,5],['江西',5,5],['浙江',6,4],['福建',6,5],['广东',5,6],['香港',6,6],['澳门',6,7],['台湾',7,5]];
 const root=document.createElement('section');root.id='region-browser';root.hidden=true;root.setAttribute('aria-label','按省区浏览徒步线路');
 document.querySelector('.map-stage').append(root);
 let config,mode='blocks',boundaryData=null,boundaryMap=null,savedView=null;
 fetch('china-provinces.json').then(r=>{if(!r.ok)throw Error('boundary load');return r.json();}).then(data=>{boundaryData=data;if(config)render(config);}).catch(()=>{if(config){root.append(el('p','省区轮廓加载失败，请刷新重试。'));}});
 const shortName=full=>provinces.find(([name])=>full.startsWith(name))?.[0]||'';
 function drawBoundaries(next){
   const holder=el('div',undefined,'province-boundary-map');holder.setAttribute('aria-label','中国省区着色地图，可缩放并点击省份');root.append(holder);
   if(!boundaryData){holder.textContent='正在加载省区轮廓…';return;}
   if(!window.L){holder.textContent='地图组件加载失败，请刷新。';return;}
   boundaryMap=L.map(holder,{zoomControl:true,attributionControl:true,minZoom:2,maxZoom:9,zoomSnap:.25,scrollWheelZoom:true});
   const colors=['#64998c','#80bb9b','#a5ce92','#d2d789','#e7ba77','#d48e6c'];
   L.geoJSON(boundaryData,{style:feature=>{const name=shortName(feature.properties.name||'');const count=next.filtered.filter(r=>r.province?.split(' / ').includes(name)).length;const index=provinces.findIndex(([n])=>n===name);return {color:'#e3f5d9',weight:2.5,opacity:.95,fillColor:name?colors[(index+colors.length)%colors.length]:'#648278',fillOpacity:count?.85:.4};},onEachFeature:(feature,layer)=>{const name=shortName(feature.properties.name||'');if(!name)return;const count=next.filtered.filter(r=>r.province?.split(' / ').includes(name)).length;const text=el('span',name+' · '+count+' 条');layer.bindTooltip(text,{sticky:true,direction:'top'});layer.on('mouseover',()=>layer.setStyle({weight:4,fillOpacity:1}));layer.on('mouseout',()=>layer.setStyle({weight:2.5,fillOpacity:count?.85:.4}));layer.on('click',()=>next.choose(name));
     const center=feature.properties.centroid||feature.properties.center;if(center && !['香港','澳门','北京','天津','上海'].includes(name)){const label=L.divIcon({className:'province-map-label',html:'<span>'+name+'</span><small>'+count+' 条</small>',iconSize:[60,36],iconAnchor:[30,18]});L.marker([center[1],center[0]],{icon:label,title:name+'，'+count+'条线路',keyboard:true}).on('click',()=>next.choose(name)).addTo(boundaryMap);}
   }}).addTo(boundaryMap);
   boundaryMap.attributionControl.addAttribution('<a href="https://datav.aliyun.com/portal/school/atlas/area_selector" target="_blank" rel="noopener">省区轮廓 · 阿里云 DataV</a>');
   if(savedView)boundaryMap.setView(savedView.center,savedView.zoom);else boundaryMap.fitBounds([[17.5,73],[54,136]],{padding:[12,12]});
   boundaryMap.on('moveend',()=>{savedView={center:boundaryMap.getCenter(),zoom:boundaryMap.getZoom()};});
   requestAnimationFrame(()=>boundaryMap?.invalidateSize({pan:false}));
   const quick=el('div',undefined,'province-quick-select');for(const name of ['北京','天津','上海','香港','澳门']){const b=el('button',name);b.onclick=()=>next.choose(name);quick.append(b);}root.append(quick);
 }

 const el=(tag,text,cls)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;};
 function render(next){config=next;const visible=next.scope==='china'&&!next.selected&&mode==='blocks';if(!visible&&boundaryMap){boundaryMap.remove();boundaryMap=null;}root.hidden=!visible;document.querySelector('.map-stage').classList.toggle('region-mode',visible);if(!visible)return;
 if(boundaryMap){boundaryMap.remove();boundaryMap=null;}root.replaceChildren();const head=el('div',undefined,'region-heading');const title=el('div');title.append(el('small','CHINA · EXPLORE BY REGION'),el('h2',next.province?next.province+' · 山野线路':'点击省份，探索山野'));head.append(title);const mapButton=el('button','查看路线地图');mapButton.onclick=()=>{mode='map';render(config);};head.append(mapButton);root.append(head);
 const controls=el('div',undefined,'region-controls');if(next.province){const back=el('button','← 全部省区');back.onclick=()=>next.choose('');controls.append(back);}controls.append(el('p',next.province?'点击线路查看照片、难度、装备与详细介绍。':'点击地图上的省份色块查看线路。双指或使用 ＋ / − 放大地图。'));root.append(controls);
 if(next.province){const routes=el('div',undefined,'region-routes');for(const route of next.filtered){const b=el('button',undefined,'region-route');const photo=window.AtlasRegionPhotos?.[route.id]?.[0];if(photo){const img=el('img');img.src=photo.url;img.alt=route.name;img.loading='lazy';b.append(img);}const body=el('span');body.append(el('strong',route.name),el('small',`${route.level===2?'中等':route.level===3?'困难':'挑战'} · ${route.duration} · ${route.distance?'约 '+route.distance+' km':'里程待核实'}`));if(route.infoOnly)body.append(el('small','资料展示 · 出发前核实通行'));b.append(body,el('span','↗'));b.onclick=()=>next.select(route.id);routes.append(b);}if(!next.filtered.length)routes.append(el('p','当前筛选下暂无线路。可清除难度、月份等筛选，或分享你的线路。'));root.append(routes);
 }else{drawBoundaries(next);}
 root.append(el('p','省区轮廓来源：阿里云 DataV；已简化用于浏览，不作导航。跨省线路会出现在相关省区。','region-note'));
 }
 const toggle=el('button','▦ 省区色块','region-toggle');toggle.hidden=true;document.querySelector('.map-tools').prepend(toggle);toggle.onclick=()=>{mode='blocks';render(config);};
 window.AtlasRegions={render(next){toggle.hidden=next.scope!=='china';render(next);},provinces:provinces.map(x=>x[0])};
})();

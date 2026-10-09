'use strict';
(() => {
  const trails = window.TRAILS;
  const meta = window.TRAIL_META;
  const $ = id => document.getElementById(id);
  const escape = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const safeUrl = url => { try { const parsed = new URL(url); if(parsed.protocol==='http:') parsed.protocol='https:'; return parsed.protocol === 'https:' ? parsed.href : ''; } catch { return ''; } };
  const external = (url, text) => `<a href="${escape(safeUrl(url))}" target="_blank" rel="noopener noreferrer">${escape(text)}</a>`;
  const detailTabs = ['overview','itinerary','gear','media'];
  const knownIds = new Set(trails.map(route => route.id));
  const state = {scope:"china",selected:null,tab:'overview',photos:{},favorites:new Set(),completed:new Set(),onlyCompleted:false,compare:[],gear:{},onlyFavorites:false,filtered:trails,photoIndex:0};
  let map, tiles, routeLayers = new Map(), selectedLayer, traveler, toastTimer, tourFrame;
  let tourPlaying = false, tourValue = 0;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let accountUser=null,saveQueue=Promise.resolve(),saveRevision=0,dirty=false;

  try {
    const saved = JSON.parse(localStorage.getItem('trail-atlas-v1') || '{}');
    if (Array.isArray(saved.favorites)) state.favorites = new Set(saved.favorites.filter(id => (knownIds.has(id)||/^u-[a-z0-9-]{1,48}$/.test(id))));
    if (saved.gear && typeof saved.gear === 'object' && !Array.isArray(saved.gear)) {
      for (const route of trails) if (Array.isArray(saved.gear[route.id])) state.gear[route.id] = saved.gear[route.id].filter(index => Number.isInteger(index) && index >= 0 && index < route.gear.length);
    }
  } catch { /* 存储不可用时仍可浏览；本次会话继续保留状态。 */ }

  function save() {
    const data={favorites:[...state.favorites],completed:[...state.completed],gear:JSON.parse(JSON.stringify(state.gear))};
    try { localStorage.setItem(accountUser?'trail-atlas-user-'+accountUser.id:'trail-atlas-v1', JSON.stringify(data)); }
    catch { toast('浏览器未允许保存，本次会话仍可使用收藏和装备清单。'); }
    if(accountUser){
      dirty=true;const revision=++saveRevision,payload={...data,userId:accountUser.id};
      saveQueue=saveQueue.then(()=>window.AtlasAuth.api('/api/preferences',payload)).then(()=>{if(revision===saveRevision)dirty=false;}).catch(()=>{if(revision===saveRevision)toast('账号资料未能保存，准备状态暂留当前浏览器；请检查服务后重试。');});
    }
  }
  window.AtlasAuth.flush=async()=>{
    await saveQueue;
    if(accountUser&&dirty){await window.AtlasAuth.api('/api/preferences',{userId:accountUser.id,favorites:[...state.favorites],completed:[...state.completed],gear:state.gear});dirty=false;}
  };
  window.addEventListener('atlas-account',event=>{
    accountUser=event.detail.user;dirty=false;saveRevision++;
    let saved=event.detail.preferences || {};
    if(!accountUser){try{saved=JSON.parse(localStorage.getItem('trail-atlas-v1') || '{}');}catch{saved={};}}
    state.favorites=new Set((Array.isArray(saved.favorites)?saved.favorites:[]).filter(id=>(knownIds.has(id)||/^u-[a-z0-9-]{1,48}$/.test(id))));
    state.completed=new Set(accountUser&&Array.isArray(saved.completed)?saved.completed.filter(id=>(knownIds.has(id)||/^u-[a-z0-9-]{1,48}$/.test(id))):[]);
    state.onlyCompleted=false;
    state.gear={};
    for(const [id,checks] of Object.entries(saved.gear||{})){const route=findRoute(id);if(Array.isArray(checks)&&(route||/^u-[a-z0-9-]{1,48}$/.test(id)))state.gear[id]=checks.filter(index=>Number.isInteger(index)&&index>=0&&index<(route?route.gear.length:100));}
    state.onlyFavorites=false;filterRoutes();
    if(state.selected){const scroll=$('detail').scrollTop;renderDetail();$('detail').scrollTop=scroll;}
  });
  window.AtlasAddRoutes=routes=>{
    for(const route of routes)if(!knownIds.has(route.id)){trails.push(route);knownIds.add(route.id);if(state.gear[route.id])state.gear[route.id]=state.gear[route.id].filter(i=>i<route.gear.length);}
    const chosen=$('province').value;
    const provinces=[...new Set(trails.flatMap(r=>r.province?.split(' / ')||[]))].sort((a,b)=>a.localeCompare(b,'zh-CN'));
    $('province').replaceChildren(new Option('全部省区',''));
    for(const province of provinces)$('province').append(new Option(province,province));
    $('province').value=chosen;$('total-routes').textContent=trails.length;$('china-count').textContent=trails.filter(r=>r.country.startsWith('中国')).length;
    filterRoutes();
  };
  function toast(message) {
    $('toast').textContent = message; $('toast').hidden = false;
    clearTimeout(toastTimer); toastTimer = setTimeout(() => {$('toast').hidden = true;}, 3200);
  }
  function photoImage(photo, options = '') {
    return photo ? `<img src="${escape(safeUrl(photo.url))}" alt="${escape(photo.caption)}" ${options} decoding="async" referrerpolicy="no-referrer">` : '';
  }
  function badge(route) { return `<span class="badge level-${route.level}">${'▴'.repeat(route.level)} ${meta.levels[route.level]}</span>`; }
  function findRoute(id) { return trails.find(route => route.id === id); }
  function updateCounts() {
    $('completed-count').textContent=state.completed.size;
    $('completed-toggle').setAttribute('aria-pressed',String(state.onlyCompleted));
    $('favorite-count').textContent = state.favorites.size;
    $('compare-count').textContent = state.compare.length;
    $('compare-open').disabled = state.compare.length < 2;
    $('favorites-toggle').setAttribute('aria-pressed', String(state.onlyFavorites));
  }

  function filterRoutes() {
    const query = $('search').value.trim().toLowerCase();
    state.filtered = trails.filter(route => {
      if(state.scope==='china' && !route.country.startsWith('中国')) return false;
      if($('province').value && !route.province?.split(' / ').includes($('province').value)) return false;
      if($('access').value==='restricted' && !route.infoOnly) return false;
      if($('access').value==='planning' && route.infoOnly) return false;
      const searchable = [route.name,route.english,route.country,route.continent,...route.tags].join(' ').toLowerCase();
      if (query && !searchable.includes(query)) return false;
      if ($('continent').value && route.continent !== $('continent').value) return false;
      if ($('difficulty').value && route.level !== Number($('difficulty').value)) return false;
      if ($('month').value && !route.season.includes(Number($('month').value))) return false;
      if(state.onlyCompleted && !state.completed.has(route.id))return false;
      if (state.onlyFavorites && !state.favorites.has(route.id)) return false;
      const duration = $('duration').value;
      return !duration || (duration === 'short' && route.days <= 3) || (duration === 'medium' && route.days >= 4 && route.days <= 7) || (duration === 'long' && route.days >= 8);
    });
    const sort = $('sort').value;
    if (sort !== 'featured') state.filtered.sort((a,b) => a[sort] - b[sort]);
    else state.filtered.sort((a,b)=>Number(!!a.infoOnly)-Number(!!b.infoOnly));
    if (state.selected && !state.filtered.some(route => route.id === state.selected.id)) closeDetail(false);
    renderCards(); renderMapLayers();
    $('feature-card').hidden = !!state.selected || !state.filtered.some(route => route.id === 'tmb');
    $('world-view').textContent=state.scope==='china'?'◎ 中国全览':'◎ 世界视角';
    $('surprise').disabled = !state.filtered.length;
  }
  function clearFilters() {
    for (const id of ['search','continent','difficulty','duration','month','province','access']) $(id).value = '';
    $('sort').value = 'featured'; state.onlyFavorites = false;state.onlyCompleted=false;
    updateCounts(); filterRoutes();
  }
  function renderCards() {
    $('result-count').textContent = state.filtered.length;
    $('route-list').innerHTML = state.filtered.length ? state.filtered.map(route => {
      const favorite = state.favorites.has(route.id), compared = state.compare.includes(route.id);
      return `<article class="route-card ${state.completed.has(route.id)?'is-completed':''} ${state.selected?.id === route.id ? 'selected' : ''}" data-route="${route.id}">
        <button class="card-open" data-select="${route.id}" aria-label="查看${escape(route.name)}详情"><div class="card-image">${photoImage(state.photos[route.id]?.[0], 'loading="lazy"')}<span class="card-continent">${escape(route.continent)} / ${escape(route.english.split(' · ')[0])}</span><span class="card-level level-${route.level}">${'▴'.repeat(route.level)} ${meta.levels[route.level]}</span></div><div class="card-body"><h3>${escape(route.name)}</h3><p class="card-country">${route.flag} ${escape(route.country)}</p><span class="access-badge ${route.infoOnly?'restricted':''}">${escape(route.accessText || '出发前核实开放')}</span><div class="card-metrics"><span title="${escape(route.distanceText)}">↔ ${route.distance?'约 '+route.distance+' km':'待核实'}</span><span>◷ ${escape(route.duration)}</span><span title="${escape(route.altitudeLabel+'：'+route.altitudeText)}">△ ${route.altitude?route.altitude.toLocaleString()+' m':'待核实'}</span></div></div></button>
        <div class="card-actions"><button data-completed="${route.id}" class="${state.completed.has(route.id)?'lit':''}" aria-pressed="${state.completed.has(route.id)}" aria-label="${state.completed.has(route.id)?'取消点亮':'点亮已走过'}${escape(route.name)}">${state.completed.has(route.id)?'✦ 已走过':'☆ 点亮'}</button><button data-favorite="${route.id}" class="${favorite ? 'on' : ''}" aria-pressed="${favorite}" aria-label="${favorite ? '取消收藏' : '收藏'}${escape(route.name)}">${favorite ? '♥ 已收藏' : '♡ 收藏'}</button><button data-compare="${route.id}" class="${compared ? 'on' : ''}" aria-pressed="${compared}" aria-label="${compared ? '移除对比' : '加入对比'}${escape(route.name)}">${compared ? '✓ 已加入对比' : '＋ 加入对比'}</button></div></article>`;
    }).join('') : `<div class="empty-state"><strong>${state.onlyCompleted?'还没有匹配的已走过线路':state.onlyFavorites ? '这里还没有匹配的收藏' : '暂时没有匹配的线路'}</strong><p>换个目的地、月份或难度，<br>看看另一片山野。</p><button data-reset>清除筛选</button></div>`;
    updateCounts();
  }

  function initializeMap() {
    if (!window.L) { $('map-network').hidden = false; return; }
    map = L.map('map',{minZoom:.5,maxZoom:16,zoomSnap:.25,zoomDelta:.5,zoomControl:false,worldCopyJump:true}).setView([15,10],1.5);
    $('map').classList.add('night-map');
    L.control.zoom({position:'bottomright'}).addTo(map);
    L.control.scale({imperial:false,position:'bottomright'}).addTo(map);
    tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxNativeZoom:19,maxZoom:19,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);
    let loadedTiles = 0, failedTiles = 0;
    tiles.on('loading',()=>{loadedTiles = 0; failedTiles = 0;});
    tiles.on('tileload',()=>{loadedTiles++; $('map-network').hidden = true;});
    tiles.on('tileerror',()=>{failedTiles++; if (!loadedTiles) $('map-network').hidden = false;});
    tiles.on('load',()=>{$('map-network').hidden = loadedTiles > 0 || failedTiles === 0;});
    const readout = point => {
      const wrapped = point.wrap();
      $('coordinates').textContent = `${Math.abs(wrapped.lat).toFixed(2)}° ${wrapped.lat >= 0 ? 'N' : 'S'} · ${Math.abs(wrapped.lng).toFixed(2)}° ${wrapped.lng >= 0 ? 'E' : 'W'}`;
      $('zoom-readout').textContent = 'Z ' + map.getZoom();
    };
    map.on('mousemove',event => readout(event.latlng));
    map.on('moveend zoomend',()=>readout(map.getCenter()));
    new ResizeObserver(()=>map.invalidateSize({pan:false})).observe($('map'));
    renderMapLayers();
    worldView(false);
  }
  function worldView(animate = true) {
    if(!map) return;
    const pool=state.filtered.length?state.filtered:trails;
    const bounds=L.latLngBounds(pool.flatMap(route=>route.points));
    map.flyToBounds(bounds,{paddingTopLeft:[40,110],paddingBottomRight:[40,90],maxZoom:state.scope==='china'?5:2,duration:animate&&!reducedMotion.matches?1.4:0,animate:animate&&!reducedMotion.matches});
  }
  function renderMapLayers() {
    if (!map) return;
    for (const layers of routeLayers.values()) layers.remove();
    routeLayers.clear();
    for (const route of state.filtered) {
      const line = L.polyline(route.infoOnly || route.locationOnly?[]:route.points,{color:state.completed.has(route.id)?'#ffd178':meta.colors[route.level],weight:state.completed.has(route.id)?5:3,opacity:state.completed.has(route.id)?.95:.65});
      const point = route.points[Math.floor(route.points.length / 2)];
      const icon = L.divIcon({className:'trail-marker'+(state.completed.has(route.id)?' is-completed':'') + (state.selected?.id === route.id ? ' is-selected' : ''),html:`<span class="marker-dot" style="--marker-color:${meta.colors[route.level]}">${state.completed.has(route.id)?'✓':route.infoOnly?'!':'⌃'}</span>`,iconSize:[27,27],iconAnchor:[13.5,13.5]});
      const marker = L.marker(point,{icon,title:route.name,alt:'查看' + route.name + '详情',keyboard:true});
      const tooltip = document.createElement('span'); tooltip.textContent = `${route.name}${state.completed.has(route.id)?' · 已走过':''} · ${meta.levels[route.level]} · ${route.duration}`;
      marker.bindTooltip(tooltip,{direction:'top',offset:[0,-12]});
      marker.on('click',()=>selectRoute(route.id)); line.on('click',()=>selectRoute(route.id));
      routeLayers.set(route.id,L.layerGroup([line,marker]).addTo(map));
    }
  }
  function drawSelected() {
    if (!map) return;
    selectedLayer?.remove();
    const route = state.selected;
    if (!route) return;
    const halo = L.polyline(route.infoOnly || route.locationOnly?[]:route.points,{color:state.completed.has(route.id)?'#ffd178':'#d2f58a',weight:12,opacity:.12,interactive:false});
    const flow = L.polyline(route.infoOnly || route.locationOnly?[]:route.points,{color:state.completed.has(route.id)?'#ffd178':'#d2f58a',weight:3.5,opacity:1,className:'route-flow',interactive:false});
    const stops = (route.infoOnly?[]:route.locationOnly?[route.points[0]]:route.points).map((point,index) => L.circleMarker(point,{radius:route.locationOnly?16:3,weight:1,color:'#d2f58a',fillColor:'#193531',fillOpacity:.3}).bindTooltip(route.locationOnly?'线路所在区域（非导航）':`示意关键点 ${index + 1}`));
    selectedLayer = L.layerGroup([halo,flow,...stops]).addTo(map);
    traveler?.remove(); traveler = L.marker(route.points[0],{icon:L.divIcon({className:'traveler',iconSize:[12,12],iconAnchor:[6,6]}),interactive:false}).addTo(map);
    tourValue = 0; updateTour(0);
    requestAnimationFrame(()=>{
      if (state.selected?.id !== route.id) return;
      map.invalidateSize({pan:false});
      map.flyToBounds(L.latLngBounds(route.points),{paddingTopLeft:[30,120],paddingBottomRight:[105,170],maxZoom:route.locationOnly?9:12,duration:reducedMotion.matches ? 0 : 1.45,animate:!reducedMotion.matches});
    });
  }
  window.AtlasExploreRoute=id=>{const route=findRoute(id);if(!route)return;if(!route.country.startsWith('中国'))$('scope-world').click();clearFilters();selectRoute(id);};
  function selectRoute(id) {
    const route = findRoute(id); if (!route) return;
    pauseTour(); state.selected = route; state.tab = 'overview';
    $('detail').hidden = false; document.querySelector('.workspace').classList.add('has-detail');
    $('feature-card').hidden = true; $('tour-control').hidden = !map || route.infoOnly || route.locationOnly;
    $('map-title').textContent = route.name; $('map-subtitle').textContent = `${route.country} · ${route.type} · ${route.locationOnly?'区域位置':'走向示意'}`;
    renderDetail(); renderCards(); renderMapLayers(); drawSelected();
    history.replaceState(null,'','#' + route.id);
    $('detail').scrollTop = 0;
    $('detail').querySelector('[data-close-detail]').focus({preventScroll:true});
  }
  function closeDetail(restoreFocus = true) {
    const previous = state.selected?.id;
    pauseTour(); map?.stop(); state.selected = null; selectedLayer?.remove(); selectedLayer = null; traveler?.remove(); traveler = null;
    $('detail').hidden = true; document.querySelector('.workspace').classList.remove('has-detail');
    $('tour-control').hidden = true; $('feature-card').hidden = !state.filtered.some(route => route.id === 'tmb');
    $('map-title').textContent = '把世界，变成你的足迹。'; $('map-subtitle').textContent = '点击地图标记，开启一场山野探索。';
    history.replaceState(null,'',location.pathname + location.search);
    renderCards(); renderMapLayers();
    requestAnimationFrame(()=>{map?.invalidateSize({pan:false});});
    if (restoreFocus && previous) document.querySelector(`[data-select="${previous}"]`)?.focus({preventScroll:true});
  }

  function photoCredit(photo) {
    return `${external(photo.source, photo.author + ' · ' + photo.license)}${photo.licenseUrl ? ' / ' + external(photo.licenseUrl, '许可') : ''}`;
  }
  window.AtlasRefreshPhotoGallery=id=>{if(state.selected?.id===id){const scroll=$('detail').scrollTop;renderDetail();$('detail').scrollTop=scroll;}};
  function renderDetail() {
    const route = state.selected; if (!route) return;
    const photos = [...(state.photos[route.id]||[]),...(window.AtlasRoutePhotos?.photos[route.id]||[])];
    const favorite = state.favorites.has(route.id), compared = state.compare.includes(route.id);
    const checks = new Set(state.gear[route.id] || []);
    const sections = [['出发与交通',route.logistics],['住宿方式',route.stay],['补给与饮水',route.food],['预约与许可',route.permit]];
    $('detail').innerHTML = `<div class="detail-hero">${photoImage(photos[0])}<button class="detail-close icon-button" data-close-detail aria-label="关闭线路详情">×</button>${photos.length ? `<button class="hero-gallery" data-photo="0">▧ 风景相册 · ${photos.length} 张</button>` : ''}<div class="detail-hero-title"><span class="eyebrow">${escape(route.english.toUpperCase())}</span><h2>${escape(route.name)}</h2><p>${route.flag} ${escape(route.country)}</p></div></div>
      <div class="detail-main">${route.community?`<div class="submission-author">社区投稿 · <button data-author="${route.author.id}">${escape(route.author.username)}</button><p>作者经验与轨迹未经独立核验；出发前确认开放范围和实际路况。</p></div>`:''}<div class="detail-meta">${badge(route)}${route.tags.map(tag => `<span class="tag">${escape(tag)}</span>`).join('')}</div><div class="access-notice ${route.infoOnly?'restricted':''}"><strong>${escape(route.accessText || '出发前核实开放')}</strong>${route.infoOnly?`<p>${escape(route.permit)}</p>`:''}</div><p class="detail-subtitle">${escape(route.subtitle)}</p>
      <div class="detail-stats"><div><small>↔ 路线距离</small><strong>${escape(route.distanceText)}</strong></div><div><small>◷ 参考行程</small><strong>${escape(route.duration)}</strong></div><div><small>△ ${escape(route.altitudeLabel)}</small><strong>${escape(route.altitudeText)}</strong></div><div><small>⌁ 路线形式</small><strong>${escape(route.type)}</strong></div></div>
      <div class="detail-actions"><button data-completed="${route.id}" class="${state.completed.has(route.id)?'lit':''}" aria-pressed="${state.completed.has(route.id)}">${state.completed.has(route.id)?'✦ 已走过 · 取消点亮':'☆ 点亮已走过'}</button><button data-favorite="${route.id}" class="${favorite?'on':''}" aria-pressed="${favorite}">${favorite?'♥ 已收藏':'♡ 收藏线路'}</button><button data-compare="${route.id}" class="${compared?'on':''}" aria-pressed="${compared}">${compared?'✓ 已加入对比':'⇄ 加入对比'}</button>${route.infoOnly?'':'<button data-export>↓ 导出行程卡</button>'}</div>
      <div class="detail-tabs" role="tablist" aria-label="线路详情栏目">${[['overview','线路概览'],['itinerary',route.infoOnly?'通行限制':'行程计划'],['gear','装备清单'],['media','视频 / 社区']].map(([id,name]) => `<button role="tab" id="tab-${id}" aria-controls="pane-${id}" aria-selected="${state.tab===id}" class="${state.tab===id?'active':''}" data-tab="${id}" tabindex="${state.tab===id?0:-1}">${name}</button>`).join('')}</div>
      <div class="tab-pane" id="pane-overview" role="tabpanel" aria-labelledby="tab-overview" ${state.tab!=='overview'?'hidden':''}>
        <section class="detail-section"><h3 class="section-label">关于这段旅程</h3><p>${escape(route.description)}</p><ul class="highlights">${route.highlights.map(text => `<li>${escape(text)}</li>`).join('')}</ul></section>
        <section class="detail-section"><h3 class="section-label">风景相册 <span class="eyebrow">REAL PLACES</span></h3><div class="photo-grid ${photos.length===1?'one':''}">${photos.map((photo,index) => `<button class="photo-tile" data-photo="${index}" aria-label="放大${escape(photo.caption)}">${photoImage(photo,'loading="lazy"')}<span>${escape(photo.caption)} ↗</span></button>`).join('')}</div><p class="photo-credits">${photos.length ? photos.map(photoCredit).join('<br>') : route.photoPending?'暂无已授权风景照片，可在社区交流路线经验。':'照片资料暂未加载，请刷新后重试。'}</p></section>
        <section id="user-route-photos" class="detail-section"></section><section class="detail-section"><h3 class="section-label">适合什么时候去？</h3><div class="season-strip">${Array.from({length:12},(_,index) => `<span class="season-month ${route.season.includes(index+1)?'in-season':''}" title="${index+1} 月${route.season.includes(index+1)?'：参考适宜月份':'：非主要推荐月份'}">${index+1}</span>`).join('')}</div><p class="season-note">${escape(route.seasonText)} · 实际开放与天气需另行核实</p></section>
        <section class="detail-section"><h3 class="section-label">摄影灵感</h3><p>${escape(route.photoTip)}</p></section>
        <section class="detail-section"><h3 class="section-label">出发前的准备</h3><div class="info-grid">${sections.map(([label,text]) => `<div class="info-row"><strong>${label}</strong><span>${escape(text)}</span></div>`).join('')}</div></section>
        <section class="detail-section notice"><h3>地形与天气提醒</h3><p>${escape(route.risks)}</p></section>
        <section class="detail-section"><h3 class="section-label">资料来源</h3><div class="source-links">${route.sources.map(([name,url]) => external(url,name)).join('')}</div><p class="reference-note">整理日期：${meta.updated}。难度为本站参考分级，不等同当地官方等级。里程与海拔随路线版本变化；页面不提供实时开放状态。地图连线仅示意关键地点，不能用于现场导航。</p></section>
      </div>
      <div class="tab-pane" id="pane-itinerary" role="tabpanel" aria-labelledby="tab-itinerary" ${state.tab!=='itinerary'?'hidden':''}><h3 class="section-label">行程分段</h3><p>这是一份探索框架。具体每日里程、适应日、住宿与接驳应按体能和当地情况安排。</p><ol class="timeline">${route.itinerary.map(([label,text]) => `<li><strong>${escape(label)}</strong><p>${escape(text)}</p></li>`).join('')}</ol><div class="notice"><h3>先落实关键预约</h3><p>${escape(route.permit)}</p></div>${route.infoOnly?'':'<button class="download-plan" data-export>↓ 保存行程与装备清单</button>'}</div>
      <div class="tab-pane" id="pane-gear" role="tabpanel" aria-labelledby="tab-gear" ${state.tab!=='gear'?'hidden':''}><h3 class="section-label">把准备，变成安心。</h3><div class="gear-progress"><span>装备准备进度</span><strong id="gear-count">${checks.size} / ${route.gear.length}</strong></div><div class="gear-track"><div id="gear-bar" style="width:${checks.size/route.gear.length*100}%"></div></div><div class="gear-list">${route.gear.map((item,index) => `<label><input type="checkbox" data-gear="${index}" ${checks.has(index)?'checked':''}><span>${escape(item)}</span></label>`).join('')}</div><p class="gear-disclaimer">以上为基础建议，应按季节、天气与住宿方式调整。冬季、冰雪或技术地形需要额外装备与使用技能；勾选完成不代表已具备通行条件。${accountUser?'清单保存在此账号的本地数据库。':'访客清单保存在当前浏览器。'}</p>${route.infoOnly?'':'<button class="download-plan" data-export>↓ 导出我的准备清单</button>'}</div><div class="tab-pane" id="pane-media" role="tabpanel" aria-labelledby="tab-media" ${state.tab!=='media'?'hidden':''}>${renderMedia(route)}<section id="route-comments" class="detail-section route-comments"></section></div></div>`;
    window.AtlasRoutePhotos?.mount(route.id);
    if(state.tab==='media')window.AtlasComments?.mount(route.id);
  }

  function renderMedia(route) {
    const videos=route.videos || [];
    const keyword=encodeURIComponent(route.name.replace(/ · .*/, '')+' 徒步');
    return `<section class="detail-section"><h3 class="section-label">山野影像 <span class="eyebrow">BILIBILI</span></h3><p>已检索到的具体视频：${videos.length} 条。游记拍摄时间和路线版本各异，不能作为当前开放依据。</p><div class="video-grid">${videos.map(video=>`<article class="video-card"><div class="video-cover">${photoImage(state.photos[route.id]?.[0],'loading="lazy"')}<button data-video="${escape(video.bvid)}" aria-label="播放${escape(video.title)}">▶</button><span>线路景观参考 · 非视频封面</span></div><h4>${escape(video.title)}</h4><p>B站 · 链接检索于 ${escape(video.checked)}</p>${external(video.url,'在 B站观看 ↗')}</article>`).join('')}</div>${!videos.length?'<p class="media-empty">本线路暂未收录核验过的具体视频，可使用下方站内搜索。</p>':''}<div id="video-player"></div></section><section class="detail-section"><h3 class="section-label">寻找更多当地视角</h3><div class="community-links">${external('https://search.bilibili.com/all?keyword='+keyword,'B站 · 搜索更多视频 ↗')}${external('https://www.xiaohongshu.com/search_result?keyword='+keyword+'&source=web_explore_feed','小红书 · 搜索图文与视频 ↗')}</div><p class="reference-note">以上是平台搜索入口，未计入已收录视频。小红书可能要求登录；社区图片与视频保留在原平台，未授权转载的内容不复制进相册。</p></section>`;
  }
  function playVideo(bvid) {
    const video=state.selected?.videos?.find(item=>item.bvid===bvid);if(!video)return;
    pauseTour();
    $('video-player').innerHTML=`<div class="embedded-video"><button id="stop-video" class="text-button">关闭播放器 ×</button><iframe src="https://player.bilibili.com/player.html?bvid=${encodeURIComponent(bvid)}&autoplay=0" title="${escape(video.title)}" loading="lazy" allow="fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe><p>若嵌入播放受平台限制，${external(video.url,'打开 B站原视频')}。</p></div>`;
    $('stop-video').addEventListener('click',()=>{$('video-player').innerHTML='';});
    $('video-player').scrollIntoView({behavior:reducedMotion.matches?'auto':'smooth',block:'nearest'});
  }

  function setTab(tab) {
    if (!detailTabs.includes(tab)) return;
    if(tab!=='media' && $('video-player')) $('video-player').innerHTML='';
    state.tab = tab;
    if(tab==='media')window.AtlasComments?.mount(state.selected.id);
    for (const id of detailTabs) {
      $('tab-' + id).classList.toggle('active',id===tab);
      $('tab-' + id).setAttribute('aria-selected',String(id===tab));
      $('tab-' + id).tabIndex = id===tab ? 0 : -1;
      $('pane-' + id).hidden = id!==tab;
    }
  }
  function toggleCompleted(id) {
    if(!knownIds.has(id))return;
    if(!accountUser){toast('登录后点亮你的徒步足迹');$('account-open').click();return;}
    const scroll=$('detail').scrollTop;
    state.completed.has(id)?state.completed.delete(id):state.completed.add(id);
    save();filterRoutes();
    if(state.selected){renderDetail();$('detail').scrollTop=scroll;}
    if(state.selected)selectedLayer?.eachLayer(layer=>layer.setStyle?.({color:state.completed.has(state.selected.id)?'#ffd178':'#d2f58a'}));
    toast(state.completed.has(id)?'✦ 已点亮！这段山野留下了你的足迹':'已取消点亮');
  }
  function toggleFavorite(id) {
    if (!knownIds.has(id)) return;
    const scroll = $('detail').scrollTop;
    state.favorites.has(id) ? state.favorites.delete(id) : state.favorites.add(id);
    save(); filterRoutes();
    if (state.selected) { renderDetail(); $('detail').scrollTop = scroll; }
    toast(state.favorites.has(id) ? '已放进你的山野心愿单' : '已取消收藏');
  }
  function toggleCompare(id) {
    if (!knownIds.has(id)) return;
    const index = state.compare.indexOf(id);
    if (index>=0) state.compare.splice(index,1);
    else if (state.compare.length<3) state.compare.push(id);
    else { toast('最多对比 3 条线路，请先移除一条。'); return; }
    renderCards();
    if (state.selected) { const scroll=$('detail').scrollTop; renderDetail(); $('detail').scrollTop=scroll; }
    if ($('compare-dialog').open) renderCompare();
    else if (index<0) toast(state.compare.length<2 ? '已加入对比，再选一条即可比较' : '已加入对比，点击顶部「线路对比」查看');
  }
  function renderCompare() {
    const selected = state.compare.map(findRoute);
    if (!selected.length) { $('compare-dialog').close(); return; }
    const rows = [
      ['目的地',route=>escape(route.country)],['参考难度',route=>badge(route)],['距离',route=>escape(route.distanceText)],['行程',route=>escape(route.duration)],
      ['海拔',route=>`${escape(route.altitudeText)}<small>${escape(route.altitudeLabel)}</small><div class="altitude-bar"><div style="width:${route.altitude/6000*100}%"></div></div>`],
      ['主要季节',route=>escape(route.seasonText)],['住宿',route=>escape(route.stay)],['预约与许可',route=>escape(route.permit)],['主要挑战',route=>escape(route.risks)]
    ];
    $('compare-content').innerHTML = `<div class="comparison-scroll"><table class="comparison-table"><thead><tr><th scope="col">对比维度</th>${selected.map(route=>`<td>${escape(route.name)}<small>${escape(route.english)}</small><button class="compare-remove" data-compare="${route.id}" aria-label="从对比移除${escape(route.name)}">移除 ×</button></td>`).join('')}</tr></thead><tbody>${rows.map(([title,cell])=>`<tr><th scope="row">${title}</th>${selected.map(route=>`<td>${cell(route)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
  }
  function openPhoto(index) {
    const photos = [...(state.photos[state.selected?.id]||[]),...(window.AtlasRoutePhotos?.photos[state.selected?.id]||[])];
    if (!photos.length) return;
    state.photoIndex = (index + photos.length) % photos.length;
    const photo = photos[state.photoIndex];
    const img = $('lightbox-image'); img.classList.remove('image-failed');
    $('lightbox-error').hidden = true; img.alt = photo.caption; img.src = safeUrl(photo.url);
    $('lightbox-caption').textContent = `${photo.caption} · ${state.photoIndex+1}/${photos.length}`;
    $('lightbox-credit').innerHTML = photoCredit(photo) + ' · ' + external(photo.source,'原图来源');
    $('photo-prev').disabled = $('photo-next').disabled = photos.length===1;
    if (!$('photo-dialog').open) { pauseTour(); $('photo-dialog').showModal(); }
  }
  function exportPlan() {
    const route = state.selected; if (!route || route.infoOnly) return;
    const checks = new Set(state.gear[route.id] || []);
    const text = `# ${route.name} · ${route.english}\n\n目的地：${route.country}\n难度：${meta.levels[route.level]}（本站参考）\n距离：${route.distanceText}\n行程：${route.duration}\n${route.altitudeLabel}：${route.altitudeText}\n季节：${route.seasonText}\n\n## 线路介绍\n${route.description}\n\n## 行程框架\n${route.itinerary.map(([title,step])=>'- '+title+'：'+step).join('\n')}\n\n## 出发准备\n交通：${route.logistics}\n住宿：${route.stay}\n补给：${route.food}\n预约：${route.permit}\n\n## 装备清单\n${route.gear.map((item,index)=>'- ['+(checks.has(index)?'x':' ')+'] '+item).join('\n')}\n\n## 地形与天气\n${route.risks}\n\n## 来源\n${route.sources.map(([name,url])=>'- ['+name+']('+url+')').join('\n')}\n\n资料整理于 ${meta.updated}，不含实时天气或开放状态。里程、海拔随版本变化；地图走向示意不能用于现场导航。\n`;
    const url = URL.createObjectURL(new Blob(['\ufeff'+text],{type:'text/markdown;charset=utf-8'}));
    const link=document.createElement('a'); link.href=url; link.download=route.name+'-行程卡.md'; document.body.append(link); link.click(); link.remove();
    setTimeout(()=>URL.revokeObjectURL(url),2000); toast('已导出行程卡，包含你勾选的装备状态。');
  }

  function updateTour(value) {
    tourValue = Math.max(0,Math.min(100,value));
    $('tour-progress').value = tourValue; $('tour-percent').textContent = Math.round(tourValue)+'%';
    if (!state.selected || !traveler) return;
    const points = state.selected.points;
    const lengths = points.slice(1).map((point,index)=>L.latLng(points[index]).distanceTo(L.latLng(point)));
    const target = lengths.reduce((sum,length)=>sum+length,0)*tourValue/100;
    let traversed=0, index=0;
    while(index<lengths.length-1 && traversed+lengths[index]<target) traversed+=lengths[index++];
    const t = lengths[index] ? Math.min(1,(target-traversed)/lengths[index]) : 0;
    const a=points[index], b=points[index+1];
    traveler.setLatLng([a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t]);
  }
  function pauseTour() { tourPlaying=false; cancelAnimationFrame(tourFrame); $('tour-play').textContent='▶ 漫游线路'; }
  function playTour() {
    if (!map || !state.selected || state.selected.infoOnly) return;
    if (tourPlaying) { pauseTour(); return; }
    if (tourValue>=100) updateTour(0);
    tourPlaying=true; $('tour-play').textContent='Ⅱ 暂停漫游';
    const startValue=tourValue, start=performance.now();
    const tick = time => {
      if(!tourPlaying) return;
      updateTour(startValue+(time-start)/180);
      if(tourValue>=100) { pauseTour(); toast('漫游完成，这只是旅程的开始。'); }
      else tourFrame=requestAnimationFrame(tick);
    };
    tourFrame=requestAnimationFrame(tick);
  }

  for(let month=1;month<=12;month++) { const option=document.createElement('option');option.value=month;option.textContent=month+' 月';$('month').append(option); }
  $('search').addEventListener('input',filterRoutes);
  for(const id of ['continent','difficulty','duration','month','sort','province','access']) $(id).addEventListener('change',()=>{filterRoutes();if(id==='province')worldView();});
  $('clear-filters').addEventListener('click',clearFilters);
  $('completed-toggle').addEventListener('click',async()=>{if(!accountUser){$('account-open').click();return;}const enable=!state.onlyCompleted;if(enable){const missing=[...state.completed].filter(id=>!knownIds.has(id));if(missing.length){$('completed-toggle').disabled=true;toast('正在加载你的社区线路足迹…');try{for(const id of missing)await window.AtlasEnsureRoute?.(id);}catch{toast('部分足迹暂时无法加载，请稍后重试。');}finally{$('completed-toggle').disabled=false;}}$('scope-world').click();clearFilters();}state.onlyCompleted=enable;updateCounts();filterRoutes();});
  $('favorites-toggle').addEventListener('click',()=>{state.onlyFavorites=!state.onlyFavorites;updateCounts();filterRoutes();});
  $('compare-open').addEventListener('click',()=>{renderCompare();pauseTour();$('compare-dialog').showModal();});
  $('feature-open').addEventListener('click',()=>selectRoute('tmb'));
  $('surprise').addEventListener('click',()=>{const choices=state.filtered.filter(route=>route.id!==state.selected?.id);const pool=choices.length?choices:state.filtered;if(pool.length)selectRoute(pool[Math.floor(Math.random()*pool.length)].id);});
  $('world-view').addEventListener('click',()=>{closeDetail();requestAnimationFrame(()=>worldView());});
  for(const style of ['dark','light']) $('style-'+style).addEventListener('click',()=>{
    $('map').classList.toggle('night-map',style==='dark');
    for(const id of ['dark','light']) { $('style-'+id).classList.toggle('active',id===style);$('style-'+id).setAttribute('aria-pressed',String(id===style)); }
  });
  $('tour-play').addEventListener('click',playTour);
  $('tour-progress').addEventListener('input',event=>{pauseTour();updateTour(Number(event.target.value));});
  $('photo-prev').addEventListener('click',()=>openPhoto(state.photoIndex-1));
  $('photo-next').addEventListener('click',()=>openPhoto(state.photoIndex+1));
  document.addEventListener('click',event=>{
    const button=event.target.closest('button'); if(!button) return;
    if(button.dataset.select) selectRoute(button.dataset.select);
    else if(button.dataset.author) window.AtlasSocial?.profile(Number(button.dataset.author));
    else if(button.dataset.completed) toggleCompleted(button.dataset.completed);
    else if(button.dataset.favorite) toggleFavorite(button.dataset.favorite);
    else if(button.dataset.compare) toggleCompare(button.dataset.compare);
    else if(button.hasAttribute('data-close-detail')) closeDetail();
    else if(button.dataset.video) playVideo(button.dataset.video);
    else if(button.dataset.tab) setTab(button.dataset.tab);
    else if(button.hasAttribute('data-photo')) openPhoto(Number(button.dataset.photo));
    else if(button.dataset.close) $(button.dataset.close).close();
    else if(button.hasAttribute('data-export')) exportPlan();
    else if(button.hasAttribute('data-reset')) clearFilters();
  });
  $('detail').addEventListener('change',event=>{
    if(!event.target.hasAttribute('data-gear') || !state.selected) return;
    const index=Number(event.target.dataset.gear), route=state.selected;
    const checks=new Set(state.gear[route.id] || []);
    event.target.checked ? checks.add(index) : checks.delete(index);
    state.gear[route.id]=[...checks]; save();
    $('gear-count').textContent=`${checks.size} / ${route.gear.length}`;
    $('gear-bar').style.width=checks.size/route.gear.length*100+'%';
  });
  document.addEventListener('error',event=>{
    if(event.target.tagName!=='IMG') return;
    event.target.classList.add('image-failed');
    if(event.target.id==='lightbox-image') $('lightbox-error').hidden=false;
    else event.target.parentElement.setAttribute('title','照片暂未加载，可在相册中打开原图来源');
  },true);
  document.addEventListener('keydown',event=>{
    const editable=['INPUT','SELECT','TEXTAREA'].includes(document.activeElement?.tagName);
    if(event.key==='/' && !editable && !$('photo-dialog').open && !$('compare-dialog').open && !$('auth-dialog').open && !$('social-dialog').open && !$('photo-upload-dialog').open && !$('photo-review-dialog').open && !$('user-photo-dialog').open) {event.preventDefault();$('search').focus();}
    if(event.key==='Escape' && !$('photo-dialog').open && !$('compare-dialog').open && !$('auth-dialog').open && !$('social-dialog').open && !$('photo-upload-dialog').open && !$('photo-review-dialog').open && !$('user-photo-dialog').open && state.selected) closeDetail();
    if($('photo-dialog').open && (event.key==='ArrowRight'||event.key==='ArrowLeft')) {event.preventDefault();openPhoto(state.photoIndex+(event.key==='ArrowRight'?1:-1));}
    if(event.target.getAttribute('role')==='tab' && ['ArrowRight','ArrowLeft','Home','End'].includes(event.key)) {
      event.preventDefault();const tabs=detailTabs;const index=tabs.indexOf(state.tab);
      const next=event.key==='Home'?0:event.key==='End'?tabs.length-1:(index+(event.key==='ArrowRight'?1:tabs.length-1))%tabs.length;
      setTab(tabs[next]);$('tab-'+tabs[next]).focus();
    }
  });
  document.addEventListener('visibilitychange',()=>{if(document.hidden)pauseTour();});
  for(const id of ['compare-dialog','photo-dialog']) $(id).addEventListener('click',event=>{if(event.target===$(id)){const rect=$(id).getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)$(id).close();}});

  $('total-routes').textContent=trails.length;
  $('china-count').textContent=trails.filter(r=>r.country.startsWith('中国')).length;
  const provinces=[...new Set(trails.flatMap(r=>r.province?.split(' / ') || []))].sort((a,b)=>a.localeCompare(b,'zh-CN'));
  for(const province of provinces){const option=document.createElement('option');option.value=option.textContent=province;$('province').append(option);}
  for(const scope of ['china','world']) $('scope-'+scope).addEventListener('click',()=>{
    state.scope=scope;closeDetail(false);clearFilters();
    for(const id of ['china','world']) {$('scope-'+id).classList.toggle('active',id===scope);$('scope-'+id).setAttribute('aria-pressed',String(id===scope));}
    $('province').disabled=scope!=='china';worldView();
  });
  if(window.AtlasAuth.user)window.dispatchEvent(new CustomEvent('atlas-account',{detail:{user:window.AtlasAuth.user,preferences:window.AtlasAuth.preferences||{}}}));
  filterRoutes(); initializeMap(); renderCards();
  const initialId=location.hash.slice(1);
  if(knownIds.has(initialId)) {if(!findRoute(initialId).country.startsWith('中国')){$('scope-world').click();} selectRoute(initialId);}
  window.addEventListener('hashchange',()=>{
    const id=location.hash.slice(1),route=findRoute(id);
    if(!route)return;
    if(state.scope==='china' && !route.country.startsWith('中国')) $('scope-world').click();
    else clearFilters();
    selectRoute(id);
  });
  fetch('photos.json').then(response=>{if(!response.ok)throw new Error('Photo metadata unavailable');return response.json();}).then(photos=>{
    state.photos=photos;renderCards();if(state.selected){const scroll=$('detail').scrollTop;renderDetail();$('detail').scrollTop=scroll;}
  }).catch(()=>toast('照片资料未能加载，线路介绍仍可浏览；请刷新后重试。'));
})();

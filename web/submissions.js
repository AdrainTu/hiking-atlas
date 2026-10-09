'use strict';
(() => {
  const $=id=>document.getElementById(id),dialog=$('submit-route-dialog'),form=$('submit-route-form'),status=$('submit-route-status');
  const provinces=['北京','天津','河北','山西','内蒙古','辽宁','吉林','黑龙江','上海','江苏','浙江','安徽','福建','江西','山东','河南','湖北','湖南','广东','广西','海南','重庆','四川','贵州','云南','西藏','陕西','甘肃','青海','宁夏','新疆','香港','澳门','台湾'];
  const fields={};let gpxPoints=null,pending=false,cursor=null;
  function field(key,label,type='text',defaultValue='',options={}){
    const wrap=document.createElement('label');wrap.textContent=label;
    const input=document.createElement(type==='textarea'?'textarea':type==='select'?'select':'input');input.name=key;input.id='route-input-'+key;
    if(type==='select')for(const [value,text] of options.choices){const option=document.createElement('option');option.value=value;option.textContent=text;input.append(option);}
    else if(type!=='textarea')input.type=type;
    Object.assign(input,options);input.value=defaultValue;wrap.append(input);form.append(wrap);fields[key]=input;return input;
  }
  field('name','线路名称','text','',{required:true,minLength:2,maxLength:80});
  field('province','省区','select','四川',{choices:provinces.map(p=>[p,p])});
  field('level','参考难度','select','2',{choices:[['2','轻徒步'],['3','进阶徒步'],['4','高强度 / 专业准备']]});
  field('distance','参考里程（公里）','number','',{required:true,min:0.1,max:1000,step:'any'});
  field('days','行程天数','number','1',{required:true,min:1,max:60,step:1});
  field('altitude','参考海拔（米，未知填 0）','number','0',{required:true,min:0,max:9000,step:'any'});
  field('lat','位置纬度（GPX 可自动填写）','number','',{required:true,min:17,max:55,step:'any'});
  field('lon','位置经度（GPX 可自动填写）','number','',{required:true,min:73,max:136,step:'any'});
  const file=field('gpx','导入 GPX（可选，单段轨迹，最大 1 MB）','file');file.accept='.gpx,application/gpx+xml';
  field('description','线路介绍与亲历经验（至少 20 字）','textarea','',{required:true,minLength:20,maxLength:4000,rows:5});
  field('itinerary','行程分段（至少 2 行，每行一段）','textarea','确认入口、天气与开放范围\n按计划行走，预留折返与返程时间',{required:true,maxLength:3000,rows:3});
  field('gear','装备建议（至少 5 行，每行一条）','textarea','防滑徒步鞋\n雨衣\n饮水与食物\n离线地图与充电宝\n急救包',{required:true,maxLength:1500,rows:5});
  field('logistics','入口与交通','textarea','请提前确认入口与接驳。',{maxLength:1500,rows:2});
  field('risks','路况与风险提示','textarea','请关注天气、体力、开放范围与现场路况。',{maxLength:1500,rows:2});
  const submit=document.createElement('button');submit.type='submit';submit.className='social-follow';submit.textContent='发布公开线路';form.append(submit);
  function busy(value){pending=value;for(const el of form.elements)el.disabled=value;$('submit-route-close').disabled=value;submit.textContent=value?'正在发布…':'发布公开线路';}
  function distance(points){let sum=0;const rad=d=>d*Math.PI/180;for(let i=1;i<points.length;i++){const [a,b]=points[i-1],[c,d]=points[i];const h=Math.sin(rad(c-a)/2)**2+Math.cos(rad(a))*Math.cos(rad(c))*Math.sin(rad(d-b)/2)**2;sum+=6371*2*Math.asin(Math.sqrt(Math.min(1,h)));}return Math.round(sum*100)/100;}
  file.addEventListener('change',async()=>{
    gpxPoints=null;status.textContent='';if(!file.files[0])return;busy(true);
    try{
      const chosen=file.files[0];if(chosen.size>1024*1024)throw new Error('GPX 文件最大 1 MB。');
      const xml=await chosen.text();if(/<!DOCTYPE|<!ENTITY/i.test(xml))throw new Error('不支持带外部实体的 GPX。');
      const doc=new DOMParser().parseFromString(xml,'application/xml');
      if(doc.querySelector('parsererror')||doc.documentElement.localName!=='gpx')throw new Error('GPX 格式无法读取。');
      if(doc.querySelectorAll('trkseg').length>1||doc.querySelectorAll('rte').length>1||(doc.querySelector('trkpt')&&doc.querySelector('rtept')))throw new Error('请导入单段轨迹，避免把不相连的路段连在一起。');
      const nodes=[...doc.querySelectorAll('trkpt,rtept')];if(nodes.length<2||nodes.length>50000)throw new Error('GPX 需要 2–50000 个有效轨迹点。');
      const points=nodes.map(n=>[Number(n.getAttribute('lat')),Number(n.getAttribute('lon'))]);
      if(points.some(([lat,lon])=>!Number.isFinite(lat)||!Number.isFinite(lon)||lat<17||lat>55||lon<73||lon>136))throw new Error('请导入中国境内有效经纬度的轨迹。');
      gpxPoints=points.length<=300?points:Array.from({length:300},(_,i)=>points[Math.round(i*(points.length-1)/299)]);
      fields.lat.value=points[0][0];fields.lon.value=points[0][1];if(!fields.distance.value)fields.distance.value=Math.max(.1,distance(points));
      status.textContent='GPX 已读取 '+points.length+' 个轨迹点，展示 '+gpxPoints.length+' 个点。发布的是展示轨迹，不可用于现场导航。';
    }catch(e){file.value='';gpxPoints=null;status.textContent=e.message;}
    finally{busy(false);}
  });
  $('submit-route-open').addEventListener('click',()=>{if(!window.AtlasAuth.user){$('account-open').click();return;}dialog.showModal();fields.name.focus();});
  $('submit-route-close').addEventListener('click',()=>{if(!pending)dialog.close();});dialog.addEventListener('cancel',e=>{if(pending)e.preventDefault();});
  form.addEventListener('submit',async event=>{
    event.preventDefault();if(pending)return;const user=window.AtlasAuth.user;if(!user){status.textContent='请先登录。';return;}
    const data={userId:user.id};for(const key of ['name','province','description','itinerary','gear','logistics','risks'])data[key]=fields[key].value;
    for(const key of ['distance','days','altitude','level'])data[key]=Number(fields[key].value);
    data.points=gpxPoints||[[Number(fields.lat.value),Number(fields.lon.value)]];
    busy(true);status.textContent='';
    try{const result=await window.AtlasAuth.api('/api/submissions',data);window.AtlasAddRoutes([result.route]);form.reset();gpxPoints=null;dialog.close();window.AtlasExploreRoute(result.route.id);}
    catch(e){status.textContent=e.message;}
    finally{busy(false);}
  });
  window.AtlasEnsureRoute=async rid=>{const existing=window.TRAILS.find(r=>r.id===rid);if(existing)return existing;const result=await window.AtlasAuth.api('/api/submissions/'+encodeURIComponent(rid));window.AtlasAddRoutes([result.route]);return result.route;};
  async function load(){const more=$('load-community-routes');more.disabled=true;try{const result=await window.AtlasAuth.api('/api/submissions'+(cursor?'?before='+encodeURIComponent(cursor):''));window.AtlasAddRoutes(result.routes);cursor=result.next;more.hidden=!cursor;more.textContent='加载更多社区线路';}catch{more.hidden=false;more.textContent='重试加载社区线路';}finally{more.disabled=false;}}
  $('load-community-routes').addEventListener('click',load);
  async function fromHash(){const rid=location.hash.slice(1);if(!/^u-[a-z0-9-]{1,48}$/.test(rid))return;try{await window.AtlasEnsureRoute(rid);if(location.hash.slice(1)===rid)window.AtlasExploreRoute(rid);}catch{}}
  window.addEventListener('hashchange',fromHash);load().then(fromHash);
})();

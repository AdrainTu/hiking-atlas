'use strict';
(() => {
  const $=id=>document.getElementById(id),uploadDialog=$('photo-upload-dialog'),form=$('photo-upload-form'),message=$('photo-upload-status'),queueDialog=$('photo-review-dialog');
  let routeId=null,pending=false,queueRevision=0,permissionRevision=0;
  function node(tag,text,cls){const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e;}
  function button(text,action,cls='social-button'){const e=node('button',text,cls);e.type='button';e.addEventListener('click',action);return e;}
  function imageUrl(id){return '/api/photos/'+encodeURIComponent(id)+'/image';}
  function view(item){$('user-photo-image').src=imageUrl(item.id);$('user-photo-caption').textContent=item.caption+(item.username?' · '+item.username:'');$('user-photo-dialog').showModal();}
  function tile(item){const result=button('',()=>view(item),'photo-tile'),img=node('img');img.src=imageUrl(item.id);img.alt=item.caption;img.loading='lazy';result.append(img,node('span',item.caption+' · '+item.username));return result;}
  $('user-photo-close').addEventListener('click',()=>$('user-photo-dialog').close());$('user-photo-dialog').addEventListener('close',()=>$('user-photo-image').removeAttribute('src'));
  async function mount(route){
    const host=$('user-route-photos');if(!host||host.dataset.mounted)return;host.dataset.mounted='1';host.dataset.route=route;
    host.append(node('h3','同行者的线路相册','section-label'),node('p','分享本条线路的实拍照片。文件检查通过后进入待审核队列，人工通过后才公开。','social-note'));
    host.append(button('＋ 上传本条线路照片',()=>{if(!window.AtlasAuth.user){$('account-open').click();return;}routeId=route;message.textContent='';uploadDialog.showModal();}));
    const status=node('p','正在加载相册…','social-note'),gallery=node('div',undefined,'photo-grid'),mine=node('div',undefined,'photo-upload-history');host.append(status,gallery,mine);
    try{
      const data=await window.AtlasAuth.api('/api/routes/'+encodeURIComponent(route)+'/photos');if(!host.isConnected)return;
      $('photo-review-open').hidden=!data.canModerate;status.textContent=data.photos.length?'':'暂无已审核的用户照片，来分享你的山野视角。';
      for(const item of data.photos)gallery.append(tile(item));
      let cursor=data.next;
      const more=button('加载更多用户照片',async()=>{more.disabled=true;try{const page=await window.AtlasAuth.api('/api/routes/'+encodeURIComponent(route)+'/photos?before='+encodeURIComponent(cursor));if(!host.isConnected)return;for(const item of page.photos)gallery.append(tile(item));cursor=page.next;more.hidden=!cursor;}catch(e){status.textContent=e.message;}finally{more.disabled=false;}});more.hidden=!cursor;host.append(more);
      for(const item of data.mine){const row=node('div',undefined,'photo-history-row');const labels={pending:'待审核',approved:'已公开',rejected:'未通过'};row.append(button(item.caption,()=>view(item)),node('span',labels[item.status]||item.status,'photo-status-'+item.status));if(item.reason)row.append(node('p','原因：'+item.reason));mine.append(row);}
      const photos=data.photos.map(item=>({url:location.origin+imageUrl(item.id),source:location.origin+imageUrl(item.id),caption:item.caption,author:'上传者 '+item.username,license:'用户投稿 · 非开放授权'}));
      const changed=JSON.stringify(window.AtlasRoutePhotos.photos[route]||[])!==JSON.stringify(photos);window.AtlasRoutePhotos.photos[route]=photos;if(changed)window.AtlasRefreshPhotoGallery?.(route);
    }catch(e){if(host.isConnected)status.textContent=e.message;}
  }
  window.AtlasRoutePhotos={photos:{},mount,refresh(){const host=$('user-route-photos');if(host){const route=host.dataset.route;host.replaceChildren();delete host.dataset.mounted;mount(route);}}};
  $('photo-upload-close').addEventListener('click',()=>{if(!pending)uploadDialog.close();});uploadDialog.addEventListener('cancel',e=>{if(pending)e.preventDefault();});
  async function encodedPhoto(file){
    if(!file||file.size>8*1024*1024)throw new Error('请选择 8 MB 内的 JPEG、PNG 或 WebP 照片。');
    if(!['image/jpeg','image/png','image/webp'].includes(file.type))throw new Error('只支持 JPEG、PNG、WebP。');
    const bitmap=await createImageBitmap(file);try{
      if(bitmap.width<64||bitmap.height<64||bitmap.width*bitmap.height>64000000)throw new Error('照片尺寸不符合要求。');
      const scale=Math.min(1,1600/Math.max(bitmap.width,bitmap.height)),canvas=document.createElement('canvas');canvas.width=Math.round(bitmap.width*scale);canvas.height=Math.round(bitmap.height*scale);
      const ctx=canvas.getContext('2d');ctx.fillStyle='#fff';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.drawImage(bitmap,0,0,canvas.width,canvas.height);
      let url=canvas.toDataURL('image/jpeg',.8);if(url.length>1000000)url=canvas.toDataURL('image/jpeg',.6);
      if(url.length>1000000)throw new Error('压缩后仍过大，请选择更小的照片。');return url.split(',')[1];
    }finally{bitmap.close();}
  }
  form.addEventListener('submit',async e=>{
    e.preventDefault();if(pending)return;const user=window.AtlasAuth.user;if(!user){message.textContent='请先登录。';return;}
    pending=true;for(const field of form.elements)field.disabled=true;$('photo-upload-close').disabled=true;message.textContent='正在处理并提交照片…';
    try{const image=await encodedPhoto($('route-photo-file').files[0]);const result=await window.AtlasAuth.api('/api/routes/'+encodeURIComponent(routeId)+'/photos',{userId:user.id,image,caption:$('route-photo-caption').value,rightsConfirmed:$('route-photo-rights').checked});message.textContent=result.message;form.reset();window.AtlasRoutePhotos.refresh();}
    catch(error){message.textContent=error.message;}
    finally{pending=false;for(const field of form.elements)field.disabled=false;$('photo-upload-close').disabled=false;}
  });
  async function reviewQueue(mode='pending'){
    const revision=++queueRevision,permission=permissionRevision;
    const content=$('photo-review-content');content.replaceChildren(node('p','正在加载…'));if(!queueDialog.open)queueDialog.showModal();
    try{const data=await window.AtlasAuth.api('/api/photo-review?status='+mode);if(revision!==queueRevision||permission!==permissionRevision||!queueDialog.open)return;content.replaceChildren(button('待审核',()=>reviewQueue('pending')),button('已公开 / 下架管理',()=>reviewQueue('approved')));if(!data.photos.length)content.append(node('p','当前列表没有照片。'));
      for(const item of data.photos){const card=node('article',undefined,'photo-review-card'),img=node('img');img.src=imageUrl(item.id);img.alt=item.caption;img.loading='lazy';card.append(img,node('h3',item.caption),node('p','作者：'+item.username+' · 线路：'+item.route_id));const reason=node('textarea');reason.placeholder='拒绝原因：内容不适宜、与线路无关、侵权、隐私泄露等';reason.maxLength=400;reason.setAttribute('aria-label','审核原因');card.append(reason);
        for(const [decision,label] of (mode==='approved'?[['rejected','下架照片']]:[['approved','通过并公开'],['rejected','拒绝']])){const action=button(label,async()=>{const user=window.AtlasAuth.user;if(!user)return;for(const b of card.querySelectorAll('button'))b.disabled=true;try{await window.AtlasAuth.api('/api/photo-review/'+item.id,{userId:user.id,decision,reason:reason.value,expectedStatus:item.status});await reviewQueue(mode);window.AtlasRoutePhotos.refresh();}catch(e){const note=node('p',e.message);note.setAttribute('role','status');card.append(note);for(const b of card.querySelectorAll('button'))b.disabled=false;}});card.append(action);}
        content.append(card);
      }
    }catch(e){if(revision===queueRevision&&permission===permissionRevision)content.replaceChildren(node('p',e.message));}
  }
  $('photo-review-open').addEventListener('click',()=>reviewQueue());$('photo-review-close').addEventListener('click',()=>queueDialog.close());
  queueDialog.addEventListener('close',()=>{queueRevision++;$('photo-review-content').replaceChildren();});
  window.addEventListener('atlas-account',async()=>{const revision=++permissionRevision;queueDialog.close();$('photo-review-content').replaceChildren();$('user-photo-dialog').close();$('user-photo-image').removeAttribute('src');$('photo-review-open').hidden=true;uploadDialog.close();form.reset();message.textContent='';try{const data=await window.AtlasAuth.api('/api/photo-permissions');if(revision===permissionRevision)$('photo-review-open').hidden=!data.canModerate;}catch{}});
})();

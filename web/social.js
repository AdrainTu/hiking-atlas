'use strict';
(() => {
  const $=id=>document.getElementById(id),dialog=$('social-dialog'),body=$('social-content'),status=$('social-status');
  let revision=0,current=null;
  function node(tag,text,cls){const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e;}
  function button(text,action,cls='social-button'){const b=node('button',text,cls);b.type='button';b.addEventListener('click',action);return b;}
  function start(){const id=++revision;body.replaceChildren();status.textContent='正在加载…';return id;}
  function error(e,id){if(id===revision)status.textContent=e.message;}
  async function profile(uid){
    current=uid;const id=start();if(!dialog.open)dialog.showModal();
    try{
      if(window.AtlasAuth.user?.id===uid)await window.AtlasAuth.flush();
      const result=await window.AtlasAuth.api('/api/users/'+uid);if(id!==revision)return;
      status.textContent='';const self=window.AtlasAuth.user?.id===result.user.id;
      const hero=node('section',undefined,'social-profile');hero.append(node('div',result.user.username.slice(0,1),'social-avatar'),node('h3',result.user.username));
      hero.append(node('p',self?'你的山野足迹 · 点亮走过的旅程':'同行者的山野足迹'));
      const stats=node('div',undefined,'social-stats');stats.append(button('✦ '+result.completed.length+' 条已走过',()=>profile(uid)),button(result.followingCount+' 关注',()=>connections(uid,'following')),button(result.followerCount+' 粉丝',()=>connections(uid,'followers')));hero.append(stats);
      if(!self){
        const follow=button(result.isFollowing?'✓ 已关注 · 取消关注':'＋ 关注同行者',async()=>{
          const user=window.AtlasAuth.user;if(!user){dialog.close();$('account-open').click();return;}
          follow.disabled=true;
          try{await window.AtlasAuth.api('/api/users/'+uid+'/follow',{userId:user.id,following:!result.isFollowing});if(id===revision)await profile(uid);}
          catch(e){error(e,id);follow.disabled=false;}
        },'social-follow'+(result.isFollowing?' following':''));hero.append(follow);
      }
      body.append(hero,node('h4','已走过的线路','social-section-title'),node('p','点亮的线路会出现在公开主页中，同行者可以查看。','social-note'));
      const routes=node('div',undefined,'social-routes');
      for(const rid of result.completed){const route=window.TRAILS.find(t=>t.id===rid);
        const b=button(route?'✦ '+route.name+' · '+route.country:'✦ 社区线路 · 查看详情',async()=>{try{if(!route)await window.AtlasEnsureRoute?.(rid);dialog.close();window.AtlasExploreRoute?.(rid);}catch(e){error(e,id);}},'social-route');routes.append(b);}
      if(!result.completed.length)routes.append(node('p',self?'还没有点亮线路。打开线路详情，点击「点亮已走过」留下足迹。':'这位同行者还没有点亮线路。','social-empty'));
      body.append(routes);
    }catch(e){error(e,id);}
  }
  function showUsers(result,list){
    for(const user of result.users){list.append(button(user.username+'  → 查看足迹',()=>profile(user.id),'social-person'));}
  }
  async function connections(uid,kind){
    const id=start();body.append(button('← 返回个人主页',()=>profile(uid)),node('h3',kind==='following'?'关注的同行者':'粉丝'));
    const list=node('div',undefined,'social-people');body.append(list);const more=button('加载更多',()=>load(),'social-more');more.hidden=true;body.append(more);
    let cursor=null;
    async function load(){more.disabled=true;try{const result=await window.AtlasAuth.api('/api/users/'+uid+'/'+kind+(cursor?'?after='+cursor:''));if(id!==revision)return;showUsers(result,list);cursor=result.next;more.hidden=!cursor;status.textContent=list.childElementCount?'':'这里暂时还没有同行者。';}catch(e){error(e,id);}finally{more.disabled=false;}}
    load();
  }
  function explore(){
    current=null;const id=start();if(!dialog.open)dialog.showModal();
    const user=window.AtlasAuth.user;if(user)body.append(button('◉ 我的主页 / 关注 / 粉丝',()=>profile(user.id),'social-self'));
    const form=node('form',undefined,'social-search'),input=node('input');input.placeholder='搜索同行者的用户名';input.maxLength=24;input.setAttribute('aria-label','搜索用户');
    const submit=node('button','搜索');submit.type='submit';form.append(input,submit);body.append(form);
    const list=node('div',undefined,'social-people');body.append(list);const more=button('加载更多',()=>load(true),'social-more');more.hidden=true;body.append(more);
    let cursor=null,query='',sequence=0;
    async function load(append=false){const seq=++sequence;more.disabled=true;submit.disabled=true;status.textContent='正在查找同行者…';try{
      const result=await window.AtlasAuth.api('/api/users?search='+encodeURIComponent(query)+(append&&cursor?'&after='+cursor:''));if(id!==revision||seq!==sequence)return;
      if(!append)list.replaceChildren();showUsers(result,list);cursor=result.next;more.hidden=!cursor;status.textContent=list.childElementCount?'':'没有找到匹配的同行者。';
    }catch(e){error(e,id);}finally{if(seq===sequence){more.disabled=false;submit.disabled=false;}}}
    form.addEventListener('submit',e=>{e.preventDefault();query=input.value.trim();cursor=null;load();});load();
  }
  window.AtlasSocial={profile,explore};
  $('social-open').addEventListener('click',explore);$('social-close').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('close',()=>{revision++;status.textContent='';});
  window.addEventListener('atlas-account',()=>{if(dialog.open)explore();});
})();

'use strict';
(() => {
  const drafts=new Map();
  const labels={experience:'徒步经验',conditions:'路况反馈',gear:'装备建议',question:'线路提问'};
  function node(tag,text,className){const el=document.createElement(tag);if(text!==undefined)el.textContent=text;if(className)el.className=className;return el;}
  window.AtlasComments={mount(route){
    const host=document.getElementById('route-comments');if(!host||host.dataset.mounted)return;
    host.dataset.mounted='1';
    const title=node('h3','线路讨论','section-label');const count=node('span','', 'comment-count');title.append(count);host.append(title);
    host.append(node('p','分享走过的路、装备体验和出行日期，也可以向同行者提问。','comment-intro'));
    const user=window.AtlasAuth?.user;
    const form=node('form',undefined,'comment-form');
    const select=node('select');select.setAttribute('aria-label','讨论类型');
    for(const [value,label] of Object.entries(labels)){const option=node('option',label);option.value=value;select.append(option);}
    const input=node('textarea');input.placeholder='例如：10 月走过这条线，垭口风大，建议带防风外套……';input.setAttribute('aria-label','线路评论');input.maxLength=2000;input.minLength=2;input.required=true;input.rows=4;
    input.value=drafts.get(route)||'';input.addEventListener('input',()=>{drafts.set(route,input.value);length.textContent=input.value.length+' / 2000';});
    const length=node('small',input.value.length+' / 2000');const submit=node('button','发布评论','comment-submit');submit.type='submit';
    const bar=node('div',undefined,'comment-form-bar');bar.append(length,submit);
    if(user){form.append(node('p','以 '+user.username+' 的身份分享'),select,input,bar);host.append(form);}
    else {const login=node('button','登录 / 注册后参与讨论','comment-submit');login.type='button';login.addEventListener('click',()=>document.getElementById('account-open').click());host.append(login);}
    const status=node('p','正在加载讨论…','comment-status');status.setAttribute('role','status');host.append(status);
    const list=node('div',undefined,'comment-list');host.append(list);
    const more=node('button','加载更多','comment-more');more.type='button';more.hidden=true;host.append(more);
    let cursor=null,loading=false;
    async function load(append=false){
      if(loading)return;loading=true;more.disabled=true;submit.disabled=true;
      try{
        const result=await window.AtlasAuth.api('/api/routes/'+encodeURIComponent(route)+'/comments'+(append&&cursor?'?before='+cursor:''));
        if(!host.isConnected)return;
        if(!append)list.replaceChildren();count.textContent=' · '+result.total+' 条';
        for(const item of result.comments){
          const card=node('article',undefined,'comment-card');const head=node('div',undefined,'comment-meta');
          const date=new Date(item.created_at*1000);const time=node('time',date.toLocaleString('zh-CN',{year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit'}));time.dateTime=date.toISOString();
          head.append(node('strong',item.username),node('span',labels[item.category]||'徒步经验','comment-tag'),time);
          card.append(head,node('p',item.content,'comment-body'));list.append(card);
        }
        cursor=result.next;more.hidden=!cursor;more.textContent='加载更多';status.textContent=result.total?'':'还没有讨论，来分享这条线路的第一份经验吧。';
      }catch(error){if(host.isConnected){status.textContent=error.message;more.hidden=false;more.textContent='重试加载';}}
      finally{loading=false;more.disabled=false;if(submit.textContent!=='正在发布…')submit.disabled=false;}
    }
    more.addEventListener('click',()=>load(!!cursor));
    form.addEventListener('submit',async event=>{
      event.preventDefault();if(submit.disabled)return;
      if(window.AtlasAuth.user?.id!==user.id){status.textContent='账号已切换，请重新打开这条线路。';return;}
      submit.disabled=true;input.disabled=true;select.disabled=true;submit.textContent='正在发布…';
      try{
        await window.AtlasAuth.api('/api/routes/'+encodeURIComponent(route)+'/comments',{userId:user.id,category:select.value,content:input.value.trim()});
        drafts.delete(route);input.value='';length.textContent='0 / 2000';
        if(host.isConnected){await load();status.textContent='评论已发布，谢谢你分享经验。';}
      }catch(error){if(host.isConnected)status.textContent=error.message;}
      finally{submit.disabled=false;input.disabled=false;select.disabled=false;submit.textContent='发布评论';}
    });
    load();
  }};
})();

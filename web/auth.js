'use strict';
(() => {
  const $=id=>document.getElementById(id);
  let mode='login',user=null,pending=false,ready=false;
  async function api(path,data) {
    const response=await fetch(path,{method:data===undefined?'GET':'POST',credentials:'same-origin',cache:'no-store',keepalive:path==='/api/preferences'&&data!==undefined,headers:{'Content-Type':'application/json','X-Atlas-Request':'1'},...(data===undefined?{}:{body:JSON.stringify(data)})});
    let result;
    try {result=await response.json();} catch {throw new Error('账号服务尚未启动，请重启项目服务后重试。');}
    if(!response.ok){const error=new Error(result.error || '操作未成功，请稍后重试。');error.status=response.status;throw error;}
    return result;
  }
  function message(text,error=false){$('auth-message').textContent=text;$('auth-message').classList.toggle('error',error);}
  function render() {
    $('account-open').textContent=user?'◉ '+user.username:'◉ 登录 / 注册';
    $('account-open').title=user?'管理账号：'+user.username:'登录或注册账号';
    $('auth-title').textContent=user?'你的山野账户':mode==='login'?'欢迎回到野途':'开启你的山野旅程';
    $('auth-account').hidden=!user;$('auth-form').hidden=!!user;$('auth-switches').hidden=!!user;
    $('auth-name').textContent=user?.username || '';
    $('auth-confirm-row').hidden=mode!=='register';$('auth-confirm').required=mode==='register'&&!user;
    $('auth-password').minLength=mode==='register'?12:1;
    $('auth-password').autocomplete=mode==='register'?'new-password':'current-password';
    $('auth-password-help').textContent=mode==='register'?'至少 12 个字符，最长 128 个字符。建议使用独有的长口令。':'输入注册时设置的密码。';
    $('auth-submit').textContent=pending?'正在处理…':mode==='login'?'登录，继续探索':'注册并登录';
    $('auth-submit').disabled=$('auth-logout').disabled=pending;
    for(const value of ['login','register']){$('auth-'+value+'-tab').classList.toggle('active',mode===value);$('auth-'+value+'-tab').setAttribute('aria-pressed',String(mode===value));$('auth-'+value+'-tab').disabled=pending;}
  }
  async function acceptUser(nextUser) {
    const preferences=nextUser?await api('/api/preferences'):null;
    user=nextUser;ready=true;window.AtlasAuth.user=user;
    window.dispatchEvent(new CustomEvent('atlas-account',{detail:{user,preferences}}));render();
  }
  const auth=window.AtlasAuth={user:null,api,flush:async()=>{}};
  $('account-open').addEventListener('click',()=>{render();message(ready?'':'正在连接账号服务…');$('auth-dialog').showModal();if(!user)$('auth-username').focus();});
  $('auth-close').addEventListener('click',()=>{if(!pending)$('auth-dialog').close();});
  $('auth-dialog').addEventListener('cancel',event=>{if(pending)event.preventDefault();});
  $('auth-dialog').addEventListener('close',()=>{$('auth-password').value='';$('auth-confirm').value='';});
  for(const value of ['login','register'])$('auth-'+value+'-tab').addEventListener('click',()=>{mode=value;message('');$('auth-password').value='';$('auth-confirm').value='';render();});
  $('auth-form').addEventListener('submit',async event=>{
    event.preventDefault();if(pending)return;
    if(mode==='register'&&$('auth-password').value!==$('auth-confirm').value){message('两次输入的密码不一致。',true);$('auth-confirm').focus();return;}
    pending=true;render();message('');
    try {const result=await api('/api/auth/'+mode,{username:$('auth-username').value.trim(),password:$('auth-password').value});await acceptUser(result.user);message(mode==='register'?'注册成功，已自动登录。':'登录成功，账号资料已加载。');$('auth-password').value='';$('auth-confirm').value='';}
    catch(error){message(error.message || '连接失败，请检查本地服务。',true);}
    finally{pending=false;render();}
  });
  $('auth-logout').addEventListener('click',async()=>{
    if(pending)return;pending=true;render();message('');
    try {try{await auth.flush();}catch(error){if(error.status!==401)throw error;}await api('/api/auth/logout',{});await acceptUser(null);mode='login';message('已退出登录，当前显示访客的收藏与装备。');}
    catch(error){message(error.message || '退出未完成，请重试。',true);}
    finally{pending=false;render();}
  });
  render();
  (async()=>{try {const result=await api('/api/auth/me');await acceptUser(result.user);ready=true;} catch {message('账号服务未连接。请重启项目服务后，再刷新页面。',true);}})();
})();

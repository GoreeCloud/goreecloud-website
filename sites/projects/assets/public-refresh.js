const currentProjectDirection={
  'GoreeCloud Backup':['Native rebuild target','Backup, restoration, verification, and recovery workflows are moving to an original GoreeCloud application architecture. Kopia-derived implementation remains transitional continuity and reference material until the native replacement satisfies recovery and production gates.'],
  'GoreeCloud Identity':['Native rebuild target','Central identity, authentication, single sign-on, and identity-provider capabilities are required to move to an original GoreeCloud application architecture. Existing authentik-derived work is transitional migration and reference material.'],
  'GoreeCloud GitHub Dashboard':['Transitional GitHub integration','Repository visibility remains useful during migration, but self-hosted Gitea is the planned permanent authoritative source-control platform. Future GoreeCloud development dashboards and AI integrations must be Gitea-first or provider-neutral rather than make GitHub a permanent dependency.'],
  'GoreeCloud Network':['Native rebuild active','Private networking and Conduit capabilities are moving into an original GoreeCloud application layer. NetBird and other mature protocol or networking foundations may remain only within narrowly justified technical boundaries.'],
  'GoreeCloud DNS':['Native rebuild active','DNS and Beacon capabilities are moving into an original GoreeCloud application layer. Mature DNS protocol foundations may remain where replacing them would increase standards, interoperability, or security risk, but upstream product architecture is transitional.'],
  'GoreeCloud Search':['Native rebuild active · GoreeCloud AI research provider','GoreeCloud Search is being rebuilt as original GoreeCloud-owned software and is the required first-party current-information and Internet-research provider for GoreeCloud AI. The SearXNG-derived production line remains transitional continuity and reference material.'],
  'GoreeCloud Browser':['Native rebuild target · transitional browser line','GoreeCloud Browser is moving toward an original GoreeCloud-owned product and application layer. Mature browser-engine foundations may remain where technically justified, but the inherited Firefox product architecture is transitional rather than the approved long-term application model.'],
  'GoreeCloud Memos':['Stable web/server 0.1.3 · native rebuild required','GoreeCloud Memos v0.1.3 remains the accepted production web/server release while the platform-wide native mandate requires an original GoreeCloud application end state. Newer client acceptance and native replacement work remain separately gated.'],
  'GoreeCloud Bookmarks':['Native rebuild active · foundation and persistence work integrated','The original GoreeCloud Bookmarks Go foundation has been integrated with owner-scoped records, fail-closed isolation, native service boundaries, and PostgreSQL persistence/runtime contracts progressing through validated source work. The Linkwarden-derived application and Browser capture path remain transitional continuity surfaces; no native production cutover is claimed.'],
  'GoreeCloud Photos':['Native rebuild target · transitional media service','GoreeCloud Photos is required to become an original GoreeCloud application. Immich-derived code and behavior may be retained temporarily for migration, compatibility, testing, and reference while native photo-preservation capabilities replace the upstream product layer.'],
  'GoreeCloud Video':['Native rebuild active · Milestone 1','GoreeCloud Video is being rebuilt as original GoreeCloud software. Jellyfin-derived code and protocol behavior remain transitional compatibility and reference material while native video-library, playback, client, and family capabilities replace the upstream product layer.'],
  'GoreeCloud Gallery':['Native rebuild target','GoreeCloud Gallery is required to become original GoreeCloud-owned software at the application layer. Existing upstream-derived Android gallery code is transitional while equivalent local-media capabilities are rebuilt and accepted natively.'],
  'GoreeCloud Vault Server':['Native rebuild target · transitional service','The password and credential server is required to move to an original GoreeCloud application architecture. Vaultwarden-derived code remains transitional continuity and compatibility material until the native replacement satisfies security, migration, recovery, and client-compatibility gates.'],
  'GoreeCloud Keyboard':['Native rebuild active','GoreeCloud Keyboard is an original native application target powered by first-party Quill capabilities. Any inherited upstream application layer is transitional; platform keyboard APIs, language resources, and mature technical dependencies remain bounded supporting foundations.'],
  'GoreeCloud Terminal':['50.2-rc.2 source · native rebuild required','The current 50.2-rc.2 line remains a release candidate and transitional implementation. GoreeCloud Terminal must reach an original GoreeCloud application end state while retaining only narrowly justified terminal, shell, toolkit, and operating-system foundations. Stable and production acceptance remain separate evidence gates.']
};

function ensureAugust25Entries(){
  if(!entries.some(entry=>entry.name==='GoreeCloud AI'))entries.push({name:'GoreeCloud AI',repo:'goreecloud-ai',category:'Platform & Administration',model:'Native',kind:'Application',status:'Initial native development',role:'Native AI conversation, Workspace, knowledge, RAG, research, and orchestration application. Ollama is the local model runtime and GoreeCloud Search is the first-party current-information provider; Open WebUI, AnythingLLM, and SearXNG are replacement targets.',visibility:'Private'});
  if(!entries.some(entry=>entry.name==='GoreeCloud Mesh'))entries.push({name:'GoreeCloud Mesh',repo:'goreecloud-mesh',category:'Shared Foundations',model:'Coordination and governance plane',kind:'Foundation',status:'Active development',role:'Platform-wide coordination plane for service and capability registration, explicit relationships, policy decisions, evidence-aware dependency context, lifecycle events, and interoperability. Mesh coordinates specialized systems without replacing their authority.',visibility:'Public'});
}
ensureAugust25Entries();

if(typeof appCount!=='undefined'&&appCount)appCount.textContent=entries.filter(entry=>entry.kind==='Application').length;
if(typeof foundationCount!=='undefined'&&foundationCount)foundationCount.textContent=entries.filter(entry=>entry.kind==='Foundation').length;

function applyCurrentDirection(){
  document.querySelectorAll('#projects .card').forEach(card=>{
    const name=card.querySelector('h3')?.textContent?.trim();
    const update=currentProjectDirection[name];
    if(!update)return;
    const status=card.querySelector('.status');
    const role=card.querySelector('.role');
    const model=card.querySelector('.model');
    if(status)status.textContent=update[0];
    if(role)role.textContent=update[1];
    if(model)model.textContent='Native GoreeCloud end state · transitional upstream provenance retained where applicable';
  });
}

const projectGrid=document.querySelector('#projects');
if(projectGrid){
  new MutationObserver(applyCurrentDirection).observe(projectGrid,{childList:true,subtree:true});
  render();
  applyCurrentDirection();
}

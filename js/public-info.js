const s=document.querySelector('[data-service="memos"]');
if(s){const p=s.querySelector('p:not(.service-kicker)'),b=s.querySelector('.badge');if(p)p.textContent='A lightweight GoreeCloud quick-note capture application for fast, focused notes when a full knowledge workspace is unnecessary. GoreeCloud Memos v0.1.3 is the accepted Stable production web/server release while newer client acceptance and the mandatory native-rebuild direction continue separately.';if(b)b.textContent='Stable 0.1.3';}

const projectMemos=document.querySelector('[data-project="goreecloud-memos"]');
if(projectMemos){const d=projectMemos.querySelector('span'),t=projectMemos.querySelector('small');if(d)d.textContent='Quick-note capture remains available through the accepted v0.1.3 web/server release while GoreeCloud applies the platform-wide native-application mandate and keeps newer client acceptance separate.';if(t)t.textContent='Stable production web/server v0.1.3 · native rebuild required';}

const serviceIntro=document.querySelector('#services .section-heading p:last-child');
if(serviceIntro)serviceIntro.textContent='GoreeCloud uses open-source infrastructure and narrowly scoped supporting components while every GoreeCloud application is now required to become an original, native-from-the-ground-up GoreeCloud implementation. Existing upstream applications may remain temporarily for continuity, migration, compatibility, testing, or reference, but they are not permanent GoreeCloud application architectures. Public descriptions stay high level; private service addresses, internal topology, and administrative interfaces are intentionally not published here.';

const platformIntro=document.querySelector('#platform .section-heading p:last-child');
if(platformIntro)platformIntro.textContent='The current VPS foundation and planned local Proxmox environment use separate open-source technologies for virtualization, Linux, containers, private networking, DNS, HTTPS, monitoring, notifications, backup, and private search. These supporting foundations remain independently replaceable. At the application layer, GoreeCloud now requires original native implementations, with complete upstream products limited to controlled transitional or reference roles.';

for(const card of document.querySelectorAll('#platform .platform-card')){
  const title=card.querySelector('h3')?.textContent?.trim();
  if(title==='GoreeCloud Search'){
    const description=card.querySelector('.platform-description');
    const role=card.querySelector('.platform-role');
    if(description)description.textContent='GoreeCloud Search is the current GoreeCloud-facing private search service while a native GoreeCloud-owned replacement is actively being built. The SearXNG-derived production line remains transitional continuity and reference material, not the approved long-term application architecture.';
    if(role)role.innerHTML='<strong>Role:</strong> Private search, discovery, Browser integration, and local-AI research gateway while the native replacement advances through controlled validation.';
  }
}

const heroNote=document.querySelector('.current-platform-update');
if(heroNote){
  heroNote.textContent='Glaze UI, Wardveil Security, Privacy Shield, and Everkeep are mandatory integral GoreeCloud platform systems—not decorative labels. Every GoreeCloud application must be an original native implementation and remain current with all four applicable platform contracts before Stable qualification. Public claims remain limited to what current implementation and evidence can support.';
  const mandate=document.createElement('p');
  mandate.className='status-note native-application-update';
  mandate.textContent='Native application direction · August 24, 2026: maintained forks and adopted complete application codebases are transitional migration, compatibility, testing, historical, or reference sources only. Narrow mature technical dependencies may remain where replacing them would materially increase security, standards, protocol, codec, rendering, runtime, or interoperability risk.';
  heroNote.after(mandate);
}

const footer=document.querySelector('.footer-glaze');
if(footer)footer.innerHTML='<strong>Glaze UI</strong> design • <strong>Privacy Shield</strong> privacy • <strong>Wardveil Security</strong> security • <strong>Everkeep</strong> resilience &amp; preservation.';

const story=document.querySelector('#story .timeline');
if(story&&!story.querySelector('[data-native-mandate]')){
  const article=document.createElement('article');
  article.dataset.nativeMandate='true';
  article.innerHTML='<time datetime="2026-08-24">August 24, 2026</time><div><h3>Native applications become the mandatory end state</h3><p>GoreeCloud formalizes original native-from-the-ground-up application development as the required product model. Existing upstream-derived applications become controlled transition and reference surfaces, while Glaze UI, Wardveil Security, Privacy Shield, and Everkeep become mandatory Stable-release gates.</p></div>';
  const final=story.querySelector('article:last-child');
  if(final)story.insertBefore(article,final);else story.append(article);
}

const projectUpdates={
  'goreecloud-bookmarks':{
    description:'GoreeCloud Bookmarks now has an integrated original Go foundation with owner-scoped records, validated native service boundaries, and PostgreSQL persistence/runtime work progressing. The Linkwarden-derived application and existing Browser capture path remain transitional continuity surfaces until equivalent native capabilities and production evidence are complete.',
    status:'Native rebuild active · transitional production continuity'
  },
  'goreecloud-search':{
    description:'Private web search and GoreeCloud-controlled research gateway. The current SearXNG-derived service remains transitional while the native GoreeCloud Search replacement preserves required features and advances through controlled validation.',
    status:'Native rebuild active · transitional service maintained'
  },
  'goreecloud-browser':{
    description:'Privacy-first browser project moving toward a fully GoreeCloud-owned native product layer while retaining mature browser-engine foundations only where technically justified. Existing Firefox-derived application architecture is transitional.',
    status:'Native rebuild target · transitional browser line active'
  },
  'goreecloud-video':{
    description:'Private video library and playback platform being rebuilt as original GoreeCloud software. Jellyfin-derived code and protocol behavior remain transitional compatibility/reference material while native server and client capabilities replace the upstream product layer.',
    status:'Native rebuild active · Milestone 1 development'
  },
  'goreecloud-backup':{
    description:'Backup, restoration, verification, and recovery workflows under Everkeep are moving to an original GoreeCloud application architecture. Kopia-derived implementation remains transitional continuity/reference material until the native replacement satisfies recovery and production gates.',
    status:'Native rebuild required · transitional continuity'
  }
};
for(const [name,update] of Object.entries(projectUpdates)){
  const card=document.querySelector(`[data-project="${name}"]`);
  if(!card)continue;
  const description=card.querySelector('span');
  const status=card.querySelector('small');
  if(description)description.textContent=update.description;
  if(status)status.textContent=update.status;
}

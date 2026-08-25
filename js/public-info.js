const projectMemos=document.querySelector('[data-project="goreecloud-memos"]');
if(projectMemos){const d=projectMemos.querySelector('span'),t=projectMemos.querySelector('small');if(d)d.textContent='Quick-note capture remains available through the accepted v0.1.3 web/server release while GoreeCloud applies the platform-wide native-application mandate and keeps newer client acceptance separate.';if(t)t.textContent='Stable production web/server v0.1.3 · native rebuild required';}

const serviceIntro=document.querySelector('#services .section-heading p:last-child');
if(serviceIntro)serviceIntro.textContent='This directory presents GoreeCloud products rather than the complete upstream applications used for migration, compatibility, testing, or reference. Every GoreeCloud Suite application is required to become an original GoreeCloud-owned native implementation. Narrowly scoped mature technical dependencies may remain where they materially improve security, standards, protocol, codec, runtime, rendering, or interoperability outcomes.';

const pendingArt='assets/services/goreecloud-artwork-pending.svg';
const serviceDirectory=[
  {key:'drive',name:'GoreeCloud Drive',kicker:'Files & Storage',description:'The first-party GoreeCloud file-management application for owned files, folders, sharing, storage access, organization, and user-scoped data boundaries. Synchronization and secure transfer are provided by GoreeCloud Sync as a separate first-party capability.',status:'Native Development'},
  {key:'sync',name:'GoreeCloud Sync',kicker:'Sync & Transfer',description:'The first-party synchronization and secure-transfer application for controlled file replication, device synchronization, movement, and portability across GoreeCloud-managed storage and supported clients.',status:'Native Development'},
  {key:'photos',name:'GoreeCloud Photos',kicker:'Photos & Memories',description:'The first-party photo and personal-video preservation application for organization, memories, search, private sharing, camera media, and long-term ownership. Upstream photo applications are transition or reference sources rather than the GoreeCloud product identity.',status:'Native Development'},
  {key:'video',name:'GoreeCloud Video',kicker:'Video & Media',description:'The first-party video-streaming application for movies, television, home videos, profiles, discovery, and playback. Jellyfin-derived material is retained only where needed for transition, compatibility, migration, recovery, or engineering reference while the native GoreeCloud product advances.',status:'Native Development'},
  {key:'music',name:'GoreeCloud Music',kicker:'Music',description:'The first-party self-hosted music application for owned libraries, scanning, metadata, artwork, playback, multi-user access, and the GoreeCloud Resonance capability family.',status:'Native Development'},
  {key:'documents',name:'GoreeCloud Documents',kicker:'Documents & Records',description:'The first-party document and records direction for ingestion, organization, search, preservation, OCR-related workflows, and durable ownership of important documents without making Paperless-ngx the permanent product architecture.',status:'Planned Native'},
  {key:'vault-server',name:'GoreeCloud Vault Server',kicker:'Passwords & Secrets',description:'The first-party server direction for passwords, credentials, secure records, recovery information, and other sensitive data. Existing Vaultwarden-derived material is transitional continuity and compatibility material, not the final product identity.',status:'Native Development'},
  {key:'notes',name:'GoreeCloud Notes',kicker:'Notes & Knowledge',description:'The larger native GoreeCloud note-taking, knowledge-management, and personal-productivity application for deeper organization, retrieval, durable knowledge, and cross-application workflows.',status:'Native Development'},
  {key:'memos',name:'GoreeCloud Memos',kicker:'Quick Capture',description:'A lightweight GoreeCloud quick-note capture application for fast, focused notes when a full knowledge workspace is unnecessary. GoreeCloud Memos v0.1.3 is the accepted Stable production web/server release while newer client acceptance remains separate.',status:'Stable 0.1.3',art:'assets/services/goreecloud-memos.svg',active:true},
  {key:'messenger',name:'GoreeCloud Messenger',kicker:'Messaging & Calling',description:'The original GoreeCloud communication application for GoreeCloud Data messaging, supported E2EE, usernames, groups, attachments, voice/video architecture, and optional SMS, MMS, or RCS adapters where the client platform legitimately supports them.',status:'Native Development'},
  {key:'tasks',name:'GoreeCloud Tasks',kicker:'Tasks & Projects',description:'Native multi-user task and project management for personal, family, collaborative, and GoreeCloud operational work with private-by-default data boundaries.',status:'Native Development'},
  {key:'contacts',name:'GoreeCloud Contacts',kicker:'Contacts & Address Book',description:'Native contacts management built around CardDAV interoperability, controlled writes, individual data boundaries, portable address-book data, and first-party GoreeCloud workflows.',status:'Native Development'},
  {key:'ai',name:'GoreeCloud AI',kicker:'Local AI & Research',description:'The first-party GoreeCloud AI application around Ollama, with an established source foundation for native conversation and a broader Workspace, knowledge, RAG, research, file, tool, and orchestration direction. This remains a development milestone rather than a production claim.',status:'Initial Source Foundation'}
];

const serviceGrid=document.querySelector('#services .service-grid');
if(serviceGrid){
  const cards=serviceDirectory.map((service)=>{
    const card=document.createElement('article');
    card.className='service-card';
    card.dataset.service=service.key;

    const art=document.createElement('div');
    art.className='service-art';
    const image=document.createElement('img');
    image.src=service.art||pendingArt;
    image.width=52;
    image.height=52;
    image.alt='';
    art.append(image);
    if(!service.art){
      art.setAttribute('aria-label',`Official ${service.name} artwork pending`);
      art.title=`Official ${service.name} artwork pending`;
    }else{
      art.setAttribute('aria-hidden','true');
    }

    const kicker=document.createElement('p');
    kicker.className='service-kicker';
    kicker.textContent=service.kicker;
    const title=document.createElement('h3');
    title.textContent=service.name;
    const description=document.createElement('p');
    description.textContent=service.description;
    const badge=document.createElement('span');
    badge.className=`badge ${service.active?'active':'growing'}`;
    badge.textContent=service.status;
    card.append(art,kicker,title,description,badge);
    return card;
  });
  serviceGrid.replaceChildren(...cards);

  const note=serviceGrid.nextElementSibling;
  if(note?.classList.contains('status-note'))note.textContent='The public directory uses current GoreeCloud application identities and current GoreeCloud status—not upstream product names or upstream maturity. A neutral GoreeCloud artwork marker means the application does not yet have approved canonical product artwork; upstream logos are not substituted for missing first-party identity.';
}

const platformIntro=document.querySelector('#platform .section-heading p:last-child');
if(platformIntro)platformIntro.textContent='The current VPS foundation and planned local Proxmox environment use separate open-source technologies for virtualization, Linux, containers, private networking, DNS, HTTPS, monitoring, notifications, backup, private search, and local AI. These supporting foundations remain independently replaceable. At the application layer, GoreeCloud requires original native implementations, with complete upstream products limited to controlled transitional or reference roles.';

for(const card of document.querySelectorAll('#platform .platform-card')){
  const title=card.querySelector('h3')?.textContent?.trim();
  if(title==='GoreeCloud Search'){
    const description=card.querySelector('.platform-description');
    const role=card.querySelector('.platform-role');
    if(description)description.textContent='GoreeCloud Search is being rebuilt as the first-party private search and Internet-research provider for GoreeCloud, including the research boundary used by GoreeCloud AI. Native Search now includes a fail-closed category request and readiness contract with accessible category controls. The SearXNG-derived production line remains transitional continuity and reference material, not the approved long-term application architecture.';
    if(role)role.innerHTML='<strong>Role:</strong> Private search, discovery, Browser integration, and the current-information research provider for GoreeCloud AI while native request, category, and readiness boundaries advance through controlled validation.';
  }
}

const platformGrid=document.querySelector('#platform .platform-grid');
if(platformGrid&&!platformGrid.querySelector('[data-platform="mesh"]')){
  const card=document.createElement('article');
  card.className='platform-card';
  card.dataset.platform='mesh';
  card.innerHTML='<div class="platform-card-head"><span class="platform-state planned">Active Development</span></div><p class="platform-kicker">Coordination &amp; Governance</p><h3>GoreeCloud Mesh</h3><p class="platform-description">Mesh now implements fail-closed scoped authorization for private mutating APIs, producer-bound evidence validity, and durable Everkeep recovery-evidence persistence. These capabilities coordinate platform relationships without allowing Mesh to manufacture stronger privacy, security, conformance, or recovery state.</p><p class="platform-role"><strong>Role:</strong> Service and capability registration, explicit relationships, policy decisions, lifecycle events, dependency context, and evidence-aware coordination while specialized systems retain authority.</p>';
  platformGrid.append(card);
}

const heroLabels=document.querySelector('#top .hero-labels');
if(heroLabels){
  const platformLabels=[['Glaze UI','https://design.goreecloud.com/'],['Privacy Shield','https://privacy.goreecloud.com/'],['Wardveil Security','https://security.goreecloud.com/'],['Everkeep',null],['GoreeCloud Mesh',null],['GoreeCloud Identity',null]];
  heroLabels.replaceChildren();
  for(const [label,href] of platformLabels){const chip=document.createElement(href?'a':'span');chip.className='glaze-chip';chip.textContent=label;if(href)chip.href=href;heroLabels.append(chip);}
  const eyebrow=document.createElement('span');eyebrow.className='eyebrow';eyebrow.textContent='Design • Privacy • Security • Resilience • Coordination • Identity';heroLabels.append(eyebrow);
}

const heroNote=document.querySelector('.current-platform-update');
if(heroNote){
  heroNote.textContent='Glaze UI, Wardveil Security, Privacy Shield, Everkeep, and GoreeCloud Mesh are integral GoreeCloud platform systems—not decorative labels. Glaze UI defines interface behavior, Wardveil and Privacy Shield preserve evidence-backed security and privacy state, Everkeep governs resilience and preservation, and Mesh coordinates relationships without replacing the authority of specialized systems.';
  if(!document.querySelector('.native-application-update')){const mandate=document.createElement('p');mandate.className='status-note native-application-update';mandate.textContent='Native application direction · August 24, 2026: maintained forks and adopted complete application codebases are transitional migration, compatibility, testing, historical, or reference sources only. Narrow mature technical dependencies may remain where replacing them would materially increase security, standards, protocol, codec, rendering, runtime, or interoperability risk.';heroNote.after(mandate);const current=document.createElement('p');current.className='status-note current-platform-update-2026-08-25';current.textContent='August 25, 2026 implementation pulse: GoreeCloud AI now has a first-party source repository for its Ollama front end; GoreeCloud Search has a native fail-closed category contract; and Mesh now enforces scoped private API authorization while persisting producer-bound Everkeep recovery evidence. These are source and contract milestones, not automatic Stable or production acceptance.';mandate.after(current);}
}

const footer=document.querySelector('.footer-glaze');
if(footer)footer.innerHTML='<strong>Glaze UI</strong> design • <strong>Privacy Shield</strong> privacy • <strong>Wardveil Security</strong> security • <strong>Everkeep</strong> resilience &amp; preservation • <strong>Mesh</strong> coordination.';

const story=document.querySelector('#story .timeline');
if(story&&!story.querySelector('[data-native-mandate]')){const article=document.createElement('article');article.dataset.nativeMandate='true';article.innerHTML='<time datetime="2026-08-24">August 24, 2026</time><div><h3>Native applications become the mandatory end state</h3><p>GoreeCloud formalizes original native-from-the-ground-up application development as the required product model. Existing upstream-derived applications become controlled transition and reference surfaces, while Glaze UI, Wardveil Security, Privacy Shield, and Everkeep become mandatory Stable-release gates.</p></div>';const final=story.querySelector('article:last-child');if(final)story.insertBefore(article,final);else story.append(article);}
if(story&&!story.querySelector('[data-ai-gitea-milestone]')){const article=document.createElement('article');article.dataset.aiGiteaMilestone='true';article.innerHTML='<time datetime="2026-08-25">August 25, 2026</time><div><h3>GoreeCloud AI, Mesh, and self-hosted source control become explicit platform directions</h3><p>GoreeCloud AI is defined as the native AI application around Ollama, Workspaces, knowledge, RAG, and GoreeCloud Search. GoreeCloud Mesh advances as the coordination and governance plane for platform relationships, while self-hosted Gitea is selected as the planned permanent authoritative source-control platform.</p></div>';story.append(article);}
if(story&&!story.querySelector('[data-implementation-pulse]')){const article=document.createElement('article');article.dataset.implementationPulse='true';article.innerHTML='<time datetime="2026-08-25">August 25, 2026</time><div><h3>AI source, Mesh durability, and native Search boundaries move from direction into code</h3><p>The first GoreeCloud AI source repository is established for the Ollama-facing native application. Mesh adds scoped private API authorization plus durable producer-bound Everkeep recovery evidence, while GoreeCloud Search adds a fail-closed native category request and readiness contract. Each remains subject to its separate validation, release, and production gates.</p></div>';story.append(article);}

const projectUpdates={
  'goreecloud-bookmarks':{description:'GoreeCloud Bookmarks now has an integrated original Go foundation with owner-scoped records, validated native service boundaries, PostgreSQL persistence/runtime work, fail-closed native repository mode selection, and a fail-closed native readiness boundary. The Linkwarden-derived application and existing Browser capture path remain transitional continuity surfaces until equivalent native capabilities and production evidence are complete.',status:'Native rebuild active · fail-closed native readiness boundary added'},
  'goreecloud-search':{description:'Private web search and GoreeCloud-controlled research gateway. GoreeCloud Search is the required first-party current-information provider for GoreeCloud AI; native Search now includes a fail-closed category request/readiness contract and accessible native category controls. The current SearXNG-derived service remains transitional while the native replacement advances through controlled validation.',status:'Native rebuild active · native category contract implemented'},
  'goreecloud-browser':{description:'Privacy-first browser project moving toward a fully GoreeCloud-owned native product layer while retaining mature browser-engine foundations only where technically justified. Existing Firefox-derived application architecture is transitional.',status:'Native rebuild target · transitional browser line active'},
  'goreecloud-video':{description:'Private video library and playback platform advancing as original GoreeCloud software. Jellyfin-derived material remains transitional compatibility, migration, recovery, and reference material while native server and client capabilities replace the upstream product layer.',status:'Native development · Jellyfin product identity retired'},
  'goreecloud-backup':{description:'Backup, restoration, verification, and recovery workflows under Everkeep are moving to an original GoreeCloud application architecture. Kopia-derived implementation remains transitional continuity/reference material until the native replacement satisfies recovery and production gates.',status:'Native rebuild required · transitional continuity'},
  'goreecloud-github-dashboard':{description:'Repository and development visibility remains useful during the GitHub transition, but the permanent platform direction is self-hosted Gitea. Future first-party development dashboards and GoreeCloud AI integrations must target provider-neutral or Gitea-first boundaries rather than make GitHub a permanent dependency.',status:'Transitional GitHub integration · Gitea direction planned'}
};
for(const [name,update] of Object.entries(projectUpdates)){const card=document.querySelector(`[data-project="${name}"]`);if(!card)continue;const description=card.querySelector('span');const status=card.querySelector('small');if(description)description.textContent=update.description;if(status)status.textContent=update.status;}

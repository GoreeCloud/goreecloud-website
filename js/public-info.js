const s=document.querySelector('[data-service="memos"]');
if(s){const p=s.querySelector('p:not(.service-kicker)'),b=s.querySelector('.badge');if(p)p.textContent='A lightweight GoreeCloud quick-note capture application for fast, focused notes when a full knowledge workspace is unnecessary. GoreeCloud Memos v0.1.3 is the accepted Stable production web/server release while newer client acceptance and the mandatory native-rebuild direction continue separately.';if(b)b.textContent='Stable 0.1.3';}

const projectMemos=document.querySelector('[data-project="goreecloud-memos"]');
if(projectMemos){const d=projectMemos.querySelector('span'),t=projectMemos.querySelector('small');if(d)d.textContent='Quick-note capture remains available through the accepted v0.1.3 web/server release while GoreeCloud applies the platform-wide native-application mandate and keeps newer client acceptance separate.';if(t)t.textContent='Stable production web/server v0.1.3 · native rebuild required';}

const serviceIntro=document.querySelector('#services .section-heading p:last-child');
if(serviceIntro)serviceIntro.textContent='GoreeCloud uses open-source infrastructure and narrowly scoped supporting components while every GoreeCloud application is required to become an original, native-from-the-ground-up GoreeCloud implementation. Existing upstream applications may remain temporarily for continuity, migration, compatibility, testing, or reference, but they are not permanent GoreeCloud application architectures. Public descriptions stay high level; private service addresses, internal topology, and administrative interfaces are intentionally not published here.';

const serviceReplacements={
  nextcloud:['GoreeCloud Drive + Sync','Files & Sync','GoreeCloud Drive is the first-party file-management platform and GoreeCloud Sync is the first-party synchronization and secure-transfer platform. Nextcloud remains a historical or transitional reference rather than the intended GoreeCloud product layer.','Native Development'],
  immich:['GoreeCloud Photos','Photos & Memories','GoreeCloud Photos is the native long-term photo and video preservation, organization, search, and sharing application. Immich-derived behavior may remain temporarily for migration, compatibility, testing, and reference while the native product is completed.','Native Rebuild'],
  jellyfin:['GoreeCloud Video','Video & Media','GoreeCloud Video is the first-party private video library and playback application. Jellyfin-derived code and protocol behavior remain transitional compatibility and reference material while the native server and clients advance.','Native Rebuild'],
  navidrome:['GoreeCloud Music','Music','GoreeCloud Music is the first-party self-hosted music service for owned libraries, scanning, metadata, artwork, playback, and Resonance capabilities.','Native Development'],
  paperless:['GoreeCloud Documents','Documents & Records','GoreeCloud Documents is the planned first-party document-management direction for important records, ingestion, organization, search, and preservation. Paperless-ngx remains a reference point rather than the intended GoreeCloud product layer.','Planned Native'],
  element:['GoreeCloud Messenger','Messaging','GoreeCloud Messenger is the first-party private communication application for data messaging and future standards-compatible messaging, group, voice, and video capabilities with explicit privacy and security boundaries.','Native Development']
};
for(const [key,[name,kicker,description,badgeText]] of Object.entries(serviceReplacements)){
  const card=document.querySelector(`[data-service="${key}"]`);
  if(!card)continue;
  const title=card.querySelector('h3');
  const kick=card.querySelector('.service-kicker');
  const descriptionNode=card.querySelector('p:not(.service-kicker)');
  const badge=card.querySelector('.badge');
  const art=card.querySelector('.service-art');
  if(title)title.textContent=name;
  if(kick)kick.textContent=kicker;
  if(descriptionNode)descriptionNode.textContent=description;
  if(badge){badge.textContent=badgeText;badge.className='badge growing';}
  if(art)art.hidden=true;
}

const serviceGrid=document.querySelector('#services .service-grid');
if(serviceGrid&&!serviceGrid.querySelector('[data-service="ai"]')){
  const card=document.createElement('article');
  card.className='service-card';
  card.dataset.service='ai';
  card.innerHTML='<p class="service-kicker">Local AI & Research</p><h3>GoreeCloud AI</h3><p>GoreeCloud AI is the native conversation, Workspace, knowledge, RAG, research, and AI-orchestration application. Ollama remains the local model runtime, while GoreeCloud Search is the required first-party current-information provider. Open WebUI, AnythingLLM, and SearXNG are replacement targets rather than long-term product dependencies.</p><span class="badge growing">Native Development</span>';
  serviceGrid.append(card);
}

const platformIntro=document.querySelector('#platform .section-heading p:last-child');
if(platformIntro)platformIntro.textContent='The current VPS foundation and planned local Proxmox environment use separate open-source technologies for virtualization, Linux, containers, private networking, DNS, HTTPS, monitoring, notifications, backup, private search, and local AI. These supporting foundations remain independently replaceable. At the application layer, GoreeCloud requires original native implementations, with complete upstream products limited to controlled transitional or reference roles.';

for(const card of document.querySelectorAll('#platform .platform-card')){
  const title=card.querySelector('h3')?.textContent?.trim();
  if(title==='GoreeCloud Search'){
    const description=card.querySelector('.platform-description');
    const role=card.querySelector('.platform-role');
    if(description)description.textContent='GoreeCloud Search is being rebuilt as the first-party private search and Internet-research provider for GoreeCloud, including the research boundary used by GoreeCloud AI. The SearXNG-derived production line remains transitional continuity and reference material, not the approved long-term application architecture.';
    if(role)role.innerHTML='<strong>Role:</strong> Private search, discovery, Browser integration, and the current-information research provider for GoreeCloud AI while the native replacement advances through controlled validation.';
  }
}

const heroNote=document.querySelector('.current-platform-update');
if(heroNote){
  heroNote.textContent='Glaze UI, Wardveil Security, Privacy Shield, Everkeep, and GoreeCloud Mesh are integral GoreeCloud platform systems—not decorative labels. Glaze UI defines interface behavior, Wardveil and Privacy Shield preserve evidence-backed security and privacy state, Everkeep governs resilience and preservation, and Mesh coordinates relationships without replacing the authority of specialized systems.';
  const mandate=document.createElement('p');
  mandate.className='status-note native-application-update';
  mandate.textContent='Native application direction · August 24, 2026: maintained forks and adopted complete application codebases are transitional migration, compatibility, testing, historical, or reference sources only. Narrow mature technical dependencies may remain where replacing them would materially increase security, standards, protocol, codec, rendering, runtime, or interoperability risk.';
  heroNote.after(mandate);
  const current=document.createElement('p');
  current.className='status-note current-platform-update-2026-08-25';
  current.textContent='August 25, 2026: GoreeCloud AI is now defined as the native AI experience around Ollama, Workspaces, knowledge and RAG, with GoreeCloud Search as its first-party Internet-research provider. Self-hosted Gitea is the planned permanent authoritative source-control platform; GitHub becomes a transitional migration and optional interoperability surface rather than a required dependency.';
  mandate.after(current);
}

const footer=document.querySelector('.footer-glaze');
if(footer)footer.innerHTML='<strong>Glaze UI</strong> design • <strong>Privacy Shield</strong> privacy • <strong>Wardveil Security</strong> security • <strong>Everkeep</strong> resilience &amp; preservation • <strong>Mesh</strong> coordination.';

const story=document.querySelector('#story .timeline');
if(story&&!story.querySelector('[data-native-mandate]')){
  const article=document.createElement('article');
  article.dataset.nativeMandate='true';
  article.innerHTML='<time datetime="2026-08-24">August 24, 2026</time><div><h3>Native applications become the mandatory end state</h3><p>GoreeCloud formalizes original native-from-the-ground-up application development as the required product model. Existing upstream-derived applications become controlled transition and reference surfaces, while Glaze UI, Wardveil Security, Privacy Shield, and Everkeep become mandatory Stable-release gates.</p></div>';
  const final=story.querySelector('article:last-child');
  if(final)story.insertBefore(article,final);else story.append(article);
}
if(story&&!story.querySelector('[data-ai-gitea-milestone]')){
  const article=document.createElement('article');
  article.dataset.aiGiteaMilestone='true';
  article.innerHTML='<time datetime="2026-08-25">August 25, 2026</time><div><h3>GoreeCloud AI, Mesh, and self-hosted source control become explicit platform directions</h3><p>GoreeCloud AI is defined as the native AI application around Ollama, Workspaces, knowledge, RAG, and GoreeCloud Search. GoreeCloud Mesh advances as the coordination and governance plane for platform relationships, while self-hosted Gitea is selected as the planned permanent authoritative source-control platform.</p></div>';
  story.append(article);
}

const projectUpdates={
  'goreecloud-bookmarks':{
    description:'GoreeCloud Bookmarks now has an integrated original Go foundation with owner-scoped records, validated native service boundaries, and PostgreSQL persistence/runtime work progressing. The Linkwarden-derived application and existing Browser capture path remain transitional continuity surfaces until equivalent native capabilities and production evidence are complete.',
    status:'Native rebuild active · transitional production continuity'
  },
  'goreecloud-search':{
    description:'Private web search and GoreeCloud-controlled research gateway. GoreeCloud Search is the required first-party current-information provider for GoreeCloud AI; the current SearXNG-derived service remains transitional while the native replacement preserves required features and advances through controlled validation.',
    status:'Native rebuild active · GoreeCloud AI research provider'
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
  },
  'goreecloud-github-dashboard':{
    description:'Repository and development visibility remains useful during the GitHub transition, but the permanent platform direction is self-hosted Gitea. Future first-party development dashboards and GoreeCloud AI integrations must target provider-neutral or Gitea-first boundaries rather than make GitHub a permanent dependency.',
    status:'Transitional GitHub integration · Gitea direction planned'
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

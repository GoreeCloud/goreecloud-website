const currentProjectDirection={
  'GoreeCloud Backup':['Native rebuild target','Backup, restoration, verification, and recovery workflows are moving to an original GoreeCloud application architecture. Transitional implementation may remain for continuity and reference until the native replacement satisfies recovery and production gates.'],
  'GoreeCloud Identity':['Identity platform · active development','First-party GoreeCloud platform system responsible for identity, authentication, authorization, accounts, devices, credentials, sessions, and delegated authority. Existing migration foundations remain bounded implementation details; public readiness claims remain evidence-scoped.','Identity platform system'],
  'GoreeCloud GitHub Dashboard':['Transitional GitHub integration','Repository visibility remains useful during migration, but GoreeCloud Code is the first-party developer and source-control platform. Forgejo is its initial replaceable infrastructure foundation, so future dashboards and AI integrations should become GoreeCloud Code-first or provider-neutral.'],
  'GoreeCloud Network':['Native rebuild active','Private networking and Conduit capabilities are moving into an original GoreeCloud application layer. Mature protocol or networking foundations may remain only within narrowly justified technical boundaries.'],
  'GoreeCloud DNS':['Native rebuild active','GoreeCloud DNS is the first-party DNS filtering and policy project. Recursive resolution remains a separate responsibility and is not claimed by this product surface.'],
  'GoreeCloud Search':['Native rebuild active','GoreeCloud Search is being rebuilt as original GoreeCloud-owned software and remains the first-party search and research gateway. Transitional foundations do not change the required native end state.'],
  'GoreeCloud Browser':['Native rebuild active · Android beta path','GoreeCloud Browser is moving toward an original GoreeCloud-owned product and application layer. Mature browser-engine foundations may remain where technically justified, but inherited product architecture is transitional rather than the approved long-term application model.'],
  'GoreeCloud Memos':['Stable web/server line · native evolution continues','GoreeCloud Memos retains its accepted web/server scope while native replacement and client work remain separately gated.'],
  'GoreeCloud Bookmarks':['Native rebuild active · fail-closed readiness boundary','The original GoreeCloud Bookmarks foundation includes owner-scoped records and fail-closed native readiness semantics. Transitional capture and application surfaces do not establish a native production cutover.'],
  'GoreeCloud Photos':['Native rebuild target · transitional media service','GoreeCloud Photos is required to become an original GoreeCloud application. Transitional implementation may remain for migration, compatibility, testing, and reference while native photo-preservation capabilities replace the upstream product layer.'],
  'GoreeCloud Video':['Native rebuild active','GoreeCloud Video is being rebuilt as original GoreeCloud software. Transitional protocol and compatibility behavior may remain while native video-library, playback, client, and family capabilities replace inherited product layers.'],
  'GoreeCloud Gallery':['Native rebuild target','GoreeCloud Gallery is required to become original GoreeCloud-owned software at the application layer. Existing upstream-derived Android gallery code is transitional while equivalent local-media capabilities are rebuilt and accepted natively.'],
  'GoreeCloud Vault Server':['Native rebuild target · transitional service','The credential server is required to move to an original GoreeCloud application architecture. Transitional compatibility material remains bounded until the native replacement satisfies security, migration, recovery, and client-compatibility gates.'],
  'GoreeCloud Keyboard':['Native rebuild active','GoreeCloud Keyboard is an original GoreeCloud application target powered by first-party Quill capabilities. Platform keyboard APIs, language resources, and mature technical dependencies remain bounded supporting foundations.'],
  'GoreeCloud Terminal':['Release-candidate source · Stable not assumed','GoreeCloud Terminal must reach an original GoreeCloud application end state while retaining only narrowly justified terminal, shell, toolkit, and operating-system foundations. Stable and production acceptance remain separate evidence gates.'],
  'Glaze UI':['2.0.0 current Stable','GoreeCloud Design Center and shared design-system authority for Glaze UI 2.0.0 Stable across supported GoreeCloud surfaces. Glaze UI 2.1 remains Candidate and does not establish Stable consumer conformance.','Design system · Stable 2.0.0']
};

function addCurrentPortfolioEntries(){
  const add=entry=>{if(!entries.some(existing=>existing.name===entry.name))entries.push(entry);};
  add({name:'GoreeCloud AI',repo:'goreecloud-ai',category:'Developer & Intelligence',model:'Native',kind:'Application',status:'Active development',role:'First-party conversational AI and local-model workspace built around GoreeCloud services, knowledge, research, files, tools, RAG, orchestration, and governed integrations.',visibility:'Public'});
  add({name:'GoreeCloud Code',repo:'goreecloud-code',category:'Developer & Intelligence',model:'Native with replaceable forge foundation',kind:'Application',status:'Active development',role:'First-party developer and source-control platform for repositories, collaboration, CI/CD, packages, security, and AI-assisted development. Forgejo is the initial replaceable infrastructure foundation, not the permanent product boundary.',visibility:'Private'});
  add({name:'GoreeCloud Documents',repo:'goreecloud-documents',category:'Productivity & Knowledge',model:'Native',kind:'Application',status:'Active development',role:'First-party document-management platform for capture, OCR, search, organization, automation, collaboration, and preservation.',visibility:'Public'});
  add({name:'GoreeCloud Messenger',repo:'goreecloud-messenger',category:'Communication',model:'Native',kind:'Application',status:'Active development',role:'First-party private messaging and calling application with explicit transport, identity, group, calling, and GoreeCloud integration boundaries.',visibility:'Private'});
  add({name:'GoreeCloud Gateway',repo:'goreecloud-gateway',category:'Platform & Administration',model:'Native',kind:'Application',status:'Active development',role:'Native reverse proxy, HTTPS ingress, routing, certificate-management, and controlled service-publication platform.',visibility:'Public'});
  add({name:'GoreeCloud Quill',repo:'goreecloud-quill',category:'Shared Foundations',model:'First-party capability system',kind:'Capability',status:'Active development',role:'Typing, writing assistance, editing, privacy, personalization, dictionaries, clipboard, and intelligent-input capability family used by GoreeCloud Keyboard and related input experiences.',visibility:'Public'});
  add({name:'GoreeCloud Mesh',repo:'goreecloud-mesh',category:'Shared Foundations',model:'Coordination and governance plane',kind:'Foundation',status:'Active development',role:'Substantive platform coordination and governance plane for explicit service relationships, dependencies, capability exchange, events, and evidence. Mesh preserves the authority boundaries of Identity, Wardveil Security, Privacy Shield, Everkeep, Glaze UI, and specialized applications.',visibility:'Public'});
  add({name:'GoreeCloud File Manager',repo:'goreecloud-file-manager',category:'Productivity & Knowledge',model:'Native',kind:'Application',status:'Active development',role:'First-party GoreeCloud file-management application for local and connected storage surfaces.',visibility:'Public'});
  add({name:'GoreeCloud Maps',repo:'goreecloud-maps',category:'Personal Data & Security',model:'Native',kind:'Application',status:'Active development',role:'GoreeCloud mapping experience with privacy, navigation, GoreeCloud Location, and identity boundaries kept explicit.',visibility:'Private'});
  add({name:'GoreeCloud App Store',repo:'goreecloud-app-store',category:'Platform & Administration',model:'Native',kind:'Application',status:'Active development',role:'Official multi-user catalog and distribution experience for GoreeCloud applications and services, with access determined by account identity and entitlement.',visibility:'Public'});
}
addCurrentPortfolioEntries();

// Identity is both a user-facing service and a substantive platform system. In
// the Projects taxonomy it is represented as a Foundation so the platform
// systems are counted and grouped consistently without duplicating the entry.
const identityEntry=entries.find(entry=>entry.name==='GoreeCloud Identity');
if(identityEntry){identityEntry.kind='Foundation';identityEntry.category='Shared Foundations';}

for(const entry of entries){
  const update=currentProjectDirection[entry.name];
  if(!update)continue;
  entry.status=update[0];
  entry.role=update[1];
  entry.model=update[2]||'Native GoreeCloud end state · transitional upstream provenance retained where applicable';
}

if(typeof appCount!=='undefined'&&appCount)appCount.textContent=entries.filter(entry=>entry.kind==='Application').length;
if(typeof foundationCount!=='undefined'&&foundationCount)foundationCount.textContent=entries.filter(entry=>entry.kind==='Foundation').length;

// Current-direction overrides live in the data model itself, so every later
// search/filter render stays current without observing or rewriting DOM.
render();

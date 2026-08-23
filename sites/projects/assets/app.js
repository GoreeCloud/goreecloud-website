const entries=[
{name:'GoreeCloud Suite',repo:'goreecloud-suite',category:'Platform & Administration',model:'Ecosystem authority',kind:'Foundation',status:'Active',role:'Portfolio-level authority for the integrated GoreeCloud application ecosystem, shared boundaries, interoperability, and Suite-wide conventions.',visibility:'Private'},
{name:'GoreeCloud Manager',repo:'goreecloud-manager',category:'Platform & Administration',model:'Native',kind:'Application',status:'Active development',role:'Central administration, operations, service health, protection status, and management console.',visibility:'Public'},
{name:'GoreeCloud Monitor',repo:'goreecloud-monitor',category:'Platform & Administration',model:'Native',kind:'Application',status:'Active development',role:'Infrastructure and service monitoring, observability, health visibility, and operational monitoring.',visibility:'Public'},
{name:'GoreeCloud Notify',repo:'goreecloud-notify',category:'Platform & Administration',model:'Native',kind:'Application',status:'Release candidate',role:'Notifications, system alerts, operational messages, and application notification delivery.',visibility:'Private'},
{name:'GoreeCloud Backup',repo:'goreecloud-backup',category:'Platform & Administration',model:'Maintained fork',kind:'Application',status:'Active development',role:'Backup repositories, snapshots, restoration, recovery, and protected-data workflows beneath the Everkeep resilience model.',visibility:'Public'},
{name:'GoreeCloud Identity',repo:'goreecloud-identity',category:'Platform & Administration',model:'Maintained fork direction',kind:'Application',status:'Active development',role:'Centralized identity, authentication, single sign-on, identity-provider services, and account integration.',visibility:'Public'},
{name:'GoreeCloud GitHub Dashboard',repo:'goreecloud-github-dashboard',category:'Platform & Administration',model:'Native',kind:'Application',status:'Active development',role:'Private dashboard for repository activity, changelogs, pull requests, issues, releases, and project health.',visibility:'Private'},
{name:'GoreeCloud Network',repo:'goreecloud-network',category:'Internet & Networking',model:'Maintained fork to native',kind:'Application',status:'Active development',role:'Private networking, device enrollment, access policies, secure remote connectivity, and first-party Conduit capabilities.',visibility:'Public'},
{name:'GoreeCloud DNS',repo:'goreecloud-dns',category:'Internet & Networking',model:'Maintained fork to native',kind:'Application',status:'Active development',role:'DNS filtering, recursive resolution, authoritative DNS, encrypted DNS, caching, policy management, and Beacon capabilities.',visibility:'Public'},
{name:'GoreeCloud Search',repo:'goreecloud-search',category:'Internet & Networking',model:'Maintained fork',kind:'Application',status:'Production validated',role:'Private web search and GoreeCloud-controlled search experience.',visibility:'Public'},
{name:'GoreeCloud Browser',repo:'goreecloud-browser',category:'Internet & Networking',model:'Maintained fork',kind:'Application',status:'Active development',role:'Privacy-first Firefox-based browser integrated with GoreeCloud Search, Privacy Shield, Glaze UI, and Wardveil Security.',visibility:'Public'},
{name:'GoreeCloud Drive',repo:'goreecloud-drive',category:'Productivity & Knowledge',model:'Native',kind:'Application',status:'Active development',role:'Private multi-user cloud storage and file management with authorization-first file operations, sharing, version history, collaboration, and long-term portability.',visibility:'Public'},
{name:'GoreeCloud Sync',repo:'goreecloud-sync',category:'Productivity & Knowledge',model:'Native',kind:'Application',status:'Active development',role:'Private multi-user synchronization and secure-transfer platform for nearby and remote file and device workflows.',visibility:'Public'},
{name:'GoreeCloud Notes',repo:'goreecloud-notes',category:'Productivity & Knowledge',model:'Native',kind:'Application',status:'Active development',role:'Full notes, knowledge management, retrieval, attachments, revision recovery, and portable data workflows.',visibility:'Public'},
{name:'GoreeCloud Memos',repo:'goreecloud-memos',category:'Productivity & Knowledge',model:'Maintained fork',kind:'Application',status:'Production / stabilization',role:'Lightweight quick-note capture for focused notes, snippets, lists, reminders, and ideas.',visibility:'Public'},
{name:'GoreeCloud Tasks',repo:'goreecloud-tasks',category:'Productivity & Knowledge',model:'Native',kind:'Application',status:'Active development',role:'Private multi-user task and project management with Waypoint capabilities and Calendar interoperability.',visibility:'Private'},
{name:'GoreeCloud Calendar',repo:'goreecloud-calendar',category:'Productivity & Knowledge',model:'Native',kind:'Application',status:'Active development',role:'First-party calendar, events, scheduling, agenda, CalDAV interoperability, and Tasks integration.',visibility:'Public'},
{name:'GoreeCloud Contacts',repo:'goreecloud-contacts',category:'Productivity & Knowledge',model:'Native',kind:'Application',status:'Active development',role:'Contact management with CardDAV interoperability, controlled writes, and portable address-book data.',visibility:'Private'},
{name:'GoreeCloud Feed',repo:'goreecloud-rss',category:'Productivity & Knowledge',model:'Native',kind:'Application',status:'Web stable; native clients in development',role:'Private feed-reading experience with controlled aggregation and reading workflows.',visibility:'Public'},
{name:'GoreeCloud Bookmarks',repo:'goreecloud-bookmarks',category:'Productivity & Knowledge',model:'Maintained fork',kind:'Application',status:'Active development',role:'Bookmark preservation, authenticated browser capture, organization, retrieval, and web-knowledge management.',visibility:'Public'},
{name:'GoreeCloud Changelogs',repo:'goreecloud-changelogs',category:'Productivity & Knowledge',model:'Native',kind:'Application',status:'Active development',role:'Historical GoreeCloud change-ledger web application and API.',visibility:'Private'},
{name:'GoreeCloud Mail',repo:'goreecloud-mail',category:'Communication & Media',model:'Native',kind:'Application',status:'Active development',role:'First-party email client for web, Linux, Android, and future iOS with Courier capabilities and provider-independent account architecture.',visibility:'Private'},
{name:'GoreeCloud Music',repo:'goreecloud-music',category:'Communication & Media',model:'Native',kind:'Application',status:'Active development',role:'Self-hosted multi-user music service with library scanning, metadata, artwork, playback, and Resonance capabilities.',visibility:'Public'},
{name:'GoreeCloud Photos',repo:'goreecloud-photos',category:'Communication & Media',model:'Maintained fork to native',kind:'Application',status:'Active development',role:'Long-term photo and video preservation, organization, search, sharing, and Keepsake capabilities.',visibility:'Public'},
{name:'GoreeCloud Video',repo:'goreecloud-video',category:'Communication & Media',model:'Maintained fork to native',kind:'Application',status:'Milestone 1 development',role:'Private video library and playback platform with a deliberately video-only media scope, first-party client direction, metadata, family access, and controlled Jellyfin-derived compatibility.',visibility:'Public'},
{name:'GoreeCloud Gallery',repo:'goreecloud-gallery',category:'Communication & Media',model:'Maintained fork',kind:'Application',status:'Active development',role:'Offline-focused Android gallery for local photo and image browsing, organization, and viewing.',visibility:'Public'},
{name:'GoreeCloud Location',repo:'goreecloud-location',category:'Personal Data & Security',model:'Native',kind:'Application',status:'Active development',role:'Private multi-user location platform for device tracking, location history, places, trips, geofencing, maps, sharing, and native Android collection.',visibility:'Public'},
{name:'GoreeCloud Vault Server',repo:'goreecloud-vault-server',category:'Personal Data & Security',model:'Maintained fork to native',kind:'Application',status:'Active development',role:'Self-hosted password, credential, secret, secure-record, and sensitive-information server.',visibility:'Public'},
{name:'GoreeCloud Keyboard',repo:'goreecloud-keyboard',category:'Device Software',model:'Maintained fork',kind:'Application',status:'Active development',role:'System keyboard powered by Quill capabilities for typing, editing, personalization, dictionaries, clipboard, and input workflows.',visibility:'Public'},
{name:'GoreeCloud Terminal',repo:'goreecloud-terminal',category:'Device Software',model:'Maintained fork',kind:'Application',status:'Release candidate',role:'Native Linux terminal for local shells, SSH administration, and GoreeCloud workstation workflows.',visibility:'Public'},
{name:'GoreeCloud Launcher',repo:'goreecloud-launcher',category:'Device Software',model:'Native',kind:'Application',status:'Active development',role:'First-party Android HOME experience with application discovery, search, persistent favorites and dock state, accessible ordering, workspace placement, and launcher lifecycle integration.',visibility:'Public'},
{name:'GoreeCloud Firefox Extensions',repo:'goreecloud-firefox-extensions',category:'Device Software',model:'First-party extension collection',kind:'Application',status:'Active development',role:'Canonical home for GoreeCloud-maintained Firefox extensions and browser integration components.',visibility:'Private'},
{name:'GoreeCloud Website',repo:'goreecloud-website',category:'Public Experience',model:'Native',kind:'Application',status:'Production',role:'Main public GoreeCloud identity plus Projects, Roadmap, Blog, and Archive public websites.',visibility:'Private'},
{name:'GoreeCloud Autobiography',repo:'goreecloud-autobiography',category:'Public Experience',model:'Native',kind:'Application',status:'Early development',role:'Public long-form project for preserving and presenting the story, history, lessons, and evolution behind GoreeCloud.',visibility:'Public'},
{name:'Glaze UI',repo:'glaze-ui',category:'Shared Foundations',model:'Design language',kind:'Foundation',status:'1.4 Stable · 1.3 supported older stable',role:'Official visual and interaction system for mobile, tablet, desktop, TV, accessibility, semantic components, and product consistency.',visibility:'Public',icon:'/assets/glaze-ui-mark.svg',url:'https://design.goreecloud.com/'},
{name:'GoreeCloud Privacy Shield',repo:'goreecloud-privacy-shield',category:'Shared Foundations',model:'Privacy identity',kind:'Foundation',status:'Platform-wide active development',role:'Platform-wide privacy identity and shared privacy-control foundation with first-party adapters and privacy-state contracts.',visibility:'Private',icon:'/assets/privacy-shield-icon.svg',url:'https://privacy.goreecloud.com/'},
{name:'Wardveil Security',repo:'goreecloud-wardveil-security',category:'Shared Foundations',model:'Security identity',kind:'Foundation',status:'0.7 foundation',role:'Platform-wide security and protection identity for evidence-scoped security states, warnings, posture, and protection experiences.',visibility:'Private',icon:'/assets/wardveil-security-icon.svg',url:'https://security.goreecloud.com/'},
{name:'Everkeep',repo:'goreecloud-everkeep',category:'Shared Foundations',model:'Resilience identity',kind:'Foundation',status:'Active',role:'Platform-wide resilience, backup and recovery, preservation, portability, succession, and digital-legacy identity.',visibility:'Private'},
{name:'GoreeCloud Waypoint',repo:'goreecloud-waypoint',category:'Shared Foundations',model:'Capability identity',kind:'Foundation',status:'Active identity',role:'First-party task and work-management capability family used by GoreeCloud Tasks and related Suite integrations.',visibility:'Public'}
];

const grid=document.querySelector('#projects');
const search=document.querySelector('#search');
const filters=document.querySelector('#filters');
const resultCount=document.querySelector('#result-count');
const appCount=document.querySelector('#app-count');
const foundationCount=document.querySelector('#foundation-count');
const themeButtons=[...document.querySelectorAll('[data-theme-choice]')];
let filter='All';

appCount.textContent=entries.filter(entry=>entry.kind==='Application').length;
foundationCount.textContent=entries.filter(entry=>entry.kind==='Foundation').length;

const filtersList=['All','Applications','Foundations','Platform & Administration','Internet & Networking','Productivity & Knowledge','Communication & Media','Personal Data & Security','Device Software','Public Experience'];
for(const name of filtersList){
  const button=document.createElement('button');
  button.className='filter';
  button.type='button';
  button.textContent=name;
  button.dataset.filter=name;
  button.setAttribute('aria-pressed',String(name==='All'));
  button.addEventListener('click',()=>{
    filter=name;
    document.querySelectorAll('.filter').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));
    render();
  });
  filters.append(button);
}

function matchesFilter(entry){
  if(filter==='All')return true;
  if(filter==='Applications')return entry.kind==='Application';
  if(filter==='Foundations')return entry.kind==='Foundation';
  return entry.category===filter;
}

function render(){
  const query=search.value.trim().toLowerCase();
  const list=entries.filter(entry=>matchesFilter(entry)&&(!query||`${entry.name} ${entry.repo} ${entry.category} ${entry.model} ${entry.kind} ${entry.status} ${entry.role}`.toLowerCase().includes(query)));
  grid.replaceChildren(...list.map(card));
  resultCount.textContent=`${list.length} ${list.length===1?'entry':'entries'} shown`;
}

function card(entry){
  const article=document.createElement('article');
  article.className='card';
  article.dataset.kind=entry.kind.toLowerCase();

  const head=document.createElement('div');head.className='card-head';
  const iconWrap=document.createElement('div');iconWrap.className='project-icon';
  const icon=document.createElement('img');icon.src=entry.icon||'/assets/goreecloud-logo.svg';icon.alt='';icon.width=48;icon.height=48;iconWrap.append(icon);
  const kind=document.createElement('span');kind.className='kind';kind.textContent=entry.kind;
  head.append(iconWrap,kind);

  const meta=document.createElement('div');meta.className='card-meta';
  const category=document.createElement('span');category.className='badge';category.textContent=entry.category;
  const status=document.createElement('span');status.className='status';status.textContent=entry.status;
  meta.append(category,status);

  const title=document.createElement('h3');title.textContent=entry.name;
  const role=document.createElement('p');role.className='role';role.textContent=entry.role;
  const model=document.createElement('p');model.className='model';model.textContent=entry.model;

  const footer=document.createElement('footer');
  const visibility=document.createElement('span');visibility.className='visibility';visibility.textContent=`${entry.visibility} source`;
  footer.append(visibility);
  const destination=entry.url||(entry.visibility==='Public'?`https://github.com/GoreeCloud/${entry.repo}`:null);
  if(destination){
    const link=document.createElement('a');link.href=destination;link.target='_blank';link.rel='noopener noreferrer';link.textContent=entry.kind==='Foundation'?'View foundation':'Open repository';footer.append(link);
  }

  article.append(head,meta,title,role,model,footer);
  return article;
}

function applyTheme(choice){
  document.documentElement.dataset.theme=choice;
  themeButtons.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.themeChoice===choice)));
}
let saved='system';
try{saved=localStorage.getItem('goreecloud-projects-theme')||'system';}catch(_){ }
if(!['system','light','dark'].includes(saved))saved='system';
applyTheme(saved);
themeButtons.forEach(button=>button.addEventListener('click',()=>{const choice=button.dataset.themeChoice;applyTheme(choice);try{localStorage.setItem('goreecloud-projects-theme',choice);}catch(_){}}));

search.addEventListener('input',render);
render();

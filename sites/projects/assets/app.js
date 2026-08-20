const artworkBase='https://raw.githubusercontent.com/GoreeCloud/glaze-ui/main/branding';
const fallbackIcon='/assets/goreecloud-logo.svg';

const entries=[
{name:'GoreeCloud Manager',repo:'goreecloud-manager',category:'Platform & Administration',model:'Native',kind:'Application',status:'In development',role:'Central administration, operations, service health, protection status, and management console.',visibility:'Public'},
{name:'GoreeCloud Monitor',repo:'goreecloud-monitor',category:'Platform & Administration',model:'Native',kind:'Application',status:'Active development',role:'Infrastructure and service monitoring, observability, health visibility, and operational monitoring.',visibility:'Public'},
{name:'GoreeCloud Notify',repo:'goreecloud-notify',category:'Platform & Administration',model:'Native',kind:'Application',status:'Release candidate',role:'Notifications, system alerts, operational messages, and application notification delivery.',visibility:'Private'},
{name:'GoreeCloud Backup',repo:'goreecloud-backup',category:'Platform & Administration',model:'Maintained fork',kind:'Application',status:'Active development',role:'Backup repositories, snapshots, restoration, recovery, and protected-data workflows.',visibility:'Public'},
{name:'GoreeCloud Identity',repo:'goreecloud-identity',category:'Platform & Administration',model:'Maintained fork direction',kind:'Application',status:'Evaluation & development',role:'Centralized identity, authentication, single sign-on, identity-provider services, and account integration.',visibility:'Public'},
{name:'GoreeCloud Network',repo:'goreecloud-network',category:'Internet & Networking',model:'Maintained fork',kind:'Application',status:'Active development',role:'Private networking, VPN connectivity, device enrollment, access policies, and secure remote connectivity.',visibility:'Public'},
{name:'GoreeCloud DNS',repo:'goreecloud-dns',category:'Internet & Networking',model:'Maintained fork',kind:'Application',status:'Active development',role:'DNS filtering, privacy protection, blocking, resolver administration, and GoreeCloud DNS policy management.',visibility:'Public'},
{name:'GoreeCloud Search',repo:'goreecloud-search',category:'Internet & Networking',model:'Maintained fork',kind:'Application',status:'Production validated',role:'Private web search and GoreeCloud-controlled search experience.',visibility:'Public'},
{name:'GoreeCloud Browser',repo:'goreecloud-browser',category:'Internet & Networking',model:'Maintained fork',kind:'Application',status:'Active development',role:'Privacy-first web browsing integrated with GoreeCloud services and security/privacy controls.',visibility:'Public'},
{name:'GoreeCloud Notes',repo:'goreecloud-notes',category:'Productivity & Knowledge',model:'Native',kind:'Application',status:'Active development',role:'Full notes, knowledge management, retrieval, attachments, revision recovery, and portable data workflows.',visibility:'Public'},
{name:'GoreeCloud Memos',repo:'goreecloud-memos',category:'Productivity & Knowledge',model:'Maintained fork',kind:'Application',status:'Active stabilization',role:'Lightweight quick-note capture for focused notes, snippets, lists, reminders, and ideas.',visibility:'Public'},
{name:'GoreeCloud Tasks',repo:'goreecloud-tasks',category:'Productivity & Knowledge',model:'Native',kind:'Application',status:'Active development',role:'Private multi-user task and project management for personal, family, collaborative, and operational work.',visibility:'Private'},
{name:'GoreeCloud Calendar',repo:'goreecloud-calendar',category:'Productivity & Knowledge',model:'Native',kind:'Application',status:'Active development',role:'Standards-based GoreeCloud calendar experience with CalDAV interoperability.',visibility:'Public'},
{name:'GoreeCloud Contacts',repo:'goreecloud-contacts',category:'Productivity & Knowledge',model:'Native',kind:'Application',status:'Active development',role:'Contact management with CardDAV interoperability, controlled writes, and portable address-book data.',visibility:'Private'},
{name:'GoreeCloud Feed',repo:'goreecloud-rss',category:'Productivity & Knowledge',model:'Native',kind:'Application',status:'Active development',role:'GoreeCloud feed-reading experience with private, controlled aggregation and reading workflows.',visibility:'Public'},
{name:'GoreeCloud Bookmarks',repo:'goreecloud-bookmarks',category:'Productivity & Knowledge',model:'Maintained fork',kind:'Application',status:'Active development',role:'Bookmark preservation, organization, retrieval, and web-knowledge management.',visibility:'Public'},
{name:'GoreeCloud Research Library',repo:'goreecloud-research-library',category:'Productivity & Knowledge',model:'Maintained fork',kind:'Application',status:'Staging candidate',role:'Research-source preservation, organization, retrieval, and long-term knowledge-library workflows.',visibility:'Public'},
{name:'GoreeCloud Changelogs',repo:'goreecloud-changelogs',category:'Productivity & Knowledge',model:'Native',kind:'Application',status:'Active development',role:'Historical GoreeCloud change-ledger web application and API.',visibility:'Private'},
{name:'GoreeCloud Gallery',repo:'goreecloud-gallery',category:'Personal Data & Security',model:'Maintained fork',kind:'Application',status:'Active development',role:'Photo and image browsing, organization, viewing, and private local-media experiences.',visibility:'Public'},
{name:'GoreeVault',repo:'goreevault-server',category:'Personal Data & Security',model:'Maintained fork',kind:'Application',status:'Active development',role:'Passwords, credentials, secrets, secure records, and sensitive-information management.',visibility:'Public'},
{name:'GoreeCloud Keyboard',repo:'goreecloud-keyboard',category:'Device Software',model:'Maintained fork',kind:'Application',status:'Active development',role:'System keyboard with swipe typing, clipboard tools, GoreeCloud terminology, autocomplete, and learned suggestions.',visibility:'Public'},
{name:'GoreeCloud Website',repo:'goreecloud-website',category:'Public Experience',model:'Native',kind:'Application',status:'Active deployment',role:'Public GoreeCloud identity, platform information, project communication, and public presentation.',visibility:'Private'},
{name:'Glaze UI',repo:'glaze-ui',category:'Shared Foundations',model:'Design language',kind:'Foundation',status:'1.3.0 Stable',role:'Official GoreeCloud visual and interaction system for shared semantics, components, accessibility, and product consistency.',visibility:'Public',icon:`${artworkBase}/icons/glaze-ui/glaze-ui-symbol.svg`,url:'https://design.goreecloud.com/'},
{name:'GoreeCloud Privacy Shield',repo:'goreecloud-privacy-shield',category:'Shared Foundations',model:'Privacy identity',kind:'Foundation',status:'Platform foundation',role:'Privacy identity and privacy-protection component, currently centered on GoreeCloud Browser and applicable privacy surfaces.',visibility:'Private',icon:`${artworkBase}/identities/privacy-shield/symbol.svg`,url:'https://privacy.goreecloud.com/'},
{name:'Wardveil Security',repo:'goreecloud-wardveil-security',category:'Shared Foundations',model:'Security identity',kind:'Foundation',status:'Platform foundation',role:'Official GoreeCloud platform-wide security and protection identity for security-related interfaces and controls.',visibility:'Private',icon:`${artworkBase}/identities/wardveil-security/emblem.svg`,url:'https://security.goreecloud.com/'}
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

const filtersList=['All','Applications','Foundations','Platform & Administration','Internet & Networking','Productivity & Knowledge','Personal Data & Security','Device Software','Public Experience'];
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

function artworkFor(entry){
  if(entry.icon)return entry.icon;
  return `${artworkBase}/applications/${entry.repo}/symbol.svg`;
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

  const head=document.createElement('div');
  head.className='card-head';
  const iconWrap=document.createElement('div');
  iconWrap.className='project-icon';
  const icon=document.createElement('img');
  icon.src=artworkFor(entry);
  icon.alt='';
  icon.width=48;
  icon.height=48;
  icon.loading='lazy';
  icon.decoding='async';
  icon.addEventListener('error',()=>{icon.src=fallbackIcon;},{once:true});
  iconWrap.append(icon);
  const kind=document.createElement('span');
  kind.className='kind';
  kind.textContent=entry.kind;
  head.append(iconWrap,kind);

  const meta=document.createElement('div');
  meta.className='card-meta';
  const category=document.createElement('span');
  category.className='badge';
  category.textContent=entry.category;
  const status=document.createElement('span');
  status.className='status';
  status.textContent=entry.status;
  meta.append(category,status);

  const title=document.createElement('h3');
  title.textContent=entry.name;
  const role=document.createElement('p');
  role.className='role';
  role.textContent=entry.role;
  const model=document.createElement('p');
  model.className='model';
  model.textContent=entry.model;

  const footer=document.createElement('footer');
  const visibility=document.createElement('span');
  visibility.className='visibility';
  visibility.textContent=`${entry.visibility} source`;
  footer.append(visibility);
  const destination=entry.url||(entry.visibility==='Public'?`https://github.com/GoreeCloud/${entry.repo}`:null);
  if(destination){
    const link=document.createElement('a');
    link.href=destination;
    link.target='_blank';
    link.rel='noopener noreferrer';
    link.textContent=entry.kind==='Foundation'?'View foundation':'Open repository';
    footer.append(link);
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
themeButtons.forEach(button=>button.addEventListener('click',()=>{
  const choice=button.dataset.themeChoice;
  applyTheme(choice);
  try{localStorage.setItem('goreecloud-projects-theme',choice);}catch(_){ }
}));

search.addEventListener('input',render);
render();

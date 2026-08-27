const canonicalSuiteIconBase='https://www.goreecloud.com/assets/suite/';
const canonicalRepositoryIcons={
  'goreecloud-manager':'manager.svg',
  'goreecloud-monitor':'monitor.svg',
  'goreecloud-notify':'notify.svg',
  'goreecloud-backup':'backup.svg',
  'goreecloud-identity':'identity.svg',
  'goreecloud-network':'network.svg',
  'goreecloud-dns':'dns.svg',
  'goreecloud-search':'search.svg',
  'goreecloud-browser':'browser.svg',
  'goreecloud-drive':'drive.svg',
  'goreecloud-sync':'sync.svg',
  'goreecloud-notes':'notes.svg',
  'goreecloud-memos':'memos.svg',
  'goreecloud-tasks':'tasks.svg',
  'goreecloud-calendar':'calendar.svg',
  'goreecloud-contacts':'contacts.svg',
  'goreecloud-rss':'feed.svg',
  'goreecloud-bookmarks':'bookmarks.svg',
  'goreecloud-changelogs':'changelogs.svg',
  'goreecloud-mail':'mail.svg',
  'goreecloud-music':'music.svg',
  'goreecloud-photos':'photos.svg',
  'goreecloud-video':'video.svg',
  'goreecloud-gallery':'gallery.svg',
  'goreecloud-location':'location.svg',
  'goreecloud-vault-server':'vault.svg',
  'goreecloud-keyboard':'keyboard.svg',
  'goreecloud-terminal':'terminal.svg',
  'goreecloud-launcher':'launcher.svg',
  'goreecloud-ai':'ai.svg',
  'goreecloud-code':'code.svg',
  'goreecloud-documents':'documents.svg',
  'goreecloud-messenger':'messenger.svg',
  'goreecloud-gateway':'gateway.svg'
};

function projectInitials(name){
  return name.replace(/^GoreeCloud\s+/,'').split(/\s+/).filter(Boolean).slice(0,2).map(word=>word[0]).join('').toUpperCase()||'GC';
}

function projectMonogram(name){
  const label=projectInitials(name);
  const svg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="8" y1="8" x2="56" y2="56" gradientUnits="userSpaceOnUse"><stop stop-color="#38BDF8"/><stop offset="1" stop-color="#6366F1"/></linearGradient></defs><rect x="5" y="5" width="54" height="54" rx="17" fill="url(#g)"/><text x="32" y="38" text-anchor="middle" font-family="system-ui,sans-serif" font-size="18" font-weight="800" fill="#fff">${label}</text></svg>`;
  return `data:image/svg+xml,${encodeURIComponent(svg)}`;
}

function meshSymbol(){
  const svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="m" x1="10" y1="9" x2="54" y2="55" gradientUnits="userSpaceOnUse"><stop stop-color="#2DD4BF"/><stop offset=".5" stop-color="#38BDF8"/><stop offset="1" stop-color="#7C3AED"/></linearGradient></defs><path d="M18 19 32 11l14 8v16L32 53 18 45Z" fill="none" stroke="url(#m)" stroke-width="4" stroke-linejoin="round"/><path d="m18 19 14 13 14-13M18 45l14-13 14 3M32 11v21M32 53V32" fill="none" stroke="url(#m)" stroke-width="3" stroke-linecap="round"/><circle cx="18" cy="19" r="4" fill="#2DD4BF"/><circle cx="32" cy="11" r="4" fill="#38BDF8"/><circle cx="46" cy="19" r="4" fill="#60A5FA"/><circle cx="18" cy="45" r="4" fill="#38BDF8"/><circle cx="32" cy="53" r="4" fill="#6366F1"/><circle cx="46" cy="35" r="4" fill="#7C3AED"/><circle cx="32" cy="32" r="5" fill="#F8FAFC" stroke="#326DF5" stroke-width="3"/></svg>';
  return `data:image/svg+xml,${encodeURIComponent(svg)}`;
}

for(const entry of entries){
  if(entry.repo==='goreecloud-everkeep'){
    entry.icon='/assets/everkeep.svg';
    continue;
  }
  if(entry.repo==='goreecloud-mesh'){
    entry.icon=meshSymbol();
    continue;
  }
  const canonical=canonicalRepositoryIcons[entry.repo];
  if(canonical){
    entry.icon=`${canonicalSuiteIconBase}${canonical}`;
    continue;
  }
  if(entry.icon)continue;
  if(entry.repo==='goreecloud-suite'||entry.repo==='goreecloud-website'){
    entry.icon='/assets/goreecloud-logo.svg';
    continue;
  }
  entry.icon=projectMonogram(entry.name);
}

render();

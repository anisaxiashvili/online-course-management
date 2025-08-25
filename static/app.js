const API_BASE = '/api/v1';
const PATHS = {
  login: '/static/frontend/login.html',
  signup: '/static/frontend/signup.html',
  courses: '/static/frontend/courses.html',
  courseDetail: '/static/frontend/course_detail.html',
  lectureDetail: '/static/frontend/lecture_detail.html',
  assignmentDetail: '/static/frontend/assignment_detail.html',
};

function saveTokens({access, refresh}){
  if(access) localStorage.setItem('access', access);
  if(refresh) localStorage.setItem('refresh', refresh);
}
function clearTokens(){
  localStorage.removeItem('access'); localStorage.removeItem('refresh');
}
function getAccess(){ return localStorage.getItem('access'); }
function getRefresh(){ return localStorage.getItem('refresh'); }

async function apiFetch(path, options={}){
  const headers = options.headers ? {...options.headers} : {};
  if(!(options.body instanceof FormData)){
    headers['Content-Type'] = headers['Content-Type'] || 'application/json';
  }
  const token = getAccess();
  if(token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}${path}`, {...options, headers});
  if(res.status === 401 && getRefresh()){
    const refreshed = await tryRefresh();
    if(refreshed) return apiFetch(path, options);
  }
  if(!res.ok){
    let details = await res.text();
    throw new Error(details || res.statusText);
  }
  const ct = res.headers.get('content-type') || '';
  return ct.includes('application/json') ? res.json() : res.text();
}

async function tryRefresh(){
  try{
    const res = await fetch(`${API_BASE}/accounts/token/refresh/`, {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({refresh: getRefresh()})
    });
    const data = await res.json();
    if(data.access){ saveTokens({access: data.access}); return true; }
  }catch(e){}
  logout();
  return false;
}

function logout(){
  clearTokens(); window.location.href = PATHS.login;
}

async function getMe(){
  return apiFetch('/accounts/me/');
}

function qs(name, url){
  url = url || window.location.href;
  name = name.replace(/[[\]]/g, '\\$&');
  const regex = new RegExp('[?&]'+name+'(=([^&#]*)|&|#|$)');
  const results = regex.exec(url);
  if(!results) return null;
  if(!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

function ensureAuthed(){
  if(!getAccess()){ window.location.href = PATHS.login; }
}

function setNav(user){
  const name = [user.first_name, user.last_name].filter(Boolean).join(' ') || '@'+user.username;
  document.getElementById('userChip').textContent = `${name} — ${user.role}`;
  document.getElementById('logoutBtn').onclick = logout;
}

function isTeacher(user){ return user.role === 'teacher'; }

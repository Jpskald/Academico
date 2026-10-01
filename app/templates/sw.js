// Service Worker - Sistema Acadêmico (com Offline Sync)
importScripts('https://cdn.jsdelivr.net/npm/localforage@1.10.0/dist/localforage.min.js');

const CACHE_NAME = 'academico-v2';
const urlsToCache = [
    '/',
    '/pessoas/',
    '/cursos/',
    '/disciplinas/',
    '/static/icons/academico-icon-192x192.png',
    'https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css',
];

// ===== INSTALAÇÃO =====
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
    );
    self.skipWaiting();
});

// ===== ATIVAÇÃO =====
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
        )
    );
    self.clients.claim();
});

// ===== FETCH (Estratégia inteligente por tipo de recurso) =====
self.addEventListener('fetch', event => {
    // Não intercepta chamadas de API POST
    if (event.request.method === 'POST') return;

    const url = new URL(event.request.url);
    const isStaticAsset = url.pathname.startsWith('/static/') ||
                          url.hostname.includes('bootstrapcdn') ||
                          url.hostname.includes('jsdelivr') ||
                          url.hostname.includes('jquery');

    if (isStaticAsset) {
        // CACHE FIRST: estáticos raramente mudam — serve do cache, rápido
        event.respondWith(
            caches.match(event.request).then(cached =>
                cached || fetch(event.request).then(response => {
                    caches.open(CACHE_NAME).then(c => c.put(event.request, response.clone()));
                    return response;
                })
            )
        );
    } else {
        // NETWORK FIRST: páginas Django são dinâmicas — sempre tenta a rede primeiro
        // e só usa cache se estiver offline
        event.respondWith(
            fetch(event.request)
                .then(response => {
                    // Atualiza o cache com a versão mais recente
                    caches.open(CACHE_NAME).then(c => c.put(event.request, response.clone()));
                    return response;
                })
                .catch(() => {
                    // Offline: serve do cache
                    return caches.match(event.request) || caches.match('/');
                })
        );
    }
});

// ===== BACKGROUND SYNC - PESSOAS =====
self.addEventListener('sync', event => {
    if (event.tag === 'sync-pessoas') {
        event.waitUntil(syncPessoas());
    }
    if (event.tag === 'sync-cursos') {
        event.waitUntil(syncCursos());
    }
    if (event.tag === 'sync-disciplinas') {
        event.waitUntil(syncDisciplinas());
    }
});

async function syncPessoas() {
    const fila = await localforage.getItem('fila-pessoas') || [];
    if (fila.length === 0) return;

    const enviados = [];
    for (const dados of fila) {
        try {
            const resp = await fetch('/api/pessoa/criar/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dados)
            });
            if (resp.ok) enviados.push(dados);
        } catch (e) {
            console.error('Falha ao sincronizar pessoa:', e);
        }
    }

    // Remove da fila apenas os que foram enviados com sucesso
    const restantes = fila.filter(d => !enviados.includes(d));
    await localforage.setItem('fila-pessoas', restantes);
}

async function syncCursos() {
    const fila = await localforage.getItem('fila-cursos') || [];
    if (fila.length === 0) return;

    const enviados = [];
    for (const dados of fila) {
        try {
            const resp = await fetch('/api/curso/criar/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dados)
            });
            if (resp.ok) enviados.push(dados);
        } catch (e) {
            console.error('Falha ao sincronizar curso:', e);
        }
    }
    const restantes = fila.filter(d => !enviados.includes(d));
    await localforage.setItem('fila-cursos', restantes);
}

async function syncDisciplinas() {
    const fila = await localforage.getItem('fila-disciplinas') || [];
    if (fila.length === 0) return;

    const enviados = [];
    for (const dados of fila) {
        try {
            const resp = await fetch('/api/disciplina/criar/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dados)
            });
            if (resp.ok) enviados.push(dados);
        } catch (e) {
            console.error('Falha ao sincronizar disciplina:', e);
        }
    }
    const restantes = fila.filter(d => !enviados.includes(d));
    await localforage.setItem('fila-disciplinas', restantes);
}

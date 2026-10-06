# 🎓 Sistema Acadêmico PWA (Offline-First com IndexedDB)

Aplicação web completa para gestão acadêmica desenvolvida com **Django** e arquitetada sob o modelo **PWA (Progressive Web App)** com suporte **Offline-First**.

O sistema foi projetado para continuar operando mesmo em situações de instabilidade ou ausência total de conexão à internet, armazenando dados localmente no navegador via **IndexedDB** e sincronizando-os automaticamente com o servidor assim que a conectividade for restabelecida.

---

## 🚀 Destaques da Arquitetura Offline-First

### 1. Progressive Web App (PWA)
- **Instalável:** Configurado com [`manifest.json`] e ícones dedicados em várias resoluções, permitindo a instalação no celular ou desktop como um aplicativo nativo (`standalone`).
- **Tema e UI Adaptada:** Alerta em tempo real no topo da aplicação indicando se o usuário está online ou offline via eventos `window.addEventListener('online' | 'offline')`.

### 2. Estratégias Inteligentes de Cache com Service Worker (`sw.js`)
O [`sw.js`] implementa duas estratégias distintas para otimizar desempenho e confiabilidade:
- **Cache First (Ativos Estáticos):** Estilos (Bootstrap), scripts de terceiros e ícones são servidos instantaneamente a partir do cache local.
- **Network First com Fallback para Cache (Páginas Django):** O sistema prioriza a rede para buscar sempre a versão mais atualizada dos dados; caso a rede falhe ou esteja offline, o Service Worker serve a versão armazenada no cache local.

### 3. Fila Local com IndexedDB (`localforage`)
Quando um usuário tenta cadastrar uma **Pessoa**, **Curso** ou **Disciplina** sem conexão:
1. O formulário detecta `!navigator.onLine` e intercepta o evento de `submit`.
2. Os dados são serializados e enfileirados em coleções dedicadas no **IndexedDB** via biblioteca [localforage](https://localforage.github.io/localForage/) (`fila-pessoas`, `fila-cursos`, `fila-disciplinas`).
3. O usuário recebe feedback imediato de que os dados foram preservados com segurança no dispositivo.

### 4. Sincronização em Segundo Plano (Background Sync API)
- O navegador registra uma tarefa de sincronização (`sync-pessoas`, `sync-cursos`, etc.).
- Ao restabelecer a conexão com a internet, o Service Worker desperta em segundo plano, lê a fila do IndexedDB e envia os registros pendentes para as rotas dedicadas da API Django (`/api/pessoa/criar/`, `/api/curso/criar/`, etc.).
- Itens transmitidos com sucesso são limpos da fila local, garantindo integridade e idempotência.

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** [Python 3](https://www.python.org/) & [Django](https://www.djangoproject.com/)
- **Frontend:** HTML5, CSS3, JavaScript (ES6+), Bootstrap
- **Armazenamento Offline:** [IndexedDB](https://developer.mozilla.org/pt-BR/docs/Web/API/IndexedDB_API) (gerenciado com `localforage`)
- **PWA & Sincronização:** [Service Workers API](https://developer.mozilla.org/pt-BR/docs/Web/API/Service_Worker_API), [Web App Manifest](https://developer.mozilla.org/pt-BR/docs/Web/Manifest), [Background Sync API](https://developer.mozilla.org/en-US/docs/Web/API/Background_Synchronization_API)
- **Banco de Dados Relacional:** SQLite (armazenamento central no servidor)

---

## 📁 Estrutura do Projeto

```text
Academico/
│
├── config/                      # Configurações do projeto Django
│   ├── settings.py              # Definições do Django e apps instalados
│   ├── urls.py                  # Rotas principais, views e endpoints de API
│   └── wsgi.py
│
├── app/                         # Aplicação principal
│   ├── models.py                # Modelos: Pessoa, Curso, Disciplina, Instituicao, etc.
│   ├── forms.py                 # Formulários Django
│   ├── views.py                 # Views normais (CBVs) + Endpoints JSON de Sincronização
│   ├── static/
│   │   ├── manifest.json        # Configuração do PWA
│   │   └── icons/               # Ícones de instalação do aplicativo
│   └── templates/
│       ├── sw.js                # Service Worker com cache e Background Sync
│       ├── index.html           # Página inicial / Menu principal
│       ├── pessoas.html         # Listagem e cadastro de pessoas (offline habilitado)
│       ├── pessoa_detalhe.html  # Detalhes completos da pessoa
│       ├── cursos.html          # Listagem e cadastro de cursos (offline habilitado)
│       └── disciplinas.html     # Listagem e cadastro de disciplinas (offline habilitado)
│
├── db.sqlite3                   # Banco de dados SQLite local
├── manage.py                    # Gerenciador CLI do Django
└── README.md
```

---

## 🚀 Como Executar o Projeto

### 1. Clonar ou Acessar a Pasta
```bash
cd Academico
```

### 2. Ativar o Ambiente Virtual
```bash
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# Linux / MacOS:
source .venv/bin/activate
```

### 3. Executar as Migrações
```bash
python manage.py migrate
```

### 4. Iniciar o Servidor Django
```bash
python manage.py runserver
```

Abra seu navegador em [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## 🧪 Como Testar a Experiência Offline

1. Acesse o sistema pelo Google Chrome, Edge ou navegador compatível.
2. Abra as Ferramentas do Desenvolvedor (**F12** ou `Ctrl + Shift + I`).
3. Navegue até a aba **Network** (Rede) e altere a velocidade de *No throttling* para **Offline**.
   - *Alternativa:* desligue a rede Wi-Fi / cabo de rede da máquina.
4. Observe que o banner amarelo de alerta **"Você está offline"** aparecerá na tela.
5. Acesse uma das telas (ex: **Pessoas**) e preencha um novo cadastro:
   - Clique em **Salvar**.
   - Uma mensagem confirmará que os dados foram gravados localmente no **IndexedDB**.
6. Para auditar a fila salva no navegador:
   - Vá na aba **Application** do DevTools -> **Storage** -> **IndexedDB** -> `localforage` -> verifique o item `fila-pessoas`.
7. Volte na aba **Network** e altere o status de volta para **Online**:
   - A API de sincronização enviará automaticamente os dados para o Django via `POST /api/pessoa/criar/`.
   - Ao atualizar a página, o novo registro estará gravado de forma persistente no banco de dados SQLite!

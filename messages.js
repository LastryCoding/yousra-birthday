const list = document.querySelector('#messages-list');
const count = document.querySelector('#message-count');

async function loadMessages() {
  try {
    const response = await fetch('/api/messages');
    if (!response.ok) throw new Error('Chargement impossible');
    const { messages } = await response.json();
    list.replaceChildren();
    count.textContent = String(messages.length);
    const format = new Intl.DateTimeFormat('fr-FR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });
    for (const entry of messages) {
      const article = document.createElement('article');
      article.className = 'guest-message';
      const top = document.createElement('div');
      top.className = 'note-top';
      const name = document.createElement('span');
      name.className = 'note-name';
      name.textContent = entry.name;
      const date = document.createElement('time');
      date.className = 'note-date';
      date.dateTime = entry.created_at;
      date.textContent = format.format(new Date(entry.created_at));
      const body = document.createElement('p');
      body.className = 'note-body';
      body.textContent = entry.message;
      top.append(name, date);
      article.append(top, body);
      list.append(article);
    }
    if (!messages.length) list.textContent = 'Aucun message pour le moment.';
  } catch {
    list.textContent = 'Les messages sont momentanément indisponibles.';
  }
}

loadMessages();

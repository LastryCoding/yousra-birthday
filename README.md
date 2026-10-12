# Anniversaire Yousra

Site d'affichage en lecture seule pour `https://yousra.lastry.fr`.

- `index.html` affiche les messages de `messages.json` via `/api/messages`.
- `messages.json` est un export des messages visibles : `id`, `name`, `message`, `created_at` uniquement.
- `compose.yaml` déploie un serveur Nginx sans montage de base de données et sans service d'administration.
- La base SQLite historique complète (y compris les messages supprimés et données techniques) est conservée **uniquement sur le VPS**, dans `/home/lastry/backups/yousra-birthday-original/`, hors de ce dépôt public.

Pour redéployer : `docker compose -f compose.yaml up -d`. Le réseau Docker externe `web` doit exister.
Pour reconstruire un SQLite d'affichage depuis l'export public : `python3 restore_messages.py messages.json /chemin/vers/nouveau-messages.db`.
Ne jamais publier ni écraser la base historique privée avec cette base reconstruite.

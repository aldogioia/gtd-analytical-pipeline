# Pubblicazione su GitHub Pages

## Rami

- `main`: monorepo con codice Python, SQL, Tableau e web app.
- `gh-pages`: solo la build statica del sito, con `CNAME` e `.nojekyll`.

Il comando dalla radice o da `gtd-story/` è:

```sh
npm run deploy
```

Per costruire e controllare la build senza push:

```sh
npm run deploy:check
```

Git deve essere autenticato su `aldogioia/gtd-analytical-pipeline`. Per esempio, `gh auth login` e `gh auth setup-git`. Il deploy non richiede token in file o variabili del progetto.

## Impostazioni della repository

In **Settings → Pages**:

1. Source: **Deploy from a branch**.
2. Branch: **gh-pages**, cartella **/ (root)**.
3. Custom domain: **gtd.aldogioia.com**.
4. Attivare **Enforce HTTPS** quando GitHub ha emesso il certificato.

Il file `gtd-story/public/CNAME`, incluso in ogni build, conserva il dominio tra i deploy. Le risorse usano la radice `/` perché il sito è servito direttamente dal sottodominio.

## DNS Squarespace

Aggiungere un solo record alla zona di `aldogioia.com`:

| Tipo  | Nome / Host | Dati / Destinazione | TTL                                 |
| ----- | ----------- | ------------------- | ----------------------------------- |
| CNAME | gtd         | aldogioia.github.io | 1 ora, oppure il valore predefinito |

La destinazione non contiene `https://` né il nome della repository. I quattro record A per `@` e il CNAME `www` del portfolio restano invariati. Non aggiungere altri record A, AAAA o CNAME allo stesso host `gtd`.

Impostare il custom domain su GitHub prima di aggiungere il record DNS. La propagazione e l’emissione del certificato possono richiedere tempo.

Verifica:

```sh
dig +short CNAME gtd.aldogioia.com
```

La risposta attesa è `aldogioia.github.io.`.

Documentazione ufficiale: [custom domain e sottodomini](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site), [origine di pubblicazione](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

# Lieger – web de suport, màrqueting i privacitat

Web estàtica (HTML + CSS, sense JavaScript ni cookies ni analítica) per publicar amb **GitHub Pages**.
Està en català (arrel) i en castellà (`es/`).

| Pàgina | Català | Castellano |
|---|---|---|
| Inici (màrqueting) | `index.html` | `es/index.html` |
| Suport | `suport.html` | `es/soporte.html` |
| Política de privacitat | `privacitat.html` | `es/privacidad.html` |
| Condicions d'ús | `condicions.html` | `es/condiciones.html` |

## Dades personals

Com a la web de Baby & Bond, només hi consten el **nom** (Nivard Arboix), la **marca** (Brel Lab) i el **correu de contacte**.
No hi ha NIF, adreça postal ni telèfon. Es configuren a dalt de `build.py` (`PUBLISHER`, `CONTACT_EMAIL`).
Els textos legals són a `legal-source/*.md` (còpia dels de l'app, `Lieger/Lieger/Legal/`); si es canvien a l'app,
es copien aquí i es torna a executar `python3 build.py`.

> Nota: Apple demana les dades d'editor (nom, adreça i correu) a **App Store Connect** per a apps que es venen a la UE
> (condició de «trader»); allà és on van, no a la web.

## Publicar a GitHub Pages

1. Crea un repositori nou a GitHub (per exemple `lieger`) i puja-hi aquesta carpeta:
   ```
   git remote add origin https://github.com/EL-TEU-USUARI/lieger.git
   git branch -M main
   git push -u origin main
   ```
2. Al repositori: **Settings > Pages > Build and deployment > Deploy from a branch**, branca `main`, carpeta `/ (root)`.
3. En uns minuts, la web és a `https://EL-TEU-USUARI.github.io/lieger/`.

## Adreces per a App Store Connect

A **App Information** i a la fitxa de cada localització:

| Camp | Català | Castellano |
|---|---|---|
| Marketing URL | `https://EL-TEU-USUARI.github.io/lieger/` | `https://EL-TEU-USUARI.github.io/lieger/es/` |
| Support URL | `…/lieger/suport.html` | `…/lieger/es/soporte.html` |
| Privacy Policy URL | `…/lieger/privacitat.html` | `…/lieger/es/privacidad.html` |

## Quan l'app sigui a l'App Store

A `build.py`, posa l'adreça de l'app a `APP_STORE_URL` i torna a generar: «Properament a l'App Store» passarà a ser un botó.

## Contingut

- `build.py` genera tots els `.html` (textos, estructura) a partir de `legal-source/*.md` i de les cadenes del mateix script.
- `style.css` és l'estil; `assets/` té la icona, les captures i la tipografia Andika (llicència OFL a `assets/fonts/`).
- Les captures són de l'app real (`assets/shots/`). Si l'app canvia molt, es poden substituir per les noves.

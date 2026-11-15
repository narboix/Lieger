#!/usr/bin/env python3
"""Genera la web de Lieger (suport, màrqueting, privacitat i condicions) en català i castellà.

Els textos legals surten de `legal-source/*.md` (còpia dels de l'app, `Lieger/Lieger/Legal/`). Si es canvien a l'app,
es copien aquí i es torna a executar aquest script.

Dades personals: com a Baby & Bond, només hi consten el nom, la marca (Brel Lab) i el correu de contacte.
No hi surten NIF, adreça postal ni telèfon.

Ús:
    python3 build.py
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
YEAR = 2026
PUBLISHER = "Nivard Arboix"
CONTACT_EMAIL = "aibrickcode@gmail.com"
# Adreça de l'app a l'App Store; mentre sigui None, la portada diu «Properament».
APP_STORE_URL = None

# (clau de pàgina) -> nom de fitxer per idioma
FILES = {
    "ca": {"home": "index.html", "support": "suport.html", "privacy": "privacitat.html", "terms": "condicions.html"},
    "es": {"home": "index.html", "support": "soporte.html", "privacy": "privacidad.html", "terms": "condiciones.html"},
}

T = {
    "ca": {
        "lang_name": "Català", "other": "es", "other_name": "Español",
        "nav": {"home": "Inici", "support": "Suport", "privacy": "Privacitat", "terms": "Condicions"},
        "title_suffix": "Lieger – aprèn a llegir pas a pas",
        "desc": "Lieger ajuda els infants de 6 a 8 anys a practicar la lectura amb més de 180 exercicis, un lector amb càmera "
                "i un viatge amb marcians. Sense comptes, sense anuncis i sense dades personals.",
        "h1": "Aprèn a llegir pas a pas",
        "lead": "Lieger ajuda els infants de 6 a 8 anys a practicar la lectura, acompanyats d'una persona adulta.",
        "soon": "Properament a l'App Store",
        "store": "Descarrega-la a l'App Store",
        "features_h": "Què hi trobaràs",
        "features": [
            ("Exercicis pas a pas", "Més de 180 exercicis en 8 blocs, de les vocals i les síl·labes directes fins a les frases i els textos breus. "
                                    "Cada exercici combina escalfament oral, taules de síl·labes, paraules de marcià, paraules de veritat, dictat i comprensió."),
            ("La persona adulta acompanya", "Lieger no corregeix sola: l'adult escolta, marca les paraules que han costat, cronometra tres lectures "
                                            "i decideix si cal repetir o avançar. Cada pas té una guia."),
            ("Un viatge amb marcians", "Cada exercici dona estrelles i descobreix un marcià nou per a l'àlbum. Sense ratxes que es perdin, "
                                       "sense competicions i sense missatges negatius: repetir no és fallar."),
            ("Lector amb la càmera", "Fotografia un text o importa'l d'una foto i Lieger el mostra amb lletra gran, síl·labes de colors o separades amb punts, "
                                     "majúscules i espaiats a mida. Pensat per facilitar la lectura també als infants amb dificultats o trastorns de la lectura."),
            ("Un perfil per a cada infant", "Fins a 8 perfils al mateix dispositiu, cadascun amb el seu viatge i els seus ajustaments de lectura. "
                                            "Sense comptes, sense correu i sense dades personals."),
            ("Català i castellà", "Els exercicis existeixen en les dues llengües, adaptats a cadascuna (no són traduccions). "
                                  "Tipografia per a primers lectors i paper sense distraccions."),
        ],
        "shots_h": "Mira-la per dins",
        "shots_alt": ["El viatge", "Una taula de síl·labes amb mode color", "El lector amb la càmera", "L'àlbum de marcians", "Un perfil per a cada infant"],
        "how_h": "Com funciona",
        "how": [
            "L'infant llegeix l'exercici: taules de síl·labes, paraules de marcià, paraules de veritat, frases o un text breu.",
            "L'adult escolta, toca les paraules que han costat i cronometra tres lectures de la mateixa taula.",
            "L'adult decideix si cal repetir o avançar. L'infant guanya estrelles i troba un marcià nou.",
        ],
        "price_h": "Gratuït i compra única",
        "price": "Els 3 primers exercicis de cada bloc i una captura setmanal amb el lector són gratuïts. Una sola compra desbloqueja tots els exercicis "
                 "i el lector sense límit. Pagament únic, sense subscripcions. Les compres queden protegides per una porta parental.",
        "science": "Lieger està inspirada en la recerca científica sobre l'aprenentatge de la lectura (consciència fonològica, síl·labes i lectura repetida) "
                   "per ajudar els nens i les nenes a aprendre a llegir de manera progressiva i divertida.",
        "disclaimer": "Lieger és una eina per practicar la lectura; no és un tractament mèdic ni un diagnòstic.",
        "privacy_h": "Privacitat",
        "privacy": "No hi ha comptes ni registre, ni analítica, ni publicitat, ni seguiment. Tot el que fa l'app es queda al dispositiu.",
        "privacy_link": "Llegeix la política de privacitat",
        "footer_by": "Una app de",
        "footer_contact": "Suport i contacte",
        # suport
        "support_title": "Suport",
        "support_intro": "Respostes a les preguntes més habituals sobre Lieger. Si no hi trobes el que busques, escriu-nos.",
        "faq": [
            ("Com començo?",
             "<p>Obre l'app i toca un exercici del <strong>Viatge</strong>. L'infant llegeix la pantalla i l'adult l'acompanya amb el botó "
             "«Guia per a l'adult» (la icona de la persona gran amb un infant), que explica què cal fer a cada pas. Al final, l'adult decideix "
             "si cal repetir l'exercici o avançar.</p>"),
            ("Què és gratuït i què inclou la versió completa?",
             "<p>Són gratuïts els <strong>3 primers exercicis de cada bloc</strong> i <strong>una captura setmanal</strong> amb el lector de càmera. "
             "La <strong>versió completa</strong> és una compra única que desbloqueja tots els exercicis (blocs A–H) i el lector sense límit. "
             "No hi ha subscripcions.</p>"),
            ("Com compro la versió completa?",
             "<p>A <strong>Ajustaments &gt; Opcions de compra</strong>. Primer cal resoldre un càlcul senzill (la porta parental), perquè la compra "
             "sigui cosa d'un adult. La compra la fa i la factura Apple.</p>"),
            ("He canviat d'iPhone o d'iPad, com recupero la compra?",
             "<p>Obre <strong>Ajustaments &gt; Opcions de compra</strong>, resol la porta parental i toca <strong>«Restaura les compres»</strong>. "
             "Cal haver iniciat sessió amb el mateix compte d'Apple amb què vas comprar.</p>"),
            ("Com demano un reembossament?",
             "<p>Els reembossaments els gestiona Apple. Pots demanar-lo a <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>.</p>"),
            ("Com afegeixo més infants?",
             "<p>A <strong>Ajustaments &gt; Perfils &gt; Gestiona els perfils</strong> (amb la porta parental) pots crear fins a 8 perfils. Cada perfil és un marcià "
             "i, si vols, un àlies o sobrenom opcional; tria'n un que no sigui el nom complet. Cada perfil té el seu propi viatge i els seus ajustaments de lectura. "
             "Per canviar de perfil, toca el marcià de dalt a la dreta del Viatge o, en obrir l'app, tria «Qui llegeix avui?».</p>"),
            ("Com esborro el progrés d'un infant?",
             "<p>A <strong>Gestiona els perfils</strong>, entra al perfil i tria <strong>«Reinicia el viatge»</strong> (esborra estrelles i marcians) "
             "o <strong>«Esborra el perfil»</strong>. No es pot desfer.</p>"),
            ("Com canvio l'idioma dels exercicis?",
             "<p>A <strong>Ajustaments &gt; Idioma dels exercicis</strong>: català o castellà. Cada idioma té el seu propi progrés.</p>"),
            ("Puc veure el text en majúscules o amb colors?",
             "<p>Sí. A <strong>Ajustaments</strong> hi ha la lletra (normal o MAJÚSCULES), el <strong>mode color</strong> i la paleta de colors de les síl·labes. "
             "Són ajustaments de cada perfil i s'apliquen als exercicis i al lector.</p>"),
            ("Com faig servir el lector de càmera?",
             "<p>A la pestanya <strong>Lector</strong>, toca «Captura amb la càmera» o «Tria una foto». Funciona millor amb text imprès, ben il·luminat. "
             "Si alguna paraula no s'ha llegit bé, toca la icona del llapis per corregir el text. També hi ha un text d'exemple. "
             "El text i les imatges es processen al dispositiu i no es desen ni s'envien enlloc.</p>"
             "<p>Fes servir el lector només amb textos que tinguis dret a copiar o utilitzar.</p>"),
            ("L'app envia dades meves o dels infants?",
             "<p>No. No hi ha comptes, ni analítica, ni publicitat, ni seguiment. El progrés, els perfils i els ajustaments són només al dispositiu. "
             "Més detalls a la <a href=\"privacitat.html\">política de privacitat</a>.</p>"),
            ("L'app funciona sense connexió?",
             "<p>Sí. Els exercicis, la tipografia i el lector funcionen sense connexió. Només cal connexió per fer o restaurar una compra.</p>"),
        ],
        "contact_h": "Contacte",
        "contact": "Per a qualsevol dubte, problema o suggeriment, escriu-nos a {EMAIL}. Indica el model del teu dispositiu, "
                   "la versió d'iOS i la versió de Lieger (a Configuració &gt; General &gt; Emmagatzematge de l'iPhone).",
    },
    "es": {
        "lang_name": "Español", "other": "ca", "other_name": "Català",
        "nav": {"home": "Inicio", "support": "Soporte", "privacy": "Privacidad", "terms": "Condiciones"},
        "title_suffix": "Lieger – aprende a leer paso a paso",
        "desc": "Lieger ayuda a niños de 6 a 8 años a practicar la lectura con más de 180 ejercicios, un lector con cámara "
                "y un viaje con marcianos. Sin cuentas, sin anuncios y sin datos personales.",
        "h1": "Aprende a leer paso a paso",
        "lead": "Lieger ayuda a niños de 6 a 8 años a practicar la lectura, acompañados de una persona adulta.",
        "soon": "Próximamente en la App Store",
        "store": "Descárgala en la App Store",
        "features_h": "Qué encontrarás",
        "features": [
            ("Ejercicios paso a paso", "Más de 180 ejercicios en 8 bloques, desde las vocales y las sílabas directas hasta las frases y los textos breves. "
                                       "Cada ejercicio combina calentamiento oral, tablas de sílabas, palabras de marciano, palabras de verdad, dictado y comprensión."),
            ("La persona adulta acompaña", "Lieger no corrige sola: la persona adulta escucha, marca las palabras que han costado, cronometra tres lecturas "
                                           "y decide si hay que repetir o avanzar. Cada paso tiene una guía."),
            ("Un viaje con marcianos", "Cada ejercicio da estrellas y descubre un marciano nuevo para el álbum. Sin rachas que se pierdan, "
                                       "sin competiciones y sin mensajes negativos: repetir no es fallar."),
            ("Lector con la cámara", "Fotografía un texto o impórtalo desde una foto y Lieger lo muestra con letra grande, sílabas de colores o separadas con puntos, "
                                     "mayúsculas y espaciados a medida. Pensado para facilitar la lectura también a niños y niñas con dificultades o trastornos de la lectura."),
            ("Un perfil para cada niño o niña", "Hasta 8 perfiles en el mismo dispositivo, cada uno con su viaje y sus ajustes de lectura. "
                                                "Sin cuentas, sin correo y sin datos personales."),
            ("Catalán y castellano", "Los ejercicios existen en las dos lenguas, adaptados a cada una (no son traducciones). "
                                     "Tipografía para primeros lectores y papel sin distracciones."),
        ],
        "shots_h": "Míralo por dentro",
        "shots_alt": ["El viaje", "Una tabla de sílabas con modo color", "El lector con la cámara", "El álbum de marcianos", "Un perfil para cada niño"],
        "how_h": "Cómo funciona",
        "how": [
            "El niño o la niña lee el ejercicio: tablas de sílabas, palabras de marciano, palabras de verdad, frases o un texto breve.",
            "La persona adulta escucha, toca las palabras que han costado y cronometra tres lecturas de la misma tabla.",
            "La persona adulta decide si hay que repetir o avanzar. El niño o la niña gana estrellas y encuentra un marciano nuevo.",
        ],
        "price_h": "Gratis y compra única",
        "price": "Los 3 primeros ejercicios de cada bloque y una captura semanal con el lector son gratuitos. Una sola compra desbloquea todos los ejercicios "
                 "y el lector sin límite. Pago único, sin suscripciones. Las compras quedan protegidas por una puerta parental.",
        "science": "Lieger está inspirada en la investigación científica sobre el aprendizaje de la lectura (conciencia fonológica, sílabas y lectura repetida) "
                   "para ayudar a niños y niñas a aprender a leer de forma progresiva y divertida.",
        "disclaimer": "Lieger es una herramienta para practicar la lectura; no es un tratamiento médico ni un diagnóstico.",
        "privacy_h": "Privacidad",
        "privacy": "No hay cuentas ni registro, ni analítica, ni publicidad, ni seguimiento. Todo lo que hace la app se queda en el dispositivo.",
        "privacy_link": "Lee la política de privacidad",
        "footer_by": "Una app de",
        "footer_contact": "Soporte y contacto",
        "support_title": "Soporte",
        "support_intro": "Respuestas a las preguntas más habituales sobre Lieger. Si no encuentras lo que buscas, escríbenos.",
        "faq": [
            ("¿Cómo empiezo?",
             "<p>Abre la app y toca un ejercicio del <strong>Viaje</strong>. El niño o la niña lee la pantalla y la persona adulta lo acompaña con el botón "
             "«Guía para adultos», que explica qué hay que hacer en cada paso. Al final, la persona adulta decide si hay que repetir "
             "el ejercicio o avanzar.</p>"),
            ("¿Qué es gratis y qué incluye la versión completa?",
             "<p>Son gratuitos los <strong>3 primeros ejercicios de cada bloque</strong> y <strong>una captura semanal</strong> con el lector de cámara. "
             "La <strong>versión completa</strong> es una compra única que desbloquea todos los ejercicios (bloques A–H) y el lector sin límite. "
             "No hay suscripciones.</p>"),
            ("¿Cómo compro la versión completa?",
             "<p>En <strong>Ajustes &gt; Opciones de compra</strong>. Primero hay que resolver un cálculo sencillo (la puerta parental), para que la compra "
             "sea cosa de una persona adulta. La compra la realiza y la factura Apple.</p>"),
            ("He cambiado de iPhone o de iPad, ¿cómo recupero la compra?",
             "<p>Abre <strong>Ajustes &gt; Opciones de compra</strong>, resuelve la puerta parental y toca <strong>«Restaurar compras»</strong>. "
             "Hay que haber iniciado sesión con la misma cuenta de Apple con la que compraste.</p>"),
            ("¿Cómo pido un reembolso?",
             "<p>Los reembolsos los gestiona Apple. Puedes pedirlo en <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>.</p>"),
            ("¿Cómo añado más niños?",
             "<p>En <strong>Ajustes &gt; Perfiles &gt; Gestionar los perfiles</strong> (con la puerta parental) puedes crear hasta 8 perfiles. Cada perfil es un marciano "
             "y, si quieres, un alias o apodo opcional; elige uno que no sea el nombre completo. Cada perfil tiene su propio viaje y sus ajustes de lectura. "
             "Para cambiar de perfil, toca el marciano de arriba a la derecha del Viaje o, al abrir la app, elige «¿Quién lee hoy?».</p>"),
            ("¿Cómo borro el progreso de un niño?",
             "<p>En <strong>Gestionar los perfiles</strong>, entra en el perfil y elige <strong>«Reiniciar el viaje»</strong> (borra estrellas y marcianos) "
             "o <strong>«Borrar el perfil»</strong>. No se puede deshacer.</p>"),
            ("¿Cómo cambio el idioma de los ejercicios?",
             "<p>En <strong>Ajustes &gt; Idioma de los ejercicios</strong>: catalán o castellano. Cada idioma tiene su propio progreso.</p>"),
            ("¿Puedo ver el texto en mayúsculas o con colores?",
             "<p>Sí. En <strong>Ajustes</strong> está la letra (normal o MAYÚSCULAS), el <strong>modo color</strong> y la paleta de colores de las sílabas. "
             "Son ajustes de cada perfil y se aplican a los ejercicios y al lector.</p>"),
            ("¿Cómo uso el lector de cámara?",
             "<p>En la pestaña <strong>Lector</strong>, toca «Capturar con la cámara» o «Elegir una foto». Funciona mejor con texto impreso y bien iluminado. "
             "Si alguna palabra no se ha leído bien, toca el icono del lápiz para corregir el texto. También hay un texto de ejemplo. "
             "El texto y las imágenes se procesan en el dispositivo y no se guardan ni se envían a ningún sitio.</p>"
             "<p>Usa el lector solo con textos que tengas derecho a copiar o utilizar.</p>"),
            ("¿La app envía datos míos o de los niños?",
             "<p>No. No hay cuentas, ni analítica, ni publicidad, ni seguimiento. El progreso, los perfiles y los ajustes están solo en el dispositivo. "
             "Más detalles en la <a href=\"privacidad.html\">política de privacidad</a>.</p>"),
            ("¿La app funciona sin conexión?",
             "<p>Sí. Los ejercicios, la tipografía y el lector funcionan sin conexión. Solo hace falta conexión para hacer o restaurar una compra.</p>"),
        ],
        "contact_h": "Contacto",
        "contact": "Para cualquier duda, problema o sugerencia, escríbenos a {EMAIL}. Indica el modelo de tu dispositivo, "
                   "la versión de iOS y la versión de Lieger (en Ajustes &gt; General &gt; Almacenamiento del iPhone).",
    },
}

def inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"([\w.+-]+@[\w-]+\.[\w.-]+\w)", r'<a href="mailto:\1">\1</a>', text)
    text = re.sub(r"(?<![\w/])(www\.[\w./-]+[\w/])", r'<a href="https://\1">\1</a>', text)
    return text


def markdown(source: str) -> str:
    """Convertidor mínim per als textos legals: títols, llistes, paràgrafs i negretes."""
    out, para, items = [], [], []

    def flush():
        nonlocal para, items
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para = []
        if items:
            out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>")
            items = []

    for line in source.splitlines():
        if not line.strip():
            flush()
        elif line.startswith("# "):
            flush(); out.append(f"<h1>{inline(line[2:])}</h1>")
        elif line.startswith("## "):
            flush(); out.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("- "):
            if para:
                flush()
            items.append(line[2:])
        else:
            if items:
                flush()
            para.append(line.strip())
    flush()
    return "\n".join(out)


def layout(lang: str, key: str, title: str, body: str, hero: str = "") -> str:
    t = T[lang]
    prefix = "../" if lang == "es" else ""
    other = t["other"]
    other_href = f"es/{FILES['es'][key]}" if lang == "ca" else f"../{FILES['ca'][key]}"
    links = []
    for k in ("home", "support", "privacy", "terms"):
        current = ' aria-current="page"' if k == key else ""
        links.append(f'<a class="link" href="{FILES[lang][k]}"{current}>{t["nav"][k]}</a>')
    nav = "".join(links)
    description = html.escape(t["desc"], quote=True)
    alternates = (
        f'<link rel="alternate" hreflang="ca" href="{("../" if lang == "es" else "")}{FILES["ca"][key]}">\n'
        f'<link rel="alternate" hreflang="es" href="{("" if lang == "es" else "es/")}{FILES["es"][key]}">'
    )
    contact_nav = FILES[lang]["support"]
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · Lieger</title>
<meta name="description" content="{description}">
{alternates}
<link rel="icon" href="{prefix}assets/icon.png">
<link rel="stylesheet" href="{prefix}style.css">
</head>
<body>
<header class="site-header">
<nav aria-label="Navegació">
<a class="brand" href="{FILES[lang]['home']}"><img src="{prefix}assets/icon.png" alt="" width="34" height="34">Lieger</a>
{nav}
<a class="link lang" href="{other_href}" hreflang="{other}" lang="{other}">{t['other_name']}</a>
</nav>
</header>
{hero}
{body}
<footer class="site-footer">
<div class="inner">
<div class="links">
<a href="{FILES[lang]['support']}">{t['footer_contact']}</a>
<a href="{FILES[lang]['privacy']}">{t['nav']['privacy']}</a>
<a href="{FILES[lang]['terms']}">{t['nav']['terms']}</a>
</div>
<span>© {YEAR} {PUBLISHER}</span>
<span class="by">{t['footer_by']} <img class="brel" src="{prefix}assets/brel-lab.png" alt="brel lab"></span>
</div>
</footer>
</body>
</html>
"""


def home(lang: str) -> str:
    t = T[lang]
    prefix = "../" if lang == "es" else ""
    cta = (f'<a class="soon" href="{APP_STORE_URL}">{t["store"]}</a>' if APP_STORE_URL
           else f'<span class="soon">{t["soon"]}</span>')
    phones = "".join(
        f'<img src="{prefix}assets/shots/{lang}/0{i}.jpg" alt="{html.escape(t["shots_alt"][i - 1])}" loading="lazy">'
        for i in (1, 2, 3)
    )
    hero = f"""<section class="hero"><div class="inner">
<div>
<img class="icon" src="{prefix}assets/icon.png" alt="Lieger" width="96" height="96">
<h1>{t['h1']}</h1>
<p class="lead">{t['lead']}</p>
{cta}
</div>
<div class="phones">{phones}</div>
</div></section>"""
    features = "".join(f"<li><h3>{h}</h3><p>{p}</p></li>" for h, p in t["features"])
    shots = "".join(
        f'<img src="{prefix}assets/shots/{lang}/0{i}.jpg" alt="{html.escape(t["shots_alt"][i - 1])}" loading="lazy" height="440">'
        for i in range(1, 6)
    )
    steps = "".join(f"<li>{s}</li>" for s in t["how"])
    body = f"""<main class="wide">
<section class="block"><h2>{t['features_h']}</h2><ul class="features">{features}</ul></section>
<section class="block"><h2>{t['shots_h']}</h2><div class="shots">{shots}</div></section>
<section class="block"><h2>{t['how_h']}</h2><ol class="steps">{steps}</ol></section>
<section class="block"><h2>{t['price_h']}</h2><p>{t['price']}</p></section>
<section class="block"><p>{t['science']}</p><p class="note">{t['disclaimer']}</p></section>
<section class="block"><h2>{t['privacy_h']}</h2><p>{t['privacy']} <a href="{FILES[lang]['privacy']}">{t['privacy_link']}</a>.</p></section>
</main>"""
    return layout(lang, "home", t["title_suffix"], body, hero)


def support(lang: str) -> str:
    t = T[lang]
    faq = "".join(f"<details><summary>{q}</summary>{a}</details>" for q, a in t["faq"])
    mail = f'<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>'
    body = f"""<main><article>
<h1>{t['support_title']}</h1>
<p>{t['support_intro']}</p>
{faq}
<h2>{t['contact_h']}</h2>
<p>{t['contact'].replace("{EMAIL}", mail)}</p>
</article></main>"""
    return layout(lang, "support", t["support_title"], body)


def legal(lang: str, key: str) -> str:
    name = "privacy" if key == "privacy" else "terms"
    source = (ROOT / "legal-source" / f"{name}.{lang}.md").read_text(encoding="utf-8")
    title = re.match(r"# (.+)", source).group(1)
    body = f"<main><article>\n{markdown(source)}\n</article></main>"
    return layout(lang, key, title, body)


def main():
    for lang in ("ca", "es"):
        folder = ROOT if lang == "ca" else ROOT / "es"
        folder.mkdir(exist_ok=True)
        pages = {
            FILES[lang]["home"]: home(lang),
            FILES[lang]["support"]: support(lang),
            FILES[lang]["privacy"]: legal(lang, "privacy"),
            FILES[lang]["terms"]: legal(lang, "terms"),
        }
        for name, content in pages.items():
            (folder / name).write_text(content, encoding="utf-8")
            print((folder / name).relative_to(ROOT))


if __name__ == "__main__":
    main()

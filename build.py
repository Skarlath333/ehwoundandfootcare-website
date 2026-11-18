"""Builds the static Empowered Health Wound & Foot Care site into ./docs (served by GitHub Pages) from the page bodies in ./src.

Run: python3 build.py
Each src/*.html file starts with header lines:
  title: <page title>
  description: <meta description>
  path: <output path, e.g. index.html or about/index.html>
  base: <optional, e.g. / for 404.html>
followed by a blank line and the page body HTML. In bodies, {base} is the relative path to the site root.
"""
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "docs"
SITE_URL = "https://www.ehwoundandfootcare.com"

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta property="og:image" content="{site}/assets/logo-footer.webp">
<link rel="icon" href="{base}assets/icon-1.webp" type="image/webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&family=Rosario:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/styles.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"MedicalBusiness","name":"Empowered Health Wound and Foot Care","url":"{site}/","email":"admin@ehwoundandfootcare.com","telephone":"+1-865-219-3222","faxNumber":"+1-865-999-7033","description":"Advanced wound and foot care for patients in skilled nursing and assisted living facilities and at home in East Tennessee.","areaServed":"East Tennessee","sameAs":["https://www.facebook.com/people/Empowered-Health-Wound-Foot-Care/61581203884362/","https://www.instagram.com/empoweredhealthwf/"]}}
</script>
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{base}"><img src="{base}assets/logo.webp" alt="Empowered Health Wound &amp; Foot Care" width="233" height="46"></a>
    <button class="menu-toggle" aria-label="Open menu" aria-expanded="false" onclick="var n=document.querySelector('.nav');n.classList.toggle('open');this.setAttribute('aria-expanded',n.classList.contains('open'))"><span></span><span></span><span></span></button>
    <nav class="nav">
      <a href="{base}about/">About</a>
      <a href="{base}service/">Services</a>
      <a href="{base}team/">Team</a>
      <a href="{base}resources/">Resources</a>
      <a class="btn" href="{base}contact/">Request a visit</a>
    </nav>
  </div>
</header>
<main>
"""

FOOT = """</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <img class="footer-logo" src="{base}assets/logo-footer.webp" alt="" width="170" height="100">
        <p>Compassionate wound and foot care wherever you call home: skilled nursing, assisted living and in-home visits.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="{base}about/">About</a></li>
          <li><a href="{base}service/">Services</a></li>
          <li><a href="{base}team/">Team</a></li>
          <li><a href="{base}resources/">Resources</a></li>
          <li><a href="{base}contact/">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="tel:+18652193222">Office: (865) 219-3222</a></li>
          <li>Fax: (865) 999-7033</li>
          <li><a href="mailto:admin@ehwoundandfootcare.com">admin@ehwoundandfootcare.com</a></li>
          <li><a href="https://www.facebook.com/people/Empowered-Health-Wound-Foot-Care/61581203884362/" target="_blank" rel="noopener">Facebook</a> &middot; <a href="https://www.instagram.com/empoweredhealthwf/" target="_blank" rel="noopener">Instagram</a></li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <span>&copy; <span id="yr">2026</span> Empowered Health Wound and Foot Care. All rights reserved.</span>
      <span><a href="{base}privacy-policy/">Privacy Policy</a> &middot; <a href="{base}cookie-policy/">Cookie Policy</a></span>
    </div>
  </div>
</footer>
<script>document.getElementById('yr').textContent=new Date().getFullYear();
document.querySelectorAll('.nav a').forEach(function(a){{a.addEventListener('click',function(){{document.querySelector('.nav').classList.remove('open')}})}});</script>
</body>
</html>
"""

CONTACT_CTA = """<section class="booking center">
  <div class="wrap">
    <div class="eyebrow" style="color:#cfe6a8">Get started</div>
    <h2>Request an Appointment or Consultation</h2>
    <p class="lead">Need a referral or consultation? Call or email us and a member of our team will reach out to schedule your visit.</p>
    <div class="actions">
      <a class="btn" href="tel:+18652193222">Call (865) 219-3222</a>
      <a class="btn light" href="mailto:admin@ehwoundandfootcare.com">Email referrals</a>
    </div>
    <p class="note">Fax referrals to (865) 999-7033. Please don't include medical details by email. We'll discuss your health privately during your visit.</p>
  </div>
</section>
"""


def read_page(src):
    text = src.read_text()
    header, body = text.split("\n\n", 1)
    meta = dict(line.split(": ", 1) for line in header.splitlines())
    return meta, body


def posts_html(base):
    posts = []
    for src in SRC.glob("article-*.html"):
        meta, _ = read_page(src)
        posts.append(meta)
    posts.sort(key=lambda m: int(m.get("order", 99)))
    cards = "".join(
        '<article class="post"><div class="date">{date}</div><h3>{heading}</h3><p>{excerpt}</p>'
        '<a class="more" href="{base}{url}">Read more &rarr;</a></article>'.format(
            base=base, url=m["path"][: -len("index.html")], **{k: m[k] for k in ("date", "heading", "excerpt")})
        for m in posts)
    return '<div class="posts">' + cards + "</div>"


def build():
    for src in sorted(SRC.glob("*.html")):
        meta, body = read_page(src)
        path = meta["path"]
        depth = path.count("/")
        base = meta.get("base") or ("../" * depth if depth else "./")
        canonical = SITE_URL + "/" + (path[: -len("index.html")] if path.endswith("index.html") else path)
        ctx = dict(title=meta["title"], description=meta["description"], canonical=canonical, site=SITE_URL, base=base)
        body = body.replace("{contact_cta}", CONTACT_CTA)
        if "{posts}" in body:
            body = body.replace("{posts}", posts_html(base))
        body = body.replace("{base}", base)
        html = HEAD.format(**ctx) + body + FOOT.format(**ctx)
        out = OUT / path
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html)
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    build()

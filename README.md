# Empowered Health Wound & Foot Care website

Source for www.ehwoundandfootcare.com, a static site served by GitHub Pages from the `docs/` folder on `main`.

- Page content lives in `src/*.html` (each file starts with `title:`, `description:` and `path:` lines; articles also have `heading:`, `excerpt:`, `date:` and `order:`).
- Shared header, footer, contact section and page shell live in `build.py`.
- Styles and images live in `docs/assets/`.

Page addresses match the old WordPress site (`/about/`, `/service/`, `/team/`, `/resources/`, `/contact/`, `/10/<article>/`), so existing links and search results keep working.

To change the site, edit `src/` or `build.py`, run `python3 build.py`, and commit the updated `docs/` folder.

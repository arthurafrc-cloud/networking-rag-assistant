"""
build_carousel.py  ->  gera o carrossel do LinkedIn a partir do HTML editável

Saídas:
  docs/portfolio/linkedin-carousel.pdf      (7 páginas de 1080 x 1350 px, formato 4:5)
  assets/social/slide-1.png ... slide-7.png (2160 x 2700 px, as mesmas páginas em imagem)
  assets/social/cover.png                   (1280 x 640 px, capa para o GitHub)

Para mudar o texto (por exemplo, colocar o link real do repositório), edite
carousel.html e rode este script de novo.

Requisitos (apenas para gerar os arquivos; o projeto em si não precisa deles):
    pip install playwright
    playwright install chromium

Como rodar:
    python docs/portfolio/carousel-source/build_carousel.py
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parent.parent.parent
PDF_SAIDA = PASTA.parent / "linkedin-carousel.pdf"
PASTA_SOCIAL = RAIZ / "assets" / "social"
QTD_SLIDES = 7


def main():
    PASTA_SOCIAL.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        navegador = p.chromium.launch()

        # ---- Carrossel ----
        pagina = navegador.new_page(
            viewport={"width": 1080, "height": 1350}, device_scale_factor=2
        )
        pagina.goto((PASTA / "carousel.html").as_uri())
        pagina.evaluate("document.fonts.ready")
        pagina.wait_for_load_state("networkidle")

        # Aviso se algum slide tiver conteúdo transbordando
        for i in range(1, QTD_SLIDES + 1):
            sobra = pagina.evaluate(
                f"""() => {{
                    const s = document.querySelector('#slide-{i}');
                    return s.scrollHeight - s.clientHeight;
                }}"""
            )
            if sobra > 0:
                print(f"ATENÇÃO: slide {i} transborda {sobra}px")

        for i in range(1, QTD_SLIDES + 1):
            pagina.locator(f"#slide-{i}").screenshot(path=str(PASTA_SOCIAL / f"slide-{i}.png"))

        pagina.pdf(
            path=str(PDF_SAIDA),
            width="1080px",
            height="1350px",
            print_background=True,
        )

        # ---- Capa do repositório ----
        capa = navegador.new_page(
            viewport={"width": 1280, "height": 640}, device_scale_factor=1
        )
        capa.goto((PASTA / "cover.html").as_uri())
        capa.evaluate("document.fonts.ready")
        capa.locator("#capa").screenshot(path=str(PASTA_SOCIAL / "cover.png"))

        navegador.close()

    print("Gerado:", PDF_SAIDA)
    print("Gerado:", PASTA_SOCIAL)


if __name__ == "__main__":
    main()

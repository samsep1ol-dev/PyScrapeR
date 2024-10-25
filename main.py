import os
import requests
from lxml import html
from urllib.parse import urljoin, urlparse

# Banner
banner = r"""
⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⣠⣴⣶⣿⣶⢠⣾⣿⣿⣶⣦⣀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣷⣄
⠀⠀⠀⠀⠀⠀⠀ ⣰⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⣀⡀
⠀⠀⠀ ⡀⠤⠤⢤⣿⣿⣿⣿⣿⣿⣿⡏⠈⣿⣿⣿⣿⣿⣿⣿⣿⣍⣴⣶⣾⣵⡄
⠀ ⠀⣬⣾⠿⢷⣮⣿⣿⡿⠛⠉⠉⠉⠉⠀⠀⠀⠈⠉⠙⢿⣿⣿⣿⣿⡇⠉⠉⡹⠀
 ⠀⢉⠀⢀⢸⢿⣿⣿⠀⠠⡲⣶⠶⡆⠀⡶⢛⣉⡠⡂⠀⢿⣿⣿⡟⣡⠿⠎⠁⠀
  ⠀⠀⠑⠻⠳⣼⣿⣿⡄⠈⠘⠿⠓⠙⠀⠃⠚⠛⠁⠀⠀⢸⣿⣿⣿⡅⠊⠀⠀
  ⠀ ⠀⠀ ⠀⠊⢽⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣿⣿⣿⡙⠃⠀⠀
  ⠀⠀   ⠀⠀⢸⣿⣿⣿⡗⠀⠀⠐⠄⠔⠀⠀⠀⠀⢻⣿⣿⣟⢷⠀⠀
  ⠀⠀⠀ ⠀⠀⠀⠘⢹⣿⣿⡅⠀⠀⠀⠀⠀⠀⠀⠀⣀⣿⣿⣿⣿⠀⠀
  ⠀⠀⠀⠀ ⠀⠀ ⢸⣿⣿⣷⣦⣤⣤⣤⣤⠤⠔⣊⣿⣿⣿⣟⢿⡇⠀
  ⠀⠀⠀⠀ ⠀⠀⠀⠀⠘⡟⣿⣿⣷⡐⠶⠶⠶⠖⢻⣿⣿⣿⣿⣿⠀⠃⠀
  ⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠈⢿⠻⣿⣷⣶⣶⣶⣿⡏⠻⣿⠈⠻⠀⠀⠀
  ⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⠀⠹⣿⡇⠀⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈
                     ⠻⡆⠀⠹⠁⠀
                     
                    @samsep1ol
"""


def clear_console():
    """Limpa o console."""
    os.system('cls' if os.name == 'nt' else 'clear')


def make_dirs(path):
    """Cria diretórios se não existirem."""
    if not os.path.exists(path):
        os.makedirs(path)


def download_file(url, folder):
    """Faz o download de um arquivo e o salva no diretório especificado."""
    local_filename = os.path.join(folder, os.path.basename(urlparse(url).path))
    response = requests.get(url)
    with open(local_filename, 'wb') as f:
        f.write(response.content)
    return local_filename


def clone(url, base_folder):
    """Clona o site, incluindo arquivos HTML, CSS, JS e imagens."""
    # Limpa o console e exibe o banner
    clear_console()
    print(banner)
    print(f"Iniciando a clonagem do site: {url}...\n")

    # Requisição e parsing do HTML
    response = requests.get(url)
    response.raise_for_status()  # Verifica erros HTTP
    tree = html.fromstring(response.content)

    # Salva o HTML principal como index.html
    output_html = os.path.join(base_folder, "index.html")
    with open(output_html, 'w', encoding="utf-8") as f:
        f.write(html.tostring(tree, pretty_print=True, encoding="unicode"))

    print(f"Salvando {output_html}")

    # Baixa e atualiza links CSS
    for link in tree.xpath("//link[@rel='stylesheet']"):
        css_url = urljoin(url, link.get("href"))
        css_path = urlparse(css_url).path
        css_folder = os.path.join(base_folder, os.path.dirname(css_path).lstrip('/'))
        make_dirs(css_folder)  # Cria a pasta, se não existir
        local_path = download_file(css_url, css_folder)
        link.set("href", os.path.relpath(local_path, base_folder))

    # Baixa e atualiza links JS
    for script in tree.xpath("//script[@src]"):
        js_url = urljoin(url, script.get("src"))
        js_path = urlparse(js_url).path
        js_folder = os.path.join(base_folder, os.path.dirname(js_path).lstrip('/'))
        make_dirs(js_folder)  # Cria a pasta, se não existir
        local_path = download_file(js_url, js_folder)
        script.set("src", os.path.relpath(local_path, base_folder))

    # Baixa imagens
    for img in tree.xpath("//img[@src]"):
        img_url = urljoin(url, img.get("src"))
        img_path = urlparse(img_url).path
        img_folder = os.path.join(base_folder, os.path.dirname(img_path).lstrip('/'))
        make_dirs(img_folder)  # Cria a pasta, se não existir
        local_path = download_file(img_url, img_folder)
        img.set("src", os.path.relpath(local_path, base_folder))

    # Baixa todas as páginas HTML
    links = tree.xpath("//a[@href]")
    for link in links:
        page_url = urljoin(url, link.get("href"))
        if page_url.endswith(".html"):
            local_html_path = os.path.join(base_folder, os.path.basename(page_url))
            # Verifica se a página já foi salva
            if not os.path.exists(local_html_path):
                response = requests.get(page_url)
                with open(local_html_path, 'w', encoding="utf-8") as f:
                    f.write(response.text)
                print(f"Salvando {local_html_path}")

    print("Website clonado com sucesso!")


def main():
    while True:
        clear_console()
        print("by: https://github.com/samsep1ol-dev")
        folder_name = input("Nome da pasta: ")
        user_input = input("URL do site: ")

        print("Criando pasta...")
        base_folder = os.path.join(os.getcwd(), folder_name)
        make_dirs(base_folder)

        clone(user_input, base_folder)

        # Pergunta se o usuário deseja clonar outro site
        again = input("Deseja clonar outro site? (s/n): ").strip().lower()
        if again != 's':
            break


if __name__ == "__main__":
    main()

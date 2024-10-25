
echo "# PyScrapeR

PyScrapeR é uma ferramenta simples para clonar sites, baixando arquivos HTML, CSS, JS e imagens da URL fornecida. Ideal para desenvolvedores e designers que desejam analisar a estrutura e o conteúdo de um site.

## Instalação

Siga os passos abaixo para configurar e executar o projeto no Linux:

1. **Atualize o sistema e instale o Python 3 e o pip** (caso ainda não estejam instalados):
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **Clone o repositório**:
   ``` bash
   git clone https://github.com/samsep1ol-dev/PyScrapeR.git
   cd PyScrapeR
   ```

3. **Instale as dependências**:
   ``` bash
   pip install -r requirements.txt
   ```

4. **Execute o script**:
   ``` bash
   python3 main.py
   ```

## Uso

Após executar o script, você será solicitado a preencher os seguintes dados nos inputs do terminal:

- **Nome da pasta**: Nome do diretório onde o site clonado será salvo.
- **URL do site**: Link do site que você deseja clonar.

O script irá baixar a estrutura do site com os arquivos HTML, CSS, JS e imagens na pasta especificada.


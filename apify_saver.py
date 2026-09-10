import json
import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from apify_client import ApifyClient
from mcp.server.fastmcp import FastMCP

#mcp = FastMCP("ApifyAutoSaver")
load_dotenv()
APIFY_TOKEN = os.getenv("APIFY_TOKEN")
OUTPUT_DIR = r"C:\Users\EduardoGiannetti\Downloads\apifymcp\json"


#@mcp.tool()
def raspar_e_salvar_comentarios(post_url: str, filename: str = None) -> str:
    """Raspa comentarios do Instagram pelo Apify via URL do post do instagram que o usuário mandar, 
    salva diretamente em JSON na pasta pré-definida e retorna os textos dos comentários já filtrados
    para a janela de contexto chat"""

    client = ApifyClient(APIFY_TOKEN)

    # Executa o actor do Apify
    url_limpa = post_url.split("?")[0]
    run_input = {
        "startUrls": [{"url": url_limpa}],
        "directUrls": [url_limpa],
        "resultsLimit": 700,
    }

    run = client.actor("apidojo/instagram-comments-scraper").call(run_input=run_input)

    items = list(client.dataset(run.default_dataset_id).iterate_items())
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if not filename:
        agora = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comentarios-{agora}.json"
        
    file_path = os.path.join(OUTPUT_DIR, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
        
    subprocess.run([r"C:\Users\EduardoGiannetti\Downloads\apifymcp\QuickSort\bin\Debug\net10.0\QuickSort.exe", file_path], check=True)
    with open(file_path, "r", encoding="utf-8") as f:
        comentarios_ordenados = json.load(f)
        
    comentarios_limpos = []
    for item in comentarios_ordenados:
        texto = item.get("text") or item.get("message") or ""
        texto = texto.strip()
        if texto:
            comentarios_limpos.append(texto)

    # Limita o envio dos textos para não estourar a memória do chat se houver centenas
    amostra_comentarios = comentarios_limpos[:700]
    lista_texto = "\n".join([f"- {c}" for c in amostra_comentarios])

    return (f"Sucesso! {len(items)} comentários foram salvos no arquivo: {file_path}"
            f"\n\nAmostra dos comentários:\n{lista_texto}")


if __name__ == "__main__":
    resultado = raspar_e_salvar_comentarios("https://www.instagram.com/reel/DarBPOcMSvH/?utm_source=ig_web_copy_link&stkn=MzRlODBiNWFlZA==")
    print("\n" + resultado)
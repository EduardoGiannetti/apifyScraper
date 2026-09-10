import json
import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from apify_client import ApifyClient
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ApifyAutoSaver")
load_dotenv()
APIFY_TOKEN = os.getenv("APIFY_TOKEN")
OUTPUT_DIR = r"C:\Users\EduardoGiannetti\Downloads\apifymcp\json"


@mcp.tool()
def scrape_instagram(post_url: str, filename: str = None) -> str:
    """Use ESTA tool APENAS para extrair comentários de posts do Instagram.
    Gatilho: Acione quando o usuário fornecer uma URL contendo 'instagram.com' (ex: instagram.com/p/..., instagram.com/reel/...) ou pedir explicitamente para raspar o Instagram.
    Ação: Faz scraping pelo Apify, salva os dados em um arquivo JSON ordenado e retorna uma amostra limpa dos comentários (até 700) para o contexto do chat.
    NÃO use esta tool para URLs do TikTok."""

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
@mcp.tool()
def scrape_tiktok(post_url: str, filename: str = None) -> str:
    """Use ESTA tool APENAS para extrair comentários de vídeos do TikTok.
    Gatilho: Acione quando o usuário fornecer uma URL contendo 'tiktok.com' ou 'vm.tiktok.com', ou pedir explicitamente para raspar o TikTok.
    Ação: Faz scraping pelo Apify, salva os dados em um arquivo JSON ordenado e retorna uma amostra limpa dos comentários para o contexto do chat.
    NÃO use esta tool para URLs do Instagram. Retorne uma mensagem de erro se a raspagem falhar ou se a URL não for do TikTok."""
    
    client = ApifyClient(APIFY_TOKEN)

    # Executa o actor do Apify
    url_limpa = post_url.split("?")[0]
    run_input = {
        "startUrls": [{"url": url_limpa}],
        "directUrls": [url_limpa],
        "maxItems": 700,
    }

    run = client.actor("apidojo/tiktok-comments-scraper").call(run_input=run_input)

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
#    mcp.run()
     resultado = scrape_tiktok("https://www.tiktok.com/@by.ariela/video/7672124343807216903?is_from_webapp=1&sender_device=pc&web_id=7683217763096036884")
     print("\n" + resultado)
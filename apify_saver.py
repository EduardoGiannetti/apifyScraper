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
    try:
        url_limpa = post_url.split("?")[0]
    except Exception as e:
        return f"Erro ao processar a URL: {e}"
    
    run_input = {
        "directUrls": [url_limpa],
        "resultsLimit": 50,
    }
    try:
        run = client.actor("apify/instagram-comment-scraper").call(run_input=run_input)
    except Exception as e:
        return f"Erro ao executar o scraper: {e}"
    
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if not filename:
        agora = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comentarios-{agora}.json"
    
    file_path = os.path.join(OUTPUT_DIR, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    try:
        subprocess.run([r"C:\Users\EduardoGiannetti\Downloads\apifymcp\QuickSort\bin\Debug\net10.0\QuickSort.exe", file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o QuickSort, executando sem sort: {e}")
        pass
    
    with open(file_path, "r", encoding="utf-8") as f:
        comentarios_ordenados = json.load(f)
    
    comentarios_limpos = []
    try:
        for item in comentarios_ordenados:
            try:
                texto = item.get("text") or item.get("message") or ""
                texto = texto.strip()
                curtidas = item.get("diggCount") or item.get("likesCount") or 0
                if texto:
                    comentarios_limpos.append(f"[{curtidas} likes] {texto}")
            except Exception as e:
                print(f"Erro ao processar item: {item}, erro: {e}")
                continue
    except Exception as e:
        return f"Erro ao processar os comentários: {e}"
    
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
    try:
        url_limpa = post_url.split("?")[0]
    except Exception as e:
        return f"Erro ao processar a URL: {e}"
    
    run_input = {
        "postURLs": [url_limpa],
        "commentsPerPost": 50,
    }
    try:
        run = client.actor("clockworks/tiktok-comments-scraper").call(run_input=run_input)
    except Exception as e:
        return f"Erro ao executar o scraper: {e}"
    
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if not filename:
        agora = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comentarios-{agora}.json"
    
    file_path = os.path.join(OUTPUT_DIR, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    try:
        subprocess.run([r"C:\Users\EduardoGiannetti\Downloads\apifymcp\QuickSort\bin\Debug\net10.0\QuickSort.exe", file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o QuickSort, executando sem sort: {e}")
        pass
    
    with open(file_path, "r", encoding="utf-8") as f:
        comentarios_ordenados = json.load(f)
    
    comentarios_limpos = []
    try:
        for item in comentarios_ordenados:
            try:
                texto = item.get("text") or item.get("message") or ""
                texto = texto.strip()
                curtidas = (item.get("diggCount")
                or item.get("likesCount")
                or item.get("likeCount") 
                or 0
                )
                if texto:
                    comentarios_limpos.append(f"[{curtidas} likes] {texto}")
            except Exception as e:
                print(f"Erro ao processar item: {item}, erro: {e}")
                continue
    except Exception as e:
        return f"Erro ao processar os comentários: {e}"
    
    # Limita o envio dos textos para não estourar a memória do chat se houver centenas
    amostra_comentarios = comentarios_limpos[:700]
    lista_texto = "\n".join([f"- {c}" for c in amostra_comentarios])

    return (f"Sucesso! {len(items)} comentários foram salvos no arquivo: {file_path}"
            f"\n\nAmostra dos comentários:\n{lista_texto}")

if __name__ == "__main__":
#    mcp.run()
   resultado = scrape_tiktok("https://www.tiktok.com/@doyouknowlinux/video/7652448130037812511?is_from_webapp=1&sender_device=pc&web_id=7683217763096036884")
   print("\n" + resultado)
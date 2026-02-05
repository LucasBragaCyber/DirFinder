#!/usr/bin/env python3

import requests
import argparse
import threading
from queue import Queue
import sys
import time
import os
import random

# --- Cores ANSI ---
class Cores:
    ORANGE = '\033[1;38;5;208m'
    BLUE = '\033[1;34m'
    GREEN = '\033[0;32m'
    RED = '\033[1;91m'
    YELLOW = '\033[0;33m'
    YELLOW_STRONG = '\033[1;93m'
    NC = '\033[0m'

# --- Variáveis Globais de Controle ---
stop_event = threading.Event() # Sinalizador para parar as threads

# Lista de User-Agents para evitar bloqueios simples de WAF/Bot detection
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0'
]

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"{Cores.RED}[!] Erro: Argumentos ausentes ou inválidos.{Cores.NC}\n")
        self.print_help()
        self.exit(2)

def worker(q, base_url, print_lock):
    """
    Consome itens da fila. Verifica o stop_event a cada iteração
    para permitir uma parada rápida.
    """
    while not stop_event.is_set():
        if q.empty():
            break
        
        try:
            # timeout curto no get para verificar o stop_event frequentemente se a fila estiver vazia
            path = q.get(timeout=0.1) 
        except:
            continue

        full_url = f"{base_url}/{path}"
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        
        try:
            # Timeout reduzido para agilizar
            response = requests.get(full_url, headers=headers, timeout=3, allow_redirects=False)
            http_code = response.status_code
            
            # Lógica de output
            with print_lock:
                if http_code == 200:
                    print(f"{Cores.GREEN}[+] Encontrado (200): {full_url}{Cores.NC}")
                elif http_code in [301, 302, 307]:
                    location = response.headers.get('Location', 'N/A')
                    print(f"{Cores.BLUE}[>] Redirecionamento ({http_code}): {full_url}")
                elif http_code == 403:
                    print(f"{Cores.ORANGE}[!] Proibido (403): {full_url}{Cores.NC}")
                elif http_code == 401:
                    print(f"{Cores.RED}[!] Auth Requerida (401): {full_url}{Cores.NC}")
                    
        except requests.exceptions.RequestException:
            pass # Erros de conexão são ignorados para não poluir a tela
        finally:
            q.task_done()

def main():
    parser = CustomArgumentParser(
        description="Descobridor de diretórios e arquivos (Brute Force).",
        epilog=f"Exemplo: python3 {sys.argv[0]} -d http://alvo.com -w wordlist.txt -x php,html,txt -t 50",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    required_args = parser.add_argument_group('Obrigatórios')
    optional_args = parser.add_argument_group('Opcionais')

    required_args.add_argument("-d", "--dominio", dest="dominio", help="URL alvo.", required=True)
    required_args.add_argument("-w", "--wordlist", dest="wordlist", help="Arquivo de wordlist.", required=True)
    
    optional_args.add_argument("-t", "--threads", dest="threads", help="Nº de Threads (Padrão: 10).", type=int, default=10)
    optional_args.add_argument("-x", "--extensions", dest="extensions", help="Extensões separadas por vírgula (ex: php,html).", default="")
    
    args = parser.parse_args()
    
    # Tratamento da URL
    dominio_alvo = args.dominio
    if not (dominio_alvo.startswith('http://') or dominio_alvo.startswith('https://')):
        dominio_alvo = 'http://' + dominio_alvo
    base_url = dominio_alvo.rstrip('/')
    
    # Validação da wordlist
    if not os.path.exists(args.wordlist):
        print(f"{Cores.RED}[-] Erro: Wordlist não encontrada.{Cores.NC}")
        sys.exit(1)

    # Preparação das extensões
    ext_list = []
    if args.extensions:
        ext_list = [f".{x.strip().lstrip('.')}" for x in args.extensions.split(',')]

    print(f"{Cores.YELLOW_STRONG}[*] Alvo:{Cores.NC} {base_url}")
    print(f"{Cores.YELLOW_STRONG}[*] Wordlist:{Cores.NC} {args.wordlist}")
    if ext_list:
        print(f"{Cores.YELLOW_STRONG}[*] Extensões:{Cores.NC} {', '.join(ext_list)}")
    print(f"{Cores.YELLOW_STRONG}[*] Threads:{Cores.NC} {args.threads}\n")

    # Populando a fila
    word_queue = Queue()
    try:
        with open(args.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                word = line.strip()
                if not word: continue
                
                # Adiciona o diretório puro
                word_queue.put(word)
                
                # Adiciona variações com extensão, se houver
                for ext in ext_list:
                    word_queue.put(f"{word}{ext}")
    except Exception as e:
        print(f"{Cores.RED}[!] Erro ao ler wordlist: {e}{Cores.NC}")
        sys.exit(1)

    print_lock = threading.Lock()
    threads_list = []

    # Iniciando Threads
    for _ in range(args.threads):
        t = threading.Thread(target=worker, args=(word_queue, base_url, print_lock))
        t.daemon = True
        t.start()
        threads_list.append(t)

    # Loop principal que mantém o script vivo e permite capturar Ctrl+C
    try:
        while not word_queue.empty():
            time.sleep(0.5) # Breve pausa para não consumir 100% da CPU verificando
            # Se todas as threads morreram por algum motivo, sai
            if not any(t.is_alive() for t in threads_list):
                break
        
        # Espera final para garantir que as últimas tarefas terminaram
        word_queue.join()
        print(f"\n{Cores.GREEN}[*] Varredura concluída.{Cores.NC}")

    except KeyboardInterrupt:
        print(f"\n\n{Cores.RED}[!] Encerrando varredura... (Aguarde as threads pararem){Cores.NC}")
        stop_event.set() # Avisa as threads para pararem
        sys.exit(0)

if __name__ == "__main__":
    main()
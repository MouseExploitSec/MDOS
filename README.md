# MDOS

![Screenshot_1](https://github.com/MouseExploitSec/MDOS/blob/main/mdos.png)

> a high-frequency HTTP request sending tool designed for testing and suppression purposes. It can send random HTTP requests (GET, POST, PUT, DELETE) to specified target URLs


## Installation on Linux 

Install Python 3

```bash
sudo apt update
sudo apt install python3 python3-pip
git clone https://github.com/MouseExploitSec/MDOS
cd MDOS
pip install -r requirements.txt
python mdos.py -h
python3 mdos.py https://example.com -t 20 -r 50
```

## Installation on Termux

Install Python 3

```bash
pkg update
pkg install python
git clone https://github.com/MouseExploitSec/MDOS
cd MDOS
pip install -r requirements.txt
python mdos.py -h
python mdos.py https://example.com -t 20 -r 50
```

## List of Features Already Added


---

## [+] All Fitur  & Penjelasan

[+] Multi-target Support
→ Tool ini dapat menyerang beberapa URL target sekaligus.  
→ Contoh: kamu bisa memasukkan 3 URL dan tool akan membagi load ke semua.

[+] Multithreaded Execution 
→ Menggunakan `ThreadPoolExecutor` untuk menjalankan banyak thread paralel.  
→ Semakin banyak thread, semakin besar tekanan ke target.  
→ Parameter: `--threads`

[+] Request Rate Control (RPS)  
→ Atur kecepatan pengiriman request per detik.  
→ Misalnya `--rate 100` akan mencoba mengirim 100 request per detik.  
→ Berguna untuk menghindari rate-limiter atau menyesuaikan kapasitas.

[+] Proxy Support 
→ Dukung proxy `http` dan `socks5`.  
→ Proxy dibaca dari file `proxies.txt`.  
→ Sistem otomatis akan memutar proxy dan menghindari yang gagal.  
→ Parameter: `--proxy`, `--proxy-type socks5`

[+] Custom Headers Support
→ Header tambahan bisa dimasukkan lewat file `custom_headers.txt`.  
→ Contoh penggunaan: tambahkan `Authorization`, `X-API-Key`, dll.  
→ Cocok untuk menyerang endpoint yang membutuhkan header tertentu.

[+] Randomization Engine  
→ Randomisasi untuk membuat setiap request terlihat unik:  
   - `User-Agent` acak dari daftar browser umum  
   - IP spoofing melalui `X-Forwarded-For`  
   - `Referer` acak (misalnya dari Google)  
   - Path acak (`/`, `/login`, `/products`, dll)  
   - Metode HTTP acak: `GET`, `POST`, `PUT`, `DELETE`  
   - Payload acak (berisi username, password, email, timestamp)

[+] Retry Mechanism  
→ Jika sebuah request gagal (timeout atau error), tool akan mencoba ulang hingga `n` kali.  
→ Parameter: `--retries`

[+] SSL Verification Toggle  
→ Verifikasi SSL bisa dinonaktifkan (berguna untuk bypass atau jika target pakai self-signed cert).  
→ Parameter: `--no-ssl`

[+] Dry Run Mode 
→ Simulasikan request tanpa benar-benar mengirim ke target.  
→ Menampilkan metode, URL, dan header yang akan digunakan.  
→ Parameter: `--dry-run`

[+] Timeout Configuration
→ Atur waktu tunggu maksimal untuk tiap request (default: 10 detik).  
→ Parameter: `--timeout`

[+] Limit Request & Duration  
→ Tool bisa berhenti otomatis jika:  
   - Mencapai jumlah request tertentu (`--max-requests`)  
   - Melewati durasi waktu tertentu (`--duration` dalam detik)  
→ Cocok untuk benchmark atau serangan terbatas.

[+] Quiet Mode (Silent)  
→ Menonaktifkan semua output yang tidak penting.  
→ Hanya info penting dan error yang akan ditampilkan.  
→ Parameter: `--quiet`

[+] Output Hasil (Export)  
→ Setelah selesai, tool menyimpan ringkasan hasil:  
   - File `results.json`: format JSON  
   - File `results.csv`: format spreadsheet  
→ Data: total request, success, fail

[+] Logging System
→ Semua aktivitas juga dicatat ke file `http_flood.log`.  
→ Berguna untuk audit, debugging, atau analisis pasca serangan.

---

## Cara Penggunaan
 🔹 Basic

```bash
python mdos.py https://target.com
```

## Contact

[@mousexeploitsec](https://www.instagram.com/mousexeploitsec/)

Project Link: 
https://github.com/MouseExploitSec/MDOS

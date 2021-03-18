try:
    from os import path, system
    import aiohttp
    import logging
    from colorama import Fore, init
    from datetime import datetime, timezone
    import os
    import asyncio
    import time
    from bs4 import BeautifulSoup
    import sys
    import requests
except ImportError:
    print("Modülleri İndirmeye Çalışıyorum! \nLütfen Gerekli Tüm Dosyalar İndirildikten Sonra Deneyin.\n\n")
    input("İndirmeyi Başlatmak İçin 'enter' tuşuna bas... ")
    system("py -m pip install -r gerekenler.txt")
    system("python -m pip install -r gerekenler.txt")
    system("python3 -m pip install -r gerekenler.txt")
    input("\n\nGerekn Modüller İndirildi! programı yeniden başlatın. devam etmek için 'enter' tuşuna bas... ")
    quit()

init()

logging.basicConfig(level=logging.INFO, format='%(message)s')
times = []
global sent_reqs
sent_reqs = 0
default_config = """zamanlama_sistemi:namemc
skin: https://namemc.com/skin (Şeklinde girin!)
skin_modeli:slim (Skinin şeklini belirler) 
change_skin:kapalı
snipe_denemeleri:3
block_denemeleri:3
doğrulama_gecikmesi:800
maximum_hesap:30
auto_link_namemc:kapalı
"""


def custom_info(message):
    logging.info(f"{Fore.WHITE}[{Fore.BLUE}cenk{Fore.WHITE}] {Fore.RESET}{message}")


def print_title():
    title = f"""
     {Fore.MAGENTA}░█████╗░███████╗███╗░░██╗██╗░░██╗
     {Fore.MAGENTA}██╔══██╗██╔════╝████╗░██║██║░██╔╝
     {Fore.MAGENTA}██║░░╚═╝█████╗░░██╔██╗██║█████═╝░
     {Fore.MAGENTA}██║░░██╗██╔══╝░░██║╚████║██╔═██╗░
     {Fore.MAGENTA}╚█████╔╝███████╗██║░╚███║██║░╚██╗
         
   {Fore.YELLOW} cenk#1337 tarafından tasarlandı.
   """
    print(title)


def custom_input(message):
    print(f"{Fore.WHITE}[{Fore.BLUE}cenk{Fore.WHITE}] {Fore.RESET}", end='')
    input_return = input(message)
    return input_return


def check_resp(status):
    if str(status)[0] == str(2):
        return True
    else:
        return False


def resp_error(message):
    print(f"{Fore.WHITE}[{Fore.RED}HATA{Fore.WHITE}] {message}")


async def namemc_timing(target, block_snipe):
    now = datetime.utcnow()
    block_snipe_words = ["snipe", "block"]
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"https://namemc.com/search?q={target}", ssl=False) as page:
                # page = requests.get(namemc_url)
                soup = BeautifulSoup(await page.text(), 'html.parser')
                snipe_time = soup.find("time", {"id": "availability-time"}).attrs["datetime"]
                snipe_time = datetime.strptime(snipe_time, '%Y-%m-%dT%H:%M:%S.000Z')
        except AttributeError:
            status_bar = soup.find(id="status-bar")
            info = status_bar.find_all("div", class_="col-sm-6 my-1")
            status = info[0].text.split("\n")[2]
            if status.lower().rstrip('*') == 'uygun':
                snipe_time = custom_input("Bu İsim Şu Tarihte Alınabilir (month/day/yr, 24hrtime_hour:minute:second) (UTC)\nexample: 03/06/2020 01:06:45\n» ")
                try:
                    snipe_time = datetime.strptime(snipe_time.strip(), "%m/%d/%Y %H:%M:%S")
                except ValueError:
                    resp_error("Yanlış Zaman Formatı")
                    raise ValueError
                wait_time = snipe_time - now
                wait_time = wait_time.total_seconds()
                if wait_time >= 60:
                    custom_info(f" ~{round(wait_time / 60)} Dakika içinde snipeliyorum")
                else:
                    custom_info(f" {wait_time} Saniye içinde snipeliyorum!")
                custom_info(f"{wait_time} Dakika içinde snipeliyorum!")
                return int(snipe_time.replace(tzinfo=timezone.utc).timestamp())
            print(f"Hata.")
            quit()

        wait_time = snipe_time - now
        wait_time = wait_time.total_seconds()
        if wait_time >= 60:
            custom_info(f"~{round(wait_time / 60)} dakika içinde snipeliyorum!")
        elif wait_time >= 3600:
            custom_info(f"~{round(wait_time / 3600)} dakika içinde snipeliyorum!")
        else:
            custom_info(f"{wait_time} saniye içinde snipeliyorum!")
        return int(snipe_time.replace(tzinfo=timezone.utc).timestamp())


async def time_snipe(target, block_snipe):
    try:
        return await namemc_timing(target, block_snipe)
    except Exception:
        print(f"{Fore.WHITE}[{Fore.RED}HATA{Fore.WHITE}] Başaramadık abi...")
        time.sleep(3)
        quit()


class Config:
    def __init__(self):
        self.options = []
        if not os.path.exists("ayarlar.txt"):
            with open("ayarlar.txt", "w") as f:
                f.write(default_config)
        with open("ayarlar.txt", "r") as f:
            unconverted_lines = f.readlines()
            self.lines = list()
            for line in unconverted_lines:
                self.lines.append(line.strip())
            self.timing = self.find_parameter("zamanlama_sistemi")
            self.block_reqs = int(self.find_parameter("block_denemeleri"))
            self.snipe_reqs = int(self.find_parameter("snipe_denemeleri"))
            self.skin = self.find_parameter("skin")
            self.max_accs = int(self.find_parameter("maximum_hesap"))
            if "namemc.com/skin" in self.skin:
                self.skin = f"https://namemc.com/texture/{self.skin.split('/')[-1]}.png"
            self.change_skin = self.find_bool("change_skin", False)
            self.auth_delay = int(self.find_parameter("doğrulama_gecikmesi"))
            self.skin_model = self.find_parameter("skin_modeli")

    def find_parameter(self, parameter):
        for line in self.lines:
            line = line.split(":")
            if line[0].lower() == parameter:
                line.pop(0)
                line = ":".join(line)
                self.options.append(line)
                return line

    def find_bool(self, parameter, default):
        parameter = self.find_parameter(parameter)
        parameter = {"açık": False, "kapalı": True}[parameter]
        return parameter

    def find_all(self, parameter):
        options = []
        for line in self.lines:
            line = line.split(":")
            if line[0] == parameter:
                line.pop(0)
                options.append(":".join(line))
                self.options.append(options)
        return options


class Account:
    def __init__(self, email, password, questions=[]):
        self.email = email
        self.password = password
        self.questions = questions
        self.got_name = False
        self.user_agent = ""
        self.failed_auth = False
        self.authenticate_json = {"username": self.email, "password": self.password}
        self.headers = {""}

    async def authenticate(self, session, sleep_time, block_snipe):
        await asyncio.sleep(sleep_time)
        debug_mode = False
        async with session.post("https://authserver.mojang.com/authenticate", json=self.authenticate_json, headers=self.headers) as r:
            if check_resp(r.status):
                resp_json = await r.json()
                try:
                    self.uuid = resp_json["selectedProfile"]["id"]
                except KeyError:
                    if debug_mode:
                        print(resp_json)
                    else:
                        if block_snipe == 2:
                            custom_info(f"{self.email} Premium bir hesap değil snipeleyemiyorum. {Fore.RED} Bu Başarısız Olacak.{Fore.RESET}")
                self.auth = {"Authorization": "Bearer: " + resp_json["accessToken"]}
                self.access_token = resp_json["accessToken"]
            else:
                resp_error(f"Yanlış kimlik bilgisi| {self.email}")
                self.failed_auth = True
                return
        async with session.get("https://api.mojang.com/user/security/challenges", headers=self.auth) as r:
            answers = []
            if check_resp(r.status):
                resp_json = await r.json()
                if resp_json == []:
                    async with session.get("https://api.minecraftservices.com/minecraft/profile/namechange", headers={"Authorization": "Bearer " + self.access_token}) as ncE:
                        ncjson = await ncE.json()
                        try:
                            if ncjson['nameChangeAllowed'] is False:
                                logging.info(f"{Fore.WHITE}[{Fore.RED}HATA{Fore.WHITE}] {self.email} İsim değiştirmek için erken!")
                                self.failed_auth = True
                            else:
                                logging.info(f"{Fore.WHITE}[{Fore.GREEN}BAŞARILI{Fore.WHITE}] {self.email} Hesabına başarıyla girildi!")
                        except Exception:
                            logging.info(f"{Fore.WHITE}[{Fore.GREEN}BAŞARILI{Fore.WHITE}] {self.email} Hesabına başarıyla girildi!")
                else:
                    try:
                        for x in range(3):
                            answers.append({"id": resp_json[x]["answer"]["id"], "answer": self.questions[x]})
                    except IndexError:
                        logging.info(f"{Fore.WHITE}[{Fore.RED}HATA{Fore.WHITE}]{Fore.RESET} {self.email} Güvenlik soruları var ve bunu bize belirtmedin!")
                        self.failed_auth = True
                        return
                    async with session.post("https://api.mojang.com/user/security/location", json=answers, headers=self.auth) as r:
                        if check_resp(r.status):
                            logging.info(f"{Fore.WHITE}[{Fore.GREEN}BAŞARILI{Fore.WHITE}]{Fore.GREEN} {self.email} Hesabına başarıyla girildi!{Fore.RESET}")
                        else:
                            resp_error(f" {self.email} Hesabı için güvenlik soruları yanlış!")
                            self.failed_auth = True
            else:
                logging.info(f"{Fore.WHITE}[{Fore.RED}HATA{Fore.WHITE}]{Fore.RESET} {self.email} birşeyler yanlış gidiyor... {self.email}! | {r.status}")
                self.failed_auth = True

    async def snipe_req(self, session, target_username):
        await asyncio.sleep(0)
        try:
            async with session.put(f"https://api.minecraftservices.com/minecraft/profile/name/{target_username}", headers={"Authorization": "Bearer " + self.access_token, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0", "Content-Type": "application/json"}) as response:
                now = datetime.now()
                global sent_reqs
                sent_reqs += 1
                await response.read()
                if response.status == 204 or response.status == 200:
                    logging.info(f"{Fore.WHITE}[{Fore.GREEN}BAŞARILI{Fore.WHITE}] | {Fore.CYAN}{target_username}{Fore.WHITE} {self.email}'da snipeledim | {Fore.GREEN}{response.status}{Fore.WHITE} @ {Fore.CYAN}{now}{Fore.RESET}")
                    self.got_name = True
                    if config.change_skin:
                        await self.authenticate(session, 1, 1)
                    asyncio.get_event_loop().stop()
                else:
                    logging.info(f"{Fore.WHITE}[{Fore.RED}HATA{Fore.WHITE}] {Fore.RED} {response.status} {Fore.WHITE}@{Fore.CYAN} {now}{Fore.RESET}")
        except AttributeError as e:
            print(f'{Fore.WHITE}[{Fore.RED}HATA{Fore.WHITE}]{Fore.RESET} {self.email} | Başaramadık abi... | {e}')

    def webhook_skin_write_file(self, block_snipe):
        time.sleep(1)
        with requests.session() as session:
            with open("basarili.txt", "a") as f:
                f.write(f"{self.email}:{self.password} - {target_username}\n")
            if config.change_skin:
                payload = {"variant": str(config.skin_model)}
                files = [('file', open(str(config.skin), 'rb'))]
                with session.post(f"https://api.minecraftservices.com/minecraft/profile/skins", headers=self.auth, data=payload, files=files) as r:
                    if r.status_code == 204 or r.status_code == 200:
                        logging.info(f"{Fore.WHITE}[{Fore.GREEN}BAŞARILI{Fore.WHITE}]{Fore.RESET} {self.email} | Hesabının skini otomatik olarak değiştirildi!")
                    else:
                        logging.info(f"{Fore.WHITE}[{Fore.RED}HATA{Fore.WHITE}]{Fore.RESET} {self.email} | Hesabını skinini değiştirirken olaağanüstü bir sorun oluştu.. | {str(r.status_code)}")
                        logging.info(r.json())
            else:
                custom_info(f" {self.email} | Hesabının skini değiştirlmiyor..")

def gather_info():
    block_snipe = 0
    target_username = custom_input(f"Hangi ismi snipelemek istersin? {['', 'block'][block_snipe]}: ")
    try:
        delay = int(custom_input("Özel MS değeri? : "))
    except ValueError:
        print('Bu bir sayı değil!')
    return block_snipe, target_username, delay


def load_accounts_file():
    accounts = []
    if not path.exists("hesaplar.txt"):
        print(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}]{Fore.RESET} hesaplar.txt bulunamadı.. | bir tane oluşturuyorum")
        open('hesaplar.txt', 'w+')
        input("Hesapları yenilemek için 'enter' tuşuna bas. ")
        load_accounts_file()
    else:
        accounts = open('hesaplar.txt').readlines()
        if len(accounts) == 0:
            print(f"hesaplar accounts.txt dosyasında bulunamadı lütfen bu şekilde ekleyin (email:şifre) veya (email:şifre:soru1:soru2:soru3)")
            input("Hesapları yenilemek için herhangi bir tuşa bas.")
            load_accounts_file()
        if len(accounts) > config.max_accs:
            print(f"{Fore.WHITE}[{Fore.YELLOW}HATA{Fore.WHITE}]{Fore.RESET} limitten fazla hesap ekledin | {len(accounts) - config.max_accs} hesaplarını siliyorum!")
            accounts = accounts[0:30]
    return accounts


def load_accounts():
    accounts = []
    for acc in load_accounts_file():
        acc = acc.rstrip().split(":")
        if acc == ['']:
            continue
        try:
            accounts.append(Account(acc[0], acc[1], [acc[2], acc[3], acc[4]]))
        except IndexError:
            accounts.append(Account(acc[0], acc[1]))
    return accounts


class session:
    block_snipe = ["Snipe", "block"]

    def __init__(self, target_username, accounts, block_snipe, snipe_delay):
        self.target_username = target_username
        self.accounts = accounts
        self.block_snipe = block_snipe
        self.snipe_delay = snipe_delay
        loop = asyncio.get_event_loop()
        self.drop_time = loop.run_until_complete(time_snipe(self.target_username, self.block_snipe))
        try:
            self.setup_time = self.drop_time - 55
        except Exception:
            resp_error(f"Bu ismi snipeleyemeyiz. {target_username}")
            time.sleep(2)
            quit()
        self.setup = False
        self.ran = False
        self.drop_time = self.drop_time - snipe_delay / 1000

    def run(self):
        loop = asyncio.get_event_loop()
        while True:
            now = time.time()
            if now >= self.drop_time and not self.ran:
                try:
                    start = time.time()
                    loop.run_until_complete(self.send_requests())
                except RuntimeError:
                    pass
                end = time.time()
                elapsed_time = end - start
                for acc in self.accounts:
                    if acc.got_name:
                        time.sleep(2)
                        acc.webhook_skin_write_file(self.block_snipe)
                rq_sec = sent_reqs / elapsed_time
                times.append(rq_sec)
                logging.info(f"{Fore.GREEN}{str(sum(times))[0:13]}{Fore.CYAN} saniye {Fore.WHITE}|{Fore.CYAN} {Fore.WHITE}{str(elapsed_time)[0:8]}{Fore.CYAN} saniye{Fore.RESET} sürdü | {sent_reqs} deneme")
                try:
                    if len(sys.argv) < 3:
                        custom_input("Çıkmak için 'enter' tuşuna bas: ")
                    return
                except Exception:
                    return
            elif now >= self.setup_time and not self.setup:
                loop.run_until_complete(self.run_auth())
                for acc in accounts:
                    if acc.failed_auth:
                        logging.info(f"{Fore.WHITE}[{Fore.RED}HATA{Fore.WHITE}] Hesap Siliniyor: {acc.email} | auth failed")
                        accounts.remove(acc)
                if len(accounts) == 0:
                    logging.info(f"{Fore.WHITE}[{Fore.RED}HATA{Fore.WHITE}] Hiç Hesabın yok! | Programı Kapatıyorum...")
                    quit()
                custom_info("Kurulum başarılı!")
                self.setup = True
            time.sleep(.00001)

    async def webhook_skin_file(self, acc):
        await acc.webhook_skin_write_file()

    async def send_requests(self):
        async with aiohttp.ClientSession() as session:
            if self.block_snipe == 0:
                self.coros = [
                    acc.snipe_req(session, self.target_username) for acc in self.accounts for _ in range(config.snipe_reqs)
                ]
            elif self.block_snipe == 1:
                self.coros = [
                    acc.block_req(session, self.target_username) for acc in self.accounts for _ in range(config.block_reqs)
                ]
            await asyncio.wait(self.coros)

    async def run_auth(self):
        async with aiohttp.ClientSession() as session:
            coros = [
                acc.authenticate(session, self.accounts.index(acc) * (config.auth_delay / 1000), self.block_snipe) for acc in self.accounts
            ]
            await asyncio.wait(coros)


if __name__ == '__main__':
    print_title()
    config = Config()
    accounts = load_accounts()
    try:
        target_username = sys.argv[1]
        block_snipe = sys.argv[2]
        if str(block_snipe).lower() == "snipe" or str(block_snipe) == "0":
            block_snipe = 0
        if str(block_snipe).lower() == "block" or str(block_snipe) == "1":
            block_snipe = 1
        try:
            snipe_delay = int(sys.argv[3])
        except IndexError:
            if block_snipe == 0:
                snipe_delay = 900
            else:
                snipe_delay = 200
    except IndexError:
        block_snipe, target_username, snipe_delay = gather_info()
    session = session(target_username, accounts, block_snipe, snipe_delay)
    session.run()

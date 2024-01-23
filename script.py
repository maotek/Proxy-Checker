from multiprocessing.dummy import Pool as ThreadPool
from os import path, mkdir, system, name
#from threading import Thread, Lock
from time import sleep, strftime,  time

from colorama import Fore, init
from console.utils import set_title
from easygui import fileopenbox
from requests import Session, exceptions
#from yaml import safe_load
from threading import Thread, Lock


class main():
	def __init__(self):
		self.checked = 0
		#self.good = 0
		self.bad = 0
		#self.remaining = 0
		#self.totalproxy = 0
		self.on = True
		self.timeout = 0
		self.threads = 0
		self.transparent = 0
		self.live = 0
		#self.error = 0
		self.makefolder()
		self.checkproxytype()
		self.proxyload()
		self.main_checker()


	def proxyload(self):
		print(f'{color}select your txt file containing your {self.proxytype} proxies (window will pop-up): \n')
		sleep(0.5)
		while True:	
			try:
				with open(fileopenbox(title="Load Proxies List", default="*.txt"), 'r', encoding="utf8",errors='ignore') as g:
					loader = g.read().split('\n')

				self.proxylist = [x.strip() for x in loader if ":" in x and x != '']

				if len(self.proxylist) == 0:
					print(f'{color2}Please select good proxy list')
					continue
				
				break
			except:
				print(f'{color2}Error during proxyload.')
				print(f'{color2}Press enter to exit.')
				input()
				exit()


	def makefolder(self):
		subfolder = str(strftime('[%d-%m-%Y_%H-%M-%S]'))
		self.folder = f'results/{subfolder}'
		if not path.exists('results'):
			mkdir('results')
		if not path.exists(self.folder):
			mkdir(self.folder)

	def write(self,proxy):
		#lock.acquire() #open lock (start script)

		open(f'{self.folder}/{proxy[1]}-{self.proxytype.upper()}.txt', 'a', encoding='u8').write(f'{proxy[0]}\n')
		#print(f'checking: {proxy[0]} - {proxy[1]}')

		#lock.release() #stop script


	def proxycheck(self,proxy):
		proxyformat = {}
		if self.proxytype in ['http','https']:
			proxyformat = {'http': f'http://{proxy}','https': f'https://{proxy}'}
		elif self.proxytype == 'socks4' or 'socks5':
			proxyformat_ = f'{self.proxytype}://{proxy}'
			proxyformat = {'http': proxyformat_,'https':proxyformat_}
		try:    
			req = session.get(url='https://azenv.net', proxies=proxyformat, timeout=self.timeout).text
			self.checked += 1
			if req.__contains__(myip):
				self.trasparent += 1
				self.write([proxy, 'Transparent'])

			else:
				self.live += 1
				self.write([proxy, 'Live'])
		    #return
		except exceptions.RequestException:
		    self.bad += 1
		    self.checked += 1
		    self.write([proxy, 'Bad'])
		    #return
		#except:
			#self.error += 1
			#self.checked += 1
			#return
		    #return

	def cpmcounter(self):
		while self.on:
			if self.checked >= 1:
				now = self.checked
				sleep(4)
				self.cpm = (self.checked - now) * 15

	def titel(self):
		while self.on:
			proxies = len(self.proxylist)
			set_title(
			f'MAOTEK PROXY-CHECKER'
			f'{"" if self.live == 0 else f" | Live: {self.live}"}'
			f'{"" if self.bad == 0 else f" | Dead: {self.bad}"}'
			f'{"" if self.transparent == 0 else f" | Transparent: {self.transparent}"}'
			f' | Left: {proxies - self.checked}/{proxies}'
			#f' | CPM: {proxies/(self.total_time / 60)}'
			f' | {round(abs(self.starttime - time()),2)} Elapsed')


	def checkproxytype(self):
		self.threads = 0
		while self.threads == 0:
			try:
				self.threads = int(input('Choose thread amount(Higher = Faster = more CPU intensive): '))
			except:
				self.threads = int(input('Choose thread amount (must be 1 or more): '))

		self.timeout = (int(input('Choose proxy timeout(seconds): ')))

		self.proxytype = ''
		while True:
			if self.proxytype not in ['http','https','socks4','socks5']:
				self.proxytype = str(input('Enter Proxy Type: (HTTP,HTTPS,SOCKS4,SOCKS5): ').lower())
				continue
			else:
				break

	def main_checker(self):
		clear()
		print('Checking...')
		pool = ThreadPool(processes=self.threads)

		self.starttime = time()
		Thread(target=self.titel).start()

		start_time = time()
		pool.imap_unordered(func=self.proxycheck,iterable=self.proxylist)
		pool.close()
		pool.join()
		
		self.on = False
		self.total_time = (time() - start_time)
		self.tot = len(self.proxylist)
		clear()
		print(logo)
		print(f'{color2}RESULTS\n'
			f'{color}Total time = {self.total_time}\n'
			f'Checks per second = {self.tot / self.total_time}\n'
			f'Checks per minute = {self.tot / (self.total_time/60)}\n'
			f'Total proxies checked = {self.tot}')

		print(f"{color2}\nfinished, results are exported to the folder 'results' in the same directory\n")
		input(f'{color}press enter to exit: ')
		exit()


if __name__ == '__main__':

	#lock = Lock()
	init()
	set_title('MAOTEK PROXY-CHECKER V1.0')
	clear = lambda: system('cls' if name == 'nt' else 'clear')
	color = Fore.LIGHTCYAN_EX
	color2 = Fore.LIGHTRED_EX
	print(f'{color}\n'\
		f'{color}MAOTEK PROXY-CHECKER\n')
	logo = f"""{color}
                 ___ ___   ____   ___   ______    ___  __  _                    
                |   |   | /    | /   \\ |      |  /  _]|  |/ ]                   
                | _   _ ||  o  ||     ||      | /  [_ |  ' /                    
                |  \\_/  ||     ||  O  ||_|  |_||    _]|    \\                    
                |   |   ||  _  ||     |  |  |  |   [_ |     |                   
                |   |   ||  |  ||     |  |  |  |     ||  .  |                   
                |___|___||__|__| \\___/   |__|  |_____||__|\\_|                   
 ____  ____   ___   __ __  __ __    __  __ __    ___    __  __  _    ___  ____  
|    \\|    \\ /   \\ |  |  ||  |  |  /  ]|  |  |  /  _]  /  ]|  |/ ]  /  _]|    \\ 
|  o  )  D  )     ||  |  ||  |  | /  / |  |  | /  [_  /  / |  ' /  /  [_ |  D  )
|   _/|    /|  O  ||_   _||  ~  |/  /  |  _  ||    _]/  /  |    \\ |    _]|    / 
|  |  |    \\|     ||     ||___, /   \\_ |  |  ||   [_/   \\_ |     ||   [_ |    \\ 
|  |  |  .  \\     ||  |  ||     \\     ||  |  ||     \\     ||  .  ||     ||  .  \\
|__|  |__|\\_|\\___/ |__|__||____/ \\____||__|__||_____|\\____||__|\\_||_____||__|\\_|
                                                                                



		EDUCATIONAL PURPOSES ONLY

		"""
	print(logo)

	#lock = Lock()

	session = Session()
	myip = str(session.get('http://api.ipify.org').text)
	main()
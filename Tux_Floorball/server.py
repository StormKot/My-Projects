from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json, time, socket

state = {"p": {}, "host": None, "t1": "OMSK TIGERS", "t2": "RED BEARS", "c1": "#ffd000", "c2": "#ff5252", "md": "5v5", "dur": 120, "diff": 1, "chaos": 1, "chat": [], "acts": [], "world": None}

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(("8.8.8.8", 80)); ip = s.getsockname(); s.close(); return ip
    except Exception: return "127.0.0.1"

class H(SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_POST(self):
        d = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))) or b'{}')
        now = time.time()
        state['p'] = {k: v for k, v in state['p'].items() if now - v.get('ts', 0) < 12.0}
        state['chat'] = [m for m in state['chat'] if now - m['ts'] < 4.0]
        if state['host'] not in state['p']: state['host'] = next(iter(state['p']), None)
        if self.path == '/sync':
            pid, me = d.get('id'), d.get('me')
            if d.get('msg') and me: state['chat'].append({"id": pid, "num": me.get('num', 10), "txt": str(d['msg'])[:28], "ts": now})
            if pid and me:
                if not state['host']: state['host'] = pid
                tm = me.get('tm', 0)
                if any(k != pid and v.get('tm') == tm and v.get('cap') for k, v in state['p'].items()): me['cap'] = 0
                me['ts'] = now; state['p'][pid] = me
                if me.get('act'): state['acts'].append({"id": pid, "tm": tm, "act": me['act']})
                if me.get('cap'):
                    if me.get('tname'): state['t2' if tm else 't1'] = me['tname']
                    if me.get('tcol'): state['c2' if tm else 'c1'] = me['tcol']
                    if d.get('cfg'): state.update(d['cfg'])
                resp = dict(state)
                if pid == state['host']:
                    if d.get('world') is not None: state['world'] = d['world']
                    resp['acts'] = list(state['acts']); state['acts'].clear()
                else: resp['acts'] = []
                self.send_response(200); self.send_header('Content-Type', 'application/json'); self.end_headers(); self.wfile.write(json.dumps(resp).encode())

print(f"\n=== TUX FLOORBALL ЗАПУЩЕН ===\nЛокально: http://localhost:8080\nПо LAN:   http://{get_ip()}:8080\n")
ThreadingHTTPServer(('0.0.0.0', 8080), H).serve_forever()

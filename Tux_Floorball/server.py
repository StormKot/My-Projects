from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json, time, socket

state = {
    "p": {}, "host": None, "t1": "OMSK TIGERS", "t2": "RED BEARS",
    "md": "5v5", "dur": 120, "diff": 1,
    "world": {"bx": 450, "by": 225, "sp": 0, "sb": 0, "tl": 120, "own": None, "pwr": 0, "gt": 0, "gtxt": "", "over": 0}
}

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class H(SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_POST(self):
        l = int(self.headers.get('Content-Length', 0))
        d = json.loads(self.rfile.read(l) or b'{}')
        now = time.time()
        state['p'] = {k: v for k, v in state['p'].items() if now - v.get('ts', 0) < 3.5}
        if state['host'] not in state['p']:
            state['host'] = next(iter(state['p']), None)
        if self.path == '/sync':
            pid = d.get('id')
            me = d.get('me')
            if pid and me:
                if not state['host']:
                    state['host'] = pid
                tm = me.get('tm', 0)
                if any(k != pid and v.get('tm') == tm and v.get('cap') for k, v in state['p'].items()):
                    me['cap'] = 0
                me['ts'] = now
                state['p'][pid] = me
                if me.get('cap'):
                    if me.get('tname'):
                        state['t2' if tm else 't1'] = me['tname']
                    if d.get('cfg'):
                        state.update(d['cfg'])
                if pid == state['host'] and d.get('world'):
                    state['world'] = d['world']
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(state).encode())

print(f"\n=== TUX FLOORBALL MULTIPLAYER СЕРВЕР ===")
print(f"Твой адрес: http://localhost:8080")
print(f"Для друзей по Wi-Fi: http://{get_ip()}:8080\n")
ThreadingHTTPServer(('0.0.0.0', 8080), H).serve_forever()

const http = require("http"), fs = require("fs"), WS = require("ws");
const MAPS = {
  arena: {
    ice: [
      {x:180,y:215,w:1240,h:90},
      {x:180,y:695,w:1240,h:90},
      {x:460,y:340,w:680,h:320}
    ],
    slides: [{x:180,y:355,w:250,h:90,dx:1,dy:0}],
    blocks: [{x:430,y:580,lvl:2},{x:1170,y:420,lvl:2}]
  },
  park: {
    ice: [{x:720,y:110,w:740,h:130},{x:1330,y:110,w:130,h:780},{x:140,y:760,w:1320,h:130},{x:140,y:240,w:130,h:650}],
    slides: [{x:140,y:110,w:590,h:130,dx:1,dy:0}],
    blocks: [{x:740,y:450,lvl:2},{x:860,y:550,lvl:2}]
  },
  king: {
    ice: [{x:420,y:200,w:760,h:600}],
    slides: [{x:500,y:440,w:230,h:120,dx:1,dy:0},{x:870,y:440,w:230,h:120,dx:-1,dy:0}],
    blocks: [{x:560,y:310,lvl:1},{x:1040,y:310,lvl:1},{x:560,y:690,lvl:1},{x:1040,y:690,lvl:1}]
  },
  circle: {
    ice: [{x:250,y:120,w:1100,h:760,oval:1}],
    slides: [],
    blocks: [{x:520,y:500,lvl:2},{x:1080,y:500,lvl:2}]
  }
};
const srv = http.createServer((q, s) => {
  s.writeHead(200, {"Content-Type": "text/html; charset=utf-8"});
  s.end(fs.readFileSync("index.html"));
});
const wss = new WS.Server({server: srv}), rooms = {};
wss.on("connection", ws => {
  let rc = null, id = "p" + Math.random().toString(36).slice(2, 7);
  ws.on("message", r => {
    let m; try { m = JSON.parse(r); } catch { return; }
    if (m.t === "join"){
      rc = (m.code || "OMSK").toUpperCase().slice(0, 6);
      if (!rooms[rc]){
        const mp = MAPS[m.map] ? m.map : "arena";
        rooms[rc] = {host: id, map: mp, c: {}, b: JSON.parse(JSON.stringify(MAPS[mp].blocks)), sl: MAPS[mp].slides, ic: MAPS[mp].ice};
      }
      const rm = rooms[rc];
      rm.c[id] = {ws, s: {id, nick: m.nick || "Tux", x: 300+Math.random()*80, y: 260+Math.random()*60, z: 0, a: 0, hat: m.hat, scarf: m.scarf, sled: m.sled, onSled: 0, slip: 0, score: 0}};
      ws.send(JSON.stringify({t: "init", id, code: rc, isHost: rm.host === id, map: rm.map, blocks: rm.b, slides: rm.sl, ice: rm.ic}));
    }
    if (!rc || !rooms[rc]) return;
    const rm = rooms[rc];
    if (m.t === "setMap" && rm.host === id && MAPS[m.map]){
      rm.map = m.map; rm.b = JSON.parse(JSON.stringify(MAPS[m.map].blocks)); rm.sl = MAPS[m.map].slides; rm.ic = MAPS[m.map].ice;
      const pkt = JSON.stringify({t: "mapChanged", map: rm.map, blocks: rm.b, slides: rm.sl, ice: rm.ic});
      for (const k in rm.c) if (rm.c[k].ws.readyState === 1) rm.c[k].ws.send(pkt);
    }
    if (m.t === "me" && rm.c[id]) Object.assign(rm.c[id].s, m.s);
    if (m.t === "ball" || m.t === "push" || m.t === "blk"){
      if (m.t === "blk"){
        const ex = rm.b.find(k => Math.hypot(k.x - m.x, k.y - m.y) < 26);
        if (ex && ex.lvl < 2) ex.lvl = 2;
        else if (!ex){ rm.b.push({x: m.x, y: m.y, lvl: 1}); if (rm.b.length > 48) rm.b.shift(); }
      }
      for (const k in rm.c) if (k !== id && rm.c[k].ws.readyState === 1) rm.c[k].ws.send(JSON.stringify({...m, from: id, blocks: rm.b}));
    }
  });
  ws.on("close", () => {
    if (rc && rooms[rc]){
      delete rooms[rc].c[id]; const left = Object.keys(rooms[rc].c);
      if (!left.length) delete rooms[rc];
      else if (rooms[rc].host === id){
        rooms[rc].host = left;
        if (rooms[rc].c[left].ws.readyState === 1) rooms[rc].c[left].ws.send(JSON.stringify({t: "host"}));
      }
    }
  });
});
setInterval(() => {
  for (const rc in rooms){
    const rm = rooms[rc], pl = {};
    for (const k in rm.c) pl[k] = rm.c[k].s;
    const pkt = JSON.stringify({t: "world", pl, bk: rm.b});
    for (const k in rm.c) if (rm.c[k].ws.readyState === 1) rm.c[k].ws.send(pkt);
  }
}, 33);
srv.listen(8080, "0.0.0.0", () => console.log("SERVER OK 8080"));

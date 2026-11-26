import os, re, shutil, zipfile

s = open("index.html").read()

# 1. Вычищаем дубликат обработчика кнопки #re (там остались две лишние закрывающие скобки)
s = re.sub(r"document\.getElementById\('re'\)\._old=\(\)=>\{[\s\S]*?\};", "", s)

# 2. Заменяем участок от document.getElementById('go').onclick до function startPenalty() на чистый код без лишних скобок
i1 = s.index("document.getElementById('go').onclick=")
i2 = s.index("function startPenalty(){")

clean_mid = """document.getElementById('go').onclick=async()=>{
  gameMode=document.getElementById('md').value;myRole=document.getElementById('role').value;myTeam=+document.getElementById('tmSel').value;botMult=+document.getElementById('diff').value;chaosOn=document.getElementById('chaosCb').checked?1:0;myNum=Math.max(1,Math.min(99,+document.getElementById('pNum').value||10));
  perMax=+document.getElementById('pers').value;perDur=+document.getElementById('dur').value;perCur=1;otMode=0;bannerOnly=0;infSo=(gameMode==='inf_so'?1:0);
  const myCol=document.getElementById('tCol').value,nm=document.getElementById('tName').value.trim()||'CLUB';
  if(myTeam===0){col1=myCol;col2='#ff5252';document.getElementById('n1').textContent=nm;document.getElementById('n2').textContent='RED BEARS';}else{col1='#ffd000';col2=myCol;document.getElementById('n1').textContent='TUX TIGERS';document.getElementById('n2').textContent=nm;}
  tP.forEach(e=>{e.c=col1;e.pts=0;e.st=1;});tB.forEach(e=>{e.c=col2;e.pts=0;e.st=1;});document.getElementById('n1').style.color=col1;document.getElementById('n2').style.color=col2;
  document.getElementById('menu').style.display='none';hideMenuBanner();sP=sB=shotsP=shotsB=savesP=savesB=possP=possB=soMode=0;soLog=[];evName='';evT=0;evCd=12;tLeft=perDur;document.getElementById('sp').textContent=0;document.getElementById('sb').textContent=0;over=0;
  if(infSo){soMode=1;soTurn=0;soLog=[];startPenalty();}else rst();
  sfx(440,.1);try{ysdk?.features?.GameplayAPI?.start();}catch(e){}
  try{await document.documentElement.requestFullscreen();await screen.orientation.lock('landscape');}catch(e){}
};
document.getElementById('re').onclick=()=>{const gm=()=>{if(ac)ac.resume();over=1;soMode=0;otMode=0;bannerOnly=0;infSo=0;document.getElementById('end').style.display='none';document.getElementById('menu').style.display='flex';showMenuBanner();};if(ysdk?.adv){try{ysdk.adv.showFullscreenAdv({callbacks:{onOpen:()=>{if(ac)ac.suspend();},onClose:gm,onError:gm}});}catch(e){gm();}}else gm();};
"""

s = s[:i1] + clean_mid + s[i2:]

# 3. Проверяем идеальный баланс скобок и наличие всех 3 типов рекламы Яндекс Игр
js = s.split("<script>")[1].split("</script>")[0]
assert js.count("{") == js.count("}"), f"Скобки всё ещё не равны: {{={js.count('{')} }}={js.count('}')}"
for ad_fn in ["showBannerAdv", "hideBannerAdv", "showRewardedVideo", "showFullscreenAdv", "LoadingAPI"]:
    assert ad_fn in s, f"Не найдена функция SDK: {ad_fn}"

open("index.html", "w").write(s)

# 4. Пересобираем архив tux_floorball_yandex.zip и обновляем копии в ~/storage/shared/
with zipfile.ZipFile("tux_floorball_yandex.zip", "w", zipfile.ZIP_DEFLATED) as z:
    z.write("index.html")
    if os.path.exists("logo.png"):
        z.write("logo.png")

sd = os.path.expanduser("~/storage/shared")
if os.path.isdir(sd):
    shutil.copy2("index.html", os.path.join(sd, "index.html"))
    shutil.copy2("tux_floorball_yandex.zip", os.path.join(sd, "tux_floorball_yandex.zip"))

print("ИДЕАЛЬНО: Скобки сошлись 1-в-1, все 3 вида рекламы Яндекс Игр (Banner, Rewarded, Fullscreen) проверены!")

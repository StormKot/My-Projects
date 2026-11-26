s = open("index.html").read()
a = s.find("const fr=")
b = s.rfind("const fr=")
if a != -1 and b > a:
    s = s[:a] + s[b:]
open("index.html", "w").write(s)
open("t.js", "w").write(s.split("<script>").split("</script>"))

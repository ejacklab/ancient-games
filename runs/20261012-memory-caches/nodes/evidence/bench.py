import os, sys, time, random, sqlite3, re, subprocess, shutil, glob
random.seed(1)
words = open('/usr/share/dict/words').read().split() if os.path.exists('/usr/share/dict/words') else [f"w{i}" for i in range(5000)]
kinds=['decision','fact','lesson','runbook','observation','hypothesis']
status=['active','active','active','superseded','retired']
def make(n, root):
    shutil.rmtree(root, ignore_errors=True); os.makedirs(root)
    for i in range(n):
        k=random.choice(kinds); st=random.choice(status)
        cov=[f"src/mod{random.randrange(60)}/f{random.randrange(20)}.py" for _ in range(random.randint(1,3))]
        body=' '.join(random.choice(words) for _ in range(random.randint(60,140)))
        sup = f"D-{random.randrange(n):04d}" if st=='superseded' else ''
        open(f"{root}/{k[0].upper()}-{i:05d}.md",'w').write(
f"---\nid: {k[0].upper()}-{i:05d}\nkind: {k}\nstatus: {st}\ncovers: [{', '.join(cov)}]\nsuperseded_by: {sup}\n---\n{body}\n\n**Why:** {' '.join(random.choice(words) for _ in range(30))}\n**How to apply:** {' '.join(random.choice(words) for _ in range(30))}\n")
def fm(path):
    t=open(path).read().split('---\n',2)[1]
    d={}
    for l in t.splitlines():
        k,_,v=l.partition(': '); d[k]=v
    return d
def build(root, db):
    if os.path.exists(db): os.remove(db)
    c=sqlite3.connect(db)
    c.execute("create virtual table e using fts5(id unindexed, kind unindexed, status unindexed, covers unindexed, body)")
    c.execute("create table meta(id text primary key, kind, status, covers, superseded_by, mtime)")
    for p in glob.glob(root+'/*.md'):
        d=fm(p); body=open(p).read().split('---\n',2)[2]
        c.execute("insert into e values(?,?,?,?,?)",(d['id'],d['kind'],d['status'],d['covers'],body))
        c.execute("insert into meta values(?,?,?,?,?,?)",(d['id'],d['kind'],d['status'],d['covers'],d['superseded_by'],os.stat(p).st_mtime))
    c.commit(); c.close()
for n in [100,1000,10000,50000]:
    root=f"c{n}"; make(n,root)
    sz=sum(os.path.getsize(p) for p in glob.glob(root+'/*.md'))
    t=time.time(); build(root,f"{n}.db"); tb=time.time()-t
    # structured query: active decisions covering path X
    X='src/mod7/f3.py'
    t=time.time(); r1=[p for p in glob.glob(root+'/*.md') if (lambda d: d['kind']=='decision' and d['status']=='active' and X in d['covers'])(fm(p))]; tp=time.time()-t
    t=time.time(); g=subprocess.run(f"grep -l 'status: active' {root}/*.md 2>/dev/null | xargs grep -l 'kind: decision' | xargs grep -l '{X}' | wc -l",shell=True,capture_output=True,text=True); tg=time.time()-t
    c=sqlite3.connect(f"{n}.db")
    t=time.time(); r2=c.execute("select id from meta where kind='decision' and status='active' and covers like ?",(f"%{X}%",)).fetchall(); ts=time.time()-t
    w=random.choice(words)
    t=time.time(); subprocess.run(f"grep -rli '{w}' {root} | wc -l",shell=True,capture_output=True); tw=time.time()-t
    t=time.time(); r3=c.execute("select id from e where e match ? order by bm25(e) limit 10",(w,)).fetchall(); tf=time.time()-t
    print(f"n={n} md_MB={sz/1e6:.1f} db_MB={os.path.getsize(f'{n}.db')/1e6:.1f} build_s={tb:.2f} | struct: py_script={tp:.3f}s grep_chain={tg:.3f}s sql={ts:.4f}s (hits {len(r1)}/{len(r2)}) | word: grep={tw:.3f}s fts={tf:.4f}s")

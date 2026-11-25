# -*- coding: utf-8 -*-
"""X6 Gen3 (Rubi/Zafiro) - convertidor de saves. Funciona en Windows, Linux y Mac con Python 3.
  python x6_gen3.py svg2sav  archivo.svg            -> archivo.sav (128 KB)
  python x6_gen3.py sav2svg  plantilla.svg save.sav -> save_x6.svg
  python x6_gen3.py ring2std save.sa1               -> save_128k.sav   (el .sa1 de 64 KB del hack / VBA chino)
"""
import sys,os,struct
EW=0x8910; SB2,SB1,PKS=0x02024EA4,0x02025734,0x020300A0
SZ={0:3884,13:2000}
def chk(data):
    s=sum(struct.unpack_from('<%dI'%(len(data)//4),data))&0xFFFFFFFF
    return ((s>>16)+(s&0xFFFF))&0xFFFF
def rd(p): 
    with open(p,'rb') as f: return f.read()
def wr(p,b):
    with open(p,'wb') as f: f.write(b)
def sections(sav):
    best={}
    for o in range(0,len(sav)-0xFFF,0x1000):
        b=sav[o:o+0x1000]; sid,c,sig,cnt=struct.unpack_from('<HHII',b,0xFF4)
        if sig!=0x08012025 or sid>13: continue
        n=SZ.get(sid,3968)
        if chk(b[:n])!=c: continue
        if sid not in best or cnt>=best[sid][0]: best[sid]=(cnt,b[:n])
    miss=[i for i in range(14) if i not in best]
    if miss: raise SystemExit('Save incompleto, faltan secciones %s'%miss)
    return {k:v[1] for k,v in best.items()}
def block(sid,data,cnt):
    b=bytearray(0x1000); b[:len(data)]=data
    struct.pack_into('<HHII',b,0xFF4,sid,chk(data),0x08012025,cnt); return bytes(b)
def build(secs):
    out=bytearray(b'\xff'*0x20000)
    for sid in range(14):
        out[sid*0x1000:(sid+1)*0x1000]=block(sid,secs[sid],2)
        out[0xE000+sid*0x1000:0xE000+(sid+1)*0x1000]=block(sid,secs[sid],1)
    return bytes(out)
def chk_svg(d):
    if d[:18]!=b'ACTIONS GSVHeader!' or len(d)!=507017: raise SystemExit('Eso no es un .svg de GBA de la X6')
def svg2sav(svg,out):
    d=rd(svg); chk_svg(d)
    ram=lambda a,n:d[EW+a-0x02000000:EW+a-0x02000000+n]
    s={0:ram(SB2,3884)}
    for i in range(1,5): s[i]=ram(SB1+(i-1)*3968,3968)
    for i in range(5,14): s[i]=ram(PKS+(i-5)*3968,SZ.get(i,3968))
    wr(out,build(s)); print('Listo:',out)
def sav2svg(tpl,sav,out):
    svg=bytearray(rd(tpl)); chk_svg(svg); s=sections(rd(sav))
    def put(a,x): o=EW+a-0x02000000; svg[o:o+len(x)]=x
    put(SB2,s[0])
    for i in range(1,5): put(SB1+(i-1)*3968,s[i])
    for i in range(5,14): put(PKS+(i-5)*3968,s[i])
    wr(out,bytes(svg)); print('Listo:',out)
def ring2std(sa,out): wr(out,build(sections(rd(sa)))); print('Listo:',out)
def main(a):
    if len(a)<2: print(__doc__); return
    c,r=a[0],a[1:]; base=os.path.splitext(r[0])[0]
    if c=='svg2sav': svg2sav(r[0],r[1] if len(r)>1 else base+'.sav')
    elif c=='sav2svg': sav2svg(r[0],r[1],r[2] if len(r)>2 else os.path.splitext(r[1])[0]+'_x6.svg')
    elif c=='ring2std': ring2std(r[0],r[1] if len(r)>1 else base+'_128k.sav')
    else: print(__doc__)
if __name__=='__main__': main(sys.argv[1:])

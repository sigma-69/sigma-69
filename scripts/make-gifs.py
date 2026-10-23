# Thu nhỏ + bo góc GIF. Chạy trong thư mục chứa GIF gốc.
from PIL import Image, ImageDraw, ImageSequence
import sys,os
def proc(src,dst,size,crop=None,radius=0,circle=False,step=1,colors=128):
    im=Image.open(src); frames=[]; durs=[]
    for i,fr in enumerate(ImageSequence.Iterator(im)):
        if i%step: continue
        f=fr.convert('RGB')
        if crop: f=f.crop(crop)
        f=f.resize(size,Image.LANCZOS)
        mask=Image.new('L',size,0); d=ImageDraw.Draw(mask)
        if circle: d.ellipse((0,0,size[0]-1,size[1]-1),fill=255)
        else: d.rounded_rectangle((0,0,size[0]-1,size[1]-1),radius=radius,fill=255)
        p=f.quantize(colors=colors-1,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
        # reserve last index for transparency
        pal=p.getpalette()[:3*(colors-1)]+[0,0,0]
        p.putpalette(pal)
        px=p.load(); m=mask.load()
        for y in range(size[1]):
            for x in range(size[0]):
                if m[x,y]<128: px[x,y]=colors-1
        frames.append(p); durs.append(fr.info.get('duration',50)*step)
    frames[0].save(dst,save_all=True,append_images=frames[1:],duration=durs,loop=0,transparency=colors-1,disposal=2,optimize=False)
    print(dst,len(frames),os.path.getsize(dst)//1024,'KB')
O='/workspace/sigma-69-profile/assets/'
proc('p3cGkcctD1EAAAAC.gif',O+'miku-tea.gif',(280,158),crop=(0,40,498,320),radius=14)

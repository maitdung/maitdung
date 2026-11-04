from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, json
from pathlib import Path

W,H=1600,540
def font(n,weight=7):
 return ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc',n,index=weight)
mono='/System/Library/Fonts/Menlo.ttc'
base=Image.new('RGB',(W,H),'#090e15')
# A soft, low-contrast light field keeps the lettering crisp.
small=Image.new('RGB',(400,135)); p=small.load()
for y in range(135):
 for x in range(400):
  a=math.exp(-(((x-310)/105)**2+((y-62)/65)**2))
  b=math.exp(-(((x-380)/90)**2+((y-130)/60)**2))
  p[x,y]=(int(9+4*a+8*b),int(14+23*a+3*b),int(21+28*a+18*b))
base=small.resize((W,H),Image.Resampling.BICUBIC)
d=ImageDraw.Draw(base)
d.rounded_rectangle((1,1,W-2,H-2),radius=26,outline='#27313e',width=2)
d.line((65,79,106,79),fill='#70f0ca',width=3)
d.text((123,65),'MAITDUNG  /  DEVELOPER PORTFOLIO',font=font(17,5),fill='#a0b0c0')
d.text((62,132),'maitdung',font=font(116,0),fill='#f4f7fb',stroke_width=0)
box=d.textbbox((62,132),'maitdung',font=font(116,0)); end=box[2]
d.ellipse((end+10,239,end+27,256),fill='#70f0ca')
d.text((69,288),'Ideas into interfaces.',font=font(35,5),fill='#becbdb')
d.text((70,344),'Building across platforms. Always exploring.',font=font(21),fill='#7f91a6')
d.line((70,427,745,427),fill='#26313e',width=1)
d.text((70,453),'WEB     /     MOBILE     /     BACKEND     /     AUTOMATION',font=font(16,5),fill='#94a6b9')
d.text((1388,471),'@maitdung',font=font(14,5),fill='#60758b')

cx,cy=1210,257
# Interwoven light ribbons are projected from a rotating 3D torus knot.
def curve(a,phase):
 r=138+36*math.cos(3*a)
 x=r*math.cos(2*a); y=r*math.sin(2*a); z=42*math.sin(3*a)
 # Full rotation closes exactly after one cycle.
 rot=.25+phase
 xx=x*math.cos(rot)+z*math.sin(rot)
 zz=-x*math.sin(rot)+z*math.cos(rot)
 yy=y*.86+zz*.45
 return cx+xx*1.2,cy+yy,zz

frames=[]
for i in range(72):
 phase=i/72*math.tau
 im=base.copy(); glow=Image.new('RGBA',(W,H)); gd=ImageDraw.Draw(glow)
 segments=[]
 for j in range(360):
  a=j/360*math.tau
  # Phase is periodic, so the loop closes without a jump.
  x,y,z=curve(a,phase)
  nx,ny,nz=curve(a+math.tau/360,phase)
  shine=(.5+.5*math.cos(a-phase))**8
  depth=(z+90)/180
  col=(int(25+55*depth+140*shine),int(100+75*depth+80*shine),int(125+70*depth+60*shine))
  col=tuple(max(0,min(255,v)) for v in col)
  segments.append((z,(x,y,nx,ny),col))
  gd.line((x,y,nx,ny),fill=(*col,85),width=22)
 glow=glow.filter(ImageFilter.GaussianBlur(22))
 im=Image.alpha_composite(im.convert('RGBA'),glow)
 ribbon=Image.new('RGBA',(W*2,H*2)); rd=ImageDraw.Draw(ribbon)
 for z,xy,col in sorted(segments):
  x,y,nx,ny=xy
  rd.line((x*2,y*2,nx*2,ny*2),fill=col,width=20)
  rd.ellipse((nx*2-10,ny*2-10,nx*2+10,ny*2+10),fill=col)
 im=Image.alpha_composite(im,ribbon.resize((W,H),Image.Resampling.LANCZOS))
 # A pair of luminous particles follows the ribbon.
 particles=Image.new('RGBA',(W,H)); pd=ImageDraw.Draw(particles)
 for offset in (0,math.pi):
  px,py,pz=curve(phase*.5+offset,phase)
  pd.ellipse((px-9,py-9,px+9,py+9),fill=(103,255,217,170))
 halo=particles.filter(ImageFilter.GaussianBlur(9))
 im=Image.alpha_composite(im,halo)
 pd=ImageDraw.Draw(im)
 for offset in (0,math.pi):
  px,py,pz=curve(phase*.5+offset,phase)
  pd.ellipse((px-3,py-3,px+3,py+3),fill='#d8fff3')
 # Central glass tile, offset from the knot for a layered appearance.
 tile=Image.new('RGBA',(W,H)); td=ImageDraw.Draw(tile)
 td.rounded_rectangle((1144,197,1276,329),radius=28,fill=(12,23,34,225),outline=(111,222,201,110),width=2)
 td.text((1172,205),'m',font=font(75,2),fill='#d6fff3')
 im=Image.alpha_composite(im,tile)
 # Thin travelling accent on the left, keeping motion away from the text.
 d=ImageDraw.Draw(im)
 c=int(150+45*(math.sin(phase)+1)/2)
 d.line((2,190,2,350),fill=(65,c,174),width=3)
 frames.append(im.convert('RGB'))

# Shared palette prevents color flicker between GIF frames.
samples=Image.new('RGB',(W, H*6))
for i,k in enumerate(range(0,72,12)): samples.paste(frames[k],(0,H*i))
palette=samples.quantize(colors=256)
indexed=[fr.quantize(palette=palette,dither=Image.Dither.NONE) for fr in frames]
asset_dir=Path(__file__).resolve().parents[1] / 'assets'
asset_dir.mkdir(parents=True, exist_ok=True)
path=asset_dir / 'profile-banner-motion.gif'
indexed[0].save(path,save_all=True,append_images=indexed[1:],duration=80,loop=0,optimize=True,disposal=1)
frames[0].save(asset_dir / 'profile-banner-motion.png')
print(json.dumps({'bytes':path.stat().st_size,'frames':len(indexed),'size':[W,H]}))

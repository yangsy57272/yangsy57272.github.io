"""Animate commissioned keyframes into a 28-second film with a radial blueprint reveal,
3D projected brass orbits, camera moves, particles and a light-sweep transition.
Requires Pillow, numpy and imageio-ffmpeg. Source artwork is generated, not documentary.
"""
from pathlib import Path
import math, subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/films';ART=OUT/'art'
W,H,FPS,DURATION=1280,720,30,28
fontdir=Path('/System/Library/Fonts/Supplemental')
serif=ImageFont.truetype(str(fontdir/'Georgia.ttf'),65)
small=ImageFont.truetype(str(fontdir/'Arial.ttf'),12)
sub=ImageFont.truetype(str(fontdir/'Georgia.ttf'),17)
paint=Image.open(ART/'the-first-spark.png').convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
wire=Image.open(ART/'the-blueprint.png').convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
work=Image.open(ART/'the-workshop.png').convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
# Float fields are reused for procedural light and transition mattes.
y,x=np.mgrid[0:H,0:W].astype('float32');dist=np.sqrt((x-644)**2+(y-252)**2)
def smooth(v):
 v=max(0,min(1,v));return v*v*(3-2*v)
def move(im,scale,cx=644,cy=252,dx=0,dy=0):
 box=(cx-cx/scale+dx,cy-cy/scale+dy,cx+(W-cx)/scale+dx,cy+(H-cy)/scale+dy)
 return im.transform((W,H),Image.Transform.EXTENT,box,Image.Resampling.BICUBIC)
def alpha_mask(v):return Image.fromarray(np.clip(v*255,0,255).astype('uint8'))
def tint_glow(im,cx,cy,radius,strength):
 a=(np.exp(-((x-cx)**2+(y-cy)**2)/(radius*radius))*strength).astype('uint8')
 layer=Image.new('RGBA',(W,H),(255,196,91,0));layer.putalpha(Image.fromarray(a))
 return Image.alpha_composite(im.convert('RGBA'),layer)
# A fully time-driven orbit scene: the circles rotate in 3D before projection.
def orbit(t):
 radius=np.sqrt(((x-W/2)/W)**2+((y-H*.43)/H)**2)
 bg=np.empty((H,W,3),dtype='uint8')
 bg[:,:,0]=np.clip(9+14*np.exp(-radius*5),0,255)
 bg[:,:,1]=np.clip(22+23*np.exp(-radius*4),0,255)
 bg[:,:,2]=np.clip(18+14*np.exp(-radius*5),0,255)
 im=Image.fromarray(bg).convert('RGBA')
 im=tint_glow(im,640,305,220,46)
 lines=Image.new('RGBA',(W,H));d=ImageDraw.Draw(lines)
 cx,cy=640,305
 for r in [205,275,340]:
  pts=[(cx+math.cos(a)*r,cy+math.sin(a)*r*.42) for a in np.linspace(0,math.tau,200)]
  d.line(pts,fill=(205,157,79,55),width=1)
 # Rotating, perspective-projected gimbal rings, sorted back to front.
 segments=[]
 for j in range(3):
  angle=t*.35+j*math.pi/3;tilt=.5+j*.6
  points=[]
  for a in np.linspace(0,math.tau,241):
   px=math.cos(a)*118;py=math.sin(a)*118*math.cos(tilt);pz=math.sin(a)*118*math.sin(tilt)
   xx=px*math.cos(angle)+pz*math.sin(angle);zz=-px*math.sin(angle)+pz*math.cos(angle)
   factor=620/(620-zz);points.append((cx+xx*factor,cy+py*factor,zz))
  for p,q in zip(points,points[1:]):segments.append(((p[2]+q[2])/2,p,q))
 for depth,p,q in sorted(segments,key=lambda a:a[0]):
  bright=int(130+100*(depth+120)/240)
  d.line((p[0],p[1],q[0],q[1]),fill=(min(255,bright+25),int(bright*.79),int(bright*.42),255),width=4)
  d.line((p[0],p[1]-1,q[0],q[1]-1),fill=(255,232,166,120),width=1)
 # Orbiting symbols: camera, geometry, waveform, and code.
 for j,label in enumerate(['LOOK','PROVE','LISTEN','BUILD']):
  a=t*.18+j*math.pi/2;r=295
  px=cx+math.cos(a)*r;py=cy+math.sin(a)*r*.48
  gold=(232,191,121,210)
  d.ellipse((px-26,py-26,px+26,py+26),outline=(209,168,106,110),width=1)
  if j==0:
   d.rectangle((px-15,py-10,px+15,py+10),outline=gold,width=2);d.ellipse((px-7,py-7,px+7,py+7),outline=gold,width=2)
  elif j==1:
   d.line([(px,py-16),(px-16,py+12),(px+16,py+12),(px,py-16),(px,py+12)],fill=gold,width=2)
  elif j==2:
   d.line([(px+k,py+math.sin(k*.3+t)*9) for k in range(-18,19)],fill=gold,width=2)
  else:
   d.line([(px-7,py-10),(px-16,py),(px-7,py+10)],fill=gold,width=2);d.line([(px+7,py-10),(px+16,py),(px+7,py+10)],fill=gold,width=2)
  d.text((px,py+36),label,font=small,anchor='mt',fill=(222,200,157,190))
 im=Image.alpha_composite(im,lines)
 core=Image.new('RGBA',(W,H));d=ImageDraw.Draw(core)
 for r in range(29,0,-1):
  v=1-r/29;d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(255,int(161+90*v),int(45+177*v),255))
 return Image.alpha_composite(im,core).convert('RGB')
ff=imageio_ffmpeg.get_ffmpeg_exe()
proc=subprocess.Popen([ff,'-y','-f','rawvideo','-vcodec','rawvideo','-s',f'{W}x{H}','-pix_fmt','rgb24','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'the-spark-art-film.mp4')],stdin=subprocess.PIPE,stderr=open('/tmp/wendy-art-encode.log','w'))
rng=np.random.default_rng(17);particles=rng.uniform([0,0,0.3],[W,H,1.0],(65,3))
for frame in range(DURATION*FPS):
 t=frame/FPS
 if t<11:
  scale=1+.035*math.sin(t/11*math.pi)
  a=move(paint,scale);b=move(wire,scale)
  # An expanding ring changes the painting into a luminous blueprint.
  if t<4:im=a
  elif t<7:
   rr=smooth((t-4)/3)*1000
   im=Image.composite(b,a,alpha_mask((rr-dist)/55+.5))
  else:im=b
  if t>=9:
   scale2=1+2.8*smooth((t-9)/3)
   im=move(im,scale2)
 elif t<13:
  a=move(wire,3.8+2*smooth((t-11)/2))
  im=Image.blend(a,orbit(t),smooth((t-11)/2))
 elif t<19:
  im=orbit(t)
 elif t<21:
  a=orbit(t);b=move(work,1.04)
  # Diagonal golden sweep reveals the workshop from left to right.
  p=smooth((t-19)/2);edge=-400+p*2000
  mask=alpha_mask((edge-(x+y*.4))/130+.5)
  im=Image.composite(b,a,mask)
 elif t<26:
  im=move(work,1.04-.035*smooth((t-21)/5),cx=640,cy=340,dx=6*math.sin((t-21)/5*math.pi))
 else:
  im=Image.blend(move(work,1.005),paint,smooth((t-26)/2))
 im=im.convert('RGBA')
 if t<11:
  im=tint_glow(im,644,252,90,18+int(9*math.sin(t*1.8)))
 elif 19<t<21:
  edge=-400+smooth((t-19)/2)*2000
  layer=Image.new('RGBA',(W,H),(255,222,153,0));layer.putalpha(Image.fromarray((180*np.exp(-((x+y*.4-edge)/90)**2)).astype('uint8')))
  im=Image.alpha_composite(im,layer)
 overlay=Image.new('RGBA',(W,H));d=ImageDraw.Draw(overlay)
 # Halo expands independently of camera motion.
 if 3.5<t<7:
  r=15+smooth((t-3.5)/3.5)*900;opacity=int(220*(1-smooth((t-6)/1)))
  for extra,alpha in [(7,.1),(4,.25),(1,.8)]:
   d.ellipse((644-r-extra,252-r-extra,644+r+extra,252+r+extra),outline=(255,225,168,int(opacity*alpha)),width=extra+1)
 for px,py,speed in particles:
  xx=(px+math.sin(t*.3+py)*14)%W;yy=(py-t*9*speed)%H
  opacity=int(60+50*math.sin(t*.7+px)**2);r=1 if speed<.8 else 1.5
  d.ellipse((xx-r,yy-r,xx+r,yy+r),fill=(255,217,148,opacity))
 # Restrained scene titles keep the original reference's editorial placement.
 if t<6.5:ch=0;local=t;length=6.5
 elif t<12:ch=1;local=t-6.5;length=5.5
 elif t<20:ch=2;local=t-12;length=8
 else:ch=3;local=t-20;length=8
 opacity=int(255*min(smooth(local/.7),smooth((length-local)/.7)))
 titles=['The spark.','The blueprint.','A world of connections.','The work we share.']
 captions=['A question reaches out.','An idea shows its structure.','Looking, thinking, listening, making.','Nobody builds alone.']
 # Dark lower veil allows title legibility without darkening the artwork above.
 shade=Image.new('RGBA',(W,H),(5,14,10,0));shade.putalpha(Image.fromarray(np.clip((y-450)/270*115,0,115).astype('uint8')))
 im=Image.alpha_composite(im,shade)
 d.text((62,47),'SHIYI YANG / THE ROBOT AND ME',font=small,fill=(246,227,190,225))
 d.text((1217,47),'AN IMAGINED WORLD',font=small,anchor='rt',fill=(246,227,190,190))
 d.text((64,520),f'CHAPTER {ch+1:02}',font=small,fill=(240,199,136,opacity))
 d.text((60,543),titles[ch],font=serif,fill=(255,244,224,opacity))
 d.text((64,628),captions[ch],font=sub,fill=(234,221,198,opacity))
 d.line((64,680,1216,680),fill=(240,200,141,65),width=1)
 d.line((64,680,64+1152*t/DURATION,680),fill=(240,200,141,210),width=2)
 im=Image.alpha_composite(im,overlay).convert('RGB')
 if frame==60:im.save(OUT/'the-spark-art-poster.jpg',quality=87)
 if frame in [60,165,240,450,630,750]:im.save(f'/tmp/art-film-{frame}.jpg',quality=90)
 proc.stdin.write(im.tobytes())
 if frame%150==0:print(f'Art film {frame}/{DURATION*FPS}',flush=True)
proc.stdin.close()
if proc.wait()!=0:raise RuntimeError(Path('/tmp/wendy-art-encode.log').read_text())
print('Art film complete',flush=True)

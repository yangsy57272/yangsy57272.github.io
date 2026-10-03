"""Render the website's 24-second photo film. Requires Pillow, numpy and imageio-ffmpeg."""
from pathlib import Path
import math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1]
W,H,FPS,DURATION=1280,720,24,24
names=['behind-the-camera','between-matches','robot-portrait','mechanism-blue','match-day','together']
images=[Image.open(ROOT/'assets/life'/f'{n}.webp').convert('RGB') for n in names]
fontdir=Path('/System/Library/Fonts/Supplemental')
serif=ImageFont.truetype(str(fontdir/'Georgia.ttf'),53)
sans=ImageFont.truetype(str(fontdir/'Arial.ttf'),14)
small=ImageFont.truetype(str(fontdir/'Arial.ttf'),12)
out=ROOT/'assets/films';out.mkdir(exist_ok=True)
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
cmd=[ffmpeg,'-y','-f','rawvideo','-vcodec','rawvideo','-s',f'{W}x{H}','-pix_fmt','rgb24','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'the-robot-and-me.mp4')]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=open('/tmp/wendy-film-encode.log','w'))
def smooth(x):
 x=max(0,min(1,x));return x*x*(3-2*x)
def photo(i,p):
 im=images[i]; scale=max(W/im.width,H/im.height)*(1.03+.055*smooth(p))
 # Crop in source coordinates; one resampling pass avoids jitter.
 sw,sh=W/scale,H/scale
 x=(im.width-sw)/2-math.sin(p*math.pi)*12/scale
 y=max(0,(im.height-sh)*(.18 if i==4 else .5))
 return im.transform((W,H),Image.Transform.EXTENT,(x,y,x+sw,y+sh),Image.Resampling.BICUBIC)
y,x=np.mgrid[0:H,0:W]
wash=np.zeros((H,W,4),dtype=np.uint8);wash[:,:,:3]=[9,26,21]
wash[:,:,3]=np.clip(25+160*(y/H)**3,0,220).astype('uint8')
wash=Image.fromarray(wash)
labels=['01 / LOOK CLOSER','02 / MAKE IT MOVE','03 / THE PEOPLE AROUND IT']
titles=['It starts with curiosity.','An idea becomes a machine.','Nobody builds alone.']
subtitles=['A camera. A question. A different way of seeing.','Details, decisions, and the space between them.','The robot is part of the story. So are we.']
for frame in range(DURATION*FPS):
 t=frame/FPS;i=min(5,int(t/4));local=t-i*4
 im=photo(i,local/4)
 if local>3:im=Image.blend(im,photo((i+1)%6,(local-3)/4),smooth(local-3))
 im=Image.alpha_composite(im.convert('RGBA'),wash)
 # A restrained warm light floats over a fine moving arc.
 glow=np.zeros((H,W,4),dtype=np.uint8);glow[:,:,:3]=[250,192,106]
 radius=((x-(820+math.sin(t/5)*120))**2+(y-(290+math.cos(t/4)*55))**2)/100000
 glow[:,:,3]=(25*np.exp(-radius)).astype('uint8')
 im=Image.alpha_composite(im,Image.fromarray(glow))
 overlay=Image.new('RGBA',(W,H));d=ImageDraw.Draw(overlay)
 pts=[(j*9-80,390+math.sin(j/160*5.5+t*.13)*130) for j in range(161)]
 d.line(pts,fill=(244,198,129,85),width=1)
 for j in range(14):
  px=(j*103+t*5)%W;py=80+(j*71)%490+math.sin(t+j)*12
  d.ellipse((px,py,px+2,py+2),fill=(255,214,146,int(45+25*math.sin(t+j))))
 d.text((64,42),'SHIYI YANG / THE ROBOT AND ME',font=small,fill=(249,237,216,240))
 d.text((1100,42),'A SMALL FILM',font=small,fill=(249,237,216,240))
 ch=min(2,int(t/8));ct=t-ch*8;a=int(255*min(smooth(ct/.7),smooth((8-ct)/.65)))
 d.text((64,515),labels[ch],font=small,fill=(233,193,137,a))
 d.text((61,545),titles[ch],font=serif,fill=(255,244,223,a))
 d.text((65,620),subtitles[ch],font=sans,fill=(249,237,216,a))
 d.line((64,674,1216,674),fill=(240,200,141,70),width=1)
 d.line((64,674,64+1152*t/DURATION,674),fill=(240,200,141,225),width=2)
 im=Image.alpha_composite(im,overlay).convert('RGB')
 if frame==48: im.save(out/'the-robot-and-me-poster.jpg',quality=85)
 if frame in [48,216,336,480]:im.save(f'/tmp/wendy-film-{frame}.jpg',quality=85)
 proc.stdin.write(im.tobytes())
 if frame%144==0:print(f'Rendered {frame}/{DURATION*FPS}',flush=True)
proc.stdin.close()
if proc.wait()!=0:raise RuntimeError(Path('/tmp/wendy-film-encode.log').read_text())
print('Finished:',out/'the-robot-and-me.mp4',flush=True)

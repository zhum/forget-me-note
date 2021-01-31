from kivy.app import App

from kivy.uix.widget import Widget
from kivy.uix.button import Button

from kivy.uix.scatter import Scatter
from kivy.uix.image import Image

from kivy.uix.boxlayout import BoxLayout

from kivy.properties import ObjectProperty,  NumericProperty, StringProperty

from kivy.lang import Builder

from kivy.factory import Factory
from PIL import Image


Builder.load_string("""
<ImageCropWidget>:
    scatter: _scatter
    rect: _rect
    image: _image
    img_src: root.img_src
    canvas.after:
        Color:
            rgba: [.9, .1, .1, 0.7]
        Line:
            width: 2
            rectangle: (self.xmin, self.ymin, self.xmax-self.xmin, self.ymax-self.ymin)
           
    Scatter:
        id: _scatter
        pos: root.pos
        size: root.size        
        #do_rotation: False
        Image:
            id: _image
            source: root.img_src
            size: _scatter.size
    Widget:
        id: _rect
        size: (root.width/3, root.height/3)
        background_color: [1.,1.,1.,0.80]

<ImageEditor>:
    orientation: 'vertical'
    buttonBox: _buttonBox
    cropW: _cropW
    ImageCropWidget:
        id: _cropW
        img_src: root.img_src
    BoxLayout:    
        id: _buttonBox
        size_hint: (1,0.1)
        orientation: 'horizontal'
""")



class ImageCropWidget(Widget):
    scatter = ObjectProperty(None)
    image = ObjectProperty(None)
    rect = ObjectProperty(None)
    xmin = NumericProperty(20)
    xmax = NumericProperty(40)
    ymin = NumericProperty(20)
    ymax = NumericProperty(40)    

    img_src = StringProperty(None)
    
    def __init__(self, **kargs):
        super(ImageCropWidget, self).__init__(**kargs)
        self.bind( size = self.rescale_rec)
        self.oldsize = self.size
        self.hideLimits()
        self.defaultLimits()
        self._resizing = []
        
    def defaultLimits(self):
        self.xmin = self.width/6.
        self.xmax = self.width - self.xmin/2
        self.ymin = self.height/6.
        self.ymax = self.height - self.ymin/2

        self.xmin = self.width * .2
        self.xmax = self.width * .8
        self.ymin = self.height * .2
        self.ymax = self.height * .8

    def hideLimits(self):
        self.xmin = 0
        self.xmax = self.width
        self.ymin = 0
        self.ymax = self.height

        
    def rescale_rec(self,*l):
        #print 'resize ', self.oldsize, self.size
        f_w = float(self.size[0])/self.oldsize[0]
        f_h = float(self.size[1])/self.oldsize[1]
        self.xmin *= f_w
        self.ymin *= f_h
        self.xmax *= f_w
        self.ymax *= f_h
        self.oldsize = self.size


    def on_touch_down(self, touch):
        print(f"start={self.xmin},{self.ymin}, end={self.xmax},{self.ymax}")
        print(f"touch={touch.pos[0]},{touch.pos[1]}")
        if not self.collide_point(*touch.pos):            
            super(ImageCropWidget,self).on_touch_down(touch)
        elif touch.button in( 'scrollup', 'scrolldown'):
            if touch.button == 'scrollup':
                self.scatter.scale *=1.1
            else:
                self.scatter.scale /=1.1
        else:                            
            f = lambda x0 ,x1 : abs(x0-x1)<5
            x, y = touch.pos
            # normalize in widget coordinate
            # x += self.x
            # y += self.y 
            self._resizing = []
            if f(self.xmin,x):
                self._resizing += [self.set_xmin]
            elif f(self.xmax,x):
                self._resizing += [self.set_xmax]
            if f(self.ymin,y):
                self._resizing += [self.set_ymin]
            elif f(self.ymax,y):
                self._resizing += [self.set_ymax]
            if self._resizing==[]:
                self.scatter.dispatch('on_touch_down',touch)
        return True

    def set_xmin(self,x,y):
        self.xmin = x #- self.x
    def set_xmax(self,x,y):
        self.xmax = x #- self.x
    def set_ymin(self,x,y):
        self.ymin = y # - self.y
    def set_ymax(self,x,y):
        self.ymax = y #- self.y

    def on_touch_move(self, touch):
        #self.debug(" motion ",self.header._start_resize)
        if self._resizing != [] :
            for f in self._resizing:
                f(*touch.pos)
        else:
            super(ImageCropWidget,self).on_touch_move(touch)
        return True
    
    def on_touch_up(self, touch):
        if self._resizing == [] :
            super(ImageCropWidget,self).on_touch_up(touch)
        return True

    def reset(self):
        self.scatter.rotation = 0
        self.scatter.scale = 1.
        self.scatter.pos = self.pos
        self.hideLimits()

class ImageEditor(BoxLayout):
    cropW = ObjectProperty(None)
    buttonBox = ObjectProperty(None)
    ButtonClass= ObjectProperty(Button)

    img_src = StringProperty(None)

    
    def __init__(self, **kargs):
        super(ImageEditor, self).__init__(**kargs)
        BC  = self.ButtonClass
        cancelB = BC(text='cancel')
        cancelB.bind( on_release = self.canceled )
        self.buttonBox.add_widget( cancelB)
        cb = BC(text='Crop')
        cb.bind( on_press = self.crop_pressed)
        self.buttonBox.add_widget( cb  )
        rb = BC(text='Rotate')
        rb.bind( on_press = self.rotate_pressed)
        self.buttonBox.add_widget( rb  )
        okb = BC(text='Ok')
        okb.bind( on_release = self.save_image)
        self.buttonBox.add_widget( okb   )

    def crop_pressed(self,*l):
        self.cropW.defaultLimits()
        pass

    def rotate_pressed(self,*l):
        self.cropW.scatter.rotation -=90.

    def canceled(self, *l):
        self.cropW.reset()
        
    def save_image(self, *l):        
        im = Image.open(self.img_src)
        scatter = self.cropW.scatter
        cropW = self.cropW

        # get the exact ratio, as seen on screen :
        f_window = cropW.image.norm_image_size[0]/float(im.size[0])
        f_window *= scatter.scale

        # rotate as on screent
        im=im.rotate( scatter.rotation)


        # get the image position on screen, within the scatter widget
        size = int(im.size[0]*f_window) , int(im.size[1]*f_window)
        xmin_im = scatter.center_x -size[0]/2 - cropW.x 
        xmax_im = xmin_im + size[0]
        ymin_im = scatter.center_y -size[1]/2 - cropW.y 
        ymax_im = ymin_im + size[1]

        # resize the image as on screen 
        im=im.resize( size, Image.ANTIALIAS )

        # compute crop coordinates (translating from on screen limits position)
        xmin = int(cropW.xmin-xmin_im) 
        xmax = int(cropW.xmax-xmin_im) 
        ymax = int( ymax_im -  cropW.ymax ) 
        ymin = int( ymax_im -  cropW.ymin ) 

        # crop : left, upper, right, and lower
        im=im.crop( (xmin, ymax, xmax, ymin) )

        name_fields = self.img_src.split('.')
        ext = name_fields[-1]
        new_name = '.'.join(name_fields[:-1])+'_edited.'+ext
        print(new_name)
        im.save( new_name)
        #im.show()
        pass

Factory.register("ImageEditor",ImageEditor)
Factory.register("ImageCropWidget",ImageCropWidget)

# cw = ImageEditor(img_src=    "photo.jpeg"    )
cw = ImageCropWidget(img_src=    "photo.jpeg"    )



class MyApp(App):
    def build(self):
        return cw


ap=MyApp()


if __name__ == '__main__':
    ap.run()

import cloud

import os
import urllib2
from cStringIO import StringIO

import Image
import ImageOps

import time

def scrape_to_bucket(target):
    """Downloads image from url, and saves to bucket. *target* should
    be a dict with keys id (image id), and url (location of image).

    Returns a dict with keys id (image id), path (obj key), and
    transforms (empty list)."""

    id, url = target['id'], target['url']

    print 'id', id, 'init time', time.time()

    # path to save image in bucket
    obj_path = 'imgs/{id}/original.png'.format(id=id)

    # extract extension from url
    ext = os.path.splitext(url)[-1]

    # open connection to image
    u = urllib2.urlopen(url)

    # if image isn't png, convert it to png
    if ext.lower() != 'png':
        i = Image.open(StringIO(u.read()))
        data = StringIO()
        i.save(data, 'png')
        data = data.getvalue()
    else:
        data = u.read()

    u.close()

    print 'id', id, 'bucket time', time.time()

    # add image to bucket
    cloud.bucket.putf(data, obj_path)

    print 'id', id, 'end time', time.time()

    return {'id': id,
            'path': obj_path,
            'transforms': []}


class ImageOperation(object):
    """Base class for Message Handlers in Image Pipeline.
    
    Retrieves images from bucket, performs in-memory manipulation
    with PIL object, stores result back in bucket, and then
    outputs message with additional transform listed.
    
    Override operation() for custom operation."""

    name = 'identity'

    def get_image_from_bucket(self, obj_path):
        """Given *obj_path* in bucket, returns PIL Image object"""
        
        # get image data as string of raw bytes
        data = cloud.bucket.getf(obj_path).read()

        return Image.open(StringIO(data))

    def put_image_in_bucket(self, img, obj_path):
        """Given PIL image *img*, saves it to *obj_path* in bucket"""

        output_data = StringIO()
    
        # write raw image bytes to StringIO
        img.save(output_data, 'png')
     
        # store the image file in your bucket
        cloud.bucket.putf(output_data.getvalue(), obj_path)
        
    def add_modifier_to_key(self, obj_path):
        """Returns new *obj_path* that includes name of transform"""

        obj_key, obj_ext = os.path.splitext(obj_path)
        return '{key}.{name}.png'.format(key=obj_key,
                                         name=self.name)

    def message_handler(self, msg):
        """Entry point for message handling. Do not override."""

        img = self.get_image_from_bucket(msg['path'])

        # apply image operation
        new_img = self.operation(img)

        msg['path'] = self.add_modifier_to_key(msg['path'])
        msg['transforms'].append(self.name)

        self.put_image_in_bucket(new_img, msg['path'])

        return msg

    def operation(self, img):
        """Method to replace for custom operation"""
        
        return img


class ImageThumbnail(ImageOperation):

    name = 'thumb'

    def operation(self, img):
        """Returns a thumbnail of the *img*"""
        
        img.thumbnail((150, 150), Image.ANTIALIAS)
        return img
        
class ImageMediumSize(ImageOperation):

    name = 'med'

    def operation(self, img):
        """Returns a 400px version of the *img*"""
        
        img.thumbnail((400, 400), Image.ANTIALIAS)
        return img
        
class ImageSepia(ImageOperation):
    """Applies Sepia Filter.
    Based on: http://effbot.org/zone/pil-sepia.htm"""

    name = 'sepia'

    def __init__(self):
        
        self.sepia_palette = self.make_linear_ramp()

    @staticmethod
    def make_linear_ramp():
        """Generate a palette in a format acceptable for `putpalette`,
        which expects [r,g,b,r,g,b,...]"""

        ramp = []
        r, g, b = 255, 220, 162 
        
        for i in range(255):
            ramp.extend((r*i/255, g*i/255, b*i/255))

        return ramp

    def operation(self, img):
        """Returns a version of the *img* with Sepia applied
        for a vintage look."""
        
        # convert to grayscale
        orig_mode = img.mode
        if orig_mode != "L":
            img = img.convert("L")
     
        img = ImageOps.autocontrast(img)
     
        # apply sepia palette
        img.putpalette(self.sepia_palette)
     
        # convert back to its original mode
        if orig_mode != "L":
            img = img.convert(orig_mode)

        return img

class ImageGrayscale(ImageOperation):

    name ='gs'

    def operation(self, img):
        """Returns a grayscaled version of the *img*"""
        return ImageOps.grayscale(img)


class ImageAutoContrast(ImageOperation):

    name = 'ac'

    def operation(self, img):
        return ImageOps.autocontrast(img)


import ImageFilter

class ImageBlur(ImageOperation):

    name = 'blur'

    def operation(self, img):
        return img.filter(ImageFilter.BLUR)

class ImageEdges(ImageOperation):

    name = 'edges'

    def operation(self, img):
        return img.filter(ImageFilter.FIND_EDGES)


class ImageFaceDetection(ImageOperation):

    name = 'fd'

    def operation(self, img):
        """Input must be grayscale"""

        import cv

        cv_im = cv.CreateImageHeader(img.size, cv.IPL_DEPTH_8U, 1)
        cv.SetData(cv_im, img.tostring())

        faces = self.detect(cv_im)
        for (x,y,w,h) in faces:
            cv.Rectangle(cv_im, (x,y), (x+w,y+h), 255)

        new_img = Image.fromstring("L", cv.GetSize(cv_im), cv_im.tostring())
        return new_img

    def detect(self, cv_im):
        import cv
        HAAR_CASCADE_PATH = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"
        cascade = cv.Load(HAAR_CASCADE_PATH)
        storage = cv.CreateMemStorage()

        faces = []
        detected = cv.HaarDetectObjects(cv_im, cascade, storage, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (15,15))
        if detected:
            for (x,y,w,h),n in detected:
                faces.append((x,y,w,h))
        return faces


def callback(img):
    print img
    cloud.bucket.make_public(img['path'])


if __name__ == '__main__':

    callback_q = cloud.queue.get('callback')
    callback_q.attach(callback)

    thumbnail_q = cloud.queue.get('thumbnail')
    thumbnail_q.attach(ImageThumbnail(),
                       [callback_q],
                       _type='f2')

    sepia_q = cloud.queue.get('sepia')
    sepia_q.attach(ImageSepia(),
                   callback_q,
                   _type='f2')

    medium_q = cloud.queue.get('medium')
    medium_q.attach(ImageMediumSize(),
                    [sepia_q, callback_q],
                    max_parallel_jobs=1,
                    _type='f2')

    img_urls_q = cloud.queue.get('img-urls')
    bad_urls_q = cloud.queue.get('bad-urls')
    
    img_urls_q.attach(scrape_to_bucket,
                      [thumbnail_q, medium_q],
                      retry_on=[urllib2.HTTPError],
                      max_retries=3,
                      retry_delay=60,
                      on_error={Exception: {'queue': bad_urls_q}},
                      max_parallel_jobs=20,
                      readers_per_job=10,
                      _type='c1',
                      )


import cloud
import Image

def thumbnail(key_name):
    """Creates a thumbnail of an image object in bucket with key  *key_name*.
    Output is a new object in bucket with 'thumb_' prepended."""

    thumbnail_filename = 'thumb_' + key_name

    # download object to filesystem
    cloud.bucket.get(key_name)

    img = Image.open(key_name)
    img.thumbnail((100,100), Image.ANTIALIAS)

    # save the image to the filesystem
    img.save(thumbnail_filename, 'JPEG')

    # store the image file in your bucket
    cloud.bucket.put(thumbnail_filename)


if __name__ == '__main__':

    # put face.jpg into your bucket
    cloud.bucket.put('face.jpg')

    # run thumbnail() on the cloud
    jid = cloud.call(thumbnail, 'face.jpg')

    # wait for job to finish
    cloud.join(jid)

    # download image
    cloud.bucket.get('thumb_face.jpg')

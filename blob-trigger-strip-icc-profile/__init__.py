import logging
import azure.functions as func
import io
import sys
from PIL import Image

def main(blobin: func.InputStream, blobout: func.Out[bytes], context: func.Context):
    logging.info(f'Python blob trigger function is processing blob \n'
                 f'Name: {blobin.name}\n'
                 f'Blob Size: {blobin.length} bytes')

    input_image = None

    # Load input image in Pillow
    try:
        input_image = Image.open(blobin)
    except OSError as e:
        logging.error(f'FATAL EXCEPTION: Unable to read input as image. {e}')
        sys.exit(254)
    except Exception as e:
        logging.error(f'FATAL EXCEPTION: {e}')
        sys.exit(255)

    # Print basic image metadata
    # Note that ICC profiles are not in EXIF but in XMP block
    logging.info(f'''
        Blob name: {blobin.name}
        Format: {input_image.format}
        Mode: {input_image.mode}
        Size: {input_image.size}
    ''')

    # Let's make sure we're dealing in RGB
    if input_image.mode != 'RGB':
        logging.info(f'Image color system is {input_image.mode}, converting to RGB...')
        input_image = input_image.convert('RGB')

    # Image is RGB so let's check for embedded ICC profile
    if input_image.info.get('icc_profile') != None:
        logging.info('Image has an embedded ICC profile. Stripping on save.')

    # Store output image in a memory stream
    # Output JPEG quality is controlled by the 'quality' parameter
    out_byte_arr = io.BytesIO()
    input_image.save(out_byte_arr, 'jpeg', quality=85, icc_profile=None)

    # Set blob content from byte array in memory
    blobout.set(out_byte_arr.getvalue())
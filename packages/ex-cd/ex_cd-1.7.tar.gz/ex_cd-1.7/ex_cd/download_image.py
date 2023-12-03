import os
import sys
import json
import gallery_dl
import hashlib
from .common import META_FOLDER, metadata_args, _get_gallery_metadata_filenames
from .download_meta import _valid_gallery_meta


DOWNLOAD_COMPLETED_FILE = 'DownloadCompleted'


def _download_gallery(url, gallery_dir, config, logger):
    """download by gallery_dl and validate"""
    ok_file = os.path.join(gallery_dir, META_FOLDER, DOWNLOAD_COMPLETED_FILE)
    if os.path.isfile(ok_file):  # if downloaded
        return  # exit
    gallery_dl_meta_args = config["gallery-dl-meta-args"]
    sys.argv = ["gallery_dl", *metadata_args, *gallery_dl_meta_args, url]
    logger.debug(f"Exec: {sys.argv}")
    returncode = gallery_dl.main()
    if returncode != 0:
        raise RuntimeError(f"Download failed: {url} -> {gallery_dir}")
    if _validate_gallery(url, gallery_dir, config, logger):  # validate the gallery
        with open(ok_file, "w", encoding='utf8'):
            return  # record that this gallery has been downloaded
    else:
        raise RuntimeError(f"Download not valid: {url} -> {gallery_dir}")


VALIDATE_COMPLETED_FILE = 'ValidateCompleted'


def _validate_gallery(url, gallery_dir, config, logger):
    """validate the gallery"""
    ok_file = os.path.join(gallery_dir, META_FOLDER, VALIDATE_COMPLETED_FILE)
    if os.path.isfile(ok_file):  # if valid
        return True  # exit

    # check if has enough metadata json files
    if not _valid_gallery_meta(url, gallery_dir, config, logger):
        return False
    metafiles = _get_gallery_metadata_filenames(gallery_dir)

    # check if has enough image files
    images = []
    for img in os.listdir(gallery_dir):
        if img == META_FOLDER:
            continue
        images.append(img)
    for metafile in metafiles:
        imgfile = metafile[0:-5]
        if imgfile not in images:
            logger.error(f"Invalid {gallery_dir}: no image {imgfile} for {metafile}")
            return False

    # check if image content SHA1 match image_token
    for img in images:
        # read image_token
        metafile = img + '.json'
        if metafile not in metafiles:
            logger.warn(f"Strange {os.path.join(gallery_dir, img)}: it has no meta json")
            continue
        metadata = {}
        try:
            with open(os.path.join(gallery_dir, META_FOLDER, metafile), 'r', encoding='utf8') as fp:
                metadata = json.load(fp)
        except Exception as e:
            logger.error(f"Invalid {metafile}: cannot read json file, {e}")
            return False
        if 'image_token' not in metadata:
            logger.error(f"Invalid {metafile}: 'image_token' not in metadata")
            return False
        image_token = metadata['image_token']
        # compare image_token
        imgfile = os.path.join(gallery_dir, img)
        try:
            with open(imgfile, mode="rb") as fp:
                sha1 = hashlib.sha1(fp.read()).hexdigest()
                if image_token != sha1[0:10]:
                    logger.error(f"Invalid {imgfile}: image token not match, {image_token} != {sha1}")
                    return False
        except Exception as e:
            logger.error(f"Invalid {imgfile}: cannot compare token, {e}")
            return False

    with open(ok_file, "w", encoding='utf8'):
        return True  # record that this gallery has been validated

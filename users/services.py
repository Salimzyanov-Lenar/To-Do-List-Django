import logging
logger = logging.getLogger(__name__)


def check_image_size(image, max_size=1024):
    max_size_bytes = max_size * 1024

    if image.size > max_size_bytes:
        logger.info(f"Размер изображения больше требуемого")
        return False
    return True
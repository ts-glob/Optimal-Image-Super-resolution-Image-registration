from tqdm import tqdm
from pystackreg import StackReg


def registration(images):
    registered_images = []
    ref_image = images[0]  # задаём эталон
    registered_images.append(ref_image)
    for i in tqdm(range(1, len(images)), desc="Согласование: "):
        offset_image = images[i]
        reg_instance = StackReg(StackReg.AFFINE)
        offset_image = reg_instance.register_transform(ref_image, offset_image)
        registered_images.append(offset_image)
    return registered_images

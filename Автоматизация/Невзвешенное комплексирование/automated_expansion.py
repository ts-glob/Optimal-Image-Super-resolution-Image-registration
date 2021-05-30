from tqdm import tqdm
import cv2
import imageio


def expansion(images, video_name):
    expanded_images = []
    video = imageio.get_reader(video_name)
    original_img = video.get_next_data()
    rows = len(original_img)
    columns = len(original_img[0])
    for i in tqdm(range(0, len(images)), desc="Увеличение размерности: "):
        warped_img = images[i]
        warped_img = cv2.resize(warped_img, (columns, rows))
        expanded_images.append(warped_img)
    return expanded_images

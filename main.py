import imageio
from PIL import Image

vid = 'my_video.mp4'
gif_path = 'my_gif.gif'
n_frames = 30

vid_reader = imageio.get_reader(vid)

frames = []

for i, frame in enumerate(vid_reader):
    pil_image = Image.fromarray(frame)

    frames.append(pil_image)

    if i + 1 >= n_frames:
        break

frames[0].save(
    gif_path,
    save_all=True,
    append_images=frames[1:],  # добавляем остальные кадры к первому
    duration=100,  # длительность кадра в мс
    loop=0,  # 0 = бесконечный цикл
    optimize=True  # оптимизация цвета
)

print(f"GIF сохранён как {gif_path}")

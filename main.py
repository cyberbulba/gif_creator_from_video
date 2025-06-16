import imageio
import os
import argparse
from PIL import Image


def get_num():
    """
    функция работает до тех пор, пока не будет получено
    подходящее числовое значение
    """
    while True:
        try:
            num = int(input())
            if num >= 0:
                break
        except ValueError:
            print('Введите число')
    return num


def cut_video(vid, vid_reader, start_time, end_time, fps):
    """
    функция создаёт видео, начинающееся со start_time и заканчивающееся end_time
    :param vid: имя файла для сохранения видео
    :param start_time: время начала фрагмента
    :param end_time: время конца фрагмента
    :param fps: число кадров в секунду у видео
    :return:
    """
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    writer = imageio.get_writer(vid, fps=fps)

    for i, frame in enumerate(vid_reader):
        if start_frame <= i < end_frame:
            writer.append_data(frame)
        elif i >= end_frame:
            break

    writer.close()


def get_start_and_end_time(duration):
    """
    получаем от пользователя время начала и конца фрагмента
    :param duration: длительность видео
    :return:
    """
    while True:
        print('Введите время начала фрагмента видео для gif: ')
        start_time = get_num()

        print('Введите время окончания фрагмента видео для gif: ')
        end_time = get_num()

        if not (start_time >= duration or end_time > duration or start_time >= end_time):
            break

        print('Введены неправильное время начала или окончания фрагмента обрезки, попробуйте ещё раз.')

    return start_time, end_time


def get_gif(cutted_vid_reader, n_frames, gif_path, ms):
    """
    функция создаёт гиф
    :param cutted_vid_reader: ридер, содержащий кадры видео
    :param gif_path: путь до полученной гифки
    :param ms: время каждого кадра в милисекундах
    """
    frames = []

    for i, frame in enumerate(cutted_vid_reader):
        pil_image = Image.fromarray(frame)

        frames.append(pil_image)

        if i + 1 >= n_frames:
            break

    frames[0].save(
        gif_path,
        save_all=True,  # сохранить все кадры
        append_images=frames[1:],  # добавляем остальные кадры к первому
        duration=ms,  # длительность кадра в мс
        loop=0,  # 0 = бесконечный цикл gif
        optimize=True  # оптимизация цвета
    )

    print(f"GIF сохранён как {gif_path}")


def create_gif():
    console = argparse.ArgumentParser()
    console.add_argument('params', nargs='*')

    while True:
        vid = input('Введите имя файла видео: ')  # 'files/my_video.mp4'
        if os.path.splitext(vid)[1] in ['.mp4'] and os.path.isfile(vid):
            break

    gif_path = 'files/my_gif.gif'

    vid_reader = imageio.get_reader(vid)

    fps = vid_reader.get_meta_data()['fps']
    duration = int(vid_reader.get_meta_data()['duration'])

    start_time, end_time = get_start_and_end_time(duration)

    n_frames = (end_time - start_time) * fps

    vid = 'files/cutted_video.mp4'

    cut_video(vid, vid_reader, start_time, end_time, fps)

    cutted_vid_reader = imageio.get_reader(vid)

    print('Введите длительность кадра в милисекундах: ')
    while True:
        ms = get_num()
        if ms > 0:
            break

    get_gif(cutted_vid_reader, n_frames, gif_path, ms)


create_gif()

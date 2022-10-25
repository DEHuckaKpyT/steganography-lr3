import copy

import matplotlib.pyplot as plt

start_image = plt.imread('image.bmp')
# image = copy.deepcopy(imread('image.bmp'))  # начальная картинка
with open('message.txt') as file:
    message = file.read()  # сообщение для шифрования
_colors = [0, 1, 2]  # цвета rgb: 0 - r, 1 - g, 2 - b

width = start_image.shape[0]
height = start_image.shape[1]


def print_header():
    print(f"Высота = {width} пикселей")
    print(f"Ширина = {height} пикселей")
    print(f"Максимальный встраиваемый объём информации и максимальное встраиваемое число символов:")
    print(f"Если используются последний бит и все три компоненты цвета: "
          f"{(width * height * 3)} бит информации, "
          f"{(width * height * 3) // 8} символов")
    print(f"Если используются два последних бита и все три компоненты цвета: "
          f"{(width * height * 2 * 3)} бит информации, "
          f"{(width * height * 2 * 3) // 8} символов")
    print(f"Если используются три последних младших бита и все три компоненты цвета: "
          f"{(width * height * 3 * 3)} бит информации, "
          f"{(width * height * 3 * 3) // 8} символов")
    print()
    print(f"Последний бит, три компоненты цвета, 10% от макс объёма: "
          f"{((width * height * 3) // 8) * 10 // 100} символов")

    print(f"Последний бит, три компоненты цвета, 20% от макс объёма: "
          f"{((width * height * 3) // 8) * 20 // 100} символов")

    print(f"Последний бит, три компоненты цвета, 30% от макс объёма: "
          f"{((width * height * 3) // 8) * 30 // 100} символов")

    print(f"Последний бит, три компоненты цвета, 50% от макс объёма: "
          f"{((width * height * 3) // 8) * 50 // 100} символов")

    print(f"Последний бит, три компоненты цвета, 75% от макс объёма: "
          f"{((width * height * 3) // 8) * 75 // 100} символов")


def get_sequence():
    symbols = ['{:08b}'.format(symbol) for symbol in bytearray(message, 'utf-8')]
    return ''.join(symbols)


def insert_into(s, index, ch):
    return s[:index] + ch + s[index + 1:]


def set_pixel_bit(pixel, rgb, bit, value):
    color = '{:08b}'.format(pixel[rgb])
    color = color[:bit] + value + color[bit + 1:]
    pixel[rgb] = int(color, 2)


def embed_text_to_image(bits, percent, image):
    if percent == 0:
        return

    number = 0
    sequence = get_sequence()
    sequence_length = len(sequence)

    count_of_embed_bits = (width * height * len(bits) * 3) * percent // 100

    for row in image:
        for pixel in row:
            for color in _colors:
                for bit in bits:
                    set_pixel_bit(pixel, color, bit, sequence[number % sequence_length])

                    number += 1

                    if number == count_of_embed_bits:
                        return


def cut_pixel_bit(pixel, rgb):
    pixel[rgb] = 255 * (pixel[rgb] % 2)


def cut_pixel_bit_one_color(pixel, rgb):
    pixel[rgb] = 255 * (pixel[rgb] % 2)
    pixel[(rgb + 1) % 3] = 0
    pixel[(rgb + 2) % 3] = 0


def cut_image_bits(image, colors):
    for row in image:
        for pixel in row:
            for color in colors:
                cut_pixel_bit(pixel, color)


def cut_image_bits_one_color(image, color):
    for row in image:
        for pixel in row:
            cut_pixel_bit_one_color(pixel, color)


def main():
    print_header()
    bits = [[7]]  # номера битов для замены; отсчёт от нуля
    percents = [0, 10, 20, 30, 50, 75]

    images_for_embed = [copy.deepcopy(plt.imread('image.bmp')) for _ in range(6)]

    image_number = 0
    for percent in percents:
        for bitsList in bits:
            image = images_for_embed[image_number]
            image_number += 1
            print(f"Встраивание в картинку {image_number}")

            embed_text_to_image(bitsList, percent, image)
            plt.imsave(f'image_embed{image_number}.bmp', image)

    image_number = 0
    for image in copy.deepcopy(images_for_embed):
        image_number += 1
        print(f"Обрабатывается срез картинки {image_number}")

        cut_image_bits(image, [0, 1, 2])
        plt.imsave(f'image_cut{image_number}.bmp', image)

    for image in copy.deepcopy(images_for_embed):
        image_number += 1
        print(f"Обрабатывается срез картинки {image_number} (красный)")

        cut_image_bits_one_color(image, 0)
        plt.imsave(f'image_cut{image_number}.bmp', image)

    for image in copy.deepcopy(images_for_embed):
        image_number += 1
        print(f"Обрабатывается срез картинки {image_number} (зелёный)")

        cut_image_bits_one_color(image, 1)
        plt.imsave(f'image_cut{image_number}.bmp', image)

    for image in copy.deepcopy(images_for_embed):
        image_number += 1
        print(f"Обрабатывается срез картинки {image_number} (синий)")

        cut_image_bits_one_color(image, 2)
        plt.imsave(f'image_cut{image_number}.bmp', image)


if __name__ == '__main__':
    main()

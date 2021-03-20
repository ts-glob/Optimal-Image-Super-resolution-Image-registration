from os import listdir
from os.path import isfile, join
import numpy as np
from skimage import io
from skimage.color import rgb2gray
from skimage import img_as_ubyte
from math import pow, pi, exp, log
import locale
from skimage.util import random_noise

locale.setlocale(locale.LC_ALL, '')  # инициализирую картинки
pathIn = "../ПОЛНЫЙ АЛГОРИТМ/5. комплексирование изображений/"
files = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]
img = img_as_ubyte(rgb2gray(io.imread(join(pathIn, files[0]))))
size = (len(img), len(img))
noisy_img = random_noise(np.zeros(size) + 0.5, mode='gaussian')
noisy_img = img_as_ubyte((noisy_img - np.min(noisy_img)) / (np.max(noisy_img) - np.min(noisy_img)))

# region КОММЕНТАРИЙ
# для начала лучше получить g(tau) для самого простого случая - отсутствия вообще каких-либо искажений,
# т.е. d=0, Dv=0, Dx=1, rho=0.9, L=10, T=1
# endregion
# константы
N = 50  # длина искаженной дискретной последовательности. Лучше взять 100 или вообще 50
L = 10  # «измельчение» сетки отсчетов в L раз. Исходная последовательность = L * N
T = 1  # можно брать единичкой для расчетов
d = 0.5  # от 0 до T^2
rho = 0.9  # можно поиграться в пределах от 0 до 1
Dx = np.var(img)
Dv = np.var(noisy_img)
omegas = np.arange(N * L) * (2 * pi / (T * N * L - 1)) - pi / T
_T = T / L


# душнилово
def H(omega):
    return exp(-0.5 * d * omega * omega)


def Фx(omega):
    return (-2 * (log(rho) / T) * Dx) / ((log(rho) / T) * (log(rho) / T) + (omega * omega))


# тут вычисляем значение ЧХ в точке, бесконечную сумму не считаем, считаем конечную, но большую
def G(omega):
    upper = 0
    lower = L * T * Dv
    temp = (N * L * 2) - (N * L)
    for k in range(N * L * 2):
        upper = upper + H(-omega - 2 * pi * (k - temp) / T) * Фx(omega + 2 * pi * (k - temp) / T)
        lower = lower + pow(H(omega + 2 * pi * (k - temp) / (_T * L)), 2) * Фx(omega + 2 * pi * (k - temp) / (_T * L))
    return L * upper / lower


# тут генерим нормальную сетку частот и вычисляем ЧХ восстанавливающего фильтра
def G_array():
    Gs = np.zeros(N * L)
    for k in range(omegas.shape[0]):
        Gs[k] = G(omegas[k])
        # print(locale.format("%.8f", Gs[k]))
        # print(locale.format("%.8f", omegas[k]))
    return Gs


# тут вычисляем обратное Фурье, точно считать его нам не надо
def g(Gs):
    gs = np.zeros(N * L)
    fx = np.zeros(N * L)
    step = omegas[1] - omegas[0]
    for k in range(omegas.shape[0]):
        fx[k] = Gs[k] * exp(omegas[k] * _T)
    for k in range(Gs.shape[0] - 1):
        gs[k + 1] = gs[k] + ((fx[k] + fx[k + 1]) * step) / 2  # TODO
    gs = gs * (_T / (2 * pi))
    for k in range(gs.shape[0]):
        print(locale.format("%.8f", gs[k]))
    return gs


g(G_array())

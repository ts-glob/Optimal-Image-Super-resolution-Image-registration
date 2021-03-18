import os
from os import listdir
from os.path import isfile, join
import numpy as np
from skimage import io
from skimage.color import rgb2gray
from skimage import img_as_ubyte
from math import fabs, pow, pi, exp, log
import locale
from skimage.util import random_noise
from scipy.integrate import quad

locale.setlocale(locale.LC_ALL, '')  # инициализирую картинки
pathIn = "ПОЛНЫЙ АЛГОРИТМ/5. комплексирование изображений/"
files = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]
img = img_as_ubyte(rgb2gray(io.imread(join(pathIn, files[0]))))
size = (len(img), len(img))
noisy_img = random_noise(np.zeros(size) + 0.5, mode='gaussian')
noisy_img = img_as_ubyte((noisy_img - np.min(noisy_img)) / (np.max(noisy_img) - np.min(noisy_img)))

# константы
N = 1000  # длина искаженной дискретной последовательности
L = 10  # «измельчение» сетки отсчетов в L раз. Исходная последовательность = L * N
T = 1  # можно брать единичкой для рассчетов
Ω = (-pi * L) / T  # ЧТО ЭТО? TODO
d = 0.5  # от 0 до T^2
ρ = 0.9  # можно поиграться в пределах от 0 до 1

# константные формулы
Ṫ = T / L
a = log(ρ) / T
Dx = np.var(img)
Dv = np.var(noisy_img)
G = []
g = []


def H(Ω):
    return exp(-0.5 * d * Ω * Ω)


def Фx(Ω):
    return (2 * a * Dx) / (a * a + Ω * Ω)


step = Ω / (L * N) * 2  # шаг увеличения Ω, чтобы за L * N операций прийти от (-pi * L) / T <= Ω  < (pi * L) / T
for i in range(L * N):
    # print(locale.format("%.20f", Ω))
    A = 0
    B = 0
    Ω = Ω - step
    for s in range(20):
        A = A + (H(Ω) * (-1 * Ω - (2 * pi * s - 10) / T) * Фx(Ω) * (Ω + (2 * pi * s - 10) / T))
    for k in range(20):
        B = B + (pow(fabs(H(Ω) * (Ω + (2 * pi * k - 10) / Ṫ * L)), 2) * Фx(Ω) * (
                Ω + (2 * pi * k - 10) / Ṫ * L) + Ṫ * L * Dv)
    G.append(L * (A) / (B))
    # print(locale.format("%.80f", G[i]))


def f(x, kk):
    return exp(x * kk)


x0 = -pi / T
xn = pi / T
for i in range(L * N):
    I = quad(f, x0, xn, args=(i))
    g.append((Ṫ * G[i] * I[0]) / 2 * pi)
    print(locale.format("%.80f", g[i]))

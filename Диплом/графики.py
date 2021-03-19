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

#region КОММЕНТАРИЙ
# для начала лучше получить g(tau) для самого простого случая - отсутствия вообще каких-либо искажений,т.е. d=0, Dv=0, Dx=1, rho=0.9, L=10, T=1
#endregion
# константы
N = 1000  # длина искаженной дискретной последовательности
#region КОММЕНТАРИЙ
#не надо брать такие гигантские последовательности, питон умрет считать циклы для такого числа отсчетов, лучше взять 100 или вообще 50
#endregion
L = 10  # «измельчение» сетки отсчетов в L раз. Исходная последовательность = L * N
T = 1  # можно брать единичкой для рассчетов
Ω = (-pi * L) / T  # ЧТО ЭТО? TODO
d = 0.5  # от 0 до T^2
rho = 0.9  # можно поиграться в пределах от 0 до 1

# константные формулы
Ṫ = T / L
a = log(ρ) / T
Dx = np.var(img)
Dv = np.var(noisy_img)
G = []
g = []
#region КОММЕНТАРИЙ
# у тебя клавиатура греческая? не стоит так именовать параметры - Ω,Ф,Ṫ и т.д.
#endregion
def H(Ω):
    return exp(-0.5 * d * Ω * Ω)
#region КОММЕНТАРИЙ
#энергетический спектр лучше считать не через параметр "а", а через коэффициент корреляции - rho=ln(a)/T
#endregion
def Фx(Ω):
    return (-2 * math.log(rho) * Dx) / (math.log(rho) * math.log(rho) + Ω * Ω)
#region КОММЕНТАРИЙ+ КОД
# там дальше какое-то душнилово пошло, так что давай я тебе намекну, как это дожно выглядеть, а ты потом это дело перепишешь на питон и векторизуешь операции, чтобы полгода не считалось:
# тут генерим нормальную сетку частот и вычисляем ЧХ восстанавливающего фильтра
def G_array():
    omegas = np.arange(N*L) * (2 * math.pi / (T * N*L - 1)) - math.pi / T
    Gs = np.zeros(N*L)
    for k in range(omegas.shape[0]):
        Gs[k]=G(omegas[k])
    return Gs
# тут вычисляем значение ЧХ в точке, бесконечную сумму не считаем, считаем конечную, но большую
def G(omega):
    upper=0;
    lower=T*Dv;
    for k in range(-N*L,N*L+1):
        upper = upper +  H(-omega-2*math.pi*k/T)*Фx(omega+2*math.pi*k/T)
        lower =lower + pow(H(omega+2*math.pi*k/T),2)*Фx(omega+2*math.pi*k/T)
    return L*upper/lower

# тут вычисляем обратное Фурье, точно считать его нам не надо
def g(Gs):
    gs = np.zeros(N*L)
    "https://ru.wikipedia.org/wiki/Метод_трапеций"
    return gs
# естественно, никакой код из написанных мной, я не отлаживал, так что оскорее всего он не работает, но идею ты уловил
#endregion

#region КОММЕНТАРИЙ
# вот это все я назвал душниловом в прошлом блоке

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
#endregion
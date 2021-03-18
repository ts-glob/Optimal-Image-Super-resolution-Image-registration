fix: 
	1. реализовать динамические искажения (ака свёртку с гауссианой(???));
	2. объединить все искажения в одно;
	3. реализовать фильтр винера (как в skimage - https://scikit-image.org/docs/dev/api/skimage.restoration.html#skimage.restoration.unsupervised_wiener)
end/ запилить отчёт, даже если что то не получится.

# Optimal Image Super-resolution 

НИР **"Оптимальное сверхразрешение изображений"**

Общая постановка задачи:  
*В рамках криминалистической экспертизы производится повышение пространственного разрешения изображения плоского объекта по набору кадров видеозаписи низкого разрешения*

Допущения, упрощающие жизнь:
* Изображения полутоновые,
* Восстанавливаемый объект плоский,
* Объект в кадре испытывает "умеренное" движение - сдвиги и повороты на незначительный угол.

Общая схема экспериментального исследования предлагаемого метода:
1) Берем набор кадров,  
2) Вносим искажения в соответствии с моделью наблюдения:  
  2.1) Децимация,  
  2.2) Динамические искажения,  
  2.3) Аддитивный шум,  
3) Производим покадровое восстановление с сохранением дисперсии ошибки восстановления в каждой точке *(на данный момент можно классичеким Винером)*  
4) Производим геометрическое согласование кадров, при этом трансформируя и поле ошибок,  
5) Производим комплексирование - взвешенное суммирование согласованного набора изображений,  
6) Наслаждаемся (наверное) полученным результатом.

~~Общая схема сравнительного исследования метода геометрического согласования:~~  
~~*поскольку метод геометрического согласования кадров по сути берем из коробки, необходимо выбрать*~~
1) ~~Берем тестовый набор,~~
2) ~~Согласовываем все его изображения выбранным методом,~~
3) ~~Считаем меру близости согласованных изображений к выбранному - СКО,~~
4) ~~Перебираем параметры метода, если таковые у него есть,~~
5) ~~Выбираем из исследованных методов тот, который дал наименьшую ошибку.~~

Примерный план работ по теории:  
- [ ] Освежить в памяти теорию цифровой обработки сигналов - открыть [это](http://repo.ssau.ru/handle/Uchebnye-posobiya/Teoriya-cifrovoi-obrabotki-signalov-i-izobrazhenii-Elektronnyi-resurs-ucheb-po-specialnosti-Inform-bezopasnost-avtomatizir-sistem-54688) на разделах про обработку случайных сигналах, связи непрерывного и дискретного спектров, винеровской фильтрации
- [ ] Разобраться в препринте статьи по оптимальному сверхразрешающему восстановлению *(на данный момент не очень приоритетно)*  
- [ ] Разобраться в алгоритме комплексирования - открыть [это](http://repo.ssau.ru/handle/Informacionnye-tehnologii-i-nanotehnologii/Optimalnoe-kompleksirovanie-izobrazhenii-videoposledovatelnosti-85239)  

Примерный план работ на ближайшее время:  
- [ ] Создать тестовый набор для экспериментального исследования,
- [ ] Реализовать процедуру внесения искажений в изображение:
  - [ ] Децимацию,
  - [ ] Искажение ЛИС-системой с гауссовской импульсной характеристикой *(классический вариант динамических искажений для оптических систем)*,  
  - [ ] Добавление аддитивного шума.
- [ ] Реализовать процедуру восстановления изображения *(на данный момент можно классичеким Винером)*, для этого понадобится:  
  - [ ] Процедуры прямого и обратного БПФ с учетом паддинга изображений, размеры которых не являются степенью двойки, и (0,0) в центре изображения,  
  - [ ] Процедура вычисления АКФ исходного сигнала,  
  - [ ] Процедура вычисления частотной характеристики искажающей ЛИС-системы,  
- [ ] Реализовать процедуру вычисления поля дисперсии ошибок для восстановленного изображения,  
- [x] Посмотреть различные методы геометрического согласования изображений и выбрать тот, который дает наименьшую СКО на тестовом наборе:  
  - [x] Особые точки - [Zitová B., Flusser J.  Image Registration Methods: A Survey // Image and Vision Computing. − 2003. − Vol. 21, N 11. − P. 977−1000. − doi: 10.1016/S0262-8856(03)00137-9.](https://www.sciencedirect.com/science/article/pii/S0262885603001379):
    - [x] SIFT - [Lowe D.G. Distinctive Image Features from Scale-Invariant Keypoints // International Journal of Computer Vision. − 2004. − Vol. 60. − P. 91–110.](https://link.springer.com/article/10.1023/B:VISI.0000029664.99615.94) 
    - [x] SURF - [Bay H., Tuytelaars T., Van Gool L. SURF: Speeded Up Robust Features // European Conference on Computer Vision ECCV 2006, Graz, Austria, 7−13 may, 2006. − P. 404−417.](https://link.springer.com/chapter/10.1007/11744023_32) 
    - [x] BRIEF - [Calonder M., Lepetit V., Strecha C., Fua P. BRIEF: Binary Robust Independent Elementary Features // 11th European Conference on Computer Vision, Heraklion, Crete, Greece, 5−11 sep., 2010. − P. 778-792.](https://link.springer.com/chapter/10.1007/978-3-642-15561-1_56) 
    - [x] ORB - [Rublee E., Rabaud V., Konolige K., Bradski G.R. ORB: An efficient alternative to SIFT or SURF // The 13th International Conference on Computer Vision, Barcelona, Spain, 6−13 nov., 2011. − P. 2564−2571.](https://www.researchgate.net/publication/221111151_ORB_an_efficient_alternative_to_SIFT_or_SURF) 
  - [x] [Thévenaz P., Ruttimann U.E., Unser M. A Pyramid Approach to Subpixel Registration Based on Intensity // IEEE Transactions on Image Processing. – 1998. − Vol. 7, N 1. − P. 27−41.](https://www.semanticscholar.org/paper/A-pyramid-approach-to-subpixel-registration-based-Th%C3%A9venaz-Ruttimann/a94497d8ec66cdd00af5b6db72fb6d645e1a8f29)  
  - [x] [Guizar-Sicairos M., Thurman S.T., Fienup J.R. Efficient subpixel image registration algorithms // Optics Letters. − 2008. − Vol. 33. – P. 156−158. − doi:10.1364/OL.33.000156.](https://pdfs.semanticscholar.org/b597/8b756bdcad061e3269eafaa69452a0c43e1b.pdf)  
  - [x] [Wedel A., Pock T., Zach C., Bischof H., Cremers D. An improved algorithm for TV-L 1 optical flow // Statistical and geometrical approaches to visual motion analysis, Dagstuhl Castle, Germany, 13-18 jul., 2008. − P. 23−45. − doi:10.1007/978-3-642-03061-1_2.](https://www.researchgate.net/publication/226781293_An_Improved_Algorithm_for_TV-L1_Optical_Flow)    
- [ ] Реализовать выбранную процедуру геометрического согласования изображений с применением транформации и к полю ошибок, полученному на этапе восстановления,  
- [ ] Реализовать алгоритм комплексирования кадров последовательности. 

*На самом деле код, реализующий практически все указанные пункты, у меня есть, но он на С#, а еще я тебе его не дам*

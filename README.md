# forget-me-note

Проект органайзера "что где лежит". Идея работы программы - чтобы запомнить в каком ящике/столе/полке/шкафу какие вещи лежат, сфотографируйте их и отметьте вещи. Можно добавлять фото с текстом (подписью) или только текст. На фото при добавлении новой вещи необходимо отметить её рамкой. Можно добавлять иерархию - сфотографировали шкаф, затем добавили его полки (отметив их на фото шкафа), и т.д.

Тут прототип https://mockup.io/#projects/157161/mockups

Далее словом "элемент" обозначается вещь или место (комната, полка и т.п.), которое надо запомнить.

У элемента может быть фото (а может не быть) и обязательно есть имя
(не уникальное) и "родитель", т.е. место, где он находится.

Также у элемента есть координаты и размер его рамки на родительском фото,
если у родителя нет фото, то координаты (0,0), а размеры (50,50).

Также элемент имеет флаг "deleted", если он не 0, то элемент не отображается в списке родителя и поиске. Его можно восстановить.

У элемента есть номер в родительском списке, по этому номеру элементы списка сортируются.

Фото хранятся в одном каталоге и все имеют имя вида fmnote-XXXXXX.jpg,
где XXXXXX - номер с ведущими нулями. Все фото имеют формат 3:4
(обрезается при фотографировании, пользователь выбрает что остаётся,
a-la instagram или автоматически).

## Формат БД:

### Таблица Items:

- int id             # идентификатор, primary key, uniq
- int parent         # идентификатор родителя (0 для корневого)
- string title       # подпись
- int x,y,w,h        # описание рамки на родительском фото
- int photo          # номер фотографии (0, если фото нет)
- int weight         # порядковый номер в родительском списке
- int deleted        # признак удаления
- timedate created   # время и дата создания
- timedate updated   # время и дата последнего изменения/удаления

### Таблица Suggestions:

- int id             # идентификатор, primary key, uniq
- string name        # имя предлагаемого элемента
- int last           # последний номер такого элемента


## Описание экранов прототипа с текущими соображениями:

1. Navigation

  Это экран с тремя "режимами": Navigation, Edit, Delete. Можно разбить
  их на отдельные, если так удобнее. По сути при смене режима меняется
  только набор кнопок внизу и режим работы со списком/фото.

  В режиме Navigation кнопка режима ведёт к режиму  Edit.

  Общие элементы:

  - Название элемента + кнока его редактирования.
  - Кнопка настроек.
  - Список из текстовых элементов, если была приложена фотография,
    то она отображается вверху (может быть как первый элемент списка?).
  - Верхний элемент списка = возврат к "родителю" (у главного "родителя" его нет).
  - На фото все элементы отмечены рамками. При нажатии на элемент в списке
    или на содержимое его рамки происходит переход на страницу элемента.
  - Если подэлементов и фото нет, то на странице показывается только
    имя элемента и кнопка возврата к родителю (и предложение добавить фото/элементы?).
  - Внизу - кнопки управления. Первая = смена режима.

  На экране Navigation ещё две кнопки:

  - Добавление, при нажатии переход на экран Foto.
  - Поиск, при нажатии переход на экран Search.

1. Edit (второй режим Navigation)

  Список переходит в режим перетаскивания, можно переупорядочить элементы.

  Рамки на фото также можно менять - при клике подсвечивается
  соответствующий элемент в списке и появляются кружки на верхнем левом
  и нижнем правом углу, ими можно менять положение и размер соответственно.

  Кнопка "режим" меняет режим на "Delete".

  Вторая кнопка = переход на экран Update.

  Третья кнопка = переход на экран Move here.


1. Delete (третий режим Navigation)

  Список переходит в режим "удаление", справа от каждого элемента списка
  появлется значок, при нажатии на который элемент удаляется.

  Кнопка "режим" менеят режим на "Navigation".

  При клике на рамку, соответствующий элемент списка подсвечивается.

  Вторая кнопка = переход на экран "Restore".

1. Foto

  Сверху - превью фото.

  Ниже - поле для ввода названия + выпадающий список подсказок.
  В подсказках слова из таблицы Suggestions + очередной номер (например,
  Room 3). После выбора из списка можно отредактировать имя. Номер в
  таблице меняется, если после успешного добавления (ок на Foto 2) имя
  совпадает с одной из строк таблицы + очередной номер.

  Внизу три кнопки:

  - назад
  - пропустить (фото не делается, но имя белётся из поля ввода, оно должно быть не пустым)
  - далее - переход на экран Foto 2.


1.  Настройки:

  - цвет рамки
  - порог прилипания
  - список имён, предлагаемых при добавлении
  - кнопка "стереть удалённые" (все удалённые элементы и их фото удаляются совсем)
  - кнопка export - БД экспортируется в csv и вместе со всеми фото архивируется в zip
  - кнопка import - импорт из zip, старые данные удаляются
  - кнопка import add - добавление новых элементов из zip как потомка (выбирается его родитель и подпись)





  После добавления фото/текста предлагается выделить на "родительском" фото расположение нового элемента (рамку) - если есть родительское фото.

  Добавленный элемент добавляется в список и на фото (если есть). Если родительского фото нет, то в конец списка, если есть, то в
  порядке сортировки на фото (сверху-вниз, слева-направо). Порядок сортировки фиксируется в БД (см. поле weight), после добавления у всех
  "потомков" это поле обновляется.

  При создании рамки действует "прилипание" - если координата угла рамки X=a и хотя бы у одного существующего потомка у одного из углов
  рамки координата X=a+d, где |d| < порога прилипания (задаётся в настройках), то a делается равным a+d. Иначе говоря, углы рамок автоматически
  выравниваются по добавленным ранее рамкам. Это должно быть отключаемо, на экране добавления рамки нужно добавить галочку "прилипание".

  Четвёртая кнопка - переход к поиску.
  

## Общие замечания

В режиме поиска доступен иерархичекский список всего, а также режим "все фото" - их можно листать (а лучше проматывать, имея перед глазами  ~5 фото).

В режиме "все фото" не забыть про отображение подписей.

При добавлении элемента можно ввести подпись вручную, а можно выбрать из выпадающего списка (и отредактивать потом).
Например, по умолчанию в списке будут "Комната 1", "Шкаф 1", "Полка 1".

Если пользователь выбирает "Комната 1", он может отректировать это имя.
Если он оставляет его таким же, то в следующий раз в списке будет "Комната 2".
Если пользователь удаляет элемент, то производится проверка, не нужно ли скорректировать номер последнего предложения (например, добавили "Комната 5", а потом удалили, в списке снова появится "Комната 5", вместо 6).

Создание/редактирование рамок на фото предлагается сделать перетаскиванием
верхнего левого и нижнего правого углов. Эти углы можно выделить визуально кружками.

В режиме создания/редактирования рамок нужно предусмотреть возможность
увеличить/уменьшить масштаб фото, чтобы на небольшом экране телефона можно было
выбелить маленькую область.


## Переходы

### Экран навигации/редактирования:

- режим = смена набора кнопок навигация <-> редактирование
- "+" = экран "фото 1"
- "вверх" = смена содержимого на родительский элемент (экран не меняется)
- "поиск" = переход на экран "поиск".
- элемент из списка или клик на рамке на фото = переход на соответствующий элемент (экран не меняется)

- "обновить" = переход на экран "обновление фото"
- "переместить" = переход на экран "выбор для перемещения"
- "удалить" = меняем набор кнопок на "ок/отмена", на элементах списка появляются чекбоксы для выбора (или иная форма выбора).
  При выборе элемента списка подсвечивается его рамка на фото. При клике на рамке элемента его состояние выбора меняется.
- "восстановить" = переход на экран "выбор для восстановления"
- "перетащить" = меняем набор кнопок на "ок/отменить", элементы списка становятся перемещаемыми.
  При выделении элемента подсвечивается его рамка на фото, саму рамку тоже можно перемещать и менять размер.

### Экран "Фото 1"

- "Cancel" = возвращаемся на экран навигации (back)
- "Ок" = сохраняем уже обрезанное фото и переходим на "Фото 2" (возможно, просто смена содержимого фрейма)

### Экран "Фото 2" (или доп. логика в "фото 1")

- "Cancel" = удаляем фото, возвращаемся на экран навигации (back, если просто меняли содержимое фрейма)
- "Ок" = создаём рамку для нового элемента, задаём его имя, создаём запись в БД, возвращаемся на экран навигации, обновляя там список.

### Экран "поиск"

- "список фото" = переход на экран "список фото"
- клик по элементу = переход на его экран навигации
- "cancel" = возврат на экран навигации(back) (добавить эту кнопку, в прототипе она забыта)

Внимание, этот экран используется в двух сценариях - переход из навигации и переход из настроек.
В первом случае по клику переходим на выбранный элемент, во втором - возвращаемся в настройки, передав выбранный элемент.
Возможно проще реализовать два таких экрана с разным функционалом.

### Экран "список фото"

- "ок" = ошибка дизайна :) этой кнопки быть не должно
- "cancel" = возврат на экран "поиск"(back)
- клик по фото = переход на экран навигации с выбранным элементом

### Экран "обновление фото"

- "ок" = заменяем фото на новое, возвращаемся на экран навигации с обновлением фото
- "cancel" = возвращаемся на экран навигации (back)

### Экран "выбор для перемещения"

- "cancel" = этой кнопки нет в прототипе, надо добавить. Возвращаемся на экран навигации (back)
- клик на элемент списка = перемещаем элемент со страницы которого мы сюда пришли в список "детей" выбранного элемента.
  Тут должен присутствовать "корневой" элемент, чтобы можно быть вынести элементы в самый начальный список.
  Обновляем БД, значение weight перемещённого элемента обновляем, поместив его в конец списка, координаты рамки оставляем.
  Переходим на экран навигации кликнутого элемента (чтобы можно было сразу отредактировать его место в списке и рамку).

### Экран "выбор для восстановления"

- клик на элементе = смена статуса "выбран/нет"
- "ок" = всплывающее окно выбора "в текущий / в исходные".
  "В текущий" = добавляем выбранные элементы в конец списка "детей" элемента из которого мы сюда пришли.
  "В исходные" = восстанавливаем выбранные элементы в их родительских элементах. Помещаем их в конец списка.
  Если родительский элемент удалён, восстанавливаем в текущий.
- "cancel" = возвращаемся на экран навигации (back)

### Экран "настройки" (prototype-demo/5 preferences.html)

- "ок" = back
- "export" = создаём zip-файл с дампом БД в 2-х csv-файлах и картинками.
- "import" = получаем имя zip-файла (из сервиса?), распаковываем,
  проверяем корректность cvs-файлов, если всё ок, то удаляем данные из БД и старые фото, заменяем новыми данными и фото.
  (возможно, надо сначала спросить "мы тут всё старое удалим сейчас, точно импортируем?")
- "добавить" = получаем имя zip-файла как в import, проверяем.
  Добавляем в список "предлагаемых имён" распакованное поэлементно, если там ещё нет такого элемента - добавляем, есть - игнорируем.
  Показываем экран "поиск" (или его клон?), добавляем деревья из распакованных файлов в его список детей.
  Фото распаковываем и переименовываем, чтобы не было коллизий.
  Это сложная операция, т.к. надо менять id распакованных элементов (можно просто прибавить к ним константу) и имена фото.
- "выбор цвета рамки" (в прототипе нет) = запомнить цвет рамки
- "список предлагаемых имён" = просто текстовый список с текстовым полем для добавления и кнопкой удаления
- "порог прилипания" = (в прототипе нет) числовое поле.



Здравствуйте, вот список вопросов, он не полный, будут еще, но пока так.
1 - В режиме "все фото" не забыть про отображение подписей. При добавлении элемента можно ввести подпись вручную, а можно выбрать из выпадающего списка (и отредактивать потом).
На макете, это экран "Photo list"? Если да, то я не вижу кнопки "Добавление элемента" или "Редактирование подписи", и стрелочек описывающих архитектуру экранов в случае добавления или редактирования.
2 - "вверх" = смена содержимого на родительский элемент (экран не меняется)
Если при нажатии на элемент не менять экран, а только содержимое, получается сложная логика, в которой можно запутаться. Лучше отделить экран "Родительского элемента" от экрана "Дочернего элемента". В этом случае теряется смысл кнопки "Вверх" так как ее функции перенимает кнопка "back"
3 - "обновить" = переход на экран "обновление фото"
На макете экранов, вижу только фото и 2 кнопки, без возможностей обновления, редактирования и т.д.
4 - Третья - перемещение текущего элемента. Попадаем на экран с выбором нового родителя. После выбора родителя добавляем элемент в конец списка или, если у родителя есть фото, выделяем рамкой на фото положение элемента.
Не вижу переходов в случае, если у родителя есть фото.
5 - "удалить" = меняем набор кнопок на "ок/отмена", на элементах списка появляются чекбоксы для выбора (или иная форма выбора). При выборе элемента списка подсвечивается его рамка на фото. При клике на рамке элемента его состояние выбора меняется.
Опять же, рекомендую новый экран. Если забить одно активити таким большим функционалом и такой сложной логикой, то получится каша, которую я конечно смогу написать, но поддерживать такой код невозможно, ровно как и искать баги, если они проявятся. Здесь бы я вообще рекомендовал сделать по другому. Так как у нас есть возможность переходить на экран предметов, то кнопка "Удалить" удаляла бы именно тот элемент, на котором мы находимся, без возможности выбора.
6 - "восстановить" = переход на экран "выбор для восстановления"
Не вижу кнопки, и не очень понимаю, как будет работать кнопка "Восстановить" в случае удаления родителя. Все дочерние элементы и родитель - удалятся, и мы больше не попадем на этот экран. Как следствие, в БД будет лежать информация, которую мы никогда не сможем использовать. Рекомендовал бы отказаться от временного удаления, никогда не встречал такой функционал на практике. Лучше сделать окошко "Вы уверены, что хотите удалить?" и удалять безвозвратно.
7 - "перетащить" = меняем набор кнопок на "ок/отменить", элементы списка становятся перемещаемыми. При выделении элемента подсвечивается его рамка на фото, саму рамку тоже можно перемещать и менять размер.
Опять же, нужен либо переход на другой экран, если требуется менять только позицию элемента в списке, то я могу сделать это и без перехода на другой экран, но в таком случае, нельзя будет менять область на фотографии.
8 - "Ок" = сохраняем уже обрезанное фото и переходим на "Фото 2" (возможно, просто смена содержимого фрейма)
Смущает фраза "Уже обрезанное фото", фото нужно обрезать? Если да, то логика такова. Загрузили фото из камеры/галереи, перешли на экран обрезки фото, перешли на экран выбора области содержимого. В итоге 3 экрана.
9 - "Cancel" = удаляем фото, возвращаемся на экран навигации (back, если просто меняли содержимое фрейма).
Один экран занимается разной логикой, в первом случае при нажатии на кнопку cancel мы удаляем фото, во втором нет. Следовательно нужно передавать на экран информацию о том, с какого экрана мы на него перешли, что не очень правильно, так как в конечном итоге у нас появится куча переменных на экранах с подобной информацией, и код превратится в кашу. Кнопке cancel должно быть все равно, нужно нам удалять фото или нет, ее задача перейти на предыдущий экран. Следовательно 2 варианта, либо переносить логику удаления фотографии по нажатию на кнопку cancel в другое место, либо писать 2 разных экрана. Так же на этом экране плохо видно содержимое, не понятно, что помимо фото на нем должно отображаться и в каком виде (В обоих случаях перехода)
10 -
Внимание, этот экран используется в двух сценариях - переход из навигации и переход из настроек. В первом случае по клику переходим на выбранный элемент, во втором - возвращаемся в настройки, передав выбранный элемент. Возможно проще реализовать два таких экрана с разным функционалом.
Не вижу перехода на этот экран из настроек, и не очень понял, зачем в случае перехода на него из настроек возвращать элемент.
11 - "ок" = заменяем фото на новое, возвращаемся на экран навигации с обновлением фото.
Что делать, если к прежнему фото были добавлены предметы и рамки под них?
12 - Пожалуйста, в ТЗ используйте одинаковые название кнопок и экранов, очень сложно орентироваться.
13 - Исходя из того, что я вижу, получается довольно сложное приложение, здесь работы не на один месяц это точно. В связи с этим вопрос, распологаете ли вы нужными средствами для реализации данного проекта если он не коммерческий. Месяц будет стоить около 40-50т.р. Точное время я пока назвать не могу, так как еще есть много вопросов, возможно в конечном итоге я смогу назвать конерктную сумму, но с учетом работы которую придется проделать, она будет не маленькая. Подумайте пожалуйста над этим вопросом тоже, и если вы готовы, то я продолжу изучение вашей идеи.
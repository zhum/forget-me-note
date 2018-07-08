# forget-me-note

Проект органайзера "что где лежит". Идея работы программы - чтобы запомнить в каком ящике/столе/полке/шкафу какие вещи лежат, сфотографируйте их и отметьте вещи. Можно добавлять фото с текстом (подписью) или только текст. На фото при добавлении новой вещи необходимо отметить её рамкой. Можно добавлять иерархию - сфотографировали шкаф, затем добавили его полки (отметив их на фото шкафа), и т.д.

Тут прототип https://mockup.io/#projects/157161/mockups
Другой (без визуализации связей) - в каталоге prototype.

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

### 1. Navigation

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

  - Добавление, при нажатии переход на экран "Foto".
  - Поиск, при нажатии переход на экран "Search".

### 2. Edit (второй режим Navigation)

  Список переходит в режим перетаскивания, можно переупорядочить элементы.

  Рамки на фото также можно менять - при клике подсвечивается
  соответствующий элемент в списке и появляются кружки на верхнем левом
  и нижнем правом углу, ими можно менять положение и размер соответственно.

  Кнопка "режим" меняет режим на "Delete".

  Вторая кнопка = переход на экран "Update".

  Третья кнопка = переход на экран "Move here".


### 3. Delete (третий режим Navigation)

  Список переходит в режим "удаление", справа от каждого элемента списка
  появлется значок, при нажатии на который элемент удаляется.

  Кнопка "режим" менеят режим на "Navigation".

  При клике на рамку, соответствующий элемент списка подсвечивается.

  Вторая кнопка = переход на экран "Restore".

### 4. Foto

  Сверху - превью фото.

  Далее кнопки "выбрать из галереи" и "сделать фото". Возможны варианты,
  например, вызвать внешнее приложение. Важный момент - фото должно быть
  формата "3х4", т.е. взятое фото нужно обрезать. Предлагается сделать
  это в окне превью (a-la instagram), т.е. оно уже нужного формата и новое
  фото можно в нём двигать, менять масштаб. Что получится в результате
  в окне превью, то и берём.

  Внизу три кнопки:

  - назад
  - пропустить (фото не делается, сразу переход к слеюущему шагу)
  - далее - запомнить фото и переход на экран Foto 2.

### 5. Foto 2

  Сверху - фото родителя. На нём предлагается обозначить рамку текущего
  элемента. Если у родителя нет фото, то это поле отсутствует.

  Ниже - поле для ввода названия + выпадающий список подсказок.
  В подсказках слова из таблицы Suggestions + очередной номер (например,
  Room 3). После выбора из списка можно отредактировать имя. Номер в
  таблице меняется, если после успешного добавления (ок на Foto 2) имя
  совпадает с одной из строк таблицы + очередной номер.

  Добавленный элемент добавляется в список и на фото (если есть). 
  Если родительского фото нет, то в конец списка, если есть, то в
  порядке сортировки на фото (сверху-вниз, слева-направо). Порядок
  сортировки фиксируется в БД (см. поле weight), после добавления у всех
  "потомков" это поле обновляется.

  При создании рамки действует "прилипание" - если координата угла
  рамки X=a и хотя бы у одного существующего потомка у одного из углов
  рамки координата X=a+d, где |d| < порога прилипания (задаётся в
  настройках), то a делается равным a+d. Иначе говоря, углы рамок
  автоматически выравниваются по добавленным ранее рамкам. Это должно
  быть отключаемо, на экране добавления рамки нужно добавить галочку "прилипание".

  Внизу кнопки - назад и ОК. Кнопка ОК сохраняет все введённые данные
  в БД, обновляет Suggestions, если нужно, и переходит на страницу
  Navigation родителя.


### 6. Search

  Вверху - листаемый (справа-налево) список всех фото. Под текущим фото -
  подпись и родитель. При переходе на этот экран текущее фото - элемент,
  с которого был переход.

  Ниже - список всех элементов в иерархическом порядке. При выборе фото
  вверху в списке подсвечивается (и если надо - перематывается похиция
  на него) выбранный элемент. И наоборот, при выборе элемента в списке,
  на его фото перематывается верхний список.

  Внизу - две кнопки "назад" и "ок". По "ок" происходит переход на новый
  экран "Navigation" выбранного элемента.

  **Замечание** при импорте на экране "preferences" есть возможность
  импорта в выбранного родителя. Возможно, этот экран можно использовать и там.

### 7. Move here

  Очень схож с экраном "Search". Возможно, стоит реализовать их одним
  экраном.

  Разница в поведении - при нажатии "ок" происходит перемещение элемента,
  с которого был переход, в выбранный элемент (в конец списка, рамка
  не меняется) и происходит переход в выбранный элемент.

### 8. Restore

  Список вверху содержит все удалённые элементы (возможно, стоит указать
  и родителя). Переключатель внизу (возможны варианты другой реализации)
  указывает куда восстановить выбранные элементы - к исходным родителям
  или в элемент, из которого был переход.

  Если родитель какого-то элемента удалён и не восстанавливается сейчас,
  то восстанавливаем его в текущий элемент в конец списка. Если родитель
  в списке на восстановление, то откладываем восстановление этого элемента (помещаем в конец списка восстанавливаемых).

  "ОК" и "Cancel" выполняют или отклоняют операцию восстановления и
  делают переход на экран "Navigation" элемента из которого был переход.

### 9. Update

  Производится новое фото, если нажимается "ок", старое фото элемента заменяется им.

### 10.  Настройки:

  - цвет рамки
  - порог прилипания
  - список имён, предлагаемых при добавлении
  - кнопка "стереть удалённые" (все удалённые элементы и их фото удаляются совсем)
  - кнопка export - БД экспортируется в csv и вместе со всеми фото архивируется в zip
  - кнопка import - импорт из zip, старые данные удаляются
  - кнопка import add - добавление новых элементов из zip как потомка (выбирается его родитель через экран "Search")


## Общие замечания

При добавлении элемента можно ввести подпись вручную, а можно выбрать из выпадающего списка (и отредактивать потом).
Например, по умолчанию в списке будут "Комната 1", "Шкаф 1", "Полка 1".

Если пользователь выбирает "Комната 1", он может отректировать это имя.
Если он оставляет его таким же, то в следующий раз в списке будет "Комната 2".
Если пользователь удаляет элемент, то производится проверка, не нужно ли скорректировать номер последнего предложения (например, добавили "Комната 5", а потом удалили, в списке снова появится "Комната 5", вместо 6).

Создание/редактирование рамок на фото предлагается сделать перетаскиванием
верхнего левого и нижнего правого углов. Эти углы можно выделить визуально кружками.

В режиме создания/редактирования рамок нужно предусмотреть возможность
увеличить/уменьшить масштаб фото, чтобы на небольшом экране телефона можно было
выделить маленькую область.


## Переходы, не отмеченные в прототипе

### Navigation

- "^ UP ^" = (может быть иное обозначение, это - рабочее) смена экрана на Navigation родительского элемента.
- элемент из списка или клик на рамке на фото = переход на экран Navigation соответствующего элемента.

### Экран "Search/Move here"

- клик по элементу = подсветка его в списке и показ его фото. Если фото
  нет, показываем фото родителя с посветкой элемента. Если у родителя
  нет фото (или это корневой элемент, т.е. нет родителя) - показываем "стандартную картинку" "No photo..."

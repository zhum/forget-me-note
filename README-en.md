# Note for developer

This project is preferred to be implemented with portable framework like Cordova or Ionic. Result shold be presented as source code + full dependences list.

Please, read [NODES-en.md] for notes about UnforgettableDog3 directory, containing AndroidStudio project.

# forget-me-note

Android-based organizer application project "where does it lie". The idea of the program - to remember which drawer/desk/shelf/room which things are lying. Just take a picture of them in application and mark things. You can add a photo with text (title) or just text. At the photo, when adding a new thing, you need to mark it with a frame. You can add a hierarchy - photographed the cabinet, then added its shelves (noting them in the cabinet photo), etc.
To find some thing - press search in app and seek it in a list or by typing the name. Then you'll be pointed to desired thind place photo. If you stlii cannot remember the place by photo and title, just go one level up, to see where this photo was taken, and so on.

Here the prototype is https://mockup.io/#projects/157161/mockups
Another (without link visualization) is in the 'prototype' directory.

The word "element" in this text mostly denotes a thing or place (room, shelf, etc.) that you need to remember.

An element can have a photo (or miss it) and must have a name
(not unique) and "parent" - the place where he is.

Also, the element has the coordinates and the size of its frame on the parent photo,
if the parent does not have a photo, then the coordinates are (0,0), and the dimensions (50,50).

Also the element has the flag "deleted", if it is not 0, then the element does not appear in the parent list and search. It can be restored (see screen "Restore").

The element has an index in the parent list, by this index the elements of the list are sorted.

The photos are stored in one directory and all have a name of the form fmnote-XXXXXX.jpg,
where XXXXXX is the number with leading zeros. All photos are in 3x4 format
(it is cut off at photographing, the user chooses what remains,
a-la instagram or automatically).


## Database format:

### Items table:

- int id             # identifier, primary key, uniq
- int parent         # parent identifier (0 for root)
- string title       # thing or place title
- int x,y,w,h        # frame coordinates and size
- int photo          # photo number (0, if missed)
- int weight         # index in parent list
- int deleted        # flag for deleted items
- timedate created   # time and date of creation
- timedate updated   # time and date of last update or deletion

### Suggestions table:

- int id             # identifier, primary key, uniq
- string name        # suggested name
- int last           # last index of this suggestion


## Screens description and current thoughts:

### 1. Navigation

  This screen has three "modes": Navigation, Edit, Delete. Can be separated
  on three frames, if so it is more convenient. In fact, when the mode changes, the
  only a set of buttons at the bottom are replaced and a mode of work with the list / photo is changed.

  In Navigation mode, the mode button leads to the Edit mode.

  Common elements for all three modes:

  - The name of the element + the button for editing.
  - Settings button.
  - A list of text elements, if a photo was attached,
    then it is displayed at the top (maybe as the first element of the list?).
  - The top element of the list = return to the "parent" (the main "parent" does not have it).
  - At the photo, all the elements are marked with frames. When you click an item in the list
    or the contents of its frame, go to the page of the element.
  - If there are no sub-elements and no photo, then only
    the item name and the return button to the parent (and the suggestion to add photos / items?).
  - Bottom = the control buttons. First = change of mode.

  The Navigation screen has two additional bottom buttons:

  - Addition, when clicked go to the "Photo" screen.
  - Search, when pressed, go to the "Search" screen.
  
### 2. Edit (second mode of Navigation)

  The list goes into drag-and-drop mode, you can reorder the items.

  The frame in the photo can also be changed - when clicked
  The corresponding element in the list and the circles appear on the upper left
  and the lower right corner, they can change the position and size accordingly.

  The "mode" button changes the mode to "Delete".

  Second button = go to the "Update" screen.

  Third button = go to the "Move here" screen.

### 3. Delete (third mode of Navigation)

  The list goes into the "delete" mode, to the right of each list item
  an icon appears, when you click on which item is marked as deleted.

  The "mode" button changes the mode to "Navigation".

  When you click on a frame, the corresponding list item is highlighted.

  Second button = go to the "Restore" screen.

### 4. Photo

  On the top - a preview of the photo.

  Next, the buttons "select from the gallery" and "take a photo." There are options,
  for example, call an external application, if this way is more easier.
  Important point - the photo should be
  format "3x4", i.e. the taken photo needs to be cut off. It is proposed to do
  this is in the preview window (a-la instagram), i.e. it's already the right format
  and you can move the photo inside preview, change the scale. What will happen as a result
  in the preview window, that we take.

  There are three buttons at the bottom:

  - "back"
  - "skip" (photo is not done, immediately go to the next step)
  - "go ahead" - remember the photo and go to the screen Photo 2.

### 5. Photo 2

  On the top - a photo of the parent. On it the frame of the current
  element is drawed. If the parent does not have a photo, then this field is missing.

  Below is the field for entering the name + drop-down list of suggestions.
  Suggestions are words from the Suggestions table + the next number (for example,
  Room 3). After selecting from the list, you can edit the name. Room in
  the table changes if after the successful addition (ok on Photo 2) the name
  coincides with one of the rows of the table + the next number.

  The added item is added to the list and to the photo (if any) as a frame.
  If there is no parent photo, then it is added at the end of the list,
  if there is, then in the sort order on the photo (top-down, left-to-right). Order of
  sorting is fixed in the database (see the weight field), after adding all
  "childs" this field is updated for all list elements.

  When creating a frame, "sticking" is working - if the corner coordinate
  X = a and at least one existing element in list has one its
  frame coordinate X = a + d, where |d| is smaller than the threshold (given in
  settings), then a is made equal to a + d. In other words, the corners of the frames
  automatically aligned with previously added frames. This behavior, can be
  turned off by checkbox below.

  At the bottom - two buttons: back and OK. OK button saves all entered data
  in the database, updates the Suggestions, if necessary, and goes to the page
  Navigation parent.

### 6. Search

  On the top - a flip-through (from right to left) list of all the photos.
  Under the current photo - title and parent title. When you go to this screen,
  the current photo element, from which there was a transition, is selected.

  Below is a list of all the items in a hierarchical order. When selecting photos
  at the top, the corresponding element in the list is highlighted
  (and if necessary - rewind to it). And vice versa, when you select an item in the list,
  its photo is selected and rewound at the upper list.

  At the bottom there are two buttons "back" and "ok". By "ok" there is a
  transition to a new one "Navigation" screen of the selected item.

  **Note** when importing the "preferences" screen, there is a possibility
  import to the selected parent. Perhaps this screen can also be used there.

### 7. Move here

  Very similar to the "Search" screen. Perhaps it is worth implementing it as separated
  screen.

  The difference in the behavior - when you click "ok" you move the element,
  from which the transition was made, to the selected item as new child (at the
  end of the list, the frame does not change) and a transition to the selected item occurs.

### 8. Restore

  The list at the top contains all deleted items (possibly, it is necessary to specify
  the parent too). Switch at the bottom (other implementation options are possible)
  specifies where to restore the selected items - to the original parents
  or to the element from which the transition was made.

  If the parent of an item is deleted and is not restored now,
  then restore it to the current item at the end of the list. If the parent
  is in the list to restore, then postpone the restoration of this element
  (put the end of the list of restoring items).

  "OK" and "Cancel" perform or reject the restore operation and
  make a transition to the "Navigation" screen of the element from which the
  transition was made.

### 9. Update

  A new photo is taken. If "ok" is pressed, the old photo of the element is replaced by it.

### 10.  Preferences:

  - the color of the frame
  - stickiness threshold
  - list of names offered when adding (Suggestions)
  - "erase deleted" button (all deleted elements and their photos are deleted at all)
  - "export" button - the database is exported to csv and together with all the photos is archived in zip-file
  - "import" button - import from zip-file, old data is deleted
  - "import add" button - add new items from a zip-file as a childs (parent is selected via the "Search" screen or its clone)

## Common thought

When you add an element, you can enter the title manually, or you can select from the drop-down list (and then edit it later).
For example, by default, the suggestions list will contain "Room 1", "Cabinet 1", "Shelf 1".

If the user selects "Room 1", he can change this name.
If he leaves it the same, then the next time in the list will be "Room 2".
If the user deletes the item, then it is checked whether it is necessary to
correct the number of the last sentence (for example, added "Room 5" and then
deleted, "Room 5" instead of 6 will appear in the list again). This check may be
skipped in first implementation.

Creating / editing frames on the photo is suggested to be done by dragging
upper left and lower right corners. These corners can be distinguished visually by circles.

In the mode of frame creation/edition, it is necessary to provide the possibility
to zoom the photo to be possible to select a small area on a small phone screen.

## Transitions, missed in prototype

### Navigation

- "^ UP ^" = (this is a working name, can be better) go to Navigation screen of the parent element.
- click on an item from the list or click on the frame in the photo = go to the Navigation screen of the corresponding item.

### Screen "Search/Move here"

- click on an item = highlight it in the list and display its photo. If the photo
  is missed, show the parent photo with the item's highlight. If the parent
  has no photo (or this is the root element, i.e. there is no parent) - show "standard picture" "No photo ..."
  

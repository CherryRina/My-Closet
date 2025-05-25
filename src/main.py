from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication, QWidget, QVBoxLayout, QStackedWidget, QFileDialog, QButtonGroup
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt 
from PyQt5 import QtCore
from home_ui import Ui_MainWindow
from items_template_ui import Ui_ItemsTemplateWindow 
from add_item_ui import Ui_AddItem
from item_added_ui import Ui_ItemAddedWindow
from dotenv import load_dotenv
import sqlite3
import shutil
import sys
import os

# load private parameters
load_dotenv()

class MainPage(QMainWindow, Ui_MainWindow):
    """ Main Page - page 0 """   
    def __init__(self, stacked_widget):
        super().__init__()  # valling parents init init 
        self.setupUi(self)  # call setupUi to build the UI from the .ui layout
        self.stacked_widget = stacked_widget # give this page a number
        
        # action for items buttons
        self.tops_button.clicked.connect(lambda: self.open_page_by_index(1))
        self.pants_button.clicked.connect(lambda: self.open_page_by_index(2))
        self.skirts_button.clicked.connect(lambda: self.open_page_by_index(3))
        self.dresses_button.clicked.connect(lambda: self.open_page_by_index(4))
        self.accessories_button.clicked.connect(lambda: self.open_page_by_index(5))
        self.shoes_button.clicked.connect(lambda: self.open_page_by_index(6))
        self.add_item_button.clicked.connect(lambda: self.open_page_by_index(7))

    def open_page_by_index(self, page_index):
        # opens a page by its index
        self.stacked_widget.setCurrentIndex(page_index)



class ItemTemplatePage(QMainWindow, Ui_ItemsTemplateWindow):
    """ template page for pages 1-6 """
    def __init__(self, page_name: str, stacked_widget, images_path: str):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget
        # vars that differ from page to page
        self.page_name = page_name.lower()
        self.image_path = images_path
        self.page_title.setText(page_name) 
        # image and layout related vars
        self.scroll_area_widget_contents = self.findChild(QWidget, "scroll_area_widget_contents")
        self.grid_layout = self.scroll_area_widget_contents.layout()
        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.load_images()

        # action for buttons
        self.main_page_button.clicked.connect(self.go_to_main_menu)

    # actions
    def go_to_main_menu(self):
        # go to main page (number 0)
        self.stacked_widget.setCurrentIndex(0)

    @staticmethod
    def crop_center_square(pixmap):
        # method crops image avoiding its stretch
        width = pixmap.width()
        height = pixmap.height()
        side = min(width, height)
        x = (width - side) // 2
        y = (height - side) // 2
        return pixmap.copy(x, y, side, side)

    def load_images(self): 
        # method loads images to page by dir path
        images = [file for file in os.listdir(self.image_path) if (file.endswith((".png", ".jpg", ".jpeg", ".jfif")))]
        row, col = 0, 0
        for index, image in enumerate(images):
            # creation of the pixmap
            pixmap = QPixmap(os.path.join(self.image_path, image))
            # crop image
            cropped = self.crop_center_square(pixmap)
            resized = cropped.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # creation of the lable
            lable = QLabel()
            lable.setPixmap(resized)
            lable.setFixedSize(200, 200)
            lable.setScaledContents(True)
            # manage grid
            self.grid_layout.addWidget(lable, row, col)
            col += 1
            # max 3 images in a row
            if col == 3: 
                row += 1
                col =0



class AddItemPage(QMainWindow, Ui_AddItem):
    """ Add item page - page 7 """
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget

        # create the button group
        self.category_button_group = QButtonGroup(self)

        # add each radio button to the group
        self.category_button_group.addButton(self.tops_rad_button)
        self.category_button_group.addButton(self.pants_rad_button)
        self.category_button_group.addButton(self.skirts_rad_button)
        self.category_button_group.addButton(self.dresses_rad_button)
        self.category_button_group.addButton(self.accessories_rad_button)
        self.category_button_group.addButton(self.shoes_rad_button)

        # action for buttons
        self.cancel_button.clicked.connect(self.go_to_main_menu)
        # self.upload_photo_button.clicked.connect(self.upload_image)
        self.submit_button.clicked.connect(self.add_item_to_table)

    def go_to_main_menu(self):
        # go to main page (number 0)
        self.stacked_widget.setCurrentIndex(0)

    def item_added_menu(self):
        # item added sucessfuly menu
        self.stacked_widget.setCurrentIndex(8)

    def selected_radio_button(self):
        # finds category by radio button 
        selected_button = str(self.category_button_group.checkedButton().text())
        return selected_button
    
    def copy_image_to_category_dir(self, src_image_path, category):
        # copies image from original path to projects resources dir by category
        print(f"------DEBUG_2: {src_image_path}")
        files_name = os.path.basename(src_image_path)
        print(files_name)
        temp = files_name.split('\\')[-1]
        print(temp)
        dst_image_path = os.path.join(base_path, 'resources', category, files_name)
        shutil.copy(src_image_path, dst_image_path)

    def add_item_to_table(self):
        # collect data from user input
        # copy picture to category dir
        category = self.selected_radio_button()
        src_image_path = self.upload_image()
        self.copy_image_to_category_dir(src_image_path, category)
        item_dict = {
            'image_name': '/home/image', 'item_id': 0,
            'name': self.name_input.text(), 'color': self.color_input.text(), 'size': self.size_input.text(), 
            'price': self.price_input.text(), 'shop': self.shop_input.text(), 'category': category, 
            'hashtags': self.hashtag_input.text()
            }

        # create item object and sent into DB
        item = ItemsTable()
        item.insert_item_to_table(item_dict)
        # clear add item menu
        # reload the db so items will be shown
        self.item_added_menu()

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",                                                                     # window title
            QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.PicturesLocation),     # starting dir for dialog
            "Image Files (*.png *.jpg *.jpeg *.jfif)"                                           # visible files format
            )
        print(f"------DEBUG_1: {file_path}")
        return file_path
    
    



class ItemAddedPage(QMainWindow, Ui_ItemAddedWindow):
    """ opens when item is added to "items" table - page 8 """
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget

        # action for buttons
        self.main_page_button.clicked.connect(self.go_to_main_menu)
        
    def go_to_main_menu(self):
        # go to main page (number 0)
        self.stacked_widget.setCurrentIndex(0)




class SQLiteTables():
    """ template for all three SQLite tables """
    _connections = {}  # shared connections
    
    def __init__(self, table_name):
        # if connection doesnt exist - add it to _onnections
        if table_name not in self._connections:
            self._connections[table_name] = sqlite3.connect(f"{table_name}.db")
        # connect to table 
        self.connection = self._connections[table_name]
        self.cursor = self.connection.cursor()



class ItemsTable(SQLiteTables):
    """ all items table """
    def __init__(self):
        super().__init__(table_name='all_items')

    def create_table(self):
        # creates table
        # ADD: check if table exists
        with self.connection:
            self.cursor.execute("""CREATE TABLE items (
                    image_name,
                    item_id number,
                    name text,
                    color text,
                    size text,
                    price text,
                    shop text,
                    category text,
                    hashtags text
                    )""")
    
    def insert_item_to_table(self, item_dict):
        # inserts object data into table
        # self.create_table()
        with self.connection:
            self.cursor.execute("INSERT INTO items VALUES (:image_name, :item_id, :name, :color, :size, :price, :shop, :category, :hashtags)", item_dict)



if __name__ == '__main__':
    app = QApplication(sys.argv)

    # QStackedWidget: container that holds multiple pages but showes only one at a time
    stacked_widget = QStackedWidget()

    # define base path ans a path
    projects_env_path = os.getenv("PROJECTS_PATH")
    base_path = os.path.expanduser(projects_env_path)

    # creating objects of all pages
    main_page = MainPage(stacked_widget)
    tops_page = ItemTemplatePage(page_name="tops", stacked_widget=stacked_widget, images_path=os.path.join(base_path, 'resources', 'tops'))
    pants_page = ItemTemplatePage(page_name="pants", stacked_widget=stacked_widget, images_path=os.path.join(base_path, 'resources', 'pants'))
    skirts_page = ItemTemplatePage(page_name="skirts", stacked_widget=stacked_widget, images_path=os.path.join(base_path, 'resources', 'skirts'))
    dresses_page = ItemTemplatePage(page_name="dresses", stacked_widget=stacked_widget, images_path=os.path.join(base_path, 'resources', 'dresses'))
    accessories_page = ItemTemplatePage(page_name="accessories", stacked_widget=stacked_widget, images_path=os.path.join(base_path, 'resources', 'accessories'))
    shoes_page = ItemTemplatePage(page_name="shoes", stacked_widget=stacked_widget, images_path=os.path.join(base_path, 'resources', 'shoes'))
    add_item_page = AddItemPage(stacked_widget)
    item_added = ItemAddedPage(stacked_widget)

    # adding all pages into stacked_widget 0-10
    stacked_widget.addWidget(main_page)
    stacked_widget.addWidget(tops_page)
    stacked_widget.addWidget(pants_page)
    stacked_widget.addWidget(skirts_page)
    stacked_widget.addWidget(dresses_page)
    stacked_widget.addWidget(accessories_page)
    stacked_widget.addWidget(shoes_page)
    stacked_widget.addWidget(add_item_page)
    stacked_widget.addWidget(item_added)

    stacked_widget.setFixedSize(800, 600)
    stacked_widget.show()

    # exit app
    sys.exit(app.exec_())
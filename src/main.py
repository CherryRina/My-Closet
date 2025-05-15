from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication, QWidget, QVBoxLayout, QStackedWidget
from home_ui import Ui_MainWindow
from items_template_ui import Ui_ItemsTemplateWindow 
from add_item_ui import Ui_AddItem
from item_added_ui import Ui_ItemAddedWindow
import sqlite3
import sys



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
    def __init__(self, page_name: str, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget
        self.page_name = page_name.lower()

        # dynamic page load
        self.page_title.setText(page_name)  # set lable by page name
        # TODO: add images - show_all_item_images()

        # action for buttons
        self.main_page_button.clicked.connect(self.go_to_main_menu)
        self.show_all_item_images()

    def go_to_main_menu(self):
        # go to main page (number 0)
        self.stacked_widget.setCurrentIndex(0)

    def show_all_item_images(self):     # <------------------------------------------------------- Come back gere !!
        items_table = ItemsTable()
        items_table.cursor.execute("SELECT image_path FROM items WHERE category=:page_category", {'page_category': self.page_name})
        result = items_table.cursor.fetchall()
        paths_list = []
        for row in result:
            paths_list.append(row[0])

        # DEBUG:
        print(f" DEBUG: {paths_list}")



class AddItemPage(QMainWindow, Ui_AddItem):
    """ Add item page - page 7 """
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget

        # action for buttons
        self.cancel_button.clicked.connect(self.go_to_main_menu)
        self.submit_button.clicked.connect(self.add_item_to_table)

    def go_to_main_menu(self):
        # go to main page (number 0)
        self.stacked_widget.setCurrentIndex(0)

    def add_item_to_table(self):
        # collect data from user input
        item_dict = {
            'image_path': '/home/image', 'item_id': 0,
            'name': self.name_input.text(), 'color': self.color_input.text(), 'size': self.size_input.text(), 
            'price': self.price_input.text(), 'shop': self.shop_input.text(), 'category': 'shoes', 
            'hashtags': self.hashtag_input.text()
            }

        # create item object and sent into DB
        item = ItemsTable()
        item.insert_item_to_table(item_dict)
        self.item_added_menu()
    
    def item_added_menu(self):
        # item added sucessfuly menu
        self.stacked_widget.setCurrentIndex(8)



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
                    image_path,
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
            self.cursor.execute("INSERT INTO items VALUES (:image_path, :item_id, :name, :color, :size, :price, :shop, :category, :hashtags)", item_dict)



if __name__ == '__main__':
    app = QApplication(sys.argv)

    # QStackedWidget: container that holds multiple pages but showes only one at a time
    stacked_widget = QStackedWidget()

    # creating objects of all pages
    main_page = MainPage(stacked_widget)
    tops_page = ItemTemplatePage(page_name="Tops", stacked_widget=stacked_widget)
    pants_page = ItemTemplatePage(page_name="Pants", stacked_widget=stacked_widget)
    skirts_page = ItemTemplatePage(page_name="Skirts", stacked_widget=stacked_widget)
    dresses_page = ItemTemplatePage(page_name="Dresses", stacked_widget=stacked_widget)
    accessories_page = ItemTemplatePage(page_name="Accessories", stacked_widget=stacked_widget)
    shoes_page = ItemTemplatePage(page_name="Shoes", stacked_widget=stacked_widget)
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
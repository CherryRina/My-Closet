from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication, QWidget, QVBoxLayout, QStackedWidget
from main_ui import Ui_MainWindow
from items_template_ui import Ui_ItemsTemplateWindow 
from add_item_ui import Ui_AddItem
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
    def __init__(self, new_title: str, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget

        # change lable text by page name
        self.page_title.setText(new_title)

        # action for buttons
        self.main_page_button.clicked.connect(self.go_to_main_menu)

    def go_to_main_menu(self):
        # go to main page (number 0)
        self.stacked_widget.setCurrentIndex(0)

    def show_all_item_images(self):
        # shows all images of that item
        pass



class AddItem(QMainWindow, Ui_AddItem):
    """ Add item page - page 7 """
    def __init__(self, stacked_widget):
        super().__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget

        # action for buttons
        self.cancel_button.clicked.connect(self.go_to_main_menu)
        self.submit_button.clicked.connect(self.add_item_to_db)

    def go_to_main_menu(self):
        # go to main page (number 0)
        self.stacked_widget.setCurrentIndex(0)

    def add_item_to_db(self):
        # collect data from user input
        image_path = '-'    # CHANGE IT
        item_id = 0         # CHANGE IT
        name = self.name_input.text()
        color = self.color_input.text()
        size = self.size_input.text()
        price = self.price_input.text()
        shop =self.shop_input.text()
        category = '-'      # CHANGE IT
        hashtags =self.hashtag_input.text()

        # create item object and sent into DB
        item = ItemsTable(image_path=image_path, item_id=item_id, name=name, color=color, size=size, price=price, shop=shop, category=category, hashtags=hashtags)
        item.insert_item_to_table()



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
    def __init__(self, image_path="-", item_id=0, name="-", color="-", size="-", price="-", shop="-", category="-", hashtags="-"):
        super().__init__(table_name='all_items')
        self.image_path = image_path
        self.item_id = item_id
        self.name = name
        self.color = color
        self.size = size
        self.price = price
        self.shop = shop
        self.category = category
        self.hashtags = hashtags
    
    def __str__(self):
        return 

    def create_table(self):
        # creates table
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
    
    def insert_item_to_table(self):
        # inserts object data into table
        self.create_table()
        item_dict = {
            'image_path': self.image_path, 'item_id': self.item_id ,
            'name': self.name, 'color': self.color, 'size': self.size, 
            'price': self.price, 'shop': self.shop, 'category': self.category, 
            'hashtags': self.hashtags
            }
        with self.connection:
            self.cursor.execute("INSERT INTO items VALUES (:image_path, :item_id, :name, :color, :size, :price, :shop, :category, :hashtags)", item_dict)
        
        # DEBUG: print insertion
        self.cursor.execute("SELECT * FROM items WHERE name=:find_name", {'find_name': self.name})
        print(self.cursor.fetchone())


        


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # QStackedWidget: container that holds multiple pages but showes only one at a time
    stacked_widget = QStackedWidget()

    # creating objects of all pages
    main_page = MainPage(stacked_widget)
    tops_page = ItemTemplatePage(new_title="Tops", stacked_widget=stacked_widget)
    pants_page = ItemTemplatePage(new_title="Pants", stacked_widget=stacked_widget)
    skirts_page = ItemTemplatePage(new_title="Skirts", stacked_widget=stacked_widget)
    dresses_page = ItemTemplatePage(new_title="Dresses", stacked_widget=stacked_widget)
    accessories_page = ItemTemplatePage(new_title="Accessories", stacked_widget=stacked_widget)
    shoes_page = ItemTemplatePage(new_title="Shoes", stacked_widget=stacked_widget)
    add_item_page = AddItem(stacked_widget)

    # adding all pages into stacked_widget 0-10
    stacked_widget.addWidget(main_page)
    stacked_widget.addWidget(tops_page)
    stacked_widget.addWidget(pants_page)
    stacked_widget.addWidget(skirts_page)
    stacked_widget.addWidget(dresses_page)
    stacked_widget.addWidget(accessories_page)
    stacked_widget.addWidget(shoes_page)
    stacked_widget.addWidget(add_item_page)

    stacked_widget.setFixedSize(800, 600)
    stacked_widget.show()

    # exit app
    sys.exit(app.exec_())
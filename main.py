import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QLabel, QLineEdit, QPushButton, QMessageBox,
    QTableWidget, QTableWidgetItem, QComboBox, QSpinBox, QDateEdit,
    QDoubleSpinBox, QTabWidget, QScrollArea, QFrame, QGridLayout,
    QHeaderView, QCheckBox, QDialog, QFormLayout, QListWidget,
    QListWidgetItem, QTextEdit, QFileDialog, QSplitter, QRadioButton,
    QButtonGroup, QProgressBar
)
from PyQt6.QtCore import Qt, QDate, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QPixmap, QIcon, QColor, QFont, QCursor
import hashlib
import requests

DB_PATH = Path("trading_app.db")

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.init_db()
    
    def init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                item_id TEXT UNIQUE NOT NULL,
                game TEXT NOT NULL,
                name TEXT NOT NULL,
                item_type TEXT,
                float_value REAL,
                wear_state TEXT,
                pattern INTEGER,
                pattern_rank TEXT,
                stattrak BOOLEAN DEFAULT 0,
                souvenir BOOLEAN DEFAULT 0,
                status TEXT DEFAULT 'pending',
                buy_date DATE,
                buy_currency TEXT DEFAULT 'USD',
                buy_price REAL,
                buy_fee REAL,
                buy_fee_type TEXT,
                buy_marketplace TEXT,
                sell_date DATE,
                sell_currency TEXT,
                sell_price REAL,
                sell_fee REAL,
                sell_fee_type TEXT,
                sell_marketplace TEXT,
                trade_with TEXT,
                profit REAL,
                condition TEXT,
                notes TEXT,
                image_path TEXT,
                image_back_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS stickers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT NOT NULL,
                sticker_name TEXT,
                sticker_image TEXT,
                wear_percent REAL,
                price_at_buy REAL,
                price_at_sell REAL,
                sticker_type TEXT,
                major TEXT,
                autograph BOOLEAN DEFAULT 0,
                FOREIGN KEY (item_id) REFERENCES items(item_id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS charms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT NOT NULL,
                charm_name TEXT,
                charm_image TEXT,
                price_at_buy REAL,
                price_at_sell REAL,
                FOREIGN KEY (item_id) REFERENCES items(item_id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS finds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                game TEXT,
                item_name TEXT,
                float_value REAL,
                pattern INTEGER,
                current_price REAL,
                market_price REAL,
                marketplace TEXT,
                url TEXT,
                is_deleted BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT,
                description TEXT,
                avatar_image TEXT,
                total_price REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS set_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                set_id INTEGER,
                item_id TEXT,
                FOREIGN KEY (set_id) REFERENCES sets(id),
                FOREIGN KEY (item_id) REFERENCES items(item_id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS crafts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT,
                pattern TEXT,
                stickers TEXT,
                price REAL,
                marketplace TEXT,
                image_paths TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                theme TEXT DEFAULT 'light',
                currency TEXT DEFAULT 'USD',
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        self.conn.commit()
    
    def register_user(self, username, password):
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            self.cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                              (username, password_hash))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def authenticate_user(self, username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute('SELECT id FROM users WHERE username = ? AND password_hash = ?',
                          (username, password_hash))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def close(self):
        self.conn.close()

class MainApp(QMainWindow):
    def __init__(self, user_id, db):
        super().__init__()
        self.user_id = user_id
        self.db = db
        self.current_theme = "light"
        self.current_currency = "USD"
        self.games = ["CS2", "RUST", "DOTA2", "TF2"]
        self.marketplaces = ["CS.MONEY", "Skinport", "LIS-SKINS", "Tradeit.gg", "CSFloat",
                            "DMarket", "Swap.GG", "Market CSGO", "Steam", "Buff.163",
                            "Youpin", "Buff Market", "UU 163", "Waxpeer", "ShadowPay",
                            "White.market", "FunPay", "playerok", "TG", "Other"]
        self.currencies = ["USD", "EUR", "RUB", "UYU", "GEL", "USDT", "USDC", "USDP", "LTC"]
        
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("MyTrading")
        self.setGeometry(0, 0, 1400, 800)
        self.setStyleSheet(self.get_theme_stylesheet())
        
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget, 1)
        
        self.trading_page = self.create_trading_page()
        self.finds_page = self.create_finds_page()
        self.sets_page = self.create_sets_page()
        self.trades_page = self.create_trades_page()
        self.crafts_page = self.create_crafts_page()
        self.profit_page = self.create_profit_page()
        self.settings_page = self.create_settings_page()
        self.comparison_page = self.create_comparison_page()
        
        self.stacked_widget.addWidget(self.trading_page)
        self.stacked_widget.addWidget(self.finds_page)
        self.stacked_widget.addWidget(self.sets_page)
        self.stacked_widget.addWidget(self.trades_page)
        self.stacked_widget.addWidget(self.crafts_page)
        self.stacked_widget.addWidget(self.profit_page)
        self.stacked_widget.addWidget(self.settings_page)
        self.stacked_widget.addWidget(self.comparison_page)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def create_sidebar(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame { background-color: #f5f5f5; border-right: 1px solid #e0e0e0; }
            QPushButton { text-align: left; padding: 12px; border: none; background-color: transparent; font-size: 13px; }
            QPushButton:hover { background-color: #e0e0e0; }
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        buttons = [
            ("Trading Table", 0),
            ("Finds", 1),
            ("Sets", 2),
            ("Beautiful Trades", 3),
            ("Crafts", 4),
            ("Trade & Profit", 5),
            ("Comparison", 6),
            ("Settings", 7),
        ]
        
        for text, index in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, i=index: self.stacked_widget.setCurrentIndex(i))
            layout.addWidget(btn)
        
        layout.addStretch()
        
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)
        
        frame.setLayout(layout)
        return frame
    
    def create_trading_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("Game:"))
        game_combo = QComboBox()
        game_combo.addItems(["All"] + self.games)
        filter_layout.addWidget(game_combo)
        
        filter_layout.addWidget(QLabel("Date:"))
        date_combo = QComboBox()
        date_combo.addItems(["All", "Recent", "Old"])
        filter_layout.addWidget(date_combo)
        
        filter_layout.addWidget(QLabel("Price:"))
        price_combo = QComboBox()
        price_combo.addItems(["All", "Higher", "Lower"])
        filter_layout.addWidget(price_combo)
        
        filter_layout.addWidget(QLabel("Currency:"))
        currency_combo = QComboBox()
        currency_combo.addItems(self.currencies)
        currency_combo.currentTextChanged.connect(self.change_currency)
        filter_layout.addWidget(currency_combo)
        
        filter_layout.addStretch()
        
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search items...")
        filter_layout.addWidget(search_input)
        
        layout.addLayout(filter_layout)
        
        add_btn = QPushButton("+ Add Item")
        add_btn.clicked.connect(self.open_add_item_dialog)
        layout.addWidget(add_btn)
        
        self.trading_table = QTableWidget()
        self.trading_table.setColumnCount(6)
        self.trading_table.setHorizontalHeaderLabels(["Status", "Item Info", "Buy", "Sell", "Profit", "Accessories"])
        self.trading_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.trading_table)
        
        widget.setLayout(layout)
        return widget
    
    def create_finds_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        add_btn = QPushButton("+ Add Find")
        layout.addWidget(add_btn)
        
        layout.addWidget(QLabel("Finds section - Coming soon"))
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_sets_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        add_btn = QPushButton("+ Add Set")
        layout.addWidget(add_btn)
        
        layout.addWidget(QLabel("Sets section - Coming soon"))
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_trades_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("<b>Beautiful Trades</b>"))
        layout.addWidget(QLabel("Beautiful Trades section - Coming soon"))
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_crafts_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        add_btn = QPushButton("+ Add Craft")
        layout.addWidget(add_btn)
        
        layout.addWidget(QLabel("Crafts section - Coming soon"))
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_profit_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("<b>Trade & Profit Dashboard</b>"))
        
        stats_layout = QHBoxLayout()
        stats_layout.addWidget(QLabel("Total Profit:"))
        total_profit = QLabel("$0.00")
        total_profit.setStyleSheet("font-weight: bold; color: green;")
        stats_layout.addWidget(total_profit)
        
        stats_layout.addWidget(QLabel("Total Invested:"))
        total_invested = QLabel("$0.00")
        stats_layout.addWidget(total_invested)
        
        stats_layout.addWidget(QLabel("Avg Item Price:"))
        avg_price = QLabel("$0.00")
        stats_layout.addWidget(avg_price)
        stats_layout.addStretch()
        
        layout.addLayout(stats_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_settings_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("<b>Theme</b>"))
        theme_layout = QHBoxLayout()
        
        for i, theme in enumerate(["Light", "Dark", "Black", "Purple-Black"]):
            radio = QRadioButton(theme)
            if i == 0:
                radio.setChecked(True)
            radio.toggled.connect(lambda checked, t=theme: self.change_theme(t) if checked else None)
            theme_layout.addWidget(radio)
        
        layout.addLayout(theme_layout)
        
        layout.addWidget(QLabel("<b>Default Currency</b>"))
        currency_combo = QComboBox()
        currency_combo.addItems(self.currencies)
        currency_combo.currentTextChanged.connect(self.change_currency)
        layout.addWidget(currency_combo)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_comparison_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("<b>Item Comparison</b>"))
        layout.addWidget(QLabel("Comparison section - Coming soon"))
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def open_add_item_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Item")
        dialog.setGeometry(100, 100, 600, 800)
        dialog.setStyleSheet(self.get_theme_stylesheet())
        
        layout = QFormLayout()
        
        game_combo = QComboBox()
        game_combo.addItems(self.games)
        layout.addRow("Game:", game_combo)
        
        item_type = QComboBox()
        item_type.addItems(["Weapon", "Gloves", "Agent", "Music Kit", "Sticker", "Other"])
        layout.addRow("Type:", item_type)
        
        name_input = QLineEdit()
        layout.addRow("Name:", name_input)
        
        float_input = QDoubleSpinBox()
        float_input.setRange(0.01, 1.0)
        float_input.setDecimals(5)
        layout.addRow("Float Value:", float_input)
        
        pattern_input = QSpinBox()
        pattern_input.setRange(0, 1000)
        layout.addRow("Pattern:", pattern_input)
        
        stattrak_check = QCheckBox()
        layout.addRow("StatTrak:", stattrak_check)
        
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addRow(button_layout)
        
        cancel_btn.clicked.connect(dialog.reject)
        save_btn.clicked.connect(dialog.accept)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def change_currency(self, currency):
        self.current_currency = currency
    
    def change_theme(self, theme):
        self.current_theme = theme.lower()
        self.setStyleSheet(self.get_theme_stylesheet())
    
    def get_theme_stylesheet(self):
        if self.current_theme == "light":
            return """
                QWidget { background-color: #ffffff; color: #000000; }
                QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox { border: 1px solid #cccccc; border-radius: 5px; padding: 5px; }
                QPushButton { background-color: #007AFF; color: white; border-radius: 5px; padding: 8px; font-weight: bold; }
                QPushButton:hover { background-color: #0051D5; }
                QTableWidget { border: 1px solid #e0e0e0; }
                QHeaderView::section { background-color: #f5f5f5; padding: 5px; }
            """
        elif self.current_theme == "dark":
            return """
                QWidget { background-color: #1e1e1e; color: #ffffff; }
                QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox { background-color: #2d2d2d; color: #ffffff; border: 1px solid #444444; border-radius: 5px; padding: 5px; }
                QPushButton { background-color: #007AFF; color: white; border-radius: 5px; padding: 8px; font-weight: bold; }
                QTableWidget { background-color: #2d2d2d; color: #ffffff; border: 1px solid #444444; }
            """
        elif self.current_theme == "black":
            return """
                QWidget { background-color: #000000; color: #ffffff; }
                QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox { background-color: #1a1a1a; color: #ffffff; border: 1px solid #333333; border-radius: 5px; padding: 5px; }
                QPushButton { background-color: #007AFF; color: white; border-radius: 5px; padding: 8px; font-weight: bold; }
            """
        else:  # purple-black
            return """
                QWidget { background-color: #1a0f2e; color: #e0e0ff; }
                QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox { background-color: #2d1b4e; color: #e0e0ff; border: 1px solid #6a5acd; border-radius: 5px; padding: 5px; }
                QPushButton { background-color: #7b68ee; color: white; border-radius: 5px; padding: 8px; font-weight: bold; }
            """
    
    def logout(self):
        reply = QMessageBox.question(self, "Logout", "Are you sure?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.close()

class AuthWindow(QWidget):
    def __init__(self, db, app):
        super().__init__()
        self.db = db
        self.app = app
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("MyTrading - Authentication")
        self.setGeometry(100, 100, 400, 350)
        self.setStyleSheet(self.get_light_theme())
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("MyTrading")
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Skin Trading Manager")
        subtitle_font = QFont()
        subtitle_font.setPointSize(11)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #666666;")
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        layout.addWidget(self.username_input)
        
        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        
        self.password_input.returnPressed.connect(self.login)
        
        layout.addSpacing(10)
        
        button_layout = QHBoxLayout()
        
        login_btn = QPushButton("Login")
        login_btn.setMinimumHeight(40)
        login_btn.clicked.connect(self.login)
        button_layout.addWidget(login_btn)
        
        register_btn = QPushButton("Register")
        register_btn.setMinimumHeight(40)
        register_btn.clicked.connect(self.register)
        button_layout.addWidget(register_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Fill in all fields")
            return
        
        user_id = self.db.authenticate_user(username, password)
        if user_id:
            self.app.open_main_app(user_id)
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials")
    
    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Fill in all fields")
            return
        
        if len(password) < 4:
            QMessageBox.warning(self, "Error", "Password min 4 chars")
            return
        
        if self.db.register_user(username, password):
            QMessageBox.information(self, "Success", "Account created! Now login.")
            self.username_input.clear()
            self.password_input.clear()
        else:
            QMessageBox.warning(self, "Error", "Username exists!")
    
    def get_light_theme(self):
        return """
            QWidget { background-color: #ffffff; color: #000000; }
            QLineEdit { border: 1px solid #cccccc; border-radius: 5px; padding: 8px; }
            QPushButton { background-color: #007AFF; color: white; border-radius: 5px; padding: 8px; font-weight: bold; }
            QPushButton:hover { background-color: #0051D5; }
        """

class App(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.db = Database()
        self.auth_window = AuthWindow(self.db, self)
        self.main_window = None
        self.auth_window.show()
    
    def open_main_app(self, user_id):
        self.main_window = MainApp(user_id, self.db)
        self.main_window.show()

if __name__ == "__main__":
    app = App()
    sys.exit(app.exec())

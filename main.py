import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QComboBox, QCheckBox, QRadioButton, QTextEdit, QSlider, QSpinBox, QProgressBar, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
import random
from Baseball_Robo import generate_leg

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create layout
        self.layout = QVBoxLayout()
        
        # Create widgets
        self.title_label = QLabel("Welcome to Robot Parlay")
        self.legs_label = QLabel("How many legs do you want?")
        self.legs_combo_box = QComboBox()
        self.legs_combo_box.addItems(["3", "4", "5"])

        self.league_label = QLabel("What league do you want to bet on?")
        self.league_combo_box = QComboBox()
        self.league_combo_box.addItems(["MLB"])
        
        self.input_label = QLabel("Which team's game do you want to bet on?")
        self.string_input = QLineEdit()
        
        self.submit_button = QPushButton("Start Generating Parlay")
        
        # Add widgets to layout
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.legs_label)
        self.layout.addWidget(self.legs_combo_box)
        self.layout.addWidget(self.league_label)
        self.layout.addWidget(self.league_combo_box)
        self.layout.addWidget(self.input_label)
        self.layout.addWidget(self.string_input)
        self.layout.addWidget(self.submit_button)
        
        # Set the layout
        self.setLayout(self.layout)
        
        # Connect the button to the action
        self.submit_button.clicked.connect(self.handle_submit)

        # variable to store the user input league
        self.user_league = ""
        # Variable to store the user input string
        self.user_team = ""
    
    def handle_submit(self):
        # Store the string input to a variable
        self.user_team = self.string_input.text()
        
        # Get the selected number of legs from the leg combo box
        selected_number = int(self.legs_combo_box.currentText())

        # Get the selected league from the league combo box
        self.user_league = str(self.league_combo_box.currentText())

        # Switch the screen based on the selected number
        if selected_number == 3:
            self.show_screen_for_3()
        elif selected_number == 4:
            self.show_screen_for_4()
        elif selected_number == 5:
            self.show_screen_for_5()

    def close_program(self):
        # This method closes the window
        self.close()
    
    def show_screen_for_3(self):
        self.url = "https://www.mlb.com/" + self.user_team +"/roster/starting-lineups"
        self.legs_generated = 0
        self.players_chosen = []
        self.clear_layout()
        label = QLabel(f"Creating a 3 leg {self.user_league} parlay for the {self.user_team}")
        self.layout.addWidget(label)

        self.first_leg_label = QLabel("")
        self.layout.addWidget(self.first_leg_label)

        self.second_leg_label = QLabel("")
        self.layout.addWidget(self.second_leg_label)

        self.third_leg_label = QLabel("")
        self.layout.addWidget(self.third_leg_label)

        self.spinner = QPushButton("", self)
        self.spinner.setIcon(QIcon("Spinner.png"))
        self.spinner.setIconSize(self.spinner.size())  # Set icon size to button size
        # Set the button size
        self.spinner.resize(100, 100)
        self.layout.addWidget(self.spinner)
        self.spinner.clicked.connect(self.spin_wheel)

        self.coin = QPushButton("", self)
        self.coin.setIcon(QIcon("Coin.png"))
        self.coin.setIconSize(self.coin.size())  # Set icon size to button size
        # Set the button size
        self.coin.resize(100, 100)
        self.layout.addWidget(self.coin)
        self.coin.hide()
        self.coin.clicked.connect(self.flip_coin)

        # Create a close window button
        self.close_button = QPushButton("Done", self)
        self.layout.addWidget(self.close_button)
        self.close_button.hide()

        self.close_button.clicked.connect(self.close_program)
    
    def show_screen_for_4(self):
        self.clear_layout()
        label = QLabel(f"You picked 4! Your string: {self.user_team}")
        self.layout.addWidget(label)
    
    def show_screen_for_5(self):
        self.clear_layout()
        label = QLabel(f"You picked 5! Your string: {self.user_team}")
        self.layout.addWidget(label)

    def spin_wheel(self):
        self.picked = random.randint(1, 18)
        if self.legs_generated == 0:
            self.players_chosen.append(self.picked)
            self.first_leg_label.setText(str(self.picked))
            self.spinner.hide()
            self.coin.show()

        if self.legs_generated == 1:
            while self.picked in self.players_chosen:
                self.picked = random.randint(1, 18)
            self.players_chosen.append(self.picked)
            self.second_leg_label.setText(str(self.picked))
            self.spinner.hide()
            self.coin.show()

        if self.legs_generated == 2:
            while self.picked in self.players_chosen:
                self.picked = random.randint(1, 18)
            self.players_chosen.append(self.picked)
            self.third_leg_label.setText(str(self.picked))
            self.spinner.hide()
            self.coin.show()

    def flip_coin(self):
        coin_flip = random.choice(["Heads", "Tails"])
        if self.legs_generated == 0:
            if coin_flip == "Heads":
                self.first_leg_label.setText(self.first_leg_label.text() + " Heads")
            else:
                self.first_leg_label.setText(self.first_leg_label.text() + " Tails")
            
            self.coin.hide()
            self.legs_generated += 1
            self.spinner.show()
            self.first_leg_label.setText(generate_leg(self.url, self.players_chosen[0], coin_flip))

        elif self.legs_generated == 1:
            if coin_flip == "Heads":
                self.second_leg_label.setText(self.second_leg_label.text() + " Heads")
            else:
                self.second_leg_label.setText(self.second_leg_label.text() + " Tails")
            self.coin.hide()
            self.legs_generated += 1
            self.spinner.show()
            self.second_leg_label.setText(generate_leg(self.url, self.players_chosen[1], coin_flip))

        elif self.legs_generated == 2:
            if coin_flip == "Heads":
                self.third_leg_label.setText(self.third_leg_label.text() + " Heads")
            else:
                self.third_leg_label.setText(self.third_leg_label.text() + " Tails")
            self.coin.hide()
            self.legs_generated += 1
            self.close_button.show()
            self.third_leg_label.setText(generate_leg(self.url, self.players_chosen[2], coin_flip))
            

    def clear_layout(self):
        # Clear the current layout (removes all widgets)
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()


# Run the application
app = QApplication([])
window = MainWindow()
window.show()
app.exec()

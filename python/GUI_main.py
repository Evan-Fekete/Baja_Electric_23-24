import sys
import serial.tools.list_ports
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                             QHBoxLayout, QLCDNumber, QProgressBar, QComboBox)
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt, QSize
from PyQt5.QtGui import QFont, QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import QRect
import math

# Set ESP32 baudrate
ESP32_BAUDRATE = 115200

# Choose port name from user input
def get_port() -> str:
    ports = serial.tools.list_ports.comports()
    portsList = []

    for i in range(len(ports)):
        port = ports[i]
        portsList.append(port)
        print(f"[{i+1}] {port}")
        
    val = input("Select ESP32 Port: ")
    portVar = str(portsList[int(val)-1]).split(" ")[0]
    print(f"Selected Port: {portVar}")
    return portVar

# Creates a serial instance and opens the port
def serial_begin(portVar: str) -> serial.Serial:
    serialInst = serial.Serial()
    try:
        serialInst.baudrate = ESP32_BAUDRATE
        serialInst.port = portVar
        serialInst.open()
    except Exception as e:
        print(f"\nError: {e}")
        exit()
    return serialInst

# Reads the serial data and returns a list
def read_serial(serialInst: serial.Serial) -> list:
    while not serialInst.in_waiting:
        pass
    packet = serialInst.readline()
    return (packet.decode('utf').rstrip('\r\n').split(" "))

class SerialThread(QThread):
    data_signal = pyqtSignal(list)

    def __init__(self, portVar):
        super().__init__()
        self.serialInst = serial_begin(portVar)

    def run(self):
        while True:
            data = read_serial(self.serialInst)
            self.data_signal.emit(data)

class DriverGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Driver GUI")
        self.setFixedSize(QSize(1300, 600))  # Corrected fixed size

        # Create UI elements
        self.gear_lcd = QLabel("P")  # Now a QLabel to display letters
        self.gear_lcd.setFont(QFont("Arial", 100))  # Larger font size
        self.gear_lcd.setAlignment(Qt.AlignCenter)

        self.gas_gauge = QProgressBar()
        self.gas_gauge.setOrientation(Qt.Vertical)
        self.gas_gauge.setRange(0, 100)
        self.gas_gauge.setValue(10)
        self.gas_gauge.setFixedWidth(30)

        self.tire_pressure_label = QLabel("")
        self.tire_pressure_label.setFont(QFont("Arial", 12))

        # Create individual LCDs for each tire
        self.tire_pressure_lcd1 = QLCDNumber()
        self.tire_pressure_lcd1.setDigitCount(2)
        self.tire_pressure_lcd1.setSegmentStyle(QLCDNumber.Flat)
        self.tire_pressure_lcd1.setStyleSheet("QLCDNumber { background-color: white; color: black; }")
        self.tire_pressure_lcd1.setFixedWidth(40)  # Smaller width
        self.tire_pressure_lcd1.setFixedHeight(30)  # Smaller height

        self.tire_pressure_lcd2 = QLCDNumber()
        self.tire_pressure_lcd2.setDigitCount(2)
        self.tire_pressure_lcd2.setSegmentStyle(QLCDNumber.Flat)
        self.tire_pressure_lcd2.setStyleSheet("QLCDNumber { background-color: white; color: black; }")
        self.tire_pressure_lcd2.setFixedWidth(40)  # Smaller width
        self.tire_pressure_lcd2.setFixedHeight(30)  # Smaller height

      

        # Create layouts
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        # Add widgets to layouts
        top_layout.addWidget(self.gear_lcd)  # Add gear to top layout
        bottom_layout.addWidget(self.gas_gauge)
        bottom_layout.addWidget(self.tire_pressure_label)

        tire_pressure_layout = QHBoxLayout()  # Layout for tire pressure LCDs
        tire_pressure_layout.addWidget(self.tire_pressure_lcd1)
        tire_pressure_layout.addWidget(self.tire_pressure_lcd2)
        
        bottom_layout.addLayout(tire_pressure_layout)  # Add tire pressure LCDs to bottom layout

        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        # Set layout for the main widget
        self.setLayout(main_layout)

        # Get port from user
        self.portVar = get_port()

        # Start the serial thread
        self.serial_thread = SerialThread(self.portVar)
        self.serial_thread.data_signal.connect(self.update_ui)
        self.serial_thread.start()

        # Store the data to be used in paintEvent
        self.kph_value = 0
        self.rpm_value = 0

    def update_ui(self, data):
        # Update UI elements with received data
        try:
            # Update data for the speedometers
            self.kph_value = float(data[0])
            self.rpm_value = int(data[1])

            # Update gear display (assuming data[2] is a string)
            self.gear_lcd.setText(data[2])  

            gas_level = int(data[3])  # Assuming gas level is in data[3]
            self.gas_gauge.setValue(gas_level)

            # Update tire pressure LCDs (assuming data[4:] contains tire pressures)
            self.tire_pressure_lcd1.display(float(data[4]))
            self.tire_pressure_lcd2.display(float(data[5]))
            

            self.update()  # Redraw the widget to update the speedometers
        except IndexError:
            print("Data received from ESP32 is incomplete. Skipping update.")

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        # Calculate center of the screen
        center_x = self.width() // 2
        center_y = self.height() // 2

        # KPH Speedometer (adjusted for size and position)
        self.draw_speedometer(painter, self.kph_value, center_x - 300, center_y, 150, "KPH", 0, 240, 20)

        # RPM Speedometer (adjusted for size and position)
        self.draw_speedometer(painter, self.rpm_value, center_x + 300, center_y, 150, "RPM", 0, 8000, 1000)

        # Move the gas gauge to the bottom left
        self.gas_gauge.move(30, self.height() - self.gas_gauge.height() - 20)

        # Change gas gauge color based on level
        gas_level = self.gas_gauge.value()
        if gas_level <= 10:
            self.gas_gauge.setStyleSheet("QProgressBar::chunk { background-color: red; }"
                              "QProgressBar::chunk:horizontal { border: 0px solid #999; text-align: center; }"
                              "QProgressBar { text-align: center; }")

        elif gas_level <= 25:
            self.gas_gauge.setStyleSheet("QProgressBar::chunk { background-color: yellow; }"
                              "QProgressBar::chunk:horizontal { border: 0px solid #999; text-align: center; }"
                              "QProgressBar { text-align: center; }")

        else:
            self.gas_gauge.setStyleSheet("QProgressBar::chunk { background-color: green; }"
                              "QProgressBar::chunk:horizontal { border: 0px solid #999; text-align: center; }"
                              "QProgressBar { text-align: center; }")


    def draw_speedometer(self, painter, value, x, y, radius, label, min_value, max_value, step):
        # Draw the speedometer circle
        painter.setPen(QPen(QColor(0, 0, 0), 3))
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawEllipse(QRect(x - radius, y - radius, radius * 2, radius * 2))

        # Draw ticks and numbers
        painter.setFont(QFont("Arial", 10))
        for i in range(min_value, max_value + 1, step):
            angle = 180 * (i - min_value) / (max_value - min_value)
            tick_x = x + (radius - 10) * math.cos(math.radians(180 + angle))
            tick_y = y + (radius - 10) * math.sin(math.radians(180 + angle))
            painter.drawLine(int(x + radius * math.cos(math.radians(180 + angle))),
                             int(y + radius * math.sin(math.radians(180 + angle))),
                             int(tick_x), int(tick_y))

            number_x = x + (radius - 30) * math.cos(math.radians(180 + angle))
            number_y = y + (radius - 30) * math.sin(math.radians(180 + angle))
            painter.drawText(int(number_x) - 10, int(number_y) + 5, str(i))

        # Draw the needle
        angle = 180 * (value - min_value) / (max_value - min_value)
        needle_len = radius * 0.8
        needle_x = int(x + needle_len * math.cos(math.radians(180 + angle)))
        needle_y = int(y + needle_len * math.sin(math.radians(180 + angle)))
        painter.setPen(QPen(QColor(255, 0, 0), 5))
        painter.drawLine(x, y, needle_x, needle_y)

        # Draw the value (assuming you want to display the value)
        painter.setFont(QFont("Arial", 15))
        painter.drawText(x - 30, y + radius - 75, f"{label}: {int(value)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    driver_gui = DriverGUI()
    driver_gui.show()
    sys.exit(app.exec_())

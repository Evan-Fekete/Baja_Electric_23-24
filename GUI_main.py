from serial_reader import get_port, serial_begin, read_serial

# data variables
fuel_level = 0
speed = 0
rpm = 0
brake_pressure = 0
gear_position = 'P'

def start_GUI() -> bool:
  # TO-DO: Start the GUI
  pass

def update_GUI(fuel_level: int, speed: int, rpm: int, brake_pressure: int, gear_position: int) -> None:
  # TO-DO: Update the GUI with the new data
  pass

if __name__ == "__main__":
  # initialize the serial port
  portVar = get_port()
  serialInst = serial_begin(portVar)
  
  #initialize the GUI
  start_GUI()
  
  while True:
    # Read the serial data and store into variables
    data = read_serial(serialInst)
    fuel_level = int(data[0])
    speed = int(data[1])
    rpm = int(data[2])
    brake_pressure = int(data[3])
    gear_position = data[4]
    
    #update the GUI with new data
    update_GUI(fuel_level, speed, rpm, brake_pressure, gear_position)
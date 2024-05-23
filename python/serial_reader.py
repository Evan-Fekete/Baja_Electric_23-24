import serial.tools.list_ports

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

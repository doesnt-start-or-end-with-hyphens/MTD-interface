import turtle
import time
import serial
import serial.tools.list_ports
import tkinter
from tkinter import simpledialog
import sys

window = turtle.Screen()
painter = turtle.Turtle()
root = window._root
wipe_mode = False

#serarches for the arduino port
arduino_ports = 0
while not arduino_ports:
    arduino_ports = list(serial.tools.list_ports.grep("Arduino*"))

#connects to the port
target_port = arduino_ports[0].device
print(f"Connected to port: {target_port}")
controller = serial.Serial(port=target_port, baudrate=9600)

time.sleep(3) 

controller.write(b"request")

time.sleep(0.1)

if controller.in_waiting > 0:
    print("Connected!")
else:
    print("Exit")
    controller.close()
    sys.exit()

#resets sending and reciving data
controller.reset_input_buffer()
controller.reset_output_buffer()

painter.hideturtle()
painter.speed(30)

#draws teh menu screen
def draw_menu():
    painter.clear()
    painter.penup()
    painter.goto(0, 150)
    painter.write("Morse Training Device", align="center", font=("Impact", 30))
    painter.penup()
    painter.goto(0, 35)
    painter.write("Selected mode:", align="center", font=("Arial", 16))
    painter.penup()

#changes the selected text to the selected option
def selected(selected):
    painter.penup()
    painter.pensize(50)
    painter.goto(-100, 0)
    painter.pencolor("white")
    painter.pendown()
    painter.fd(200)
    painter.penup()
    painter.goto(0, 0)
    painter.pencolor("black")
    if selected == 1:
        painter.write("Test output", align="center", font=("Arial", 16))
    elif selected == 2:
        painter.write("Simple readback", align="center", font=("Arial", 16))
    elif selected == 3:
        painter.write("Advanced readback", align="center", font=("Arial", 16))
    elif selected == 4:
        painter.write("Test input", align="center", font=("Arial", 16))
    elif selected == 5:
        painter.write("PC readback", align="center", font=("Arial", 16))
    elif selected == 6:
        painter.write("PC writeback", align="center", font=("Arial", 16))
    elif selected == 7:
            painter.write("Exit interface", align="center", font=("Arial", 16))

#sets screeen for test output
def test_output():
    painter.clear()
    painter.penup()
    painter.goto(0, 150)
    painter.write("Test output", align="center", font=("Impact", 30))
    painter.penup()
    painter.goto(0, 120)
    painter.write("Use the large silver knob", align="center", font=("Arial", 16))
    painter.goto(0, 100)
    painter.write("to tune the speed of the readouts.", align="center", font=("Arial", 16))

#sets screeen for simple readback
def simple_readback():
    painter.clear()
    painter.penup()
    painter.goto(0, 150)
    painter.write("Simple readback", align="center", font=("Impact", 30))
    painter.penup()
    painter.goto(0, 120)
    painter.write("Listen to the morse letter,", align="center", font=("Arial", 16))
    painter.goto(0, 100)
    painter.write("then repeat it back using the black button.", align="center", font=("Arial", 16))

#sets screeen for advanced readback
def advanced_readback():
    painter.clear()
    painter.penup()
    painter.goto(0, 150)
    painter.write("Advanced readback", align="center", font=("Impact", 30))
    painter.penup()
    painter.goto(0, 120)
    painter.write("Listen to the full morse word,", align="center", font=("Arial", 16))
    painter.goto(0, 100)
    painter.write("then repeat it back using the black button.", align="center", font=("Arial", 16))

#sets screeen for pc readback
def pc_readback():
    painter.clear()
    painter.penup()
    painter.goto(0, 150)
    painter.write("PC readback", align="center", font=("Impact", 30))

#sets screeen for test input
def test_input():
    painter.clear()
    painter.penup()
    painter.goto(0, 150)
    painter.write("Test input", align="center", font=("Impact", 30))
    painter.penup()
    painter.goto(0, 120)
    painter.write("Input morse", align="center", font=("Arial", 16))
    painter.goto(0, 100)
    painter.write("and see what's detected.", align="center", font=("Arial", 16))

#sets screeen for pc writeback
def pc_writeback():
    painter.clear()
    painter.penup()
    painter.goto(0, 150)
    painter.write("PC writeback", align="center", font=("Impact", 30))
    painter.penup()
    painter.goto(0, 120)
    painter.write("Listen to the morse,", align="center", font=("Arial", 16))
    painter.goto(0, 100)
    painter.write("write what you hear.", align="center", font=("Arial", 16))

#gets answer from user and sends it to controller
def answer():
    controller.reset_output_buffer()
    controller.reset_input_buffer()
    user_ans = simpledialog.askstring("MTD", "Write the signal you just heard:", parent=root)
    if user_ans:
        controller.write(user_ans.lower().encode())

#displays letter in pc readback mode
def q_letter(letter):
    painter.penup()
    painter.goto(0, 120)
    painter.write("Input the following word in mose:", align="center", font=("Arial", 16))
    painter.goto(0, 100)
    painter.write(letter, align="center", font=("Arial", 16))

#types correct
def correct():
    if wipe_mode:
        painter.penup()
        painter.goto(-150, 125)
        painter.pencolor("White")
        painter.pendown()
        painter.fd(300)
    painter.penup()
    painter.pencolor("Green")
    painter.goto(0, 40)
    painter.write("Way to go! Try the next one.", align="center", font=("Arial", 16))
    time.sleep(2)
    painter.goto(-150, 40)
    painter.pencolor("White")
    painter.pendown()
    painter.fd(300)
    painter.penup()
    painter.pencolor("Black")

#types incorrect
def incorrect():
    if wipe_mode:
        painter.penup()
        painter.goto(-150, 125)
        painter.pencolor("White")
        painter.pendown()
        painter.fd(300)
    painter.penup()
    painter.pencolor("Red")
    painter.goto(0, 40)
    painter.write("Missed that one, Try again!", align="center", font=("Arial", 16))
    time.sleep(2)
    painter.goto(-150, 40)
    painter.pencolor("White")
    painter.pendown()
    painter.fd(300)
    painter.penup()
    painter.pencolor("Black")

#shows the speed when in test output
def write_display(speed):
    painter.goto(150, 250)
    painter.pencolor("White")
    painter.pendown()
    painter.fd(200)
    painter.penup()
    painter.pencolor("Black")
    painter.goto(150, 250)
    painter.write("Listening speed: " + str(speed), font=("Arial", 12, "bold"))
    time.sleep(1)
    controller.reset_input_buffer()

#shows the user what the system decoded
def write_test(detected):
    painter.penup()
    painter.pensize(50)
    painter.goto(-100, 0)
    painter.pencolor("white")
    painter.pendown()
    painter.fd(200)
    painter.penup()
    painter.goto(0, 0)
    painter.pencolor("black")
    painter.write("Detected morse:", align="center", font=("Arial", 16))
    painter.goto(0, -20)
    painter.write(detected, align="center", font=("Arial", 16))

#closes the interface
def finish():
    painter.clear()
    painter.penup()
    painter.goto(0, 150)
    painter.write("Exiting...", align="center", font=("Impact", 30))
    time.sleep(2)
    controller.close()
    sys.exit()

is_connected = False
#runs forever
while True:
    try:
        #only decodes if there is data
        if controller.in_waiting > 0:
            #gets a command
            command = str(controller.readline().decode('utf-8').strip())
            
            if not command:
                continue 

            controller.reset_input_buffer()
            
            #does the respective actions
            if command == "0":
                controller.write(b"request")
            elif command == "1":
                draw_menu()
            #allows command to carry arguments
            elif command[0] == "2":
                payload = command[1:] 
                selected(int(payload))
            elif command[0] == "3":
                payload = command[1:]
                write_display(payload)
            elif command == "4":
                test_output()
            elif command == "5":
                correct()
            elif command == "6":
                incorrect()
            elif command == "7":
                simple_readback()
            elif command == "8":
                advanced_readback()
            elif command == "9":
                wipe_mode = True
                pc_readback()
            elif command[0] == "1" and command[1] == "0":
                payload = command[2:]
                q_letter(payload)
            elif command == "11":
                test_input()
            elif command[0] == "1" and command[1] == "2":
                payload = command[2:]
                write_test(payload)
            elif command == "13":
                pc_writeback()
            elif command == "14":
                answer()
            elif command == "15":
                finish()
            else:
                print("Invalad command: " + command)
                
    #error catching
    except Exception as e:
        print("Device connection lost or error")
        print(e)
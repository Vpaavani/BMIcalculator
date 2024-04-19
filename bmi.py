import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
import socket
from threading import Thread

class ChatClient(QWidget):
    def _init_(self):
        super()._init_()
        self.initUI()
        self.initNetwork()

    def initUI(self):
        self.setWindowTitle('Chat Application')
        self.resize(400, 300)

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)

        self.input_box = QLineEdit()
        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.send_message)

        layout = QVBoxLayout()
        layout.addWidget(self.chat_history)
        layout.addWidget(self.input_box)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def initNetwork(self):
        self.server_ip = '127.0.0.1'
        self.server_port = 5555
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))

        # Start a thread to receive messages from the server
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                self.chat_history.append(message)
            except Exception as e:
                print(e)
                break

    def send_message(self):
        message = self.input_box.text()
        if message:
            self.client_socket.send(message.encode('utf-8'))
            self.input_box.clear()

    def closeEvent(self, event):
        self.client_socket.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_client = ChatClient()
    chat_client.show()
    sys.exit(app.exec_())

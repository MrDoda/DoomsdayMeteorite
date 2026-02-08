import websocket
import threading
import json

from engine.game_objects import GameObjects

class WebSocketSingleton:
    _instance = None
    _lock = threading.Lock()
    _player_2_control_state = None

    def __new__(cls, url):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(WebSocketSingleton, cls).__new__(cls)
                cls._instance._initialize(url)
            return cls._instance

    def _initialize(self, url):
        self.url = url
        self.ws_connected = False  # Flag to track connection status
        self.ws = websocket.WebSocketApp(url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.open_event = threading.Event()
        self.thread = threading.Thread(target=self._run_forever)
        self.thread.daemon = True
        self.thread.start()

    def _run_forever(self):
        try:
            self.ws.run_forever()
        except Exception as e:
            print(f"Failed to connect to WebSocket: {e}")
            self.on_error(self.ws, e)

    def send(self, data):
        if self.ws_connected:  
            try:
                self.open_event.wait()
                self.ws.send(data)
            except Exception as e:
                print(f"Failed to send data: {e}")

    def on_message(self, ws, new_controls):
        
        try:
            new_controls_str = new_controls.decode('utf-8')  
            new_controls_dict = json.loads(new_controls_str)  
            
            if self._player_2_control_state:
                GameObjects().player2.x = new_controls_dict.get("x", GameObjects().player2.x)
                GameObjects().player2.y = new_controls_dict.get("y", GameObjects().player2.y)
                self._player_2_control_state.set_multiple(new_controls_dict)
                
                print(f"Received message: {new_controls_dict}")
                print(f"Actual store:: {self._player_2_control_state.get()}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except AttributeError as e:
            print(f"Error processing message: {e}")

    def on_error(self, ws, error):
        print(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        self.ws_connected = False
        print(f"WebSocket closed with code: {close_status_code}, reason: {close_msg}")

    def on_open(self, ws):
        self.ws_connected = True 
        self.open_event.set()
        try:
            ws.send("Hello, Server!")
        except Exception as e:
            print(f"Failed to send initial message: {e}")
            self.ws_connected = False 

    def set_player_2_control_state(self, pstate):
        self._player_2_control_state = pstate

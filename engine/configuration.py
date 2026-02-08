class Configuration:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
            cls._instance.debug_mode = False
        return cls._instance

    @classmethod
    def toggle_debug_mode(cls):
        cls._instance.debug_mode = not cls._instance.debug_mode
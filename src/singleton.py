from threading import Lock

class SingletonMeta(type):
    """
    Implementierung von Singleton, welche auch mit Threads funktikoniert.
    """
    _instances = {}
    _lock: Lock = Lock()
    """
    Das Lock Ojekt wird genutzt, um die Threads zu synchronisieren, wenn sie das erste Mal auf den Singleton zugreifen.
    """

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
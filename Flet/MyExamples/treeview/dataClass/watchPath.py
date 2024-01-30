class WatchPath:
    """
    WatchPath Class
    """

    def __init__(self, seq=0, ip=None, watch_path=None, ad=None, save_log=None, allow_start=None, allow_end=None):
        self._seq = seq
        self._ip = ip
        self._watch_path = watch_path
        self._ad = ad
        self._save_log = save_log
        self._allow_start = allow_start
        self._allow_end = allow_end

    def __str__(self):
        return f'str : {self._ip} - {self._watch_path}'

    def __repr__(self):
        return f'repr : {self._ip} - {self._watch_path}'
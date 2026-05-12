# data/session.py
_kite = None

def set_kite_session(kite):
    global _kite
    _kite = kite

def get_kite_session():
    return _kite

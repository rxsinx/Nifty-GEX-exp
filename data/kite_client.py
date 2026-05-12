from kiteconnect import KiteConnect
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class KiteClient:
    _instance = None
    _kite = None          # will hold the authenticated KiteConnect object

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def set_kite_instance(self, kite: KiteConnect):
        """Inject an already authenticated KiteConnect instance."""
        self._kite = kite
        self._instruments_cache = None
        self._cache_time = None
        logger.info("Kite client instance set.")

    def _ensure_kite(self):
        if self._kite is None:
            raise RuntimeError("Kite client not initialized. Call set_kite_instance() first.")

    def get_instruments(self, exchange="NFO"):
        """Cache instruments for the day to avoid repeated downloading."""
        self._ensure_kite()
        import time
        now = time.time()
        if self._instruments_cache is None or (now - self._cache_time) > 3600:
            logger.info("Fetching instruments from Kite...")
            instruments = self._kite.instruments(exchange)
            self._instruments_cache = pd.DataFrame(instruments)
            self._cache_time = now
        return self._instruments_cache

    def get_quote(self, symbols):
        """Wrapper for kite.quotes with batch handling."""
        self._ensure_kite()
        if isinstance(symbols, list) and len(symbols) > 500:
            raise ValueError("Maximum 500 instruments per quotes call")
        return self._kite.quotes(symbols)

    def ltp(self, symbols):
        self._ensure_kite()
        return self._kite.ltp(symbols)

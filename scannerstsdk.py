def __init__(self, show_warnings=False, *args, **kwargs):
        """Constructor.

        Args:
            show_warnings (bool, optional): If True shows warnings, if any, when
            discovering devices not respecting the BlueSTSDK's advertising
            data format, nothing otherwise.
        """
        try:
            super(_StoppableScanner, self).__init__(*args, **kwargs)
            self._stop_called = threading.Event()
            self._process_done = threading.Event()
            with lock(self):
                self._scanner = Scanner().withDelegate(_ScannerDelegate(show_warnings))
        except BTLEException as e:
            # Save details of the exception raised but don't re-raise, just
            # complete the function.
            import sys
            self._exc = sys.exc_info() 
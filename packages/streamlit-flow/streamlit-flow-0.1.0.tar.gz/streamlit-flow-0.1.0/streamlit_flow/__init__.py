import streamlit as st
import logging

class App():
    def __init__(self):
        self._page = "main"
        self._args = []
        self._kwargs = {}
        self._pages = {}
    
    def goto(self, page, *args, **kwargs):
        self.next(page, *args, **kwargs)
        st.rerun()

    def next(self, page, *args, **kwargs):
        if page not in self._pages:
            raise ValueError(f"Page {page} not known")
        self._page = page
        self._args = args
        self._kwargs = kwargs

    def go(self):
        st.rerun()

    def show(self):
        page = self._pages[self._page]
        return page(*self._args, **self._kwargs)

    def route(self, name):
        def wrapper(func):
            self._pages[name] = func
            return func
        return wrapper 
        
def initialize(key, default):
    logging.info(list(st.session_state.keys()))
    if key in st.session_state:
        pass
    elif hasattr(default, "__call__"):
        st.session_state[key] = default() 
    else:
        st.session_state[key] = default

    return st.session_state[key]


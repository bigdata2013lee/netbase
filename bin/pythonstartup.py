#! /opt/netbase4/bin/python -W ignore:Python C API version mismatch for module
# -*- coding: UTF-8 -*-  
import readline, rlcompleter; 
readline.parse_and_bind("tab: complete");
def igtk():
    globals()['gtk'] = __import__('gtk');
    globals()['thread'] = __import__('thread');
    gtk.gdk.threads_init();
    thread.start_new_thread(gtk.main, ());
    pass;

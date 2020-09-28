#!/usr/bin/python
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import requests
from random import randint

def random_author():
        url = "http://poetrydb.org/author"
        authors = requests.get(url).json()
        authors_list = authors['authors']
        n = len(authors_list)
        rand_n = randint(0, n-1)
        return authors_list[rand_n]

def random_poetry(author):
        url = "http://poetrydb.org/author/" + str(author)
        poetries = requests.get(url).json()
        n = len(poetries)
        rand_n = randint(0, n-1)
        poetry = poetries[rand_n]
        return poetry

def formatting(poetry):
        author = poetry['author']
        title = poetry['title']
        lines = poetry['lines']
        label = "<span foreground = \"orange\" font_desc=\"Lunchtime Doubly So regular 11\"> "
        label += '\r\t\t' + title + '\t\t\r\r'
        n_lines = len(lines)
        set_cont = False
        if n_lines*15 > 1000:
            lines=lines[:16]
            set_cont = True
        for line in lines:
            label += line + '\r'
        if set_cont:
            label += "\t\t(...continue....)\t\t"
        label += '\r\t\t\t' + author + '\t\t\r\r'
        label += '</span>'
        return label 

        


class Wnd(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, skip_pager_hint=True, skip_taskbar_hint=True)
        #self.set_decorated(False)
        self.set_default_size(400, 200) 
       # self.set_keep_below(True)
        self.set_decorated(False)

        screen = self.get_screen()
        rgba = screen.get_rgba_visual()
        self.set_visual(rgba)
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0,0,0,0))

        self.connect('destroy', lambda x: Gtk.main_quit())

        self.box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        self.box.set_homogeneous(False)

        poetry=random_poetry(random_author())
        formatted_poetry = formatting(poetry)
        n_lines = len(poetry['lines'])
        if n_lines*15 > 1000:
            n_lines = 20;
        y = 1000 - n_lines*13

        self.move(50, y)

        label = Gtk.Label()
        label.set_markup(formatted_poetry)
#        label.set_markup("<span foreground = \"orange\" font_desc=\"Lunchtime Doubly So regular 11\"> Once upon a midnight dreary, while I pondered, weak and weary,\rOver many a quaint and curious volume of forgotten lore\rWhile I nodded, nearly napping, suddenly there came a tapping, \rAs of some one gently rapping, rapping at my chamber door.Tis some visitor, \rI muttered, tapping at my chamber door Only this and nothing more. </span>")
        

        self.box.pack_start(label, True, True, 0)

        self.add(self.box)
        self.abar = Gtk.ActionBar()
        self.box.pack_end(self.abar, False, False, 0)

        #self.build_contents()

        # Finalize the window itself
       # self.set_titlebar(self.headerbar())
        #self.set_title("Foreign Package Installer")
        #self.set_icon_name("system-software-install")
        #self.set_position(Gtk.WindowPosition.CENTER)
        self.show_all()

if __name__ == '__main__':

    mainwin = Wnd()
    Gtk.main()

#window = Gtk.Window(title="Hello World")
#window.
#window.show()
#window.connect("destroy", Gtk.main_quit)
#Gtk.main()

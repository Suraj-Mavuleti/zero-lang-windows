import sys
import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

class ZeroLang(Gtk.Window):
    def __init__(self):
        super().__init__(title="Zero Lang - Ultimate Studio")
        self.set_default_size(1000, 700)
        
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.props.title = ""
        self.header.get_style_context().add_class("hidden-header")
        self.set_titlebar(self.header)
        
        self.setup_css()
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(main_box)
        
        # ================= HEADER =================
        top_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        top_bar.get_style_context().add_class("top-bar")
        main_box.pack_start(top_bar, False, False, 0)
        
        logo = Gtk.Label(label="Z E R O L A N G")
        logo.get_style_context().add_class("logo")
        logo.set_margin_start(20)
        top_bar.pack_start(logo, False, False, 0)
        
        lbl_subtitle = Gtk.Label(label="Global Neural Translator")
        lbl_subtitle.get_style_context().add_class("subtitle")
        lbl_subtitle.set_margin_start(15)
        top_bar.pack_start(lbl_subtitle, False, False, 0)
        
        # ================= WORKSPACE =================
        workspace = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        workspace.get_style_context().add_class("workspace")
        workspace.set_margin_start(30)
        workspace.set_margin_end(30)
        workspace.set_margin_top(30)
        workspace.set_margin_bottom(30)
        main_box.pack_start(workspace, True, True, 0)
        
        # Left Panel (Input)
        input_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        input_box.get_style_context().add_class("panel")
        
        lang_src = Gtk.ComboBoxText()
        lang_src.append_text("Auto-Detect")
        lang_src.append_text("English")
        lang_src.append_text("Spanish")
        lang_src.set_active(0)
        lang_src.get_style_context().add_class("lang-combo")
        input_box.pack_start(lang_src, False, False, 15)
        
        self.text_in = Gtk.TextView()
        self.text_in.get_style_context().add_class("text-area")
        self.text_in.set_wrap_mode(Gtk.WrapMode.WORD)
        self.text_in.get_buffer().set_text("Enter text to translate...")
        
        scroll_in = Gtk.ScrolledWindow()
        scroll_in.add(self.text_in)
        input_box.pack_start(scroll_in, True, True, 0)
        
        btn_mic = Gtk.Button(label="🎤 Start Voice Input")
        btn_mic.get_style_context().add_class("action-btn")
        input_box.pack_start(btn_mic, False, False, 15)
        
        workspace.pack_start(input_box, True, True, 0)
        
        # Middle Control
        mid_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        mid_box.set_valign(Gtk.Align.CENTER)
        
        btn_swap = Gtk.Button(label="⇄")
        btn_swap.get_style_context().add_class("swap-btn")
        mid_box.pack_start(btn_swap, False, False, 0)
        workspace.pack_start(mid_box, False, False, 0)
        
        # Right Panel (Output)
        output_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        output_box.get_style_context().add_class("panel")
        
        lang_dst = Gtk.ComboBoxText()
        lang_dst.append_text("Japanese")
        lang_dst.append_text("French")
        lang_dst.append_text("German")
        lang_dst.set_active(0)
        lang_dst.get_style_context().add_class("lang-combo")
        output_box.pack_start(lang_dst, False, False, 15)
        
        self.text_out = Gtk.TextView()
        self.text_out.get_style_context().add_class("text-area-out")
        self.text_out.set_wrap_mode(Gtk.WrapMode.WORD)
        self.text_out.set_editable(False)
        self.text_out.get_buffer().set_text("翻訳するテキストを入力してください...")
        
        scroll_out = Gtk.ScrolledWindow()
        scroll_out.add(self.text_out)
        output_box.pack_start(scroll_out, True, True, 0)
        
        btn_speak = Gtk.Button(label="🔊 Read Aloud")
        btn_speak.get_style_context().add_class("nav-btn")
        output_box.pack_start(btn_speak, False, False, 15)
        
        workspace.pack_start(output_box, True, True, 0)
        
    def setup_css(self):
        css = b'''
            window { background-color: #030305; }
            .hidden-header { background: #030305; min-height: 0px; padding: 0px; border: none; box-shadow: none; }
            .top-bar { background-color: rgba(8, 10, 16, 0.98); padding: 20px 0px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); }
            .logo { color: #FFFFFF; font-size: 24px; font-weight: 900; letter-spacing: 5px; text-shadow: 0 0 15px rgba(153, 0, 255, 0.6); }
            .subtitle { color: #8B94A5; font-size: 14px; letter-spacing: 1px; }
            .workspace { background: radial-gradient(circle at bottom, #0A0D14, #030305); }
            .panel { background: rgba(255,255,255,0.02); border: 1px solid rgba(153, 0, 255, 0.2); border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); padding: 20px; }
            .lang-combo { background: #050608; color: #FFFFFF; border: 1px solid #1C2333; border-radius: 10px; font-weight: bold; font-size: 16px; padding: 5px; }
            .text-area { background: transparent; color: #FFFFFF; font-size: 24px; font-family: 'Segoe UI', sans-serif; caret-color: #9900FF; }
            .text-area text { background: transparent; }
            .text-area-out { background: transparent; color: #9900FF; font-size: 24px; font-weight: bold; font-family: 'Segoe UI', sans-serif; }
            .text-area-out text { background: transparent; }
            .swap-btn { background: #050608; color: #9900FF; font-size: 24px; font-weight: bold; border-radius: 50%; padding: 15px; border: 1px solid #1C2333; box-shadow: 0 5px 15px rgba(153, 0, 255, 0.2); transition: all 0.2s; }
            .swap-btn:hover { border: 1px solid #9900FF; box-shadow: 0 10px 25px rgba(153, 0, 255, 0.4); transform: scale(1.1); }
            .action-btn { background: linear-gradient(45deg, #9900FF, #6600CC); color: #FFFFFF; border-radius: 12px; font-weight: bold; padding: 15px; border: none; box-shadow: 0 5px 20px rgba(153, 0, 255, 0.3); transition: all 0.3s; }
            .action-btn:hover { box-shadow: 0 8px 30px rgba(153, 0, 255, 0.5); }
            .nav-btn { background: rgba(255,255,255,0.05); color: #FFFFFF; border-radius: 12px; border: none; padding: 15px; font-weight: bold; transition: all 0.2s; }
            .nav-btn:hover { background: rgba(255,255,255,0.1); }
        '''
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

if __name__ == "__main__":
    win = ZeroLang()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

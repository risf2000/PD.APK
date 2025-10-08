import os

# --- ⚠️ تنظیمات گرافیکی باید قبل از هر ایمپورت Kivy باشند! ---
from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)
# ---------------------------------------------------------

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.core.text import LabelBase
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

# --- پس‌زمینه سیاه برای کل پنجره ---
Window.clearcolor = (0, 0, 0, 1)  # سیاه

# --- پردازش متن فارسی ---
import arabic_reshaper
from bidi.algorithm import get_display

def farsi(text):
    if not text:
        return ""
    return get_display(arabic_reshaper.reshape(text))

# --- ثبت فونت Vazir ---
font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'Vazir.ttf')
APP_FONT = 'Vazir'

if os.path.exists(font_path):
    LabelBase.register(name=APP_FONT, fn_regular=font_path)
else:
    print("⚠️ فونت Vazir یافت نشد. از فونت پیش‌فرض استفاده می‌شود.")
    APP_FONT = None

# --- محتوای آموزشی ---
CONTENT = {
    "air": (
        "در صورت شنیدن هشدار حمله هوایی:\n\n"
        "۱. بلافاصله به نزدیک‌ترین پناهگاه یا فضای بسته بروید.\n"
        "۲. از ایستادن نزدیک به پنجره‌ها، آینه‌ها و دیوارهای خارجی خودداری کنید.\n"
        "۳. در صورت عدم دسترسی به پناهگاه، در گوشه‌ای دور از پنجره دراز بکشید و سر خود را با دست یا لباس پوشانید.\n"
        "۴. پس از پایان هشدار، منتظر دستور رسمی برای خروج باشید.\n"
        "۵. از گسترش شایعات خودداری کنید و فقط از منابع رسمی اطلاعات دریافت کنید."
    ),
    "earthquake": (
        "اقدامات فوری پس از وقوع زلزله:\n\n"
        "۱. آرامش خود را حفظ کنید و از ترس و هیجان بی‌جا خودداری نمایید.\n"
        "۲. قبل از خروج از ساختمان، برق، گاز و آب را قطع کنید.\n"
        "۳. از ساختمان به‌آرامی خارج شوید و از استفاده از آسانسور خودداری کنید.\n"
        "۴. در فضای باز و دور از ساختمان‌ها، دیوارها، سیم‌های برق و درختان بمانید.\n"
        "۵. در صورت آسیب‌دیدگی، از محل خود تا رسیدن کمک‌های امدادی تکان نخورید.\n"
        "۶. از تلفن فقط در موارد ضروری استفاده کنید تا شبکه شلوغ نشود.\n"
        "۷. دستورات مسئولان و نیروهای امدادی را به‌دقت دنبال کنید."
    )
}

class TopAppBar(BoxLayout):
    def __init__(self, title_text, icon_path=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(56)
        self.padding = (dp(12), 0, dp(12), 0)
        self.spacing = dp(12)

        with self.canvas.before:
            Color(0.1, 0.3, 0.6, 1)  # آبی تیره
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        if icon_path and os.path.exists(icon_path):
            icon = Image(source=icon_path, size_hint=(None, None), size=(dp(40), dp(40)))
            self.add_widget(icon)
        else:
            # فضای خالی به جای آیکون
            placeholder = Label(size_hint_x=None, width=dp(40))
            self.add_widget(placeholder)

        title_label = Label(
            text=farsi(title_text),
            font_name=APP_FONT,
            font_size=dp(20),
            halign='center',
            valign='middle',
            color=(1, 1, 1, 1)  # سفید
        )
        title_label.bind(size=title_label.setter('text_size'))
        self.add_widget(title_label)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class PassiveDefenseApp(App):
    def build(self):
        icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'Icon1.png')
        main_layout = BoxLayout(orientation='vertical')

        # نوار بالایی (AppBar)
        main_layout.add_widget(TopAppBar("پدافند غیرعامل", icon_path))

        # فاصله کوچک
        main_layout.add_widget(Label(size_hint_y=None, height=dp(20)))

        # دکمه‌های اصلی
        button_layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15),
            size_hint_y=None,
            height=dp(120)
        )

        topics = [
            ("تهدیدات هوایی", "air"),
            ("اقدامات پس از زلزله", "earthquake")
        ]

        for btn_text, topic_key in topics:
            btn = Button(
                text=farsi(btn_text),
                font_name=APP_FONT,
                font_size=dp(18),
                size_hint_y=None,
                height=dp(50),
                background_color=(0.6, 0.6, 0.6, 1),  # خاکستری
                color=(1, 1, 1, 1),  # متن سیاه
                on_press=lambda instance, t=topic_key: self.show_content(t)
            )
            button_layout.add_widget(btn)

        main_layout.add_widget(button_layout)

        # ScrollView برای نمایش محتوا
        scroll_view = ScrollView(size_hint=(1, 1))
        content_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(10)
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))

        self.info_label = Label(
            text=farsi("برای نمایش اطلاعات، یکی از دکمه‌ها را فشار دهید."),
            font_name=APP_FONT,
            font_size=dp(18),
            halign='right',
            valign='top',
            size_hint_y=None,
            text_size=(dp(300), None),
            color=(1, 1, 0, 1)  # زرد پررنگ
        )
        self.info_label.bind(texture_size=self._update_label_height)
        content_layout.add_widget(self.info_label)
        scroll_view.add_widget(content_layout)
        main_layout.add_widget(scroll_view)

        return main_layout

    def _update_label_height(self, instance, texture_size):
        instance.height = max(texture_size[1], dp(200))

    def show_content(self, topic):
        text = CONTENT.get(topic, "موضوع نامعتبر است.")
        self.info_label.text = farsi(text)

# --- اجرای برنامه ---
if __name__ == '__main__':
    PassiveDefenseApp().run()
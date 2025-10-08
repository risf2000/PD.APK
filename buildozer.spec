[app]
title = پدافند غیرعامل
package.name = passive_defense
package.domain = ir.yourname

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
source.include_patterns = fonts/*.ttf,icons/*.png
source.main_entrypoint = fffont2-0

version = 1.0
requirements = python3,kivy==2.3.0,arabic-reshaper,bidi

icon.filename = icons/Icon1.png
p4a.bootstrap = sdl2

[buildozer]
log_level = 2

# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Drag, Click, Match, Rule
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
import os
import subprocess
import shlex

mod = "mod4"

keys = [
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod], "Return",
        lazy.layout.toggle_split()
    ),
    Key([mod, "shift"], "Return", lazy.spawn("termite")),
    Key([mod, "control"], "l", lazy.spawn("gnome-screensaver-command -l")),
    Key([mod, "control"], "p", lazy.spawn("scrot -s")),

    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout()),
    Key([mod, "shift"], "c", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "p", lazy.spawncmd()),
    Key([mod], "w", lazy.to_screen(0)),
    Key([mod], "e", lazy.to_screen(1)),
    Key([mod], "r", lazy.to_screen(2)),

    Key([mod], "Tab", lazy.layout.next()),
    Key([mod, "shift"], "Tab", lazy.layout.client_to_next()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod, "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "shift"], "l", lazy.layout.swap_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod], "i", lazy.layout.grow()),
    Key([mod], "m", lazy.layout.shrink()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),
    Key([mod, "shift"], "space", lazy.layout.flip()),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-")),
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([mod, "shift"], "e" , lazy.window.togroup('idea'))
]

groups = [Group("1", matches=[Match(wm_class=["Emacs"])], spawn=["emacs"]),
          Group("2", matches=[Match(wm_class=["google-chrome"])], spawn=["google-chrome-stable"]),
          Group("3", matches=[Match(wm_class=["Termite"])], spawn=["termite"]),
          Group("4", matches=[Match(wm_class=["Spotify", "Slack"])], spawn=["spotify", "slack"]),
          Group("5"),
          Group("6"),
          Group("7"),
          Group("8"),
          Group("9"),]

for i in groups:
    # mod1 + letter of group = switch to group
    keys.append(
        Key([mod], i.name, lazy.group[i.name].toscreen())
    )

    # mod1 + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name))
    )

idea = Group('idea', init=True, persist=True, layout='max',
                         matches=[Match(wm_class=['jetbrains-idea-ce'])],
                         position=9, exclusive=True)


keys.append(
    Key([mod, "shift"], "e", lazy.group[idea.name].toscreen())
)

groups = groups + [Group('steam', init=False, persist=False, layout='max',
                         matches=[Match(wm_class=['Steam'])],
                         position=9, exclusive=True), idea]

dgroups_app_rules = [Rule(Match(wm_class=['Steam']), float=True, intrusive=True)]

layouts = [
    layout.Max(),
    layout.Stack()
]

widget_defaults = dict(
    font='Arial',
    fontsize=16,
    padding=3,
)


#   Screens Config
# ------------------
flat_theme = {"bg_dark": ["#606060", "#000000"],
              "bg_light": ["#707070", "#303030"],
              "font_color": ["#ffffff", "#cacaca"],

              # groupbox
              "gb_selected": ["#7BA1BA", "#215578"],
              "gb_urgent": ["#ff0000", "#820202"]
              }

gloss_theme = {"bg_dark": ["#505050",
                           "#303030",
                           "#202020",
                           "#101010",
                           "#202020",
                           "#303030",
                           "#505050"],
               "bg_light": ["#707070",
                            "#505050",
                            "#505050",
                            "#505050",
                            "#505050",
                            "#707070"],
               "font_color": ["#ffffff", "#ffffff", "#cacaca", "#707070"],

               # groupbox
               "gb_selected": ["#707070",
                               "#505050",
                               "#404040",
                               "#303030",
                               "#404040",
                               "#505050",
                               "#707070"],
               "gb_urgent": ["#ff0000",
                             "#820202",
                             "#820202",
                             "#820202",
                             "#820202",
                             "#ff0000"
                             ]
               }
theme = gloss_theme

screens = [Screen(top = bar.Bar([
        # This is a list of our virtual desktops.
        widget.GroupBox(urgent_alert_method='text', fontsize=11, this_current_screen_border='7b5830'),
        widget.sep.Sep(foreground='7b5830'), #add separator bars where deemed necessary

        # A prompt for spawning processes or switching groups. This will be
        # invisible most of the time.
        widget.Prompt(fontsize=15),
        widget.Clipboard(timeout=10),
        # Current window name.
        widget.windowtabs.WindowTabs(),
        widget.CurrentLayout(foreground='7b5830'),
        widget.sep.Sep(foreground='7b5830'),
        #NetworkStatus(theme_path='/home/deewakar/.config/qtile/icons/'),
    # system usage
    widget.CPUGraph(core=0, width=21, line_width=2,
                    graph_color='#0066FF',
                    fill_color=['#0066FF', '#001111'],
                    margin_x=0, border_width=1,
                    background=theme["bg_dark"],
                    ),
    widget.CPUGraph(core=1, width=21, line_width=2,
                    graph_color='#0066FF',
                    fill_color=['#0066FF', '#001111'],
                    margin_x=0, border_width=1,
                    background=theme["bg_dark"],
                    ),
    widget.MemoryGraph(width=42, line_width=2,
                       graph_color='#22BB44',
                       fill_color=['#11FF11', "#002200"],
                       border_width=1,
                       background=theme["bg_dark"],
                       ),
    widget.SwapGraph(width=42, line_width=2,
                     graph_color='#CC2020',
                     fill_color=['#FF1010', '#221010'],
                     border_width=1,
                     background=theme["bg_dark"],
                     ),
 widget.Battery(energy_now_file = "charge_now",
                                energy_full_file = "charge_full",
                                power_now_file = "current_now",
                                update_delay = 5,
                                foreground = "7070ff",
                                charge_char = u'↑',
                                discharge_char = u'↓',),

        widget.Volume(),
        widget.sep.Sep(foreground='7b5830'),
        widget.Systray(),
        #display 12-hour clock
        widget.Clock(format='%B %d %a %I:%M %p', fontsize=11, foreground='9c6b34'),
    ], 22, opacity=0.1)) # our bar is 22px high
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True
floating_layout = layout.Floating()
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

def runone(cmdline):
    """Check if another instance of an app is running, otherwise start a new one."""
    cmd = shlex.split(cmdline)
    try:
        subprocess.check_call(['pgrep', cmd[0]])
    except:
        run(cmdline)


def run(cmdline):
    subprocess.Popen(shlex.split(cmdline))



@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
    qtile.cmd_restart()


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

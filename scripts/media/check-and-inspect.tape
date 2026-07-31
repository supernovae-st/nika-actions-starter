# check-and-inspect.tape — the starter's two receipts in ~12 seconds:
# the audit passes clean, then the DAG draws in the terminal. Every
# verdict is the released binary's own on this repo's shipped flow;
# scripts/media/render.sh stages the copy. Replaces the unversioned
# check-and-graph.gif, which taught `nika graph` — a subcommand the
# released binary refuses (the flat truth: `nika inspect`). House theme
# = the engine's nika-hero palette + the v2 window chrome.
Output check-and-inspect.gif

Set Shell zsh
Set FontFamily "JetBrains Mono"
Set FontSize 21
Set Width 1420
Set Height 780
Set Padding 24
Set Margin 22
Set MarginFill "#4f86ff"
Set BorderRadius 14
Set WindowBar Colorful
Set WindowBarSize 42
Set Theme { "name": "nika", "background": "#08090b", "foreground": "#dbe3ee", "cursor": "#4f86ff", "black": "#10131a", "red": "#ff6b6b", "green": "#34d399", "yellow": "#f0b45b", "blue": "#4f86ff", "magenta": "#b07bff", "cyan": "#22d3ee", "white": "#dbe3ee", "brightBlack": "#5b6472", "brightRed": "#ff8f8f", "brightGreen": "#5ee6b0", "brightYellow": "#ffd08a", "brightBlue": "#8db4ff", "brightMagenta": "#c9a2ff", "brightCyan": "#67e3f5", "brightWhite": "#ffffff" }
Set TypingSpeed 30ms
Set PlaybackSpeed 1.0

Hide
Type "cd /tmp/starter-demo && export TMPDIR=/tmp && unset -m '*API_KEY*' '*_TOKEN*' '*SECRET*' 2>/dev/null; setopt interactive_comments && clear"
Enter
Show

Type "# the starter ships a working flow · audit it before any token is spent"
Enter
Sleep 700ms
Type "nika check flows/daily-brief.nika.yaml"
Enter
Sleep 4200ms

Type "clear"
Enter
Type "# the same file, as the engine schedules it"
Enter
Sleep 700ms
Type "nika inspect flows/daily-brief.nika.yaml"
Enter
Sleep 3800ms
Sleep 1400ms

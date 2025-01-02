# Defining possible variations to the correct application name

wake_words = ["hey luna", "hello luna", "hi luna", "luna", "are you still there", "are you still there luna"]

exit_words = ["goodbye", "see you later", "exit", "stop", "bye"]

WAKE_WORD_ALIAS = {
    "hey luna" : ["hay lona", "hey lona", "hay luna", "hey luna", "hey lune", "hay lune", "hey lonah", "hay lonah", "hay luner", "hey luner", "hay luner", "hey noona", "hey nona", "hay noona", "hay nona"],
    "hello luna": ["hello lona", "hello lonah", "hello luner", "hello lune", "hello luna", "hello noona", "hello nona"],
    "hi luna": ["high lona", "high luna"],
    "luna": ["lona", "lonah", "luner", "lunar", "lune", "luna", "noona", "nona", "duna", "lu na"],
    
}

EXIT_WORD_ALIAS = {
    "goodbye": ["goodbye", "good-bye", "good bye"],
    "see you later": ["see a leader", "see a lader", "see a ladder", "see you later", "see ya later",],
    "exit": ["exit"],
    "stop": ["stop"],
}

COMMAND_REGISTRY = {

    "open": {
     "aliases" : ["oben", "open"],
     "handler": "handle_open_command",
    },

    "close": {
        "aliases": ["clothe", "cluse", "close", "lows"],
        "handler": "handle_close_command",
    },

    "switch to the next tab": {
        "aliases": ["switch touh the next tamp", "switch to the next cab", "next tab", "switch to the next tab"],
        "handler": "handle_switch_tab_command",
    },

    "what's the time": {
        "aliases": ["what time is it", "what's the time", "can you tell me the time", "what is the time"],
        "handler": "handle_time_command",
    },

    "tell me a joke": {
        "aliases": ["tell me a joke", "say something funny", "make me laugh"],
        "handler": "handle_joke_command",
    },
}


PROGRAM_ALIAS = {
    "whatsapp": ["whatsapp", "what's ap", "what's up", "whatsap", "what's ap", "what's ep", "whatsep", "what sap", "what sab",],
    "notepad": ["notepad", "note pad", "note-pad", "node pad", "not pad"],
    "discord": ["this cord", "discord", "dist cord", "dis chord", "this chord", "disk cord", "disk chord", "dis cord", "this corde"],
    "word": ["word", "ward"],
    "excel": ["the excell", "excell" "axle", "exel", "excl", "excel"],
    "powerpoint": ["power point", "the power point"],
    "calculator": ["calculater", "calcu leader", "calculator"],
    "lenovo vantage": ["lanover vantage", "lenovo vantage", "lenoval vantage", "lanoval vantage"],
    "nvidia": ["and videa", "and video", "an videa"],
    "sticky notes": ["notes", "sticky nodes", "sticky notes"],
    "obsidian": [""],
    "viber": ["viber", "fiber"],
    "clock": ["clack", "clock"]
}

WORD_TO_NUMBER = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
    "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
    "twenty-one": 21, "twenty-two": 22, "twenty-three": 23, "twenty-four": 24,
    "twenty-five": 25, "twenty-six": 26, "twenty-seven": 27, "twenty-eight": 28,
    "twenty-nine": 29, "thirty": 30, "thirty-one": 31, "thirty-two": 32,
    "thirty-three": 33, "thirty-four": 34, "thirty-five": 35, "thirty-six": 36,
    "thirty-seven": 37, "thirty-eight": 38, "thirty-nine": 39, "forty": 40,
    "forty-one": 41, "forty-two": 42, "forty-three": 43, "forty-four": 44,
    "forty-five": 45, "forty-six": 46, "forty-seven": 47, "forty-eight": 48,
    "forty-nine": 49, "fifty": 50, "fifty-one": 51, "fifty-two": 52,
    "fifty-three": 53, "fifty-four": 54, "fifty-five": 55, "fifty-six": 56,
    "fifty-seven": 57, "fifty-eight": 58, "fifty-nine": 59,
}

MISRECOGNIZED_WORDS = {
    "to": "two",
    "ate": "eight",
    "fore": "four",
}

URL = {
    "www.google.com" : ["google.com", "google"],
    "www.youtube.com": ["youtube", "youtube.com"],
    "www.github.com": ["github", "github.com"],
    "www.reddit.com": ["reddit.com", "readit.com", "reddet"],
    "www.wikipedia.com": ["wikipidia"]

}

URL_MISPRONUNCIATIONS = {
    " dot colm": ".com",
    " dot calm": ".com",
    " dot net": ".net",
    " dot orge": ".org",
    " dot org": ".org",
    " dot co dot uk": ".co.uk",
    " dot co dot": ".co.",
    " dot edu dot np": ".edu.np"
}

# BROWSERS = {
#     "chrome": "C:\Program Files\Google\Chrome\Application\chrome.exe %s",
#     "edge": "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe %s",
#     "default":"",
# }

BROWSERS = {
   "chrome": "chrome",
   "edge": "msedge",
   "arc": "arc",
   "default": "arc", 
}

TASKS = {
    "tasks" : ["what's the time", "tell me a joke", "open excel", "close whatsapp", "google books", "set an alarm for 7:30 am"]
}
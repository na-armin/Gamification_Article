from termcolor import colored


def show_text(_text, highlight_color):
    text = colored(_text, highlight_color, attrs=['reverse', 'blink'])
    print(text)

def colored_text(_text, highlight_color):
    text = colored(_text, highlight_color, attrs=['reverse', 'blink'])
    return text

if  __name__ == '__main__':
    show_text('Hello, World!','red')

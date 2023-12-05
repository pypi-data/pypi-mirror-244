import os,random,re,time,sys
os.system("")

class cl:
    """A class including preset colors and additional text formatting for easier usage."""
    reset = "\033[0m"
    
    class __fr:
        """A list of preset foreground colors for your text. This includes:
        red, green, blue, cyan, pink and yellow."""
        red = "\033[38;2;255;0;0m"
        green = "\033[38;2;0;255;0m"
        blue = "\033[38;2;0;0;255m"
        cyan = "\033[38;2;0;255;255m"
        pink = "\033[38;2;255;0;255m"
        yellow = "\033[38;2;255;255;0m"
    
    fore = __fr()
    
    class __bg:
        """A list of preset background colors for your text. This includes:
        red, green, blue, cyan, pink and yellow."""
        red = "\033[48;2;255;0;0m"
        green = "\033[48;2;0;255;0m"
        blue = "\033[48;2;0;0;255m"
        cyan = "\033[48;2;0;255;255m"
        pink = "\033[48;2;255;0;255m"
        yellow = "\033[48;2;255;255;0m"
    
    back = __bg()
    
    class __fo():
        bold = "\033[1m"
        dim = "\033[2m"
        italic = "\033[3m"
        underline = "\033[4m"
        blink = "\033[5m"
        blink2 = "\033[6m"
        inverse = "\033[7m"
        hidden = "\033[8m"
        strikethrough = "\033[9m"
        
        def __call__(self,s):
            """Returns a string of multiple formatting options.
            B: bold
            D: dim
            I: italic
            U: underline
            b: blink
            i: inverse
            h: hidden
            s: strikethrough
            
            Example usage:
            print(clrflow.clr.format("BIUs")+"hello there")

            Args:
                s (str): A string containing chosen formatting options as characters.
            """
            f = ""
            for fn,c in zip((self.bold,self.dim,self.italic,self.underline,self.blink,self.inverse,self.hidden,self.strikethrough),"BDIUbihs"):
                if c in s:
                    f += fn
            return f
        
    format = __fo()
    
    def __call__(self,c:tuple,layer:str="fore"):
        """Generates a custom color sequence with chosen color.
        Example usage: clrflow.clr((100,255,255),layer='back')+"clrflow rocks!"+clrflow.clr.reset

        Args:
            c (tuple): RGB values of the color.
            layer (str, optional): The layer of the color, either background or foreground. Defaults to "foreground".

        Returns:
            str: The color sequence.
        """
        return f"\033[{3 if 'fore' in layer else 4}8;2;{c[0]};{c[1]};{c[2]}m"
        
clr = cl()



class grad:
    cls = {}
    
    def a(self,text,fr,to,ch,dr,lr,iS):
        lr = 3 if "fore" in lr.lower() else 4
        global r,g,b
        f = ""
        r,g,b = fr
        if ch=="auto":
            if dr == "horizontal":
                ch=round(255/len(max(text.splitlines(), key=len)))
            elif dr=="vertical":
                ch=round(255/len(text.splitlines()))
            else:
                raise ValueError("Direction must be either 'horizontal' or 'vertical'")
        for line in text.splitlines():
            if dr == "horizontal":
                r,g,b = fr
            for char in line:
                if not iS or not char.isspace():
                    if (r,g,b)!=to:
                        if dr == "horizontal":
                            for i,c in enumerate("rgb"):
                                if eval(c) != to[i]:
                                    if fr[i] < to[i]:
                                        exec(f"{c} += ch",locals(),globals())
                                    else:
                                        exec(f"{c} -= ch",locals(),globals())
                r,g,b = max(0,min(255,r)),max(0,min(255,g)),max(0,min(255,b))
                f += f"\033[{lr}8;2;{r};{g};{b}m{char}"

            if dr == "vertical":
              if (r,g,b)!=to:
                    for i,c in enumerate("rgb"):
                        if eval(c) != to[i]:
                                if fr[i] < to[i]:
                                      exec(f"{c} += ch",locals(),globals())
                                else:
                                     exec(f"{c} -= ch",locals(),globals())
            f+="\033[0m\n"
        return f[:-1]+"\033[0m"
    
    def __call__(self,*,fr=(0,0,0),to=(255,255,255),change:int="auto",direction:str="horizontal",layer:str="foreground",name:str=None,ignoreWhitespace:bool=False):
        """Creates a function that applies a gradient of chosen colors to your text when called.
        Example usage:
        
        green_to_blue = clrflow.gradient(fr=(0,255,0),to=(0,0,255),direction="vertical",layer="background",name="gtb")
        print(green_to_blue("clrflow rocks!"))
        ...
        green_to_blue2 = clrflow.gradient(name="gtb")
        print(green_to_blue("This does the same as before."))
        
        
        
        Args:
            fr (tuple): The starting color in rgb values.
            
            to (tuple): The end color in rgb values.
            
            change (int, optional): Difference of the rgb values per character. Detects automatically by default. Defaults to "auto".
            
            direction (str, optional): The direction of the gradient. Must be either 'horizontal' or 'vertical'. Defaults to "horizontal".
            
            layer (str, optional): The layer of the gradient, must include 'fore' or 'back'. Defaults to "foreground".
            
            name (str, optional): The name of this template. Makes it reassignable in future code. Defaults to None.
            
            ignoreWhitespace (bool, optional): Will ignore whitespaces and pause the gradient at their spot. Defaults to False.
            
        Returns:
            lambda: The gradient-applying function.
        """
        if name:
            if name in self.cls.keys():
                return lambda st: self.a(text=st,fr=self.cls[name][0],to=self.cls[name][1],ch=self.cls[name][2],dr=direction,lr=layer,iS=ignoreWhitespace)
            else:
                self.cls[name] = [fr,to,change]
        return lambda txt: self.a(txt,fr,to,change,direction,layer,ignoreWhitespace)
        
gradient = grad()

class pat:
    cls = {}
    def __call__(self,*,name: str,direction: str="horizontal",layer: str="foreground",ignoreWhitespace: bool=True):
        """Return a previously defined pattern function with editable configurations.
        Predefined patterns include:
        rainbow, galaxy, fire, sea, bubblegum, sunset, jungle

        Args:
            name (str): Name of the pattern.
            direction (str, optional): Refer to clrflow.gradient(). Defaults to "horizontal".
            layer (str, optional): Refer to clrflow.gradient(). Defaults to "foreground".
            ignoreWhitespace (bool, optional): Refer to clrflow.gradient(). Defaults to False.

        Raises:
            TypeError: If incorrect or nonexistent name given, TypeError will be raised.

        Returns:
            lambda: A pattern-applying function.
        """
        layer = 3 if "fore" in layer.lower() else 4
        def b(s):
            f = ""
            r,g,b = (0,0,0)
            if name in self.cls.keys():
                  for i,line in enumerate(s.splitlines()):
                       if direction == "vertical":
                            r,g,b = self.cls[name][i % len(self.cls[name])]
                       for y,char in enumerate(line):
                            if direction == "horizontal" and not ignoreWhitespace or not char.isspace():
                                 r,g,b = self.cls[name][y % len(self.cls[name])]
                            f += f"\033[{layer}8;2;{r};{g};{b}m{char}"
                       f += "\n"
            else:
                raise TypeError("pattern not found, existing patterns are:\n"+", ".join(list(self.cls.keys())))
            return f[:-1]+"\033[0m"
        return lambda x: b(x)
    def create(self,*,colors:list[tuple],steps:int,name=None,direction:str="horizontal",layer:str="foreground",mode:str="default",ignoreWhitespace:bool=False):
        """Creates a multicolor gradient function with stationary colors, meaning the color will depend on the index of the character.
        Example usage:
        rainbow = clrflow.pattern.create(colors=[(255,0,0),(255,255,0),(0,255,0),...],steps=10,name="rainbow",direction="vertical",layer="background",mode="random")
        print(rainbow("clrfloooooooooooooooooooooooow"))
        ...
        rainbow2 = clrflow.pattern(name="rainbow",direction="horizontal")
        print(rainbow2("clrflowwwwwwwwwwwwwwwwwwwwww"))

        Args:
            colors (list[tuple]): A list of rgb values for each color.
            steps (int): The amount of steps between each given color.
            name (str, optional): Refer to clrflow.gradient(). Defaults to None.
            direction (str, optional): Refer to clrflow.gradient(). Defaults to "horizontal".
            layer (str, optional): Refer to clrflow.gradient(). Defaults to "foreground".
            mode (str, optional): In development, either "default" or "random", which randomizes the colors order. Defaults to "default".
            ignoreWhitespace (bool, optional):Refer to clrflow.gradient(). Defaults to False.

        Returns:
            func: A pattern-applying function.
        """
        if mode == "random":
            colors *= 10
            random.shuffle(colors)
        tmp = []
        for i in range(len(colors)):
            fr = colors[i]
            to = colors[(i+1)%len(colors)]
            for y in range(steps+1):
                r = max(0, min(255, int(round(fr[0] + (to[0] - fr[0]) * y / (steps-1)))))
                g = max(0, min(255, int(round(fr[1] + (to[1] - fr[1]) * y / (steps-1)))))
                b = max(0, min(255, int(round(fr[2] + (to[2] - fr[2]) * y / (steps-1)))))
                tmp.append((r,g,b))
        if name:
            self.cls[name] = tmp
        return lambda x:self(x,direction,layer,ignoreWhitespace)
    
    def get_patterns(self):
        """Returns all existing patterns.

        Returns:
            list: A list of all patterns.
        """
        
        return self.cls
        

pattern = pat()


pattern.create(name="rainbow",colors=[(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(255,0,255),],steps=9)
pattern.create(name="fire",colors=[(255,0,0),(255,100,0),(255,0,0),(255,255,0),],steps=10)
pattern.create(name="galaxy",colors=[(0,0,255),(0,255,255),(255,0,255)],steps=10)
pattern.create(name="sea",colors=[(45, 105, 215),(0,255, 215),(0,100,255)],steps=10)
pattern.create(name="bubblegum",colors=[(255,0,255),(255,255,255),(195, 105, 220)],steps=10)
pattern.create(name="sunset",colors=[(178, 164, 255),(255, 180, 180),(255, 222, 180),(253, 247, 195),(255, 180, 180)],steps=10)
pattern.create(name="jungle",colors=[(0, 173, 124),(82, 214, 129),(181, 255, 125),(255, 248, 181),(181, 255, 125)],steps=10)


class tls:
    def align(self,*,s: str,horizontal: str="center",vertical: str="top",separate:str=False):
        """A text-aligning function for main horizontal/vertical aswell as sub-horizontal alignment in the console.
        Note: This also works with colored strings, but first color before aligning. Also, make sure to add 'end=""' to your print function when printing aligned text.
        Example use:
        a = clrflow.tools.align(s="clrflow\nrocks\n!!!!!!!!!",horizontal="right",vertical="center",separate="left")
        print(a,end="")
        Args:
            s (str): The text to align.
            horizontal (str, optional): The horizontal position of the text in the console. Must be either "left","center", or "right". Defaults to "center".
            vertical (str, optional): The vertical position of the text in the console. Must be either "top","center", or "bottom". Defaults to "top".
            separate (bool | str, optional): The sub-horizontal position of the text. This defines the position of the individual lines at the chosen spot in the console horizontally. If defined manually, must be either "left","center", or "right". Defaults to the same value as horizontal.

        Returns:
            str: The aligned text.
        """
        if separate == False:
            separate = horizontal
        copy = re.sub(r'\x1b\[[0-9;]*m', '', s)
        s = s.splitlines()
        copy = copy.splitlines()
        match horizontal:
            case "center":
                spaces = round((os.get_terminal_size()[0] - len(max(s, key=len)))/2)
            case "right":
                spaces = (os.get_terminal_size()[0] - len(max(s, key=len)))
            case _:
                spaces = 0
        
        match vertical:
            case "top":
                lines = 0
            case "center":
                lines = round((os.get_terminal_size()[1] - len(s))/2)
            case "bottom":
                lines = (os.get_terminal_size()[1] - len(s))

        f = "\n" * lines
          
        for c,i in enumerate(copy):
            if separate in ["left","center","right"]:
                match horizontal:
                    case "center":
                        spaces = int((os.get_terminal_size()[0] - len(max(copy,key=len)))//2)
                    case "right":
                        spaces = (os.get_terminal_size()[0] - len(max(copy,key=len)))
                    case _:
                        spaces = 0
                match separate:
                    case "center":
                        spaces += round((len(max(copy,key=len))-(len(i)+1))/2)
                    case "right":
                        spaces += round((len(max(copy,key=len))-len(i)))
                    case _:
                        ...
            f+=(" "*spaces)+s[c]+"\n"
        return f[:-1]
    class progressbar:
        """A class that generates customizable progressbars."""
        def __init__(self,l:int,*,mx=100,lc:str="#",mc:str=" ",fr:str="\r[{lc}{mc}] - {pr}% - {cn}/{mx}"):
            """Initialize the progressbar and its look.
            Note: When printing using self.step(), make sure to add end="" to your print function.
            Example use:
            prog1 = clrflow.tools.progressbar(l=25,lc="*",mc=".",fr="\\rLoading: ({{}}{{}}) ({{}})")
            print(prog1.step(0),end="")
            for i in range(99):
                print(prog1.step(1),end="")
            print("done!")
            Args:
                l (int): Lenght of the bar in characters.
                lc (str, optional): The character to be used to show progress. Defaults to "#".
                mc (str, optional): The character to be used to show missing progress. Defaults to " ".
                fr (str, optional): A custom format of the progressbar. Note: Add a carriage return at the front of the string, and use empty format brackets.
                mx (int, optional): The maximum value, where for example, if this were 120, the percentage at 60 steps would be 50%.
                
            Format parameters:
            lc = loading indicator characters
            mc = missing indicator characters
            pr = percentage of progress
            cn = steps
            mx = max value
            """
            self.lenght = l
            self.steps = 0
            self.lc = lc
            self.mc = mc
            self.fr = fr
            self.mx = mx
        def step(self,s:int):
            """Steps the defined progressbar instance by s steps.

            Args:
                s (int): The amount of steps.

            Returns:
                str: The progressbar as a string.
            """
            self.steps += s
            tmp = round(self.steps/(self.mx/self.lenght))
            return self.fr.format(lc=(self.lc*tmp),mc=self.mc*round(self.lenght-tmp),pr=round((self.steps/self.mx)*100,2),cn=(self.steps),mx=(self.mx))

    def custom_print(self,s:str,line:int,column:int):
        """Prints a string in chosen line and column of the console.

        Args:
            s (any): The value to print.
            line (int): The line to print to.
            column (int): The column to print to.
        """
        for c,s in enumerate(s.splitlines()):
            print(f"\r\033[{line+c};{column}H",s)
        
    def slow_print(self,s:str,dur:int="real"):
        """Prints characters one by one instead of all at once.

        Args:
            s (str): The string to print.
            dur (int, optional): The duration between each character. When set to "real", will try to make it realistic. Defaults to "real".
        """
        tmp = False
        for i in s[:-1]:
            if i == "\033":
                tmp = True
            elif tmp and i.isalpha():
                tmp = False
            sys.stdout.write(i)
            sys.stdout.flush()
            if not tmp:
                time.sleep(dur if (dur != "real") else random.uniform(0.01,0.1))
        print(s[-1])
            
tools = tls()
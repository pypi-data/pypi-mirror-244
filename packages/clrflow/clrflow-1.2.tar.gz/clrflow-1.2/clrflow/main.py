import os,random,re,time,sys,numpy as np
from collections.abc import Sequence
os.system("")

class cl:
    """A class including preset colors and additional text formatting for easier usage."""
    reset = "\033[0m"
    
    class __fr:
        """A list of preset foreground colors for your text. This includes:
        red,
        green,
        blue,
        cyan,
        pink
        and yellow."""
        red = "\033[38;2;255;0;0m"
        green = "\033[38;2;0;255;0m"
        blue = "\033[38;2;0;0;255m"
        cyan = "\033[38;2;0;255;255m"
        pink = "\033[38;2;255;0;255m"
        yellow = "\033[38;2;255;255;0m"
    
    fore = __fr()
    
    class __bg:
        """A list of preset background colors for your text. This includes:
        red,
        green,
        blue,
        cyan,
        pink
        and yellow."""
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
            ```python
            print(clrflow.clr.format("BIUs")+"hello there")
            ```

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
        
        Example usage:
        ```python
        clrflow.clr((100,255,255),layer='back')+"clrflow rocks!"+clrflow.clr.reset
        ```

        Args:
            c (tuple): RGB values of the color.
            
            layer (str, optional): The layer of the color, must include 'f' or 'b'. Defaults to "foreground".

        Returns:
            str: The color sequence.
        """
        return f"\033[{3 if 'f' in layer else 4}8;2;{c[0]};{c[1]};{c[2]}m"
        
clr = cl()



class grad:
    
    cls = {}
    
    __lin = (lambda _,fr,to,l:[np.linspace(fr[i],to[i],l,dtype=int).tolist() for i in (0,1,2)])
    
    def new(self,text,fr,to,dr,lr,iW):
        layer = 3 if "f" in lr.lower() else 4
        final = ""
        r,g,b = fr
        
        if "h" in dr:
            lenght = len(max(text.splitlines(),key=len))
        elif "v" in dr:
            lenght = len(text.splitlines())
            
        rch, gch, bch = self.__lin(fr,to,lenght)
        
        for lindex,line in enumerate(text.splitlines()):
            if "h" in dr:
                r,g,b = fr
            
            for cindex,char in enumerate(line):
                if not iW or not char.isspace():
                    if "h" in dr:
                        r,g,b = rch[cindex],gch[cindex],bch[cindex]
                final += f"\033[{layer}8;2;{r};{g};{b}m{char}"
            if "v" in dr:
                r,g,b = rch[lindex],gch[lindex],bch[lindex]
            final+="\033[0m\n"
        return final[:-1]
        
    def __call__(self,name,direction:str="horizontal",layer:str="foreground",ignoreWhitespace:bool=False):
        if name in self.cls.keys():
                return lambda st: self.new(text=st,fr=self.cls[name][0],to=self.cls[name][1],ch=self.cls[name][2],dr=direction,lr=layer,iS=ignoreWhitespace)
        else:
            return ValueError(f"no gradient of name {name}")
        
        
        
    def create(self,*,fr:tuple=(0,0,0),to:tuple=(255,255,255),direction:str="horizontal",layer:str="foreground",name:str=None,ignoreWhitespace:bool=False):
        """Creates a function that applies a gradient of chosen colors to your text when called.
        
        Example usage:
        ```python
        green_to_blue = clrflow.gradient(fr=(0,255,0),to=(0,0,255),direction="vertical",layer="background",name="gtb")
        print(green_to_blue("clrflow rocks!"))
        ...
        green_to_blue2 = clrflow.gradient(name="gtb")
        print(green_to_blue2("This does the same as before."))
        ```
        
        
        
        Args:
            fr (tuple): The starting color in rgb values.
            
            to (tuple): The end color in rgb values.
            
            direction (str, optional): The direction of the gradient. Must include 'h' or 'v'. Defaults to "horizontal".
            
            layer (str, optional): The layer of the gradient, must include 'f' or 'b'. Defaults to "foreground".
            
            name (str, optional): The name of this template. Makes it reassignable in future code. Defaults to None.
            
            ignoreWhitespace (bool, optional): Will ignore whitespaces and pause the gradient at their spot. Defaults to False.
            
        Returns:
            lambda: The gradient-applying function.
        """
        if name and not name in self.cls.keys():
            self.cls[name] = [fr,to]
        return lambda txt: self.new(txt,fr,to,direction,layer,ignoreWhitespace)
        
gradient = grad()



class pat:
    cls = {}
    
    __lin = (lambda _,c,s,l=[]:(l.extend(np.linspace(i,c[x+1],s,endpoint=False)) for x,i in enumerate(c[:-1])) and l)
    
    def create(self,name:str=None,colors:Sequence[tuple]=None,change:int=None,direction:str="horizontal",layer="foreground"):
        """Colors your text according to reusable patterns.
        
        Example:
        ```python
        a = clrflow.pattern(name='a',colors=[(0,0,0),(255,0,255),(0,255,255),(255,255,0)])
        print(a('hello world'))
        ...
        b = clrflow.pattern(name='a')
        print(b('hello world'))
        ```

        Args:
            colors (Sequence, optional): An array-like value including wanted colors as tuples. If name is not given, this must be.
            
            name (str, optional): The name of the pattern, makes it reusable in future code. Defaults to None.
            
            direction (str, optional): The direction of the pattern, must include 'h' or 'v' for horizontal or vertical. Defaults to "horizontal".
            
            layer (str, optional): The layer of the pattern, must include 'f' or 'b'. Defaults to "foreground".
            
        Returns:
            lambda: A function which takes text input and outputs it colored.
        """
        
        if not name:
            if not colors:
                return ValueError("If name is not given, colors value must be.")
            return (lambda text:self.__gen(text,colors,change,direction,layer))
        elif not name in self.cls.keys():
            self.cls[name] = colors
            return (lambda text:self.__gen(text,self.cls[name],change,direction,layer))
    
    def __call__(self,name,change=10,direction="horizontal",layer="fore"):
        """Return an existing pattern.

        Args:
            name (_type_): The name of the pattern
            
            change (int, optional): Configurable parameter. Defaults to 10.
            
            direction (str, optional): Same as change. Defaults to "horizontal".
            
            layer (str, optional): Same as change. Defaults to "fore".

        Returns:
            lambda: The pattern applying function.
        """
        if name in self.cls.keys():
            return (lambda text:self.__gen(text,self.cls[name],change,direction,layer))
        else:
            return ValueError(f"no pattern named {name}")
    
    def dothat(self,avs,i,change):
        a = []
        
        b = avs
        avs = [x[i] for x in b]
        
        for c,i in enumerate(avs[:-1]):
            a.extend(np.linspace(i,avs[c+1],change,endpoint=False,dtype=int))
        a.extend(np.linspace(avs[-1],avs[0],change,endpoint=False,dtype=int))
        
        return a
    
    def __gen(self,text,colors,change,direction,lr):
        if not change:
            change = 10
        layer = 3 if "f" in lr else 4
        r,g,b = self.dothat(colors,0,change),self.dothat(colors,1,change),self.dothat(colors,2,change)
        final = ""
        l = len(r)
        _r,_g,_b = colors[0]
        for lindex,line in enumerate(text.splitlines()):
            for cindex,char in enumerate(line):
                if "h" in direction:
                    _r,_g,_b = r[cindex%l],g[cindex%l],b[cindex%l]
                final += f"\033[{layer}8;2;{_r};{_g};{_b}m{char}"
            if "v" in direction:
                _r,_g,_b = r[lindex%l],g[lindex%l],b[lindex%l]
            final += "\033[0m\n"
        return final[:-1]
    
    def get_patterns(self):
        """Returns all existing patterns.

        Returns:
            list: A list of all patterns.
        """
        
        return self.cls
        

pattern = pat()


pattern.create(name="rainbow",colors=[(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(255,0,255),],change=9)
pattern.create(name="fire",colors=[(255,0,0),(255,100,0),(255,0,0),(255,255,0),],change=10)
pattern.create(name="galaxy",colors=[(0,0,255),(0,255,255),(255,0,255)],change=10)
pattern.create(name="sea",colors=[(45, 105, 215),(0,255, 215),(0,100,255)],change=10)
pattern.create(name="bubblegum",colors=[(255,0,255),(255,255,255),(195, 105, 220)],change=10)
pattern.create(name="sunset",colors=[(178, 164, 255),(255, 180, 180),(255, 222, 180),(253, 247, 195),(255, 180, 180)],change=10)
pattern.create(name="jungle",colors=[(0, 173, 124),(82, 214, 129),(181, 255, 125),(255, 248, 181),(181, 255, 125)],change=10)


class tls:
    def align(self,*,s: str,horizontal: str="center",vertical: str="top",separate:str=False):
        """A text-aligning function for main horizontal/vertical aswell as sub-horizontal alignment in the console.
        
        Note: This also works with colored strings, but first color before aligning. Also, make sure to add 'end=""' to your print function when printing aligned text.
        
        Example use:
        
        ```python
            a = clrflow.tools.align(s="clrflow\\nrocks\\n!!!!!!!!!",horizontal="right",vertical="center",separate="left")
            print(a,end="")
        ```
        
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
            ```python
            prog1 = clrflow.tools.progressbar(l=25,lc="*",mc=".",fr="\\rLoading: ({{}}{{}}) ({{}})")
            print(prog1.step(0),end="")
            for i in range(99):
                print(prog1.step(1),end="")
            print("done!")
            ```
            
            Args:
                l (int): Lenght of the bar in characters.
                
                lc (str, optional): The character to be used to show progress. Defaults to "#".
                
                mc (str, optional): The character to be used to show missing progress. Defaults to " ".
                
                fr (str, optional): A custom format of the progressbar. Note: Add a carriage return at the front of the string, and use the below given parameters.
                
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
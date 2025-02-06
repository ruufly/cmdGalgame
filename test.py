import time
import cmdgal
from cmdgal import *
import threading

emptycg = Image(
    """                                                                                                                        
       _____________________________________________________________________________________________________            
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |                                                                                                     |           
      |_____________________________________________________________________________________________________|           
                                                                                                                        
                                                                                                                        """
)

happy_ending = Image(
    """                          __                   
 |  |                    |         |           
 |__|  _    _   _        |__  _   _| .  _   _  
 |  | | |  | | | | | |   |   | | | | | | | | | 
 |  | |_|_ |_| |_| |_|   |__ | | |_| | | | |_| 
           |   |     |                       | 
           |   |    _|                      _| """
)

startcg_str = """                                                            
 |\\    |                    _____     |                     
 | \\   |                   |          |                     
 |  \\  |   /-\\     |--+    |____+     +--+   /-\\      |--+  
 |   \\ |  |   |    |  |         +     |  |  |   |     |  |  
 |    \\|   \\__/\\   |  |    _____|     |  |   \\__/\\    |  |  
                                                            
                                                            
              /-----                                        
              |                                             
              |   ___    /-\\     +-+-+   +--+               
              |    |    |   |    | | |   |--+               
              \\____|     \\__/\\   | | |   |___               
                                                            """

startcg = Label(startcg_str)

setting = Settings(width=120, height=30, fontSize=20)
galgame = Window(settings=setting)

# happy_ending.show(galgame, "side", sidex="right", sidey="bottom")

# galgame.wait(2000)

# clear()

# startcg.show(galgame, "side", 0, 10, sidex="center", sidey="middle")

# galgame.wait(1000)

# clear()



clear()
goto(0, 0)

# def tr(a):
#     time.sleep(1)
#     print(a)
# a = variables.set("a",10)
# threading.Thread(target=tr,args=(a,)).start()
# a.set(20)

sel = Select(
    {"A": "Wow", "B": "Please tell me", "C": "What's this"}, "SelectWidget::Normal"
)
ans = sel.run(galgame, "position", 0, 0)
cmdgal.clear()

sell = Select(
    {"A": "Wow?", "B": "Please tell me?", "C": "What's this?"}, "SelectWidget::Normal"
)
anss = sel.run(galgame, "position", 5, 5)

cmdgal.clear()
strpage = cmdgal.Page(
    "InitialPage::Normal", mainImage=startcg_str, noticeText="loading..., your answer is: %s and %s." % (ans, anss)
)

strpage.show(galgame)
# print(sel.showing,sel.choiceDict)
# print(input())

import time
import cmdgal
from cmdgal import *
import threading

emptycg_img = """                                                                                                                        
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


game_name = """_____           __                                   
  |   |        |  | |           | | |                
  |   |__ ___  |__| |      __   | | |  _  _|_  __ __ 
  |   | | |_|  |  | | | | |_|   | | | | |  |  |_| |  
  |   | | |__  |__| | |_| |__   |_|_| |_|_ |_ |__ |  """


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

testpl = cmdgal.Plugin(directory="plugin/test")
testpl.init()
testpl.loop()

# happy_ending.show(galgame, "side", sidex="right", sidey="bottom")

# galgame.wait(2000)

# clear()

# startcg.show(galgame, "side", 0, 10, sidex="center", sidey="middle")

# galgame.wait(1000)

# clear()


clear()
goto(0, 0)

cmdgal.clear()
strpage = cmdgal.Page(
    "InitialPage::Normal", mainImage=startcg_str, noticeText="loading... "
)

strpage.show(galgame)

wtg = cmdgal.Page(
    "StartPage::Normal",
    title_page=game_name,
    start_cg=emptycg_img,
    message="Copyright c 2025 distjr_.",
    choiceDict={"A": "New", "B": "Continue", "C": "Setting", "D": "About"},
    title_setup={"type": "position", "x": 10, "y": 3},
    choice_setup={"type": "position", "x": 80, "y": 10},
)

ans = wtg.show(galgame)

clear()

print(ans)


# def tr(a):
#     time.sleep(1)
#     print(a)
# a = variables.set("a",10)
# threading.Thread(target=tr,args=(a,)).start()
# a.set(20)

# sel = Select(
#     {"A": "Wow", "B": "Please tell me", "C": "What's this"}, "SelectWidget::Normal"
# )
# ans = sel.run(galgame, "position", 0, 0)
# cmdgal.clear()

# sell = Select(
#     {"A": "Wow?", "B": "Please tell me?", "C": "What's this?"}, "SelectWidget::Normal"
# )
# anss = sel.run(galgame, "position", 5, 5)

# print(sel.showing,sel.choiceDict)
# print(input())

import cmdgal

emptycg = cmdgal.Image(
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

happy_ending = cmdgal.Image(
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

startcg = cmdgal.Label(startcg_str)

setting = cmdgal.Settings(width=120, height=30, fontSize=20)
galgame = cmdgal.Window(settings=setting)

# cmdgal.goto(2,10)
# print("hello")
# input()
happy_ending.show(galgame, "side", sidex="right", sidey="bottom")
# galgame.flush()
# galgame.maintain()

galgame.wait(2000)

cmdgal.clear()

startcg.show(galgame, "side", 0, 10, sidex="center", sidey="middle")

galgame.wait(1000)

cmdgal.clear()

strpage = cmdgal.Page(
    "InitialPage::Normal", mainImage=startcg_str, noticeText="loading..."
)

strpage.show(galgame)

# print(input())

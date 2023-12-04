# JackboxPartyBot
Automatization bot for JackBox games

#

#### Example:
```
import jpb


jpb.setup(
    translate=[jpb.setup.TJPP1().whatif(5),
               jpb.setup.TJPP2().whatif(5),
               jpb.setup.TJPP3().whatif("full"),
               jpb.setup.TJPP4().whatif("full"),
               jpb.setup.TJPP5().whatif("full"),
               jpb.setup.TJPP6().whatif(5.1),
               jpb.setup.TJPP7().whatif(4),
               jpb.setup.TJPP8().whatif("full"),
               jpb.setup.TJPP9().whatif(3),
               jpb.setup.TJPP10().loamf(2)
               ],
    server=True
)
```

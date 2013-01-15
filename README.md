```
                                                       _____|\
                                                  _.--| SSt |:
                                                 <____|.----||
                                                        .---''---,
                                                         ;..__..'    _...
                                                       ,'/  ;|/..--''    \
                                                     ,'_/.-/':            :
                                                _..-'''/  /  |  \    \   _|/|
                                               \      /-./_ \;   \    \,;'   \
                                               ,\    / \:  `:\    \   //    `:`.
                                             ,'  \  /-._;   | :    : ::    ,.   .
                                           ,'     ::   /`-._| |    | || ' :  `.`.)
                                        _,'       |;._:: |  | |    | `|   :    `'
                                      ,'   `.     /   |`-:_ ; |    |  |  : \
                                      `--.   )   /|-._:    :          |   \ \
                                         /  /   :_|   ;`-._;   __..--';    : :
                                        /  (    ;|;-./_  _/.-:'o |   /     ' |
                                       /  , \._/_/_./--''/_|:|___|_,'        |
                                      :  /   `'-'--'----'---------'          |
                                      | :     O ._O   O_. O ._O   O_.      ; ;
                                      : `.      //    //    //    //     ,' /
                                    ~~~`.______//____//____//____//_______,'~
                                              //    //~   //    //
                                       ~~   _//   _//   _// ~ _//     ~
                                     ~     / /   / /   / /   / /  ~      ~~
                                          ~~~   ~~~   ~~~   ~~~
```

KeepTesting
================
This plugin basically runs `gradle test` in current project on save and shows number of failed tests in status bar.

Might absolutely not work for you, I don't care! \o/

Note: Only tested on OS X Mountain Lion but should work on all the computers, right?

Installation
------------
Place KeepTesting.py in your `Packages/User` folder (where Sublime store stuff)

You might want to ignore `.keepTestingLock` in your project if you're annoyed by the slidy slidy on saving.

Usage
-----
Add this to your preferences file to enable

    "keep_testing": true

Todo
----
Feel free to fork and dig in to any of these, it's open source, right?
+ Move this and below list to issue tracker
+ Only run if enabled on project level
+ Show progress during testing
+ Show which test(s) fail
+ Keep results in status bar if failed? (`set_timeout` party)
+ Exception handling to never have to `rm .keepTestingLock`

Known Issues
------------
+ Poor code

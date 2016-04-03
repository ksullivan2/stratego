# STRATEGO
## The classic capture-the-flag board game!

(NEED TO CREDIT WHOEVER OWNS STRATEGO and the icons)

**To Run:**
----------
	1. Install Kivy **(LINK HERE)**
	2. Clone repo into a folder called `stratego` (or whatever you'd like)
	3. EITHER:
		* Run 'kivy __main__.py'
		* (from the parent folder) run `kivy stratego` (or your folder name)


**GAME RULES:**
-----------
The purpose of the game is to capture your opponent's flag.
Place your pieces on your side of the board in a strategic formation.

RULES:
  * Higher numbered pieces capture lower pieces.
  * Attacker wins in a tie.
  * 3s can defuse bombs.
  * 2s can move unlimited spaces.
  * 1s are Spies and can capture 10s only if the Spy attacks.

v 0.8
-----------
** NOTES **
  * There is no AI. Pretend you don't know you're moving the opponent's pieces.
  * The Pop-ups should be their own class. However, creating them as such results in a segmentation fault, so I wrote around it for now until I can figure that out.
  * This is a first foray into MVC... oh, the things I would do differently now.
# Lab 4: Vibe Coding (Match-3 Gem Swap)

Assigned repo: [SETAPESU26/57_match_three_gem](https://github.com/SETAPESU26/57_match_three_gem).
My fork with the changes: [VivianSobers/57_match_three_gem](https://github.com/VivianSobers/57_match_three_gem).

| File | What it is |
|------|------------|
| [`before.webm`](before.webm) | The game before any changes |
| [`after.webm`](after.webm) | The game after the fixes and features |
| [`match_three_gem/`](match_three_gem/) | Updated code |
| [`chat_history.pdf`](chat_history.pdf) | Exported chat with the AI assistant ([`.txt`](chat_history.txt) version) |

The code as provided crashed with `NameError: name 'c' is not defined` as soon as
a match had to be cleared, because `drop_and_refill()` was missing its column
loop. That's why the before video ends in a traceback instead of showing the
move-count bug.

Changes, one commit each on the fork:

1. Restored the missing loop in `drop_and_refill()` so the game stops crashing.
2. Invalid swaps no longer cost a move (README Task 1).
3. Chain reactions score 1x, 2x, 3x and so on, with a "COMBO xN!" popup (Task 2).
4. Matching 4 or more leaves a bomb gem that clears its row or column when matched (Task 3).
5. After 5 seconds without a click, two swappable gems pulse as a hint (Task 4).

To run it: `pip install pygame` (or `pygame-ce` on Python 3.14), then `python main.py` inside `match_three_gem/`.

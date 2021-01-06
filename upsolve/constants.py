# ASCII color constants
WHITE   = '\033[0m'  # white
RED     = '\033[31m' # red
GREEN   = '\033[32m' # green
ORANGE  = '\033[33m' # orange
BLUE    = '\033[34m' # blue
PURPLE  = '\033[35m' # purple

# Difficulty name constants
EASY = "Easy"
MEDIUM = "Medium"
HARD = "Hard"
HARDER = "Harder"
DIFFICULTY_DISPLAY = {
    EASY : GREEN + EASY + WHITE,
    MEDIUM : ORANGE + MEDIUM + WHITE,
    HARD : RED + HARD + WHITE,
    HARDER : PURPLE + HARDER + WHITE
}

# Platform name constants
LEETCODE = "leetcode"
BINARYSEARCH = "binarysearch"
PLATFORM_DISPLAY = {
    LEETCODE : GREEN + LEETCODE + WHITE,
    BINARYSEARCH: BLUE + BINARYSEARCH + WHITE
}

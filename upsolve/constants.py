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

DIFFICULTIES = [EASY, MEDIUM, HARD, HARDER]

DIFFICULTY_DISPLAY = {
    EASY : GREEN + EASY + WHITE,
    MEDIUM : ORANGE + MEDIUM + WHITE,
    HARD : RED + HARD + WHITE,
    HARDER : PURPLE + HARDER + WHITE
}

# Platform name constants
LEETCODE = "leetcode"
BINARYSEARCH = "binarysearch"

LEETCODE_WEEKLY_CODE = "lcw"
LEETCODE_BIWEEKLY_CODE = "lcb"
BINARYSEARCH_WEEKLY_CODE = "bsw"
BINARYSEARCH_EDUCATIONAL_CODE = "bse"

LEETCODE_WEEKLY_NAME = "Leetcode Weekly"
LEETCODE_BIWEEKLY_NAME = "Leetcode Biweekly"
BINARYSEARCH_WEEKLY_NAME = "Binaryseach Weekly"
BINARYSEARCH_EDUCATIONAL_NAME = "Binarysearch Educational"

CODES = {LEETCODE_WEEKLY_CODE : LEETCODE_WEEKLY_NAME,
         LEETCODE_BIWEEKLY_CODE: LEETCODE_BIWEEKLY_NAME,
         BINARYSEARCH_WEEKLY_CODE: BINARYSEARCH_WEEKLY_NAME,
         BINARYSEARCH_EDUCATIONAL_CODE: BINARYSEARCH_EDUCATIONAL_NAME}

PLATFORM_DISPLAY = {
    LEETCODE : GREEN + LEETCODE + WHITE,
    BINARYSEARCH: BLUE + BINARYSEARCH + WHITE
}


def platform_display(platform):
    return PLATFORM_DISPLAY[platform]

def difficulty_display(difficulty):
    return DIFFICULTY_DISPLAY[difficulty]

def contest_display(name):
    return PURPLE + name + WHITE

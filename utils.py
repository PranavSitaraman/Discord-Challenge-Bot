from pandas import read_csv
numojis = {0 : "0️⃣", 1 : "1️⃣", 2 : "2️⃣", 3 : "3️⃣ ", 4 : "4️⃣", 5 : "5️⃣", 6 : "6️⃣", 7 : "7️⃣", 8 : "8️⃣", 9 : "9️⃣"}
def leaderSort(csvName):
    df = read_csv(csvName)
    sorted_df = df.sort_values(by=["points"], ascending=False)
    sorted_df.to_csv(csvName, index=False)
    return True
def s2c(string):
    return [char for char in string]
def int2Emoji(num):
    string = ""
    num = [int(digit) for digit in s2c(str(num))][::-1]
    for digit in num: string += numojis[digit]
    return string
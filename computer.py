
play2 = 2
play1 = 1
play0 = 0

chess_important = 3
blank_importand = 1


def getPoint(arr):
    list_score = []
    score = 0
    #c = che(-1,-1)
    for i in range(0,19):
        for j in range(0,19):
            if arr[i][j] == play0:
                arr[i][j] = play2
                scorenext = getscore(arr,i,j,play2)
                arr[i][j] = play1
                scoreplay1=getscore(arr, i, j, play1)

                list_score.append([scorenext,scoreplay1,scorenext-scoreplay1,i,j])
                arr[i][j] = play0
    print(score)

    list_scorepalyer1= sorted(list_score, key=lambda tm: (tm[0], tm[1]), reverse=True)
    list_scorepalyer2 = sorted(list_score, key=lambda tm: (tm[1], tm[0]), reverse=True)
    #print(list_scorepalyer1)
    #print(list_scorepalyer2)
    result_x = -1
    result_y = -1
    if(list_scorepalyer1[0][0] >= list_scorepalyer2[0][1]):
        result_x=list_scorepalyer1[0][3]
        result_y=list_scorepalyer1[0][4]
    else:
        result_x = list_scorepalyer2[0][3]
        result_y = list_scorepalyer2[0][4]

    return [result_x,result_y]


def getscore(arr,x,y,player):

    start_i = max(x-5,0)
    end_i = min(x+5,18)
    start_j= max(y-5,0)
    end_j = min(y + 5, 18)

    maxcount = 0
    sumcombo = 0

    #横向
    count1, combo1 = getCountCombo(player,[arr[i][y] for i in range(x,start_i, -1)])
    count2, combo2 = getCountCombo(player,[arr[i][y] for i in range(x, end_i)])
    maxcount = max(maxcount, count1 + count2 - chess_important * 2)
    sumcombo += combo1 + combo2 - 2

    #垂直
    count1, combo1 = getCountCombo(player,[arr[x][i] for i in range(y, start_j, -1)])
    count2, combo2 = getCountCombo(player,[arr[x][i] for i in range(y, end_j)])
    maxcount = max(maxcount, count1 + count2 - chess_important * 2)
    sumcombo += combo1 + combo2 - 2

    #斜 左上右下
    start_p1 = min(y - start_j, x - start_i)
    end_p1 = min(end_i - x, end_j - y)
    count1, combo1 = getCountCombo(player,[arr[x-i][y-i] for i in range(start_p1)])
    count2, combo2 = getCountCombo(player,[arr[x+i][y+i] for i in range(end_p1)])
    maxcount = max(maxcount, count1 + count2 - chess_important * 2)
    sumcombo += combo1 + combo2 - 2

    #斜 左下右上
    start_p2 = min(end_j - y, x - start_i)
    end_p2 = min(end_i - x, y - start_j)
    count1, combo1 = getCountCombo(player,[arr[x - i][y + i] for i in range(start_p2)])
    count2, combo2 = getCountCombo(player,[arr[x + i][y - i] for i in range(end_p2)])
    maxcount = max(maxcount, count1 + count2 - chess_important * 2)
    sumcombo += combo1 + combo2 - 2

    '''
    if maxcount >=3:
        print(combo1)
        print(combo2)'''

    score = maxcount * 20 + sumcombo * 10
    '''
    if(score >0):
        print("maxcount"+str(maxcount))
        print("sumcombo"+str(sumcombo))
        '''
    return score

def getCountCombo(player,list):
    count = 0
    combo = 0
    combo_count = True
    for item in list:
        if item == player:
            count += chess_important
            if combo_count:
                combo += 1
        elif item == play0:
            count += blank_importand
            combo_count = False
        else:
            break
    return count,combo





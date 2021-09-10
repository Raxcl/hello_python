# -- coding: utf-8 --
# 猜数字
import random
rand = random.randint(1, 100)
for i in range(1, 11):
    num = int(input('在我心中有一个数，请你猜猜看'))
    if num < rand:
        print('小了')
    elif num > rand:
        print('大了')
    else:
        print('你真是个小机灵鬼~')
        break
print(f'你一共猜对了{i}次')
if i < 3:
    print('你的智商已经打败了女娲')
elif i <= 7:
    print('你的智商震古烁今')
else:
    print('你真是个小菜鸡，来我家让我亲自教教你')



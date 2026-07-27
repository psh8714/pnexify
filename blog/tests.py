from django.test import TestCase

# Create your tests here.

# name = input("enter your name: ")
# school = input("enter your school name: ")
# nomre_sabet = 21
# sum = 0
# for i in range(4):
#     nomre_saier = int(input("enter your nomre: "))
#     if nomre_saier != nomre_sabet:
#         sum += nomre_saier
# sum += nomre_sabet
# print(f'name: {name}\nschool: {school}\nshomare daftar nomre: {nomre_sabet}\nmiangin nomre ha: {sum / 5}')
#
# # -----------------------------------------
#
# import turtle
#
# t = turtle.Turtle()
# t.speed(3)
# t.pensize(8)
# t.color('green')
#
# t.fd(80)
# t.rt(90)
# t.fd(80)
# t.rt(90)
# t.fd(80)
# t.rt(-90)
# t.forward(90)
# t.rt(90)
# t.forward(-100)
# t.rt(90)
# t.fd(22.5)
# t.rt(-90)
# t.fd(77.5)
# t.rt(90)
# t.fd(45)
# t.rt(90)
# t.forward(80)
# t.rt(-90)
# t.forward(120)
# t.rt(-90)
# t.fd(107)
# t.rt(-90)
# t.fd(18)
#
# t.penup()
# t.goto(150, 20)
# t.pendown()
#
# t.fd(190)
# t.rt(90)
# t.fd(20)
# t.rt(90)
# t.fd(190)
# t.rt(90)
# t.fd(20)
#
#
# turtle.done()

for i in range(100000):
    print(chr(i),end='   ')
    if i % 20 == 0:
        print("\n")
print("Welcome to gothic game! 💀")
print("#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$")
level_1_select = input(("You now in HALL!\n Where do you want to go?\n r or l? ")).lower()


if level_1_select == "l":
    print("Your now is in the BLOOD KITCHEN! 🩸 \n")
    print("You LOSE!");
elif level_1_select == "r":
    print("HaHa! You now in the OLD LIBRARY 📚🕯️")
    level_2_select = input("Look at this BOOK and look at the DOOR! Which one do you prefer?\n b or d?").lower()
    if level_2_select == "b":
        print("You LOSE!");
    elif level_2_select == "d":
        print("You now in the OLD YARD! 🛖\n")
        level_3_select = input("Look at that HELL DOG🦮👺 Do you want move slowly or quick? s or q?").lower()
        if level_3_select == "q":
            print("OH! Dog is awake! and it is going to eat YOU!!!")
        elif level_3_select == "s":
            print("You Win!")

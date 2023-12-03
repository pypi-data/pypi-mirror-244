def main():
    while True:
        with open(__file__, 'a') as f:
            user_input = input("Lütfen eklemek istediğiniz kodu girin: ")
            if "exit" in user_input:
                break
            else:
                f.write('\n' + user_input)

main()
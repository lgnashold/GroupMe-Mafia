import groupme_services

def main(args = None):
    auth_token = "iTAjSlxKUsiZmjXIVma1CoGfcDMQvN5xfWcfeout"
    print("Staring a New Game")
    # Test images
    # url = groupme_services.upload_image("iTAjSlxKUsiZmjXIVma1CoGfcDMQvN5xfWcfeout", "./test.png")
    # print(url)
    # print(groupme_services.send_message("fed24b4da45703f411f1b202f7", "Check this sickkk image", url))
    print(groupme_services.create_bot(auth_token, "50770257"))
    

if __name__ == "__main__":
    main()

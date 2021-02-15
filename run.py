from url_shortener import appF, localHost


if __name__ == '__main__':
    if localHost:
        appF.run(debug=True)
        print("running local host")
    else:
        appF.run()

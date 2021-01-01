from controller import app
import utils


def main():
    app.run()


if __name__ == '__main__':
    print(utils.base64encode('阿迪达斯(森林摩尔折扣店)'))
    main()

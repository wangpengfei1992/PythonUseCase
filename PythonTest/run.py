# 测试程序入口
import argparse


def get_arguments():
    parse = argparse.ArgumentParser("传入的内容")
    parse.add_argument("--token", required=True, help="传入token")
    parse.add_argument("--key", help="测试key")
    return parse.parse_args()


if __name__ == '__main__':
    print(f'入口参数传递测试')
    args = get_arguments()
    print(f'获取传入的内容token={args.token};key={args.key}')

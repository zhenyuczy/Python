# -*- coding: utf-8 -*-

import os


'''在指定文件目录查找对应后缀文件'''


def get_file_suffix(file_name):
    return file_name[file_name.rfind('.') + 1:]


def search_target_file(now_directory, target_suffix, output_directory_object):

    for each_file in os.listdir(now_directory):
        next_directory = os.path.join(now_directory, each_file)

        if os.path.isdir(next_directory):
            search_target_file(next_directory, target_suffix, output_directory_object)
        else:
            for each_target_suffix in target_suffix:
                if get_file_suffix(each_file).lower() == each_target_suffix:
                    output_directory_object.writelines(next_directory + '\n')
                    break
                else:
                    pass
            else:
                pass
    else:
        pass


# print(__file__)
# print(os.path.dirname(__file__))
# print(os.path.realpath(__file__))
# print(os.path.dirname(os.path.realpath(__file__)))
# print(os.getcwd())

def main():
    target_file_directory = input('请输入要查找的文件目录：')
    file_name_output_directory = input('请输入目标文件名存储目录：')
    target_file_suffix = ['cpp', 'c', 'cs', 'py']
    f = open(file_name_output_directory, "w")
    search_target_file(target_file_directory, target_file_suffix, f)
    f.close()


if __name__ == '__main__':
    main()











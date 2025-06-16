from functions.get_files_info import get_file_content


def test():
    result = get_file_content("calculator", "main.py")
    print("Result for calculator, main:")
    print(result)
    print("")

    result = get_file_content("calculator", "pkg/calculator.py")
    print("Result for calulator, pkg/calculator.py :")
    print(result)
    print("")

    result = get_file_content("calculator", "/bin/cat")
    print("Result for calculator, /bin/cat:")
    print(result)

    

if __name__ == "__main__":
    test()

import os
import json

'''
    For the given path, get the List of all files in the directory tree 
'''


def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    outside_list = []
    # inside_list = []

    # Iterate over all the entries

    for entry in listOfFile:
        # Create full path

        fullPath = os.path.join(dirName, entry)
        fsize = os.stat(fullPath).st_size

        pathsize = fullPath + ", " + str(fsize)

        # If entry is a directory then get the list of files in this directory -
        # uncomment the below code to include files in sub directories
        # if os.path.isdir(fullPath):
        #     for i in range(0,1):
        #         inside_list=[]
        #         inside_list.append(fullPath)
        #         inside_list.append(fsize)
        #     outside_list.append(inside_list)
        #     #print("###--- ", outside_list )
        #     allFiles = getListOfFiles(fullPath)
        #     allFiles.append(pathsize)
        #
        #
        # else:
        #     #allFiles.append(fullPath)
        for i in range(0,1):
            inside_list = []
            inside_list.append(fullPath)
            inside_list.append(fsize)
        outside_list.append(inside_list)

        allFiles.append(pathsize)

    return outside_list


def main():
    dirName = input("input mount point : -")

    # Get the list of all files in directory tree at given path
    listOfFiles = getListOfFiles(dirName)

    fileDict = {"files" : listOfFiles}

    fileSpace_json = json.dumps(fileDict)

    print(json.dumps(fileDict, indent=4))

    # uncomment the below code to write to a file
    # with open('data.txt', 'w') as outfile:
    #     json.dump(fileDict, outfile, sort_keys=True, indent=4,
    #               ensure_ascii=False)


if __name__ == '__main__':
    main()

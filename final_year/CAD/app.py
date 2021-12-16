import numpy as np

def main():
    while True: 
        print("===========================================================")
        inputMatrix, branches = getInputMatrix()
        if validateInputMatrix(inputMatrix): 
            print("The matrix Elements values are not accepted\n")
            continue

        cMatrix = calcCMatrix(inputMatrix, branches)
        print("\n\n C Matrix: \n", cMatrix)

        bMatrix = calcBMatrix(inputMatrix, branches)
        print("\n\n B Matrix: \n", bMatrix)


def getInputMatrix():
    R = int(input("Enter the number of rows: "))
    C = int(input("Enter the number of columns: "))
    B = int(input("Enter the number of branches: "))

    print("Enter the elements of A matrix ORDERED in a single line (separated by space): ")

    # User input of entries in a
    # single line separated by space
    entries = list(map(int, input().split()))
    return np.array(entries).reshape(R, C), B

def validateInputMatrix(inputMatrix):
    column_sums = inputMatrix.sum(axis=0)
    acceptedElementsValues = [0, 1, -1]
    for i in range(len(column_sums)):
        if column_sums[i] not in acceptedElementsValues:
            return True
    return False

def completeAMatrix(inputMatrix):
    column_sums = inputMatrix.sum(axis=0)
    facingMatrix = []
    if any(column_sums[i] != 0 for i in column_sums):
        for i in range(len(column_sums)):
            if column_sums[i] == 0:
                facingMatrix.append(0)
            elif column_sums[i] == 1:
                facingMatrix.append(-1)
            else:
                facingMatrix.append(1)
    A = np.concatenate((inputMatrix, np.array(facingMatrix).reshape(1, len(facingMatrix))), axis=0)
    if len(facingMatrix) > 0:
        return A, True
    return A, False

def getATree(AMatrix, branches, isRowAdded):
    if isRowAdded:
        AMatrix = AMatrix[:-1]
    return AMatrix[:, 0:branches]

def getInverseOfATree(ATree):
    return np.linalg.inv(ATree)

def getALinks(AMatrix, branches, isRowAdded):
    if isRowAdded:
        AMatrix = AMatrix[:-1]
    return AMatrix[:, branches:]

def calcCMatrix(inputMatrix, branches):
    AMatrix, isRowAdded = completeAMatrix(inputMatrix)
    aTree = getATree(AMatrix, branches, isRowAdded)
    aTreeInverse = getInverseOfATree(aTree)
    aLinks = getALinks(AMatrix, branches, isRowAdded)
    cLinks = getCLinks(aTreeInverse, aLinks)
    cLinksMatrixRows = np.shape(aTree)[0]
    # identity matrix * cLinks matrix
    return np.concatenate((np.identity(cLinksMatrixRows), cLinks), axis=1)

def getCLinks(aTreeInverse, aLinks):
    return np.matmul(aTreeInverse, aLinks)

def getBTree(cLinks):
    return cLinks.transpose()

def calcBMatrix(inputMatrix, branches):
     AMatrix, isRowAdded = completeAMatrix(inputMatrix)
     aTree = getATree(AMatrix, branches, isRowAdded)
     aTreeInverse = getInverseOfATree(aTree)
     aLinks = getALinks(AMatrix, branches, isRowAdded)
     cLinks = getCLinks(aTreeInverse, aLinks)
     bTree = getBTree(cLinks)
     bTreeMatrixRows = np.shape(bTree)[0]
     return np.concatenate((bTree, np.identity(bTreeMatrixRows)), axis=1)

if __name__ == "__main__":
    main()
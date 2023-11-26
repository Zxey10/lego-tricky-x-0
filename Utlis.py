class Utils:

    @staticmethod
    def convertListTo2DArr(array, cols: int):
        return [array[i:i+cols] for i in range(0, len(array), cols)]

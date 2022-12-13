import copy


class pnmImage(object):
    """
        Класс для работы с файлами в pnm формате
    """

    def __init__(self):
        """
        Создание переменных для последуещей работы с pnm файлами
        type - тип файла
        info - ширина и высота в исходном формате
        buffer - массив пикселей
        rgd - максимальное значение цвета
        size - ширина и высота в нужном формате
    """
        self.type = None
        self.info = None
        self.bufferRGB = []
        self.rgb = None
        self.width = None
        self.height = None
        self.size = None
        self.model = "RGB"
        self.colorModel = []

    def open(self, path, model):
        file = open(path, 'rb')
        if file.closed:
            return "The File is not open"
        self.type = file.readline()
        if self.type.__str__().find("P6") == -1 and self.type.__str__().find("P5") == -1:
            return "This File type is not supported "
        self.info = file.readline()

        width, height = self.info.__str__().split(' ')
        width = width.removeprefix("b'")
        height = height.removesuffix("\\n'")
        self.width, self.height = int(width), int(height)
        self.size = int(width) * int(height)
        self.rgb = file.readline()
        self.model = model
        if model == 'RGB':
            self.bufferRGB = []
            for index in range(0, self.size):
                self.bufferRGB.append([])
                for j in range(3):
                    byte_s = file.read(1)
                    self.bufferRGB[index].append(ord(byte_s) / 255)
        else:
            pass

        file.close()
        return "Success"

    def save(self, path, out, t):
        res = copy.deepcopy(out)
        file = open(path, 'wb')
        if file.closed:
            print("not open")

        if t == 1:
            file.write(self.type)
        else:
            file.write(bytearray(b'P5\n'))
        file.write(self.info)
        file.write(self.rgb)

        for i in range(0, self.size):
            if t == 1:
                res[i][0] = int(res[i][0] * 255)
                res[i][1] = int(res[i][1] * 255)
                res[i][2] = int(res[i][2] * 255)
                if res[i][0] > 255:
                    res[i][0] = 255
                if res[i][1] > 255:
                    res[i][1] = 255
                if res[i][2] > 255:
                    res[i][2] = 255

                if res[i][0] < 0:
                    res[i][0] = 0
                if res[i][1] < 0:
                    res[i][1] = 0
                if res[i][2] < 0:
                    res[i][2] = 0
            else:
                res[i] = int(res[i] * 255)
                if res[i] > 255:
                    res[i] = 255
                if res[i] < 0:
                    res[i] = 0

        if t == 1:
            for index in range(0, self.size):
                file.write(bytearray(res[index]))
        else:
            file.write(bytearray(res))
        file.close()

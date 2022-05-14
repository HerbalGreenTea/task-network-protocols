class DnsResponse:
    def __init__(self, data):
        self.data = data
        self.header = Header(data)
        self.questions = []
        self.answers = []

        self.parse()

    def parse(self):
        offset = self.parse_questions(self.data)
        offset = self.parse_answers(self.data, offset)

    def parse_questions(self, data):
        offset = 24
        for i in range(self.header.count_questions):
            name, new_offset = get_name(data, offset)
            offset += new_offset
            q_type = data[offset:offset + 4]
            q_clc = data[offset + 4:offset + 8]
            offset += 8
            self.questions.append(Queries(name, q_type, q_clc))
        return offset

    def parse_answers(self, data, start_offset):
        offset = start_offset
        for i in range(self.header.count_answers):
            name, new_offset = get_name(data, offset)
            offset += new_offset
            a_type = data[offset:offset + 4]
            a_clc = data[offset + 4:offset + 8]
            offset += 8
            time = data[offset:offset+8]
            offset += 8
            data_length = from16to10(data[offset:offset+4]) * 2
            offset += 4

            address = data[offset:offset+data_length]

            msg_type = get_type(a_type)
            ans_data = ""
            if msg_type == "A":
                ans_data = parse_address(address, data_length // 2)
            elif msg_type == "NS":
                ans_data = get_name(data, offset)

            offset += data_length

            self.answers.append(Answer(name, a_type, a_clc, time, data_length // 2, ans_data))
        return offset

    def get_data_answers(self):
        data_answers = []
        for answer in self.answers:
            data_answers.append(answer.answer_data)
        return data_answers

    def get_answer(self):
        if len(self.answers) > 0:
            return self.answers[0]


class DnsRequest:
    def __init__(self, data):
        self.data = data
        self.header = Header(data)
        self.questions = []

        self.parse_questions(self.data)

    def parse_questions(self, data):
        offset = 24
        for i in range(self.header.count_questions):
            name, new_offset = get_name(data, offset)
            offset += new_offset
            q_type = data[offset:offset + 4]
            q_clc = data[offset + 4:offset + 8]
            offset += 8
            self.questions.append(Queries(name, q_type, q_clc))
        return offset


class Header:
    def __init__(self, data):
        self.header = data[0:24]
        self.id = self.header[0:4]
        self.flags = self.header[4:8]
        self.count_questions = from16to10(self.header[8:12])
        self.count_answers = from16to10(self.header[12:16])
        self.count_authority = from16to10(self.header[16:20])
        self.count_additional = from16to10(self.header[20:24])


class Queries:
    def __init__(self, name, q_type, q_class):
        self.name = name
        self.q_type = get_type(q_type)
        self.q_class = q_class


class Answer:
    def __init__(self, name, a_type, a_class, time, data_length, answer_data):
        self.name = name
        self.a_type = get_type(a_type)
        self.a_class = a_class
        self.time = from16to10(time)
        self.data_length = data_length
        self.answer_data = answer_data


def from16to10(num):
    return int(num, 16)


def from16to2(num):
    return bin(int(num))


def parse_address(data, data_length):
    address = ""
    offset = 0
    for i in range(data_length):
        address += str(from16to10(data[offset:offset+2])) + "."
        offset += 2
    return address[0:len(address)-1]


def get_type(data):
    num = from16to10(data)
    if num == 1:
        return "A"
    elif num == 2:
        return "NS"


def get_name(data, start_from=24):
    name = ''
    offset = 0

    while True:
        i = start_from + offset
        chunks = int(data[i:i + 4], 16)

        if chunks >= 49152:
            name, offset = get_part_name(data, chunks, name)
            offset = 4
            break

        if int(data[i:i + 2], 16) == 0:
            offset += 2
            break

        name = add_part_name(data, name, i)
        offset += int(data[i:i + 2], 16) * 2 + 2

    if name[len(name) - 1] == ".":
        return name[:len(name) - 1], offset
    else:
        return name, offset


def get_part_name(data, chunks, name):
    start_from = int(str(bin(chunks))[4:], 2) * 2
    part_name, offset = get_name(data, start_from)
    if name != "" and name[len(name)-1] != '.':
        name += '.' + part_name
    else:
        name += part_name
    return name, offset


def add_part_name(data, name, index):
    for i in range(0, int(data[index:index + 2], 16) * 2, 2):
        part_name = chr(int(data[index + i + 2:index + i + 4], 16))
        name += part_name
    return name + "."


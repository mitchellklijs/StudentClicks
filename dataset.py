import csv
import operator
import random

TRAIN_SET_PERCENTAGE = 0.4

STUDENT_INFO = 'studentInfo.csv'
TRAIN_STUDENT_INFO = 'studentInfoTrain.csv'
TEST_STUDENT_INFO = 'studentInfoTest.csv'

STUDENT_VLE = 'studentVle.csv'
TRAIN_STUDENT_VLE = 'studentVleTrain.csv'
TEST_STUDENT_VLE = 'studentVleTest.csv'

if __name__ == '__main__':
    # GET ALL STUDENT IDS
    student_ids = list()

    with open(STUDENT_INFO) as student_info:
        student_info_reader = csv.reader(student_info, delimiter=',', quotechar='"')

        for row in student_info_reader:
            if student_info_reader.line_num == 1:
                continue

            student_ids.append(row[2])

    # SPLIT STUDENT IDS INTO TRAINING AND TEST
    length = len(student_ids)
    train_length = round(length * TRAIN_SET_PERCENTAGE)

    train_indexes = random.sample(range(0, length - 1), train_length)
    train_student_ids = set(operator.itemgetter(*train_indexes)(student_ids))
    test_student_ids = set(student_ids).difference(set(train_student_ids))

    # CREATE NEW DATASETS
    for [TRAIN_FILE, TEST_FILE, STUDENT_FILE] in [[TRAIN_STUDENT_INFO, TEST_STUDENT_INFO, STUDENT_INFO],
                                                  [TRAIN_STUDENT_VLE, TEST_STUDENT_VLE, STUDENT_VLE]]:
        with open(TRAIN_FILE, 'w', newline='') as train_file, open(TEST_FILE, 'w', newline='') as test_file, open(
                STUDENT_FILE) as student_info:
            student_info_reader = csv.reader(student_info, delimiter=',', quotechar='"')
            train_file_writer = csv.writer(train_file)
            test_file_writer = csv.writer(test_file)

            for row in student_info_reader:
                if student_info_reader.line_num == 1:
                    train_file_writer.writerow(row)
                    test_file_writer.writerow(row)
                    continue

                student_id = row[2]

                if student_id in train_student_ids:
                    train_file_writer.writerow(row)
                else:
                    test_file_writer.writerow(row)

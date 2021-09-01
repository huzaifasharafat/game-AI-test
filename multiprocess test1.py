import multiprocessing
import pygame

def print_records(records):
    """
    function to print record(tuples) in records(list)
    """
    for record in records:
        print("Name",record)


def insert_record(record, records):
    """
    function to add a new record to records(list)
    """
    records.append(record)
    print("New record added!\n")


if __name__ == '__main__':
    # creating a list in server process memory
    records = multiprocessing.Manager().list([])
    enemie1 = multiprocessing.Manager().__class__(pygame.sprite.Group())
    # new record to be inserted in records

    records.append(10)
    records.append(112)
    records.append(13)
    records.append(14)

    new_record = 8

    # creating new processes
    p1 = multiprocessing.Process(target=insert_record, args=(new_record, records))
    p2 = multiprocessing.Process(target=print_records, args=(records,))

    # running process p1 to insert new record
    p1.start()
    p1.join()

    # running process p2 to print records
    p2.start()
    p2.join()
    records[1] = 55
    print(records)
from getExcel import get_all_from_files, get_part_from_tables, get_one_file

# print(*get_one_file('1.xlsx'), sep='\n')
import random
def generate_phone():
    return '8' + ''.join(str(random.randint(0, 9)) for _ in range(10))


print(*[generate_phone() for _ in range(10)], sep='\n')

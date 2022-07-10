import xlsx2csv
import configparser as cf

# Reading params for input and output file
config = cf.ConfigParser()
config.read_file(open('config.cfg'))
xlsx_file = config.get('APP', 'INPUT_EXCEL')
csv_file = config.get('APP', 'OUTPUT_CSV')

print(f'Converting {xlsx_file} to {csv_file}...')

# Converting csv to xlsx
xlsx2csv.Xlsx2csv(xlsx_file, delimiter=';').convert(csv_file, sheetid=1)

print('Done!')
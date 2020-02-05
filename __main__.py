from mail import Mail
import numpy as np

def main():
    history = np.genfromtxt('history.csv', delimiter=',', dtype='object')
    present_response_codes = list(history[1:,5].astype('str'))
    sno = len(present_response_codes) + 1
    with open('history.csv', 'a') as file:
        for i in range(1,36):
            uri = f'./data/{i}.eml'
            data = Mail(uri).getData()
            if data == None:
                print('Error in collecting data from:', uri)
            else:
                if data.UIDAI_Response_Code not in present_response_codes:
                    present_response_codes.append(data.UIDAI_Response_Code)
                    file.write(f'\n{sno},{str(data)}')
                    sno += 1

if __name__ == '__main__':
    main()
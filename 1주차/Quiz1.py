'''------------------------------------------------------------------
당신의 학번을 입력해서 복소수를 연산하시오.
예시)
student ID = 12345678
(1+2i) x (3+4i) / (5+6i) x (7+8i)
------------------------------------------------------------------'''

def complex_operation(eight_digit_number):
    # Splitting the 8-digit number into individual digits
    digits = [int(d) for d in str(eight_digit_number)]

    # Creating complex numbers using the digits
    z1 = complex(digits[0], digits[1])
    z2 = complex(digits[2], digits[3])
    z3 = complex(digits[4], digits[5])
    z4 = complex(digits[6], digits[7])

    # Performing the complex number operation: (z1*z2) / (z3*z4)
    result = (z1 * z2) / (z3 * z4)
    return result

student_ID = input("enter student ID : ")

result = complex_opperation(student_ID)
print(result)

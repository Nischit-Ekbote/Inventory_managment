def validPhoneNumber(phoneNo : str) -> bool:
    if not len(phoneNo) == 10:
        return False
    
    for digit in phoneNo:
        if not (digit >= '0' and digit <= '9'):
            return False
    return True


def validPIN(pinCode : str) -> bool:
    if not len(pinCode) == 6:
        return False
    
    for digit in pinCode:
        if not (digit >= '0' and digit <= '9'):
            return False
    return True

def standarisePAN(panNo : str) ->str:
    return panNo.upper()

def validPAN(panNo : str) -> bool:
    if not len(panNo) == 10:
        return False

    for i in range(10):
        if i < 5 or i == 9:
            if not (panNo[i] >= "A" and panNo[i] <= "Z"):
                return False
        else:
            if not(panNo[i] >= '0' and panNo[i] <= '9'):
                return False
    return True

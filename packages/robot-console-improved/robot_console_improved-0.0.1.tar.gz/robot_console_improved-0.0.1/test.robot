*** Test Cases ***
Simple IF
    ${random_number}    Evaluate    random.randint(0, 10)
    IF    ${random_number} % 2
        Log To Console    \n${random_number} is odd!
    END
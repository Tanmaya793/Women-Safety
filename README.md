# Women-Safety
# Please ensure to export the folders before using. As there is a database connected to our code the user need to modify the code for their use. 
# To run the program run the flask api i.e. app.py on your terminal.
# if any errors shown, it must be due to change in system environment. Ensure proper availability of python, Camera accessability and database connectivity.
# You can use the following sql code to make your own local database system
#   -- Create the table
    CREATE TABLE users (
    USERID VARCHAR(50) PRIMARY KEY,
    PASSWORD VARCHAR(50),
    TYPE VARCHAR(50),
    STATION_NAME VARCHAR(50),
    BOOTH_NUMBER VARCHAR(50),
    LOCATION VARCHAR(50),
    telephone_number VARCHAR(15)
    );

    -- Insert the data
    INSERT INTO users (USERID, PASSWORD, TYPE, STATION_NAME, BOOTH_NUMBER, LOCATION, telephone_number) VALUES
    ('admin', 'Admin', 'None', 'None', 'None', 'None', 'None'),
    ('password', 'Authority', 'Gunupur', 'gunupur02', 'Gunupur', '111111111'),
    ('aska', 'Authority', 'Aska', 'Aska01', 'Aska', '1231231234'),
    ('123w', 'Authority', 'gunupur', 'ginupur01', 'gunupur', '12131345'),
    ('1234A', 'Authority', 'gunupur', 'ginupur02', 'gunupur', '12131345'),
    ('kbv12', 'Authority', 'kabisurya nagar', 'kabisurya nagar 01', 'kabisurya nagar', '9861946412'),
    ('gumuda01', 'Authority', 'Gumuda', 'Gumuda01', 'Gumuda', '23565872873'),
    ('gumuda02', 'Authority', 'Gumuda', 'Gumuda02', 'Gumuda', '65464665365'),
    ('kama', 'Authority', 'kama', 'kama01', 'kama', '1234567891');

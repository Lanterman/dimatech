import ctypes


token = ctypes.c_wchar_p(" ")

user_info_1 = {
    'first_name': 'test_user', 
    'last_name': 'test_user', 
    'email': 'test_user@mail.ru', 
    'is_activated': True, 
    'is_admin': False, 
    'hashed_password': 'IjQQPtNYXaLY$62285ee8c136f05cfffd5350dbbfc92e39b05349811702b1f002abb9abd7e4d8'
}

user_info_2 = {
    'first_name': 'test_admin', 
    'last_name': 'test_admin', 
    'email': 'test_admin@mail.ru', 
    'is_activated': True, 
    'is_admin': True, 
    'hashed_password': 'bTzTzoZLeWKi$5cde3d6168d27855c2e24821aa302b62159be66990b751ac67ce69beaf4b2191'
}

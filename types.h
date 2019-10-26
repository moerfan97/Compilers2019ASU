#include<iostream>
#include <fstream> 
#include<string>
#include<vector>
#pragma once

typedef enum state{START,INCOMMENT,INNUM,INID,INASSIGN,DONE}state;
typedef struct x{
	bool is_num = false;
	std::string token_type;
	std::string token_name;
	int token_value;
}token_record;
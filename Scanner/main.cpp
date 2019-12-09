#include"types.h"
using namespace std;
int main(void)
{
	ofstream output_file;
	output_file.open("out.txt");
	int flag_comment=0;
	while (1)
	{
		string input = "", output, temp, file_name;
		ifstream input_file;
		// by default open mode = ios::in mode
		cout << "Enter file name with extension: ";
		cin >> file_name;
		input_file.open(file_name);
		while (input_file) {
			// Read a Line from standard input 
			getline(input_file, temp);
			//if (temp == "\0")break;
			input += temp;
			temp = "";
		}
		cout << input;
		cout << endl;
		// Close the file 
		input_file.close();


		bool flag_continue = false;
		int tokens_number = 0,counter=0;
		vector <token_record> tokens;
		char character;
		state current_state = START;
		state next_state;
		//getline(cin, input);
		for ( int i = 0; i < input.length(); i++)
		{	
			counter++;
			if (flag_continue)
			{
				break;
			}
			switch (current_state)
			{
			case START:
				if (input[i] == ' ')
				{
					next_state = START;
				}
				else if (input[i] == '{')
				{
					next_state = INCOMMENT;
					output.push_back(input[i]);
					flag_comment=1;
				}
				else if (input[i] == ':')
				{
					next_state = INASSIGN;
					output.push_back(input[i]);
				}
				else if (input[i] >= '0' && input[i] <= '9')
				{
					next_state = INNUM;
					output.push_back(input[i]);
					if (i == (input.length() - 1))
					{
						next_state = DONE;
						token_record token;
						token.token_value = stoi(output);
						token.token_type = "number";
						token.is_num = true;
						tokens.push_back(token);
						tokens_number++;
					}
					else
					{
						if ((input[i + 1] >= 'A' && input[i + 1] <= 'Z') || (input[i + 1] >= 'a' && input[i + 1] <= 'z'))
						{
							next_state = DONE;
							flag_continue = true;
							continue;
						}
						else if (!(input[i + 1] >= '0' && input[i + 1] <= '9'))
						{
							next_state = DONE;
							token_record token;
							token.token_value = stoi(output);
							token.token_type = "number";
							token.is_num = true;
							tokens.push_back(token);
							tokens_number++;
						}
						else
						{

						}
					}
				}
				else if ((input[i] >= 'A' && input[i] <= 'Z') || (input[i] >= 'a' && input[i] <= 'z'))
				{
					next_state = INID;
					output.push_back(input[i]);

					if (i == (input.length() - 1))
					{
						next_state = DONE;
						token_record token;
						token.token_name = output;
						/////handling reserved words
						if (output == "if"
							|| output == "then" ||
							output == "else" ||
							output == "end" ||
							output == "repeat" ||
							output == "until" ||
							output == "read" ||
							output == "write")
						{
							for (int i = 0; i < output.length(); i++)
							{
								output[i] = toupper(output[i]);
							}
							token.token_type = output;
						}
						else
						{
							token.token_type = "Identifier";
						}
						token.is_num = false;
						tokens.push_back(token);
						tokens_number++;
					}
					else
					{
						if ((input[i + 1] >= '0' && input[i + 1] <= '9'))
						{
							next_state = DONE;
							flag_continue = true;
							continue;
						}
						else if (!((input[i + 1] >= 'A' && input[i + 1] <= 'Z') || (input[i + 1] >= 'a' && input[i + 1] <= 'z')))
						{
							token_record token;
							token.token_name = output;

							/////handling reserved words
							if (output == "if"
								|| output == "then" ||
								output == "else" ||
								output == "end" ||
								output == "repeat" ||
								output == "until" ||
								output == "read" ||
								output == "write")
							{
								for (int i=0;i<output.length();i++)
								{
									output[i] = toupper(output[i]);
								}
								token.token_type = output;
							}
							else
							{
								token.token_type = "Identifier";
							}

							token.is_num = false;
							tokens.push_back(token);
							tokens_number++;
							next_state = DONE;
						}
						else
						{

						}
					}
				}
				////+
				else if (input[i] == '+')
				{
					next_state = DONE;
					output.push_back(input[i]);
					token_record token;
					token.token_name = output;
					token.token_type = "plus";
					token.is_num = false;
					tokens.push_back(token);
					tokens_number++;
				}
				/////-
				else if (input[i] == '-')
				{
					next_state = DONE;
					output.push_back(input[i]);
					token_record token;
					token.token_name = output;
					token.token_type = "minus";
					token.is_num = false;
					tokens.push_back(token);
					tokens_number++;
				}
				/////////// /
				else if (input[i] == '/')
				{
					next_state = DONE;
					output.push_back(input[i]);
					token_record token;
					token.token_name = output;
					token.token_type = "divide";
					token.is_num = false;
					tokens.push_back(token);
					tokens_number++;
				}
				///////////// *
				else if (input[i] == '*')
				{
					next_state = DONE;
					output.push_back(input[i]);
					token_record token;
					token.token_name = output;
					token.token_type = "multiply";
					token.is_num = false;
					tokens.push_back(token);
					tokens_number++;
				}
				////////=
				else if (input[i] == '=')
				{
					next_state = DONE;
					output.push_back(input[i]);
					token_record token;
					token.token_name = output;
					token.token_type = "equal";
					token.is_num = false;
					tokens.push_back(token);
					tokens_number++;
				}
				//////<
				else if (input[i] == '<')
				{
					next_state = DONE;
					output.push_back(input[i]);
					token_record token;
					token.token_name = output;
					token.token_type = "LT";
					token.is_num = false;
					tokens.push_back(token);
					tokens_number++;
				}
				/////////>
				else if (input[i] == '>')
				{
					next_state = DONE;
					output.push_back(input[i]);
					token_record token;
					token.token_name = output;
					token.token_type = "MT";
					token.is_num = false;
					tokens.push_back(token);
					tokens_number++;
				}
				//////(
				else if (input[i] == '(')
				{
					next_state = DONE;
					output.push_back(input[i]);
					token_record token;
					token.token_name = output;
					token.token_type = "left bracket";
					token.is_num = false;
					tokens.push_back(token);
					tokens_number++;
				}
				///////)
				else if (input[i] == ')')
				{
					next_state = DONE;
					output.push_back(input[i]);
					token_record token;
					token.token_name = output;
					token.token_type = "right bracket";
					token.is_num = false;
					tokens.push_back(token);
					tokens_number++;
				}
				////////;
				else if (input[i] == ';')
				{
					next_state = DONE;
					output.push_back(input[i]);
					token_record token;
					token.token_name = output;
					token.token_type = "separator";
					token.is_num = false;
					tokens.push_back(token);
					tokens_number++;
				}
				/////////[
				else if (input[i] == '[')
				{
					next_state = DONE;
					output.push_back(input[i]);
					token_record token;
					token.token_name = output;
					token.token_type = "left bracket";
					token.is_num = false;
					tokens.push_back(token);
					tokens_number++;
				}
				///////]
				else if (input[i] == ']')
				{
					next_state = DONE;
					output.push_back(input[i]);
					token_record token;
					token.token_name = output;
					token.token_type = "right bracket";
					token.is_num = false;
					tokens.push_back(token);
					tokens_number++;
				}
				//else
				else
				{
					next_state = DONE;
				}

				break;
				//////////////////INCOMMENT
			case INCOMMENT:
				if (input[i] == '}')
				{
					next_state = START;
					flag_comment=0;
				}
				else
				{
					next_state = INCOMMENT;
				}
				output = "";
				break;
				///////////////////////INASSIGN
			case INASSIGN:
				if (input[i] == '=')
				{
					next_state = DONE;
					output.push_back(input[i]);
					token_record token;
					token.token_name = output;
					token.token_type = "assign";
					tokens.push_back(token);
					tokens_number++;
				}
				else
				{
					next_state = DONE;
					flag_continue = true;
					continue;
					output = "";
				}
				break;
				/////////////////INNUM
			case INNUM:
				if (input[i] >= '0' && input[i] <= '9')
				{
					next_state = INNUM;
					output.push_back(input[i]);
					if (i == (input.length() - 1))
					{
						next_state = DONE;
						token_record token;
						token.token_value = stoi(output);
						token.token_type = "number";
						token.is_num = true;
						tokens.push_back(token);
						tokens_number++;
					}
					else
					{
						if ((input[i+1] >= 'A' && input[i+1] <= 'Z') || (input[i+1] >= 'a' && input[i+1] <= 'z'))
						{
							next_state = DONE;
							flag_continue = true;
							continue;
						}
						else if (!(input[i + 1] >= '0' && input[i + 1] <= '9'))
						{
							next_state = DONE;
							token_record token;
							token.token_value = stoi(output);
							token.token_type = "number";
							token.is_num = true;
							tokens.push_back(token);
							tokens_number++;
						}
						else
						{

						}
					}
				}
				else
				{
					next_state = DONE;
					token_record token;
					token.token_value = stoi(output);
					token.token_type = "number";
					token.is_num = true;
					tokens.push_back(token);
					tokens_number++;
				}
				break;
				/////////////////INID
			case INID:
				if ((input[i] >= 'A' && input[i] <= 'Z') || (input[i] >= 'a' && input[i] <= 'z'))
				{
					next_state = INID;
					output.push_back(input[i]);
					if (i == (input.length() - 1))
					{
						next_state = DONE;
						token_record token;
						token.token_name = output;

						/////handling reserved words
						if (output == "if"
							|| output == "then" ||
							output == "else" ||
							output == "end" ||
							output == "repeat" ||
							output == "until" ||
							output == "read" ||
							output == "write")
						{
							for (int i = 0; i < output.length(); i++)
							{
								output[i] = toupper(output[i]);
							}
							token.token_type = output;
						}
						else
						{
							token.token_type = "Identifier";
						}

						token.is_num = false;
						tokens.push_back(token);
						tokens_number++;
					}
					else
					{
						if ((input[i + 1] >= '0' && input[i + 1] <= '9'))
						{
							next_state = DONE;
							flag_continue = true;
							continue;
						}
						else if (!((input[i + 1] >= 'A' && input[i + 1] <= 'Z') || (input[i + 1] >= 'a' && input[i + 1] <= 'z')))
						{
							token_record token;
							token.token_name = output;

							/////handling reserved words
							if (output == "if"
								|| output == "then" ||
								output == "else" ||
								output == "end" ||
								output == "repeat" ||
								output == "until" ||
								output == "read" ||
								output == "write")
							{
								for (int i = 0; i < output.length(); i++)
								{
									output[i] = toupper(output[i]);
								}
								token.token_type = output;
							}
							else
							{
								token.token_type = "Identifier";
							}

							token.is_num = false;
							tokens.push_back(token);
							tokens_number++;
							next_state = DONE;
						}
						else
						{

						}
					}

				}
				else
				{
					next_state = DONE;
					token_record token;
					token.token_name = output;

					/////handling reserved words
					if (output == "if"
						|| output == "then" ||
						output == "else" ||
						output == "end" ||
						output == "repeat" ||
						output == "until" ||
						output == "read" ||
						output == "write")
					{
						for (int i = 0; i < output.length(); i++)
						{
							output[i] = toupper(output[i]);
						}
						token.token_type = output;
					}
					else
					{
						token.token_type = "Identifier";
					}

					token.is_num = false;
					tokens.push_back(token);
					tokens_number++;
				}
				break;


				/////////////////DONE
			case DONE:
				next_state = START;
				output = "";
				i--;
				break;

			}


			current_state = next_state;
		}
		if (flag_continue&& counter < input.length())
		{
			/////////
		for (int i = 0; i < tokens.size(); i++)
		{
			if (tokens[i].is_num)
			{
				cout << tokens[i].token_value << ", " << tokens[i].token_type << endl;
				output_file<< tokens[i].token_value << ", " << tokens[i].token_type << endl;
			}
			else
			{
				cout <<tokens[i].token_name << ", " << tokens[i].token_type << endl;
				output_file << tokens[i].token_name << ", " << tokens[i].token_type << endl;
				//output_file << "aaaaaaaaaaaaaaaaaaa" << endl;
			}

		}
		output_file<<"Error !!!!!!"<<endl;
	if(flag_comment==1) 
	{
		output_file<<"Comment ERROR!!!!!"<<endl;
	}
			////////////
			continue;
		}



		for (int i = 0; i < tokens_number; i++)
		{
			if (tokens[i].is_num)
			{
				cout << tokens[i].token_value << ", " << tokens[i].token_type << endl;
				output_file<< tokens[i].token_value << ", " << tokens[i].token_type << endl;
			}
			else
			{
				cout <<tokens[i].token_name << ", " << tokens[i].token_type << endl;
				output_file << tokens[i].token_name << ", " << tokens[i].token_type << endl;
				//output_file << "aaaaaaaaaaaaaaaaaaa" << endl;
			}

		}
			if(flag_comment==1) 
	{
		output_file<<"Comment ERROR!!!!!"<<endl;
	}
	}

	output_file.close();
	return 0;
}
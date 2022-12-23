# !Python

**!Python** is a tiny language that I made to learn how compilers do their magic. The compiler of **!Python** is written 
in pure python ( no dependencies ). It currently supports limited functionalities only, but in the future I might add more.
Or if you are interested you can add them, power of open source right !?. 

## Setup

To set up the compiler, you need to have **python** installed on your system. You also need **g++** as the compiler uses it to 
compile the generated intermediate code.

## How to use

1. Clone the repository
2. Run `python3 main.py <filename>` to compile the file
3. Run `<filename>.exe` to execute the program

## Syntax

**!Python** uses a simple syntax. It is similar to c/c++ but with some differences. The syntax is as follows:

1. Statements should be written one per line
2. `PRINT <expression>`: Prints the value of the expression
3. `INPUT <variable>`: Takes input from the user and stores it in the variable
4. `IF <expression> { <statement> }`: Executes the statement if the expression is true
5. `WHILE <expression> { <statement> }`: Executes the statement while the expression is true
6. `LET <variable> = <expression>`: Assigns the value of the expression to the variable
7. `RETURN <expression>`: Terminates the program with expression as exit code
8. If multiple expressions are given to the print statement, they are printed in the same line

That's basically it. You can check the [examples](./examples) folder for more examples.

What about comments you ask ? Comments are for those who can't write readable code. Just kidding, I will add comments 
later.

## Keywords

The following keywords are reserved in **!Python**:

- PRINT
- INPUT
- LET
- IF
- WHILE
- RETURN

All keywords are case-sensitive, why would you want to write `print` instead of `PRINT` ? 🤷.

This means it is perfectly legal to do something like this:

    INPUT print
    PRINT "You said " print

But it is not legal to do something like this:

    INPUT PRINT
    PRINT "You said " PRINT

## Compiler Flags

Currently, there are only 2 compiler flags:

- `-d`: Enables debug mode. In debug mode, the compiler preserves the intermediate code generated. 
It will be saved as `<filename>.exe.cpp`
- `-o <filename>`: Specifies the name of the output file. By default, the output file is `<filename>.exe`

## Examples

You can check the [examples](./examples) folder for more examples.

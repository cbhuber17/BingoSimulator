# Bingo Simulator
Just a simple bingo simulator, is not the actual game!

## Table of Contents

1. [Background Information](#background-inforomation)
2. [Local Setup](#local-setup)
3. [Running Dash Server](#running-dash-server)
4. [Heroku Deployment](#heroku-deployment)
5. [Testing](#testing)

## Background Information

BINGO is a traditional game where a person is given a 5x5 card with the following characteristics:
- Under the B column, five random numbers between 1-15
- Under the I column, five random numbers between 16-30
- Under the N column, five random numbers between 31-45
- Under the G column, five random numbers between 46-60
- Under the O column, five random numbers between 61-75


A random number ("bingo ball") is called, and if the number is on the bingo card, it is considered marked at the spot on the bingo card.

To win a bingo game, a pattern is required, either as:
- Any row

```
Example Row 1 BINGO:
------------------------
|B | |I | |N | |G | |O |
------------------------
|  | |  | |  | |  | |  |
|X | |X | |X | |X | |X |
|  | |  | |  | |  | |  |
|  | |  | |  | |  | |  |
|  | |  | |  | |  | |  |
------------------------
```

- Any column

```
Example Column G (column 3) BINGO:
------------------------
|B | |I | |N | |G | |O |
------------------------
|  | |  | |  | |X | |  |
|  | |  | |  | |X | |  |
|  | |  | |  | |X | |  |
|  | |  | |  | |X | |  |
|  | |  | |  | |X | |  |
------------------------
```

- Any diagonal


```
Diagonal 1:

------------------------
|B | |I | |N | |G | |O |
------------------------
|X | |  | |  | |  | |  |
|  | |X | |  | |  | |  |
|  | |  | |X | |  | |  |
|  | |  | |  | |X | |  |
|  | |  | |  | |  | |X |
------------------------

Diagonal 2:
------------------------
|B | |I | |N | |G | |O |
------------------------
|  | |  | |  | |  | |X |
|  | |  | |  | |X | |  |
|  | |  | |X | |  | |  |
|  | |X | |  | |  | |  |
|X | |  | |  | |  | |  |
------------------------
```

- All four corners

```
------------------------
|B | |I | |N | |G | |O |
------------------------
|X | |  | |  | |  | |X |
|  | |  | |  | |  | |  |
|  | |  | |  | |  | |  |
|  | |  | |  | |  | |  |
|X | |  | |  | |  | |X |
------------------------
```

More information is available on [BINGO Wikipeida](#https://en.wikipedia.org/wiki/Bingo_(American_version)).

Note: Simulations do not include the FREE CELL as marked in the middle of the board.

## Local Setup

**Note:** The instructions below are for a Windows platform using Python 3.9.X.


### Project Directory

Create a folder on your PC to host the project files.  Navigate to the root folder and open a command window ```(Windows Key + cmd.exe)``` at this location.

### Virtual Environment

Create the virtual environment in hte root folder by running the following command:

```
python -m virtualenv bingo_env
```

For Windows, this means going into the ```bingo_env\Scripts``` folder(by using the ```cd``` command in ```cmd.exe```) and running ```activate``` via command prompt.  Now this command prompt has ```(bingo_env)``` in it and is the virtual environment for this project, only containing the dependencies required for it (i.e. those from [requirements.txt](requirements.txt)).

### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the root directory in the command window (```cd..``` twice) and running:

```
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Running Dash Server

Change directory ```cd``` into the [bingo_simulator](bingo_simulator) folder.  Run the dashboard as:

```
python dash_bingo.py
```

The server will start at [http://127.0.0.1:8050/](http://127.0.0.1:8050/)

## Heroku Deployment

The app is located at: https://bingo-simulator.herokuapp.com/

## Testing

The bingo_card.py](bingo_simulator/bingo_card.py) class has been unit tested in the [test](test) folder using ```tox```.
All forms of winning bingo patters were tested, particularly:
- Valid row, column, diagonal, and corners BINGO
- Invalid row, column, diagonal, and corners BINGO

Results are as follows, 86% of code coverage was achieved in [bingo_card.py](bingo_simulator/bingo_card.py):

```
collected 83 items

test_bingo.py::test_valid_diagonal_one PASSED                                                                    [  1%]
test_bingo.py::test_valid_diagonal_two PASSED                                                                    [  2%]
test_bingo.py::test_bad_diagonal_one[card_and_stat0] PASSED                                                      [  3%]
test_bingo.py::test_bad_diagonal_one[card_and_stat1] PASSED                                                      [  4%]
test_bingo.py::test_bad_diagonal_one[card_and_stat2] PASSED                                                      [  6%]
test_bingo.py::test_bad_diagonal_one[card_and_stat3] PASSED                                                      [  7%]
test_bingo.py::test_bad_diagonal_one[card_and_stat4] PASSED                                                      [  8%]
test_bingo.py::test_bad_diagonal_two[card_and_stat0] PASSED                                                      [  9%]
test_bingo.py::test_bad_diagonal_two[card_and_stat1] PASSED                                                      [ 10%]
test_bingo.py::test_bad_diagonal_two[card_and_stat2] PASSED                                                      [ 12%]
test_bingo.py::test_bad_diagonal_two[card_and_stat3] PASSED                                                      [ 13%]
test_bingo.py::test_bad_diagonal_two[card_and_stat4] PASSED                                                      [ 14%]
test_bingo.py::test_valid_rows[cards_and_stats_and_line_num0] PASSED                                             [ 15%]
test_bingo.py::test_valid_rows[cards_and_stats_and_line_num1] PASSED                                             [ 16%]
test_bingo.py::test_valid_rows[cards_and_stats_and_line_num2] PASSED                                             [ 18%]
test_bingo.py::test_valid_rows[cards_and_stats_and_line_num3] PASSED                                             [ 19%]
test_bingo.py::test_valid_rows[cards_and_stats_and_line_num4] PASSED                                             [ 20%]
test_bingo.py::test_valid_cols[cards_and_stats_and_line_num0] PASSED                                             [ 21%]
test_bingo.py::test_valid_cols[cards_and_stats_and_line_num1] PASSED                                             [ 22%]
test_bingo.py::test_valid_cols[cards_and_stats_and_line_num2] PASSED                                             [ 24%]
test_bingo.py::test_valid_cols[cards_and_stats_and_line_num3] PASSED                                             [ 25%]
test_bingo.py::test_valid_cols[cards_and_stats_and_line_num4] PASSED                                             [ 26%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num0] PASSED                                           [ 27%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num1] PASSED                                           [ 28%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num2] PASSED                                           [ 30%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num3] PASSED                                           [ 31%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num4] PASSED                                           [ 32%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num5] PASSED                                           [ 33%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num6] PASSED                                           [ 34%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num7] PASSED                                           [ 36%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num8] PASSED                                           [ 37%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num9] PASSED                                           [ 38%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num10] PASSED                                          [ 39%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num11] PASSED                                          [ 40%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num12] PASSED                                          [ 42%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num13] PASSED                                          [ 43%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num14] PASSED                                          [ 44%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num15] PASSED                                          [ 45%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num16] PASSED                                          [ 46%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num17] PASSED                                          [ 48%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num18] PASSED                                          [ 49%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num19] PASSED                                          [ 50%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num20] PASSED                                          [ 51%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num21] PASSED                                          [ 53%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num22] PASSED                                          [ 54%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num23] PASSED                                          [ 55%]
test_bingo.py::test_invalid_rows[cards_and_stats_and_line_num24] PASSED                                          [ 56%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num0] PASSED                                           [ 57%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num1] PASSED                                           [ 59%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num2] PASSED                                           [ 60%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num3] PASSED                                           [ 61%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num4] PASSED                                           [ 62%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num5] PASSED                                           [ 63%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num6] PASSED                                           [ 65%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num7] PASSED                                           [ 66%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num8] PASSED                                           [ 67%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num9] PASSED                                           [ 68%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num10] PASSED                                          [ 69%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num11] PASSED                                          [ 71%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num12] PASSED                                          [ 72%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num13] PASSED                                          [ 73%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num14] PASSED                                          [ 74%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num15] PASSED                                          [ 75%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num16] PASSED                                          [ 77%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num17] PASSED                                          [ 78%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num18] PASSED                                          [ 79%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num19] PASSED                                          [ 80%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num20] PASSED                                          [ 81%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num21] PASSED                                          [ 83%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num22] PASSED                                          [ 84%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num23] PASSED                                          [ 85%]
test_bingo.py::test_invalid_cols[cards_and_stats_and_line_num24] PASSED                                          [ 86%]
test_bingo.py::test_valid_corners PASSED                                                                         [ 87%]
test_bingo.py::test_invalid_corner1 PASSED                                                                       [ 89%]
test_bingo.py::test_invalid_corner2 PASSED                                                                       [ 90%]
test_bingo.py::test_invalid_corner3 PASSED                                                                       [ 91%]
test_bingo.py::test_invalid_corner4 PASSED                                                                       [ 92%]
test_bingo.py::test_valid_traditional_bingo1 PASSED                                                              [ 93%]
test_bingo.py::test_valid_traditional_bingo2 PASSED                                                              [ 95%]
test_bingo.py::test_valid_traditional_bingo3 PASSED                                                              [ 96%]
test_bingo.py::test_valid_traditional_bingo4 PASSED                                                              [ 97%]
test_bingo.py::test_valid_traditional_bingo5 PASSED                                                              [ 98%]
test_bingo.py::test_invalid_traditional_bingo PASSED                                                             [100%]

-------------------- generated xml file: \bingo_simulator\test\unit-test-report.xml ---------------------

----------- coverage: platform win32, python 3.7.9-final-0 -----------
Name                                                                                                 Stmts   Miss  Cover
------------------------------------------------------------------------------------------------------------------------
\bingo_simulator\__init__.py                   0      0   100%
\bingo_simulator\bingo_card.py                91     13    86%
\bingo_simulator\bingo_simulator_main.py      83     47    43%
\bingo_simulator\dash_bingo.py                41     41     0%
\bingo_simulator\plot_bingo.py               126    126     0%
------------------------------------------------------------------------------------------------------------------------
TOTAL                                                                                                  341    227    33%

================================================= 83 passed in 2.87s ==================================================
_______________________________________________________ summary _______________________________________________________
  py37: commands succeeded
  congratulations :)
```

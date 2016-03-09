import java.util.Random;
import java.util.Scanner;


public class GenericLane {
	public boolean isVisited[][] = new boolean[7][7];
	public char maze[][] = new char[7][7];
	public int playersCurrentRow;
	public int playersCurrentColumn;
	public boolean isExit = false;
	public int playersMovesCount = 0;
	HighScoreBoard board;

	public void initializeMaze(){
		Random randomGenerator = new Random();
		do{
			for(int row = 0; row < 7; row++){
				for(int column = 0; column < 7; column++){
					isVisited[row][column] = false;
					if(randomGenerator.nextInt(2) == 1) maze[row][column] = 'X';
					else maze[row][column] = '-';
				}
			}
		} while(!isSolvable(3, 3));
		playersCurrentRow = 3;
		playersCurrentColumn = 3;
		maze[playersCurrentRow][playersCurrentColumn] = '*';
		printMaze();
	}

	public void initializeScoreBoard(){
		board = new HighScoreBoard();
	}

	public boolean isSolvable(int row, int col){
		if(hasExit(row, col)) isExit = true;

		if (isOpenCheck(row, -1, col, 0)){
			isVisited[row][col] = true;
			isSolvable(row - 1, col);
		}

		if(isOpenCheck(row, 1,col, 0)){
			isVisited[row][col] = true;
			isSolvable(row + 1, col);
		}

		if(isOpenCheck(row, 0, col, -1)){
			isVisited[row][col] = true;
			isSolvable(row, col - 1);
		}

		if(isOpenCheck(row, 0, col, 1)){
			isVisited[row][col] = true;
			isSolvable(row, col + 1);
		}
		return isExit;
	}

	public void printMaze(){
		for(int row = 0; row < 7; row++){
			for(int column = 0; column < 7; column++){
				System.out.print(maze[row][column] + " ");
			}
			System.out.println();
		}
	}

	public void inputCommand(){
		Scanner scanner = new Scanner(System.in);

		// no description that the other commands are available in instruction
		System.out.println("Enter your next move : L(left), " + "R(right), U(up), D(down) ");
		handleCommand(scanner.next());
	}

	public void handleCommand(String command){
		int size = command.length();
		char firstLetter = Character.toLowerCase(command.charAt(0));

		if(command.equals("top")) {
			showHighScore();
		} else if(command.equals("restart")){
			isExit = false;
			initializeMaze();
		} else if(command.equals("exit")){
			System.out.println("Good bye!");
			System.exit(0);
		} else if(size == 1 && validLetter(firstLetter)){
			movePlayer(firstLetter);
		} else {
			System.out.println("Invalid command!");
		}
	}

	public void showHighScore(){
		if(board.playerList.size() > 0) board.printBoard(board.playerList);
		else System.out.println("The High score board is empty!");
	}

	public void movePlayer(char firstLetter){
		firstLetter = Character.toLowerCase(firstLetter);

		if (validLeftMove(firstLetter)) moveLeft();
		else if (validRightMove(firstLetter)) moveRight();
		else if (validUpMove(firstLetter)) moveUp();
		else if (validUpMove(firstLetter)) moveDown();
		else {
			System.out.println("Invalid move!");
			printMaze();
		}
	}

	private void swapCells(int currentRow, int newRow, int currentColumn, int newColumn){
		char previousCell = maze[currentRow][currentColumn];
		maze[currentRow][currentColumn] = maze[newRow][newColumn];
		maze[newRow][newColumn] = previousCell;
		System.out.println();
		printMaze();
	}

	private void moveLeft(){
		swapCells(playersCurrentRow, playersCurrentRow,
				  playersCurrentColumn, --playersCurrentColumn);
		playersMovesCount++;
	}

	private void moveRight(){
		swapCells(playersCurrentRow, playersCurrentRow,
				  playersCurrentColumn, ++playersCurrentColumn);
		playersMovesCount++;
	}

	private void moveUp(){
		swapCells(playersCurrentRow, --playersCurrentRow,
				  playersCurrentColumn, playersCurrentColumn);
		playersMovesCount++;
	}

	private void moveDown(){
		swapCells(playersCurrentRow, ++playersCurrentRow,
				  playersCurrentColumn, playersCurrentColumn);
		playersMovesCount++;
	}

	private boolean validLetter(char firstLetter){
		return firstLetter == 'l' || firstLetter == 'r' ||
			   firstLetter == 'd' || firstLetter == 'u';
	}

	private boolean validLeftMove(char firstLetter){
		return firstLetter == 'l' && maze[playersCurrentRow][playersCurrentColumn - 1] != 'X';
	}

	private boolean validRightMove(char firstLetter){
		return firstLetter == 'r' && maze[playersCurrentRow][playersCurrentColumn + 1] != 'X';
	}

	private boolean validDownMove(char firstLetter){
		return firstLetter == 'd' && maze[playersCurrentRow + 1][playersCurrentColumn] != 'X';
	}

	private boolean validUpMove(char firstLetter){
		return firstLetter == 'u' && maze[playersCurrentRow - 1][playersCurrentColumn] != 'X';
	}

	private boolean hasExit(int row, int col){
		return row == 6 || col == 6 || row == 0 || col == 0;
	}

	private boolean isOpenCheck(int row, int addRow, int col, int addCol){
		return (maze[row + addRow][col + addCol] == '-') &&
				(!isVisited[row + addRow][col + addCol]);
	}
}
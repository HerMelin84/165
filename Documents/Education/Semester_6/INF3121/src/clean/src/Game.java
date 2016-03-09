import java.util.Scanner;


public class Game {
	public static void main(String[] args){
		GenericLane labyrinth = new GenericLane();
		labyrinth.initializeScoreBoard();

		while(true){
			labyrinth.initializeMaze();

			while(hasNotFoundExit(labyrinth))labyrinth.inputCommand();

			System.out.println();
			labyrinth.printMaze();
			System.out.println("Congratulations! You escaped in "+labyrinth.playersMovesCount+" moves.\n");

			Scanner scanner = new Scanner(System.in);
			System.out.println("Enter your name : ");
			String name = scanner.next();
			Player player = new Player(name,labyrinth.playersMovesCount);

			if(labyrinth.board.addPlayerToChart(player)){
				System.out.println("Your score is in top 5!");
				labyrinth.board.printBoard(labyrinth.board.playerList);
			}

			labyrinth.isExit = false;
			labyrinth.playersCurrentColumn = 3;
			labyrinth.playersCurrentRow = 3;
			labyrinth.playersMovesCount = 0;
		}
	}

	static private boolean hasNotFoundExit(GenericLane labyrinth){
		return (labyrinth.playersCurrentColumn!=0) &&
			   (labyrinth.playersCurrentColumn!=6) &&
			   (labyrinth.playersCurrentRow!=0) &&
			   (labyrinth.playersCurrentRow!=6);
	}
}

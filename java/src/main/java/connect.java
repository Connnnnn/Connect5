import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.util.concurrent.TimeUnit;
import java.util.ArrayList;
import java.util.Scanner;

public class connect {

    private GetRequestHandler getRequestHandler = new GetRequestHandler();;
    private PostRequestHandler postRequestHandler = new PostRequestHandler();
    private boolean running = true;
    private Scanner input = new Scanner(System.in);;
    private String username, uid;
    private ArrayList<ArrayList<String>> users = new ArrayList<>();

    public connect() throws JSONException {
        populateScoreboard();
    }

    public void runGame() throws JSONException {
        //Display Home Screen, Prompts user to create and account or login
        while(running){
            System.out.println("----====Welcome to connect X!====-----\n\n" +
                    "To create an account, type 'create'\n" +
                    "To log in to an existing account, type 'login'\n" +
                    "To quit, type 'quit'\n");
            String userInput = input.nextLine();
            switch(userInput){
                case "login":
                    enterLoginDetails();
                    break;

                case "create":
                    enterRegisterationDetails();
                    break;

                case "quit":
                    running = false;
                    break;

                default:
                    System.out.println("Invalid Input!");
            }
        }
    }

    //Displays menu to logged in users
    private void displayMenu() throws JSONException {
        System.out.print("\n\n--==Please Select an option==--\n" +
                "Create Game: \t\tTYPE !c\n" +
                "View Open Games: \tTYPE !o\n" +
                "View Leaderboard: \tTYPE !l\n" +
                "View Stats: \t\tTYPE !s\n" +
                "Log out: \t\t\tTYPE !q\n");
        String userChoice = input.nextLine();
        switch(userChoice){
            case "!c":
                createGame(uid);
                break;
            case "!o":
                openGames();
                break;
            case "!l":
                System.out.print(openLeaderboard(populateScoreboard()));
                break;
            case "!s":
                System.out.print(openStats(uid));
                break;
            case "!q":
                System.out.println("You have been logged out");
                break;
            default:
                System.out.println("Not a valid option!");
                displayMenu();
                break;
        }
        displayMenu();
    }

    //Retrieves crednetials for log on
    private void enterLoginDetails() throws JSONException {
        System.out.println("Please enter username:");
        String userName = input.nextLine();
        System.out.println("Please enter password:");
        String password = input.nextLine();
        if(login(userName, password)){
            displayMenu();
        }
        else{
            System.out.print("Details are incorrect! Try again.\n");
        }
    }

    //Checks if details are valid with server
    public boolean login(String userName, String password) throws JSONException {
        if(getRequestHandler.getUserWithName(userName, password)!= null) {
            String [] details = getRequestHandler.getUserWithName(userName, password);
            uid = details[0];
            username = details[1];
            return true;
        }
        return false;
    }

    //Retrieves user and password for new account
    private void enterRegisterationDetails() throws JSONException {
        System.out.println("Please enter username:");
        String userName = input.nextLine();
        System.out.println("Please enter password:");
        String password = input.nextLine();
        if(registerCheck(userName, password)){
            displayMenu();
        }
    }

    ////Checks if the entered details are unique
    public boolean registerCheck(String name, String password) throws JSONException {
        if(postRequestHandler.insertUser(name, password)){
            String [] details = getRequestHandler.getUserWithName(username, password);
            uid = details[0];
            username = details[1];
            System.out.println("Successfully created user!");
            return true;
        }
        System.out.println("Couldn't create user!");
        return false;
    }

    //Displays game logic and board
    private void playGame(String game_id) throws JSONException {
        boolean ongoing = true;
        while(ongoing){
            if(checkForGameStatusChanges(game_id, uid)){
                System.out.print(getBoard(game_id));
                System.out.println("Enter a number between 0-9 to make your move");
                ongoing = makeMove(game_id);
                if(ongoing){
                    System.out.print(getBoard(game_id));
                    System.out.println("Successfully placed your colour!");
                    System.out.println("Please wait until your opponent moves...");
                }
            }else{
                try {
                    TimeUnit.SECONDS.sleep(10);
                    if(checkForGameStatusChanges(game_id, uid)){
                        System.out.print("no move");
                    }
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    //Checks if it is the current players turn
    public boolean checkForGameStatusChanges(String game_id, String uid) throws JSONException {
        JSONArray gameStatus = getRequestHandler.getGameInfo(game_id);
        JSONObject explrObject = gameStatus.getJSONObject(0);
        int playersTurn = (int)explrObject.get("current_player_turn");
        if(playersTurn == Integer.parseInt(uid)){
            return true;
        }
        return false;
    }

    //Returns true or false if move was successfull or not respectively
    private boolean makeMove(String gameID) throws JSONException {
        int selection = input.nextInt();
        if(!postRequestHandler.makeMove(selection, Integer.parseInt(gameID),uid)){
            System.out.println("Column full! Select a new column!");
        }
        JSONArray gameStatus = getRequestHandler.getGameInfo(gameID);
        JSONObject explrObject = gameStatus.getJSONObject(0);
        String state = (String) explrObject.get("gamestate");
        return checkIfGameOver(state, uid);
    }

    //Checks and displays the game state
    public boolean checkIfGameOver(String state, String uid){
        if(state == uid){
            System.out.print("==== YOU WIN! ====");
            return false;
        }
        else if(state != uid){
            System.out.print("==== YOU LOSE! ====");
            return false;
        }
        return true;
    }

    //Returns the updated board
    public String getBoard(String game_ID) throws JSONException {
        String [][] board = new String[6][9];
        for(int i=0; i<6; i++){
            for(int j = 0; j<9; j++){
                board[i][j]= "0";
            }
        }
        if(getRequestHandler.getBoard(game_ID)!=null){
            JSONArray boardInJSONFormat = getRequestHandler.getBoard(game_ID);
            for (int i = 0; i < boardInJSONFormat.length(); i++) {
                JSONObject explrObject = boardInJSONFormat.getJSONObject(i);
                if((int)explrObject.get("playerid") == Integer.parseInt(uid)){
                    board[(int)explrObject.get("x")][(int)explrObject.get("y")] = "X";
                }
                else{
                    board[(int)explrObject.get("x")][(int)explrObject.get("y")] = "O";
                }

            }
        }
        return displayBoard(board);
    }

    //Gathers board data and creates String with the board
    public static String  displayBoard(String[][]board){
        System.out.println("\n\n\n\n\n\n\n\n\n");
        String outputBoard = "\n\n\n\n\n\n\n\n\n";
        for(int i=5; i>-1; i--){
            for(int j=0; j<9;j++){
                switch(board[i][j]){
                    case "X":
                        outputBoard+= "["+board[i][j]+"]";
                        break;
                    case "O":
                        outputBoard+= "["+board[i][j]+"]";
                        break;
                    default:
                        outputBoard += "[ ]";
                        break;
                }
            }
            outputBoard+="\n";
        }
        return outputBoard;
    }

    //Create game for given user
    private void createGame(String userID) throws JSONException {
        if(postRequestHandler.createGame(uid)){
            System.out.println("Successfully created game!");
            waitOnPlayer2(findCurrentOpenGameForUser(uid));
        }
    }

    //Find game that is just been created
    public String findCurrentOpenGameForUser(String userID) throws JSONException {
        JSONArray result = getRequestHandler.getOpenUserGame(userID);
        JSONObject explrObject = result.getJSONObject(0);
        return (String) explrObject.get("game_id");
    }

    //Waits on the second player to join
    private void waitOnPlayer2(String game_id) throws JSONException {
        System.out.println("Waiting on player 2...");
        boolean hasJoined = false;
        while(!hasJoined){
            hasJoined = checkIfPlayerTwoJoined(game_id);
            try {
                TimeUnit.SECONDS.sleep(3);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        playGame(game_id);
    }

    //Check to see if player 2 joined
    public boolean checkIfPlayerTwoJoined(String gameid) throws JSONException {
        JSONArray results =  getRequestHandler.checkIfPlayerJoined(gameid);
        JSONObject explrObject = results.getJSONObject(0);
        if((int)explrObject.get("player_2")!=0){
            return true;
        }
        return false;
    }

    //displays all games that can be joined
    private void openGames() throws JSONException {
        ArrayList<ArrayList<String>> openGames = new ArrayList<>();
        int count = 0;
        if(getRequestHandler.getGames()!=null){
            JSONArray jsonArray = getRequestHandler.getGames();
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject explrObject = jsonArray.getJSONObject(i);
                if((int)explrObject.get("gamestate") == -1){
                    openGames.add(new ArrayList());
                    openGames.get(count).add((String)explrObject.get("gameid"));
                    openGames.get(count).add((String)explrObject.get("player_1"));
                    count++;
                }
            }
            if(!openGames.get(0).isEmpty()){
                System.out.println("---===Open Games===---\n" + "Game ID\t\tPlayerID");
                for(int i = 0; i < count; i++){
                    System.out.println(openGames.get(i).get(0) + "\t\t\t " + openGames.get(i).get(1));
                }
                System.out.println("\nEnter Game ID to join Game: \n");
                String game_ID = input.nextLine();
                joinGame(game_ID);
            }
            else{
                System.out.println("No open games, perhaps try creating your own?");
            }
        }
    }


    //Checks if game is joinable, and joins it if it is
    private void joinGame(String game_ID) throws JSONException {
        if(postRequestHandler.joinGame(uid, game_ID)){
            System.out.println("Joined game!");
            playGame(game_ID);
        }
        else{
            System.out.println("Unable to join game!");
            openGames();
        }
    }

    //Display the scoreboard
    public String openLeaderboard(ArrayList<ArrayList<String>> stats) throws JSONException {
        String result = "";
        for(int x = 0; x<stats.size(); x++){
            result += "====================================\n" +
                    stats.get(x).get(1)+ "'s stats:\nGames Won:" + stats.get(x).get(2)+ "\nGames Lost:" + stats.get(x).get(3)+ "\nGames Tied:" + stats.get(x).get(4) + "\n";
        }
        return result;
    }

    //Display current users stats
    public String openStats(String userID) throws JSONException {
        String result = "====================================\n";
        ArrayList<ArrayList<String>> stats = populateScoreboard();
        for(int x = 0; x<stats.size(); x++){
            if(Integer.parseInt(stats.get(x).get(0))==Integer.parseInt(userID)){
                result+=stats.get(x).get(1)+"'s Stats:\n Wins:\t" + stats.get(x).get(2);
                result+= "\n Loses:\t" + stats.get(x).get(3);
                result+= "\n Ties:\t" + stats.get(x).get(4);
            }
        }
        return result;
    }
    //populates the scoreboard with all users
    public ArrayList<ArrayList<String>> populateScoreboard() throws JSONException {
        ArrayList<ArrayList<String>> scoreboard = new ArrayList<>();
        if(getRequestHandler.getALlUsers()!=null){
            JSONArray jsonArray = getRequestHandler.getALlUsers();
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject explrObject = null;
                explrObject = jsonArray.getJSONObject(i);
                scoreboard.add(new ArrayList());
                scoreboard.get(i).add(Integer.toString((int)explrObject.get("uid")));
                scoreboard.get(i).add((String)explrObject.get("username"));
                scoreboard.get(i).add("0");
                scoreboard.get(i).add("0");
                scoreboard.get(i).add("0");
            }
        }
        return addWinLoseToScoreboard(scoreboard);
    }

    //Adds stats to each users account on the scoreboard
    private ArrayList<ArrayList<String>> addWinLoseToScoreboard(ArrayList<ArrayList<String>> scoreboard) throws JSONException {
        if(getRequestHandler.getGames()!= null){
            JSONArray jsonArray = getRequestHandler.getGames();
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject explrObject = jsonArray.getJSONObject(i);
                if(((int)explrObject.get("gameid"))!=0){
                    for(int j=0; j<scoreboard.size(); j++){
                        if(Integer.parseInt(scoreboard.get(j).get(0))==  (int)explrObject.get("player_1")){
                            if((int)explrObject.get("gamestate")==1) {
                                int wins = Integer.parseInt(scoreboard.get(j).get(2)) + 1;
                                String win = Integer.toString(wins);
                                scoreboard.get(j).set(2, win);
                            }
                            else if((int)explrObject.get("gamestate")==2){
                                int wins = Integer.parseInt(scoreboard.get(j).get(3)) + 1;
                                String win = Integer.toString(wins);
                                scoreboard.get(j).set(3, win);
                            }
                            else if((int)explrObject.get("gamestate")==3){
                                int wins = Integer.parseInt(scoreboard.get(j).get(4)) + 1;
                                String win = Integer.toString(wins);
                                scoreboard.get(j).set(4, win);
                            }
                        }
                    }
                    for(int j=0; j<scoreboard.size(); j++){
                        if(Integer.parseInt(scoreboard.get(j).get(0)) !=  0){
                            if(Integer.parseInt(scoreboard.get(j).get(0)) ==  (int)explrObject.get("player_2")){
                                if((int)explrObject.get("gamestate")==2) {
                                    int wins = Integer.parseInt(scoreboard.get(j).get(2)) + 1;
                                    String win = Integer.toString(wins);
                                    scoreboard.get(j).set(2, win);
                                }
                                else if((int)explrObject.get("gamestate")==1){
                                    int wins = Integer.parseInt(scoreboard.get(j).get(3)) + 1;
                                    String win = Integer.toString(wins);
                                    scoreboard.get(j).set(3, win);
                                }
                                else if((int)explrObject.get("gamestate")==3){
                                    int wins = Integer.parseInt(scoreboard.get(j).get(4)) + 1;
                                    String win = Integer.toString(wins);
                                    scoreboard.get(j).set(4, win);
                                }
                            }
                        }
                    }
                }
            }
        }
        return scoreboard;
    }
}


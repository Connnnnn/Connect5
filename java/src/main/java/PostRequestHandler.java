import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;


public class PostRequestHandler extends URLConcat {

    URL url;
    HttpURLConnection conn;

    private static final String URL_ADDRESS = "http://localhost:5000";

    public boolean executeInsert(String urlstring){
        String restResult = "";

        try {
            url = new URL(urlstring);
            conn = (HttpURLConnection)url.openConnection();
            conn.setRequestMethod("POST");
            conn.connect();

            if(conn.getResponseCode() != 200){
                throw new RuntimeException("HttpResponseCode" + conn.getResponseCode());
            }
            else {
                return true;
            }
        } catch (MalformedURLException e) {
            e.printStackTrace();
            return false;
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean insertUser(String username, String password){
        String url  = URL_ADDRESS + "/user/" + username + "?";

        url = addParameterToUrl(url,"username",username,false);
        url = addParameterToUrl(url,"password",password,true);


        if(executeInsert(url)){
            return true;
        } else {
            return false;
        }
    }

    public boolean createGame(String uid){
        String url  = URL_ADDRESS + "/games/" + uid + "?";
        url = addParameterToUrl(url,"player_1",uid,true);

        if(executeInsert(url)){
            return true;
        } else {
            return false;
        }
    }

    public boolean joinGame(String uid, String game_ID){

        //localhost:5000/joinGame/1?gameid=2&player_2=8
        String url  = URL_ADDRESS + "/joinGame/" + game_ID + "?";
        url = addParameterToUrl(url,"gameid",game_ID,false);
        url = addParameterToUrl(url,"player_2",uid,true);

        if(executeInsert(url)){
            return true;
        } else {
            return false;
        }
    }


    public boolean makeMove(int selection, int gameID, String uid) {
        String url  = URL_ADDRESS + "/move/" + Integer.toString(gameID) + "?";
        url = addParameterToUrl(url,"gameid",Integer.toString(gameID),false);
        url = addParameterToUrl(url,"y",Integer.toString(selection),false);
        url = addParameterToUrl(url,"playerid",uid,true);

        if(executeInsert(url)){
            return true;
        } else {
            return false;
        }
    }
}
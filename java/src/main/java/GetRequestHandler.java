import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Scanner;

public class GetRequestHandler extends  URLConcat{

    URL url;
    HttpURLConnection conn;
    private static final String URL_ADDRESS = "http://localhost:5000";

    public JSONObject executeQuery(String urlstring){
        String restResult = "";

        try {
            url = new URL(urlstring);
            conn = (HttpURLConnection)url.openConnection();
            conn.setRequestMethod("GET");
            conn.connect();

            if(conn.getResponseCode() != 200){
                throw new RuntimeException("HttpResponseCode" + conn.getResponseCode());
            }
            else{
                Scanner sc = new Scanner(url.openStream());
                while(sc.hasNext()){
                    restResult+=sc.nextLine();
                }
                sc.close();
            }
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return(createJsonObject(restResult));
    }
    private JSONObject createJsonObject(String restResult) {

        restResult = restResult.replace("\\\"","\"");
        restResult = restResult.substring(1,restResult.length()-1);

        JSONObject jsonObject = new JSONObject();
        try {
            jsonObject = new JSONObject(restResult);
        }catch (JSONException err){
            System.out.println(err);
        }
        return jsonObject;
    }

    public String[] getUserWithName(String username, String password) throws JSONException {
        String url = URL_ADDRESS + "/user/" + username + "?";
        url = addParameterToUrl(url,"username",username,false);
        url = addParameterToUrl(url,"password",password,true);
        JSONObject jsonObject = executeQuery(url);

        JSONArray jsonArray = null;
        try {
            jsonArray = jsonObject.getJSONArray("results");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        if(jsonArray.length() > 0) {
            JSONObject explrObject = jsonArray.getJSONObject(0);
            String [] userDetails = {"","",""};
            userDetails[0] = (String) explrObject.get("userId");
            userDetails[1] = (String) explrObject.get("username");
            userDetails[2] = (String) explrObject.get("password");
            return userDetails;
        }
        else {
            return null;
        }
    }

    public JSONArray getGames() throws JSONException {
        String url = URL_ADDRESS + "/getGames/";

        JSONObject jsonObject = executeQuery(url);

        JSONArray jsonArray = null;
        jsonArray = jsonObject.getJSONArray("results");


        if(jsonArray.length() > 0) {
            return jsonArray;
        }
        else {
            return null;
        }
    }

    public JSONArray getGameInfo(String game_id) throws JSONException {
        String url = URL_ADDRESS + "/games/" + game_id + "?";
        url = addParameterToUrl(url,"gameid",game_id,true);
        JSONObject jsonObject = executeQuery(url);

        JSONArray jsonArray = null;
        jsonArray = jsonObject.getJSONArray("results");

        if(jsonArray.length() > 0) {
            return jsonArray;
        }
        else {
            return null;
        }
    }

    public JSONArray getALlUsers() throws JSONException {
        String url = URL_ADDRESS + "/user/";

        JSONObject jsonObject = executeQuery(url);

        JSONArray jsonArray = null;
        jsonArray = jsonObject.getJSONArray("results");

        if(jsonArray.length() > 0) {
            return jsonArray;
        }
        else {
            return null;
        }
    }

    public JSONArray getBoard(String i) throws JSONException {
        String url = URL_ADDRESS + "/move/" + i + "?";
        url = addParameterToUrl(url,"game_id",i,true);
        JSONObject jsonObject = executeQuery(url);
        JSONArray jsonArray = null;
        jsonArray = jsonObject.getJSONArray("results");
        return jsonArray;
    }

    public JSONArray getOpenUserGame(String uid) throws JSONException {
        String url = URL_ADDRESS + "/findGame/" + uid + "?";
        url = addParameterToUrl(url,"playerid",uid,true);
        JSONObject jsonObject = executeQuery(url);
        JSONArray jsonArray = null;
        jsonArray = jsonObject.getJSONArray("results");
        return jsonArray;
    }

    public JSONArray checkIfPlayerJoined(String game_id) throws JSONException {
        String url = URL_ADDRESS + "/games/" + game_id + "?";
        url = addParameterToUrl(url,"gameid",game_id,true);
        JSONObject jsonObject = executeQuery(url);
        JSONArray jsonArray = null;
        jsonArray = jsonObject.getJSONArray("results");
        return jsonArray;
    }


}


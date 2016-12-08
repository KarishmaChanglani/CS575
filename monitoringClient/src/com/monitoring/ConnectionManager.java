package com.monitoring;

import org.json.simple.JSONObject;

import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Date;


/**
 * Created by Patrick on 11/12/2016.
 */
public class ConnectionManager
{
    private JSONObject nextPostData;
    private String connectionURL;
    private String machineId;
    private final String SAVE = "/save/data/";
    private final String AUTH = "/save/auth/";

    public ConnectionManager(String url, String machineId)
    {
        connectionURL = url;
        this.machineId = machineId;
        nextPostData = makeNextPostData(machineId);
    }

    public JSONObject getNextPostData()
    {
        return nextPostData;
    }

    JSONObject makeNextPostData(String machineId)
    {
        JSONObject rv = new JSONObject();
        rv.put("machine", machineId);
        String date = new SimpleDateFormat("YYYY-MM-dd'T'HH:mm:ss.sss").format(new Date());
        rv.put("datetime", date);
        return rv;
    }

    public void addSensorData(String key, String value)
    {
        nextPostData.put("category", key);
        nextPostData.put("data", value);
    }

    public void addKeyValue(String key, String value)
    {
        nextPostData.put(key,value);
    }

/*    private HttpURLConnection getPostingConnection(String url)
    {   HttpURLConnection connection = getNewConnection(url);
        try
        {
            connection.setRequestMethod("POST");
        }
        catch (ProtocolException e)
        {e.printStackTrace();}
        return connection;
    }
*/

    private HttpURLConnection getNewConnection(String urlString, String target)
    {
        try
        {
//            URL url = new URL(urlString);
            URL url = new URL("http", urlString.split(":")[0], Integer.parseInt(urlString.split(":")[1]), target);
            System.out.println(url);
            HttpURLConnection con = (HttpURLConnection) url.openConnection();
            return con;
        }
        catch (MalformedURLException e)
        {e.printStackTrace();}
        catch (IOException e)
        {e.printStackTrace();}

        return null;
    }

    public void sendRequest()
    {
        HttpURLConnection connection = getNewConnection(connectionURL ,nextPostData.containsKey("user") ? AUTH : SAVE);
        try
        {
            if(!connection.getDoOutput())
                connection.setDoOutput(true);
            OutputStreamWriter wr = new OutputStreamWriter(connection.getOutputStream());
            wr.write(nextPostData.toString());
            wr.flush();
            wr.close();
            if(connection.getResponseCode() == HttpURLConnection.HTTP_OK)
                System.out.println(nextPostData.toString());
        } catch (IOException e) {
            e.printStackTrace();
        }

        nextPostData = makeNextPostData(machineId);
        connection.disconnect();
    }

    public void sendSensorData(String label, String data)
    {
        addSensorData(label,data);
        sendRequest();
    }
}

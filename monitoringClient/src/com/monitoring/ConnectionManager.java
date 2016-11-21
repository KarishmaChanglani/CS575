package com.monitoring;

import java.io.DataOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import org.json.simple.JSONObject;

/**
 * Created by Patrick on 11/12/2016.
 */
public class ConnectionManager
{
    private HttpURLConnection connection;
    private JSONObject nextPostData;

    public ConnectionManager(String url)
    {
        connection = getNewConnection(url);
        try
        {
            connection.setRequestMethod("POST");
        }
        catch (ProtocolException e)
        {e.printStackTrace();}

        nextPostData = new JSONObject();
    }

    public void setProperty(String key, String value)
    {
        nextPostData.put(key, value);
    }

    private HttpURLConnection getNewConnection(String urlString)
    {
        try
        {
//            URL url = new URL(urlString);
            URL url = new URL("http", urlString.split(":")[0], Integer.parseInt(urlString.split(":")[1]), "/save/data/");
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
        try
        {
            if(!connection.getDoOutput())
                connection.setDoOutput(true);
            OutputStreamWriter wr = new OutputStreamWriter(connection.getOutputStream());
            wr.write(nextPostData.toString());
            wr.flush();
            wr.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        System.out.println(nextPostData.toString());
        nextPostData = new JSONObject();
    }
}

package com.monitoring;

import java.io.DataOutputStream;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;

/**
 * Created by Patrick on 11/12/2016.
 */
public class ConnectionManager
{
    private HttpURLConnection connection;

    public ConnectionManager(String url)
    {
        connection = getNewConnection(url);
        try
        {
            connection.setRequestMethod("POST");
        }
        catch (ProtocolException e)
        {e.printStackTrace();}
    }
    public void setProperty(String key, String value)
    {
        connection.setRequestProperty(key, value);
    }
    private HttpURLConnection getNewConnection(String urlString)
    {
        try
        {
            URL url = new URL(urlString);
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
        try {
            connection.setDoOutput(true);
            DataOutputStream wr = new DataOutputStream(connection.getOutputStream());
            wr.flush();
            wr.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

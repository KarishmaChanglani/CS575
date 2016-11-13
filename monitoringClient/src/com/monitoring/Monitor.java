package com.monitoring;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.util.Scanner;

/**
 * Created by Patrick on 11/11/2016.
 */
public class Monitor        //will probabaly become multiple calsses later
{
    ConfigFileHandler conf = new ConfigFileHandler();

    public void start(String[] args)
    {
        if(args.length != 0 && args[0].equals("-s"))
            setup();
        ConnectionManager con = new ConnectionManager(conf.getURL());
        standardRun(con);
    }

    public void setup()
    {
        Scanner in = new Scanner(System.in);
        System.out.println("Enter the receiving URL");
        String url = in.nextLine();
        System.out.println("Enter a label for this machine");
        String label = in.nextLine();
        System.out.println("Enter your admin ID");
        String adminID = in.nextLine();
        conf.setURL(url);

        ConnectionManager connection = new ConnectionManager(conf.getURL());

        connection.setProperty("MACHINE",conf.getMachineID());
        connection.setProperty("LABEL",label);
        connection.setProperty("ADMIN_ID", adminID);
        connection.sendRequest();
    }

    public void standardRun(ConnectionManager connection)
    {
        
    }
}

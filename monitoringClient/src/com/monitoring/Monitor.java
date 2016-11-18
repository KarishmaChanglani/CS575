package com.monitoring;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.Timer;

/**
 * Created by Patrick on 11/11/2016.
 */
public class Monitor        //will probabaly become multiple calsses later
{

    public void start(String[] args)
    {
        ConfigFileHandler config = new ConfigFileHandler();
        if(args.length != 0 && args[0].equals("-s"))
            setup(config);
        ConnectionManager con = new ConnectionManager(config.getURL());
        standardRun(con, );
    }

    private void setup(ConfigFileHandler config)
    {
        Scanner in = new Scanner(System.in);
        System.out.println("Enter the receiving URL");
        String url = in.nextLine();
        System.out.println("Enter a label for this machine");
        String label = in.nextLine();
        System.out.println("Enter your admin ID");
        String adminID = in.nextLine();
        config.setURL(url);

        ConnectionManager connection = new ConnectionManager(config.getURL());

        connection.setProperty("MACHINE",config.getMachineID());
        connection.setProperty("LABEL",label);
        connection.setProperty("ADMIN_ID", adminID);
        connection.sendRequest();
    }

    private void standardRun(ConnectionManager connection, ArrayList<SystemSensor> sensors)
    {
        NotificationTask notifier = new NotificationTask(sensors, connection);
        Timer timer = new Timer();
        timer.schedule(notifier, 0, 3600*1000);
    }

    private ArrayList<SystemSensor> getSensorsFromConfig(ConfigFileHandler config)
    {
        ArrayList<String> sensorList = config.getSensors();
        ArrayList<SystemSensor> sensors= new ArrayList<SystemSensor>();
        //code to populate
        return sensors;
    }

    private SystemSensor getSensorByName(String name)
    {

    }
}

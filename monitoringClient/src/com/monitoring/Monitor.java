package com.monitoring;

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
        ConfigFileHandler config = getConfigFileHandler();
        if(!config.hasUrl())
            setup(config);
        ConnectionManager con = getConnectionManager(config);
        if(args.length > 0 && args[0].equals("-a"))
            editAuthorization(con, config);
        standardRun(con, getSensorsFromConfig(config));
    }

    private void editAuthorization(ConnectionManager con, ConfigFileHandler config)
    {
        Scanner in = new Scanner(System.in);
        String choice = "";
        while(!choice.equals("1") && !choice.equals("2"))
        {
            System.out.printf("1) Authorize\n2) Deauthorize\n");
            choice = in.nextLine();
        }
        System.out.printf("Enter admin ID\n");
        String adminID = in.nextLine();

        ConnectionManager connection = getConnectionManager(config);

        connection.addKeyValue("action", choice.equals("1") ? "authorize" : "deauthorize");
        connection.addKeyValue("user", adminID);
        connection.addKeyValue("machine",config.getMachineID());
        connection.sendRequest();
    }

    ConnectionManager getConnectionManager(ConfigFileHandler config)
    {
        return new ConnectionManager(config.getURL(), config.getMachineID());
    }

    ConfigFileHandler getConfigFileHandler()
    {
        return new ConfigFileHandler();
    }

    public void setup(ConfigFileHandler config)
    {
        Scanner in = new Scanner(System.in);
        System.out.println("Enter the receiving URL");
        String url = in.nextLine();
        System.out.println("Enter your admin ID");
        String adminID = in.nextLine();
        config.setURL(url);

        ConnectionManager connection = getConnectionManager(config);

        connection.addKeyValue("action","authorize");
        connection.addKeyValue("user", adminID);
        connection.addKeyValue("machine",config.getMachineID());
        connection.sendRequest();

        config.addSensor(IPAddressSensor.LABEL);
        config.addSensor(DiskIOSensor.LABEL);
    }

    public void standardRun(ConnectionManager connection, ArrayList<SystemSensor> sensors)
    {
        ConfigFileHandler config = getConfigFileHandler();
        NotificationTask notifier = new NotificationTask(sensors, config.getURL(), config.getMachineID());
        Timer timer = new Timer();
        //timer.schedule(notifier, 0, 3600*1000);
        timer.schedule(notifier, 0, 100*360);
    }

    ArrayList<SystemSensor> getSensorsFromConfig(ConfigFileHandler config)
    {
        ArrayList<String> sensorList = config.getSensors();
        ArrayList<SystemSensor> sensors= new ArrayList<SystemSensor>();
        for(String name : sensorList)
        {
            sensors.add(getSensorByName(name));
        }
        return sensors;
    }

    SystemSensor getSensorByName(String name)
    {
        switch(name)
        {
            case IPAddressSensor.LABEL:
                return new IPAddressSensor();
            default:
                return new DiskIOSensor();
        }
    }
}

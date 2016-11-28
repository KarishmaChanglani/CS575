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
        ConfigFileHandler config = new ConfigFileHandler();
        if(!config.hasUrl())
            setup(config);
        ConnectionManager con = new ConnectionManager(config.getURL(), config.getMachineID());
        standardRun(con, getSensorsFromConfig(config));
    }

    public void setup(ConfigFileHandler config)
    {
        Scanner in = new Scanner(System.in);
        System.out.println("Enter the receiving URL");
        String url = in.nextLine();
        System.out.println("Enter a label for this machine");
        String label = in.nextLine();
        System.out.println("Enter your admin ID");
        String adminID = in.nextLine();
        config.setURL(url);

        ConnectionManager connection = new ConnectionManager(config.getURL(), config.getMachineID());

        //connection.addSensorData("LABEL",label);
        connection.addSensorData("action","authorize");
        connection.addSensorData("user", adminID);
        connection.addSensorData("machine",config.getMachineID());
        connection.sendRequest();

        config.addSensor(IPAddressSensor.LABEL);
    }

    public void standardRun(ConnectionManager connection, ArrayList<SystemSensor> sensors)
    {
        ConfigFileHandler config = new ConfigFileHandler();
        NotificationTask notifier = new NotificationTask(sensors, config.getURL(), config.getMachineID());
        Timer timer = new Timer();
        //timer.schedule(notifier, 0, 3600*1000);
        timer.schedule(notifier, 0, 100*36);
    }

    private ArrayList<SystemSensor> getSensorsFromConfig(ConfigFileHandler config)
    {
        ArrayList<String> sensorList = config.getSensors();
        ArrayList<SystemSensor> sensors= new ArrayList<SystemSensor>();
        for(String name : sensorList)
        {
            sensors.add(getSensorByName(name));
        }
        return sensors;
    }

    private SystemSensor getSensorByName(String name)
    {
        return new IPAddressSensor();
    }
}

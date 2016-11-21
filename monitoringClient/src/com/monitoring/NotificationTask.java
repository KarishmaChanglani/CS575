package com.monitoring;

import java.util.ArrayList;
import java.util.TimerTask;

/**
 * Created by Patrick on 11/17/2016.
 */
public class NotificationTask extends TimerTask
{
    private ArrayList<SystemSensor> sensors;
    private ConnectionManager postRequest;

    public NotificationTask(ArrayList<SystemSensor> sensors, ConnectionManager connection)
    {
        this.sensors = sensors;
        this.postRequest = connection;
    }

    @Override
    public void run()
    {
        for(SystemSensor sensor : sensors)
        {
            postRequest.setProperty(sensor.getLabel(), sensor.getData());
        }
        postRequest.sendRequest();
        System.out.println("sent");
    }
}

package com.monitoring;

import java.util.ArrayList;
import java.util.TimerTask;

/**
 * Created by Patrick on 11/17/2016.
 */
public class NotificationTask extends TimerTask
{
    private final String machineId;
    private ArrayList<SystemSensor> sensors;
    //private ConnectionManager postRequest;
    private String url;

/*    public NotificationTask(ArrayList<SystemSensor> sensors, ConnectionManager connection)
    {
        this.sensors = sensors;
        this.postRequest = connection;
    }
*/

    public NotificationTask(ArrayList<SystemSensor> sensors, String url, String machineId)
    {
        this.sensors = sensors;
        this.machineId = machineId;
        this.url = url;
    }

    @Override
    public void run()
    {
        ConnectionManager postRequest = new ConnectionManager(url, machineId);
        for(SystemSensor sensor : sensors)
        {
            postRequest.sendSensorData(sensor.getLabel(), sensor.getData());
        }
    }
}

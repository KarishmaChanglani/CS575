package com.monitoring;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import java.util.ArrayList;

import static org.mockito.Mockito.*;

/**
 * Created by Patrick on 11/11/2016.
 */
public class MonitorTest {

    Monitor monitor;

    @Before
    public void setup()
    {}

    @Test
    public void start_calls_standardRun()
    {
        monitor = spy(new Monitor());
        String[] args = {};
        ConnectionManager con = Mockito.mock(ConnectionManager.class);
        ConfigFileHandler config = new ConfigFileHandler();
        ArrayList<SystemSensor> sensors = new ArrayList<SystemSensor>();
        when(monitor.getConfigFileHandler()).thenReturn(config);
        when(monitor.getConnectionManager(config)).thenReturn(con);
        when(monitor.getSensorsFromConfig(config)).thenReturn(sensors);

        monitor.start(args);

        verify(monitor).standardRun(con, new ArrayList<SystemSensor>());
    }


/*    @Test
    public void setup_Sends_Request()       //Ran into some problems here.
    {
        monitor = spy(new Monitor());
        ConnectionManager con = Mockito.mock(ConnectionManager.class);
        ConfigFileHandler config = new ConfigFileHandler();
        doReturn(con).when(monitor).getConnectionManager(config);
        monitor.setup(config);

        verify(con).sendRequest();
    }
*/
    @Test
    public void getSensorsFromConfig_calls_getSensorByName()       //Ran into some problems here.
    {
        monitor = spy(new Monitor());
        ConnectionManager con = Mockito.mock(ConnectionManager.class);
        ConfigFileHandler config = spy(new ConfigFileHandler());
        ArrayList<String> strings = new ArrayList<>();
        strings.add("astring");
        doReturn(strings).when(config).getSensors();
        doReturn("").when(config).getMachineID();
        doReturn(con).when(monitor).getConnectionManager(config);
        monitor.getSensorsFromConfig(config);

        verify(monitor).getSensorByName(strings.get(0));
    }

}
package com.monitoring;

import org.junit.Assert;
import org.junit.Test;

/**
 * Created by Patrick on 11/28/2016.
 */
public class ConfigFileHandlerTest {
    @Test
    public void getMachineID_Returns_UUID_String() throws Exception
    {
        ConfigFileHandler config = new ConfigFileHandler();

        String result = config.getMachineID();
        String uuidRegex = "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}";

        Assert.assertTrue(result.matches(uuidRegex));
    }

    @Test
    public void getURL_Returns_Valid_IPv4() throws Exception
    {
        ConfigFileHandler config = new ConfigFileHandler();

        String result = config.getURL();
        String ip = result.split(":")[0];
        String[] segments = ip.split(".");
        for(String s : segments)
            Assert.assertTrue(Integer.parseInt(s) <= 255);
    }

    @Test
    public void setURL() throws Exception {

    }

    @Test
    public void getSensors() throws Exception {

    }

    @Test
    public void addSensor() throws Exception {

    }

}